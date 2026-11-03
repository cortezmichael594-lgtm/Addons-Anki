"""Valida el taller entero: archivos, marcadores, secretos, ganchos y ZIP.

Uso:
    python herramientas/validar_kit.py               taller terminado
    python herramientas/validar_kit.py --plantilla   admite marcadores {{...}} sin rellenar

Trabaja sobre una copia temporal, así que no cambia nada del proyecto. Se ejecuta cada vez que se
tocan herramientas/, .claude/ o .github/.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import zipfile
from collections.abc import Callable
from pathlib import Path

import empaquetar_kit

ROOT = empaquetar_kit.ROOT
REQUIRED = (
    "CLAUDE.md",
    "LEEME.md",
    "docs/encargo.md",
    "docs/estado.md",
    "docs/normas-del-taller.md",
    "docs/aprendizajes.md",
    "docs/automejora.md",
    "docs/preparar-entorno.md",
    ".claude/settings.json",
    ".github/workflows/comprobar.yml",
    ".gitignore",
    ".gitattributes",
    "pyproject.toml",
    "requirements-dev.txt",
    "requirements-anki.txt",
    "herramientas/comprobar.py",
    "herramientas/empaquetar.py",
    "herramientas/empaquetar_kit.py",
    "herramientas/preparar.py",
    "herramientas/validar_kit.py",
    "herramientas/version-anki.txt",
)
# Solo los archivos del kit llevan marcadores de la plantilla: en el resto, «{{Campo}}» es la
# sintaxis de las plantillas de tarjeta de Anki.
PLACEHOLDER_FILES = (
    "CLAUDE.md",
    "LEEME.md",
    "docs/encargo.md",
    "docs/estado.md",
    "pyproject.toml",
    ".claude/settings.json",
)
PLACEHOLDER = re.compile(r"\{\{[^{}\n]+\}\}")
SECRETS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"(?i)\b(api[_-]?key|secret|token|password|contraseña)\b\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"),
)
TEXT_SUFFIXES = frozenset({".md", ".toml", ".txt", ".json", ".yml", ".yaml", ".cfg", ".ini"})
CLAUDE_MD_MAX_LINES = 200
CLAUDE_MD_WARN_LINES = 150
HEAVY_DUMMIES = (
    ".venv/lib/x.py",
    "node_modules/lib/index.js",
    ".git/config",
    "complementos/demo/__pycache__/x.cpython-313.pyc",
    ".env",
    "entregas/demo-1.0.0.ankiaddon",
    ".claude/settings.local.json",
    ".cache/comprobar.json",
    # Colecciones de Anki: datos de la persona que nunca viajan en el ZIP.
    "perfil/collection.anki2",
    "perfil/collection.media/foto.jpg",
    "copias/backup-1.colpkg",
)

Check = Callable[[], list[str]]


def check_required() -> list[str]:
    """Los archivos imprescindibles del taller existen."""
    return [f"falta {name}" for name in REQUIRED if not (ROOT / name).is_file()]


def text_files() -> list[Path]:
    """Archivos de texto del proyecto que no son código Python."""
    return [p for p in empaquetar_kit.project_files(ROOT) if p.suffix in TEXT_SUFFIXES]


def check_placeholders() -> list[str]:
    """No quedan marcadores {{...}} de la plantilla sin rellenar."""
    problems: list[str] = []
    for name in PLACEHOLDER_FILES:
        path = ROOT / name
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if PLACEHOLDER.search(line):
                problems.append(f"marcador sin rellenar en {name}:{number}")
    return problems


def check_claude_md() -> list[str]:
    """CLAUDE.md corto: se carga entero en cada sesión."""
    lines = len((ROOT / "CLAUDE.md").read_text(encoding="utf-8").splitlines())
    if lines > CLAUDE_MD_MAX_LINES:
        return [f"CLAUDE.md tiene {lines} líneas; el máximo es {CLAUDE_MD_MAX_LINES}"]
    if lines > CLAUDE_MD_WARN_LINES:
        print(f"Aviso: CLAUDE.md tiene {lines} líneas; mejor por debajo de {CLAUDE_MD_WARN_LINES}.")
    return []


def check_settings() -> list[str]:
    """settings.json es JSON válido y sus ganchos apuntan a scripts que existen."""
    try:
        settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [f".claude/settings.json no se puede leer: {error}"]
    problems: list[str] = []
    for groups in settings.get("hooks", {}).values():
        for group in groups:
            for hook in group.get("hooks", []):
                for arg in hook.get("args", []):
                    if isinstance(arg, str) and arg.startswith("${CLAUDE_PROJECT_DIR}/"):
                        script = arg.removeprefix("${CLAUDE_PROJECT_DIR}/")
                        if not (ROOT / script).is_file():
                            problems.append(f"un gancho apunta a {script}, que no existe")
    return problems


def check_workflow() -> list[str]:
    """El flujo de GitHub Actions es YAML válido (si PyYAML está instalado)."""
    try:
        import yaml
    except ImportError:
        return []
    try:
        yaml.safe_load((ROOT / ".github/workflows/comprobar.yml").read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        return [f"comprobar.yml no es YAML válido: {error}"]
    return []


def check_secrets() -> list[str]:
    """Ni archivos .env ni nada con pinta de clave dentro del taller."""
    problems = [
        f"archivo de secretos dentro del taller: {rel(p)}"
        for p in ROOT.rglob(".env*")
        if p.is_file() and p.name != ".env.example" and not in_excluded_dir(p)
    ]
    for path in empaquetar_kit.project_files(ROOT):
        if path.suffix not in TEXT_SUFFIXES | {".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if any(pattern.search(text) for pattern in SECRETS):
            problems.append(f"posible clave o contraseña en {rel(path)}")
    return problems


def in_excluded_dir(path: Path) -> bool:
    """Está dentro de una carpeta que nunca entra en el ZIP (.venv, node_modules...)."""
    return any(part in empaquetar_kit.EXCLUDED_DIRS for part in path.relative_to(ROOT).parts[:-1])


def copy_project(target: Path) -> None:
    """Copia los archivos que irían en el ZIP a una carpeta temporal."""
    for path in empaquetar_kit.project_files(ROOT):
        destination = target / path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def run_tool(copy: Path, *args: str, stdin: str = "") -> subprocess.CompletedProcess[str]:
    """Ejecuta una herramienta del taller dentro de la copia temporal."""
    return subprocess.run(
        [sys.executable, *args],
        cwd=copy,
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=900,
    )


def first_test_dir(copy: Path) -> Path:
    """Carpeta de pruebas de las herramientas según pyproject.toml."""
    with (copy / "pyproject.toml").open("rb") as f:
        options = tomllib.load(f).get("tool", {}).get("pytest", {}).get("ini_options", {})
    paths = options.get("testpaths") or ["pruebas/herramientas"]
    return copy / str(paths[0])


def check_hook_and_zip() -> list[str]:
    """En una copia: comprobación completa, gancho Stop (bien, mal, sin repetir) y ZIP."""
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / ROOT.name
        copy_project(copy)
        full = run_tool(copy, "herramientas/comprobar.py", "--sin-paquete")
        if full.returncode != 0:
            return ["comprobar.py falla en una copia limpia:\n" + full.stdout[-1500:]]
        hook = "herramientas/comprobar.py"
        if run_tool(copy, hook, "--gancho", stdin="{}").stdout.strip():
            problems.append("el gancho habla sin motivo con el código limpio")
        bad_test = first_test_dir(copy) / "test_zz_validar_kit.py"
        bad_test.write_text("def test_falla_a_proposito() -> None:\n    assert 1 == 2\n", encoding="utf-8")
        answer = run_tool(copy, hook, "--gancho", stdin='{"stop_hook_active": false}')
        try:
            context = json.loads(answer.stdout)["hookSpecificOutput"]["additionalContext"]
        except (ValueError, KeyError, TypeError):
            context = ""
        if "pytest" not in context:
            problems.append("el gancho no avisa de una prueba que falla")
        repeated = run_tool(copy, hook, "--gancho", stdin='{"stop_hook_active": true}')
        if repeated.stdout.strip():
            problems.append("el gancho repite el aviso sin cambios en el código")
        bad_test.unlink()
        problems += check_zip(copy, Path(tmp) / "salida")
    return problems


def check_zip(copy: Path, output: Path) -> list[str]:
    """El ZIP lleva lo imprescindible y deja fuera lo pesado, lo secreto y las colecciones."""
    for dummy in HEAVY_DUMMIES:
        path = copy / dummy
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x", encoding="utf-8")
    name = empaquetar_kit.project_name(copy)
    target, _ = empaquetar_kit.build_package(copy, output, name, keep=1)
    with zipfile.ZipFile(target) as archive:
        names = {n.split("/", 1)[1] for n in archive.namelist()}
    missing = [f"el ZIP no lleva {r}" for r in REQUIRED if r not in names]
    leaked = [f"el ZIP lleva {d}" for d in HEAVY_DUMMIES if d in names]
    return missing + leaked


def rel(path: Path) -> str:
    """Ruta relativa al proyecto, para mensajes cortos."""
    return path.relative_to(ROOT).as_posix()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida el taller entero.")
    parser.add_argument("--plantilla", action="store_true", help="admite marcadores {{...}}")
    args = parser.parse_args(argv)
    checks: list[tuple[str, Check]] = [
        ("archivos imprescindibles", check_required),
        ("CLAUDE.md", check_claude_md),
        ("ajustes y ganchos", check_settings),
        ("GitHub Actions", check_workflow),
        ("secretos", check_secrets),
        ("gancho y ZIP", check_hook_and_zip),
    ]
    if not args.plantilla:
        checks.insert(1, ("marcadores", check_placeholders))
    failures = 0
    for label, check in checks:
        problems = check()
        print(f"{'OK   ' if not problems else 'FALLO'} {label}")
        for problem in problems:
            print(f"      {problem}")
        failures += len(problems)
    print("Kit válido." if not failures else f"Kit con {failures} problema(s).")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
