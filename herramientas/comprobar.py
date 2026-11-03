"""Comprueba el taller y, si todo pasa, deja el .ankiaddon de cada complemento cambiado.

Uso:
    python herramientas/comprobar.py                formatea herramientas y pruebas, corrige lo automático,
                                                    revisa, prueba y empaqueta los complementos cambiados
    python herramientas/comprobar.py --sin-paquete  lo mismo, sin generar ningún .ankiaddon
    python herramientas/comprobar.py --todos        revisa todos los complementos, no solo los cambiados
    python herramientas/comprobar.py --ci           solo revisa (GitHub Actions): no cambia ni empaqueta nada
    python herramientas/comprobar.py --gancho       lo lanza el gancho Stop de Claude Code
    python herramientas/comprobar.py --paquetes DIR (GitHub Actions) empaqueta los complementos cambiados
                                                    y copia sus .ankiaddon a DIR

Qué revisa:
  1. ruff: formato y reglas en herramientas/ y pruebas/; en complementos/, solo errores graves.
  2. mypy de las herramientas (los complementos los revisa empaquetar.py, con la API de Anki).
  3. pytest de las herramientas.
  4. Que todos los JSON se puedan leer.
  5. empaquetar.py --solo-comprobar en cada complemento cambiado respecto a la rama principal (su
     código, sus pruebas o su documentación): manifiesto, colores, notas FIX, documentación, mypy con
     la API de Anki, importación y sus pruebas, cada complemento en su propio proceso. Si no cambió
     ninguno, la revisión del taller (empaquetar.py --revision); si cambió empaquetar.py, además su
     autoprueba.

La salida es corta a propósito: Claude la lee entera y cada línea cuesta tokens. En modo --gancho no
cambia ningún archivo y avisa una sola vez por cada estado del código, para que Claude no entre en
bucle si no puede arreglar algo.
"""

from __future__ import annotations

import argparse
import ctypes.util
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

import empaquetar_kit

ROOT = empaquetar_kit.ROOT
STATE_FILE = ROOT / ".cache" / "comprobar.json"
PACKAGER = "herramientas/empaquetar.py"
TOOLS = ("ruff", "mypy", "pytest")
WATCHED_SUFFIXES = frozenset({".py", ".pyi", ".toml", ".json", ".cfg", ".ini", ".md", ".txt", ".js", ".css", ".html"})
CODE_DIRS = ("herramientas", "pruebas")
ADDON_TOP_DIRS = ("complementos", "pruebas", "docs")
MAIN_BRANCHES = ("origin/main", "main")
HEAD_LINES = 15
TAIL_LINES = 25
MAX_CHARS = 3000
STEP_TIMEOUT = 300  # segundos por paso
INSTALL_HINT = "python -m pip install -q -r requirements-dev.txt -r requirements-anki.txt"
EGL_HINT = "apt-get install -y libegl1"


@dataclass(frozen=True)
class StepResult:
    """Resultado de un paso: nombre, si pasó, resumen corto y salida recortada."""

    name: str
    ok: bool
    summary: str = ""
    output: str = ""


def count(n: int, singular: str, plural: str) -> str:
    """«1 archivo», «3 archivos»."""
    return f"{n} {singular if n == 1 else plural}"


def trim(text: str) -> str:
    """Recorta una salida larga: principio y final, con un tope de caracteres."""
    lines = [line for line in text.strip().splitlines() if line.strip()]
    if len(lines) > HEAD_LINES + TAIL_LINES:
        skipped = len(lines) - HEAD_LINES - TAIL_LINES
        lines = [*lines[:HEAD_LINES], f"[... {skipped} líneas omitidas ...]", *lines[-TAIL_LINES:]]
    result = "\n".join(lines)
    if len(result) > MAX_CHARS:
        result = result[:MAX_CHARS] + "\n[... recortado ...]"
    return result


def child_env() -> dict[str, str]:
    """Entorno de los procesos hijos: UTF-8, sin colores y Qt sin pantalla."""
    return {**os.environ, "PYTHONUTF8": "1", "NO_COLOR": "1", "QT_QPA_PLATFORM": "offscreen"}


def run_python(name: str, args: list[str]) -> StepResult:
    """Ejecuta `python <args>` en la raíz del proyecto y recorta su salida."""
    try:
        done = subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=STEP_TIMEOUT,
            env=child_env(),
        )
    except subprocess.TimeoutExpired:
        return StepResult(name, False, output=f"{name} tardó más de {STEP_TIMEOUT} s y se detuvo.")
    return StepResult(name, done.returncode == 0, output=trim(done.stdout + "\n" + done.stderr))


def run_module(name: str, args: list[str]) -> StepResult:
    """Ejecuta `python -m <args>` en la raíz del proyecto."""
    return run_python(name, ["-m", *args])


def git(args: list[str]) -> str | None:
    """Salida de una orden git en la raíz, o None si git falla o no hay repositorio."""
    try:
        done = subprocess.run(
            ["git", "-C", str(ROOT), *args], capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
    except OSError:
        return None
    return done.stdout if done.returncode == 0 else None


def missing_tools() -> list[str]:
    """Piezas que faltan en este Python: herramientas de revisión, Anki y, en Linux, libEGL."""
    missing = [tool for tool in TOOLS if importlib.util.find_spec(tool) is None]
    if importlib.util.find_spec("aqt") is None:
        missing.append("aqt (Anki)")
    if sys.platform.startswith("linux") and ctypes.util.find_library("EGL") is None:
        missing.append(f"libEGL (instálela con: {EGL_HINT})")
    return missing


def watched_files() -> list[Path]:
    """Archivos cuyo cambio obliga a comprobar de nuevo."""
    return [
        p
        for p in empaquetar_kit.project_files(ROOT)
        if p.suffix in WATCHED_SUFFIXES or p.name.startswith("requirements")
    ]


def fingerprint() -> str:
    """Huella del estado del código: ruta, tamaño y fecha de cada archivo vigilado."""
    digest = hashlib.sha256()
    for path in watched_files():
        info = path.stat()
        line = f"{path.relative_to(ROOT).as_posix()}|{info.st_size}|{info.st_mtime_ns}\n"
        digest.update(line.encode("utf-8"))
    return digest.hexdigest()


def load_state() -> dict[str, str]:
    """Últimas huellas comprobadas; vacío si no hay o están dañadas."""
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {k: v for k, v in data.items() if isinstance(k, str) and isinstance(v, str)}


def save_state(*, ok: str | None = None, fail: str | None = None) -> None:
    """Guarda la huella del último resultado correcto o fallido."""
    state = {k: v for k, v in (("ok", ok), ("fail", fail)) if v is not None}
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state), encoding="utf-8")


def needs_check(current: str, state: dict[str, str]) -> bool:
    """El gancho solo comprueba si este estado del código no se ha comprobado ya."""
    return current not in (state.get("ok"), state.get("fail"))


def addon_names() -> list[str]:
    """Carpetas de complementos/ que son un complemento (tienen manifest.json)."""
    folder = ROOT / "complementos"
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.iterdir() if (p / "manifest.json").is_file())


def changed_paths() -> list[str] | None:
    """Rutas cambiadas respecto a la rama principal: commits de esta rama, cambios sin guardar y archivos
    nuevos. None si no hay git o no se encuentra la rama principal."""
    base = next((ref for ref in MAIN_BRANCHES if git(["rev-parse", "--verify", "--quiet", ref]) is not None), None)
    if base is None:
        return None
    merge_base = (git(["merge-base", "HEAD", base]) or "").strip() or base
    changed = git(["diff", "--name-only", merge_base])
    new = git(["ls-files", "--others", "--exclude-standard"])
    if changed is None or new is None:
        return None
    return sorted({line.strip() for line in (changed + "\n" + new).splitlines() if line.strip()})


def addons_from_paths(paths: Iterable[str], known: Iterable[str]) -> list[str]:
    """Complementos afectados por unas rutas: su código, sus pruebas o su documentación."""
    names = set(known)
    found: set[str] = set()
    for path in paths:
        parts = PurePosixPath(path).parts
        if len(parts) > 2 and parts[0] in ADDON_TOP_DIRS and parts[1] in names:
            found.add(parts[1])
    return sorted(found)


def apply_fixes() -> str:
    """Formatea y aplica las correcciones automáticas seguras en herramientas/ y pruebas/."""
    formatted = run_module("formato", ["ruff", "format", *CODE_DIRS])
    run_module("ruff --fix", ["ruff", "check", "--fix", "--exit-zero", "--quiet", *CODE_DIRS])
    match = re.search(r"(\d+) files? reformatted", formatted.output)
    return f"Formato aplicado a {count(int(match.group(1)), 'archivo', 'archivos')}." if match else ""


def check_json() -> StepResult:
    """Todos los JSON del proyecto deben poder leerse."""
    files = [p for p in empaquetar_kit.project_files(ROOT) if p.suffix == ".json"]
    errors: list[str] = []
    for path in files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            errors.append(f"{path.relative_to(ROOT).as_posix()}: {error}")
    return StepResult("JSON", not errors, count(len(files), "archivo", "archivos"), "\n".join(errors))


def passed_tests(output: str) -> int:
    """Pruebas correctas según el resumen de pytest."""
    match = re.search(r"(\d+) passed", output)
    return int(match.group(1)) if match else 0


def addon_tests(output: str) -> int | None:
    """Pruebas correctas de un complemento según el informe de empaquetar.py («Pruebas: 37 correctas»)."""
    match = re.search(r"Pruebas: (\d+) correctas", output)
    return int(match.group(1)) if match else None


def packager_warnings(output: str) -> list[str]:
    """Líneas del apartado AVISOS de un informe de empaquetar.py."""
    warnings: list[str] = []
    inside = False
    for line in output.splitlines():
        if line.startswith("AVISOS"):
            inside = True
        elif inside and line.startswith("  - "):
            warnings.append(line[4:])
        elif inside and line.strip() and not line.startswith(" "):
            inside = False
    return warnings


def run_packager_checks(addons: list[str], tool_changed: bool) -> tuple[list[StepResult], list[str]]:
    """empaquetar.py en cada complemento (o la revisión del taller si no hay ninguno) y su autoprueba."""
    results: list[StepResult] = []
    warnings: list[str] = []
    for name in addons:
        result = run_python(f"empaquetar {name}", [PACKAGER, name, "--solo-comprobar"])
        found = packager_warnings(result.output)
        warnings += [f"{name}: {w}" for w in found]
        tests = addon_tests(result.output)
        parts = [count(tests, "prueba", "pruebas")] if tests is not None else []
        summary = ", ".join([*parts, count(len(found), "aviso", "avisos")])
        results.append(StepResult(result.name, result.ok, summary, result.output))
    if not addons:
        result = run_python("revisión del taller", [PACKAGER, "--revision"])
        warnings += [f"taller: {w}" for w in packager_warnings(result.output)]
        results.append(StepResult(result.name, result.ok, output=result.output))
    if tool_changed:
        result = run_python("autoprueba de empaquetar", [PACKAGER, "--autoprueba"])
        results.append(StepResult(result.name, result.ok, output=result.output))
    return results, warnings


def build_packages(addons: list[str]) -> tuple[list[Path], list[str]]:
    """Genera el .ankiaddon de cada complemento (ya comprobado) y devuelve los paquetes y los fallos."""
    built: list[Path] = []
    failures: list[str] = []
    for name in addons:
        result = run_python(f"paquete {name}", [PACKAGER, name, "--sin-mypy", "--sin-importar", "--sin-pruebas"])
        match = re.search(r"(?m)^PAQUETE: (.+)$", result.output)
        if result.ok and match:
            built.append(Path(match.group(1).strip()))
        else:
            failures.append(f"[{name}]\n{result.output}")
    return built, failures


def run_checks(addons: list[str], tool_changed: bool) -> tuple[list[StepResult], list[str]]:
    """Revisiones que no cambian nada del proyecto."""
    results = [
        run_module("formato", ["ruff", "format", "--check", *CODE_DIRS]),
        run_module("ruff", ["ruff", "check", "--output-format", "concise", "--quiet", "."]),
        run_module("mypy", ["mypy", "--no-pretty"]),
    ]
    tests = run_module("pytest", ["pytest", "-q", "--no-header", "--tb=short", "-rfE"])
    passed = passed_tests(tests.output)
    results.append(StepResult(tests.name, tests.ok, count(passed, "prueba", "pruebas"), tests.output))
    results.append(check_json())
    packager_results, warnings = run_packager_checks(addons, tool_changed)
    return results + packager_results, warnings


def report(results: list[StepResult], warnings: list[str]) -> tuple[bool, str]:
    """Texto corto con lo que pasó; detalle solo de lo que falla y de los avisos."""
    failed = [r for r in results if not r.ok]
    if not failed:
        names = ", ".join(f"{r.name} ({r.summary})" if r.summary else r.name for r in results)
        lines = [f"Comprobación correcta: {names}."]
    else:
        lines = [f"Comprobación con fallos: {', '.join(r.name for r in failed)}."]
        for r in failed:
            lines += [f"--- {r.name} ---", r.output or "(sin detalle)"]
    if warnings:
        lines.append("Avisos de empaquetar.py (corríjalos o explíquelos en la entrega):")
        lines += [f"  - {w}" for w in warnings[:15]]
        if len(warnings) > 15:
            lines.append(f"  [... y {len(warnings) - 15} más ...]")
    return not failed, "\n".join(lines)


def hook_feedback(text: str) -> None:
    """Respuesta del gancho Stop: Claude sigue trabajando con este aviso."""
    message = (
        "Las comprobaciones automáticas no pasan. Corrígelo y ejecuta "
        "`python herramientas/comprobar.py`; si no puedes, explica a la persona qué falla "
        "y por qué. Este aviso no se repite mientras el código no cambie.\n\n" + text
    )
    output = {"hookSpecificOutput": {"hookEventName": "Stop", "additionalContext": message}}
    print(json.dumps(output, ensure_ascii=False))


def read_hook_input() -> dict[str, object]:
    """Lee el JSON que Claude Code envía al gancho; tolera que no llegue nada."""
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def select_addons(all_addons: bool) -> tuple[list[str], bool, str]:
    """Complementos que se revisan, si cambió empaquetar.py y una nota para la salida."""
    known = addon_names()
    if all_addons:
        return known, True, ""
    paths = changed_paths()
    if paths is None:
        return [], False, "Sin git o sin rama principal: no se revisa ningún complemento con empaquetar.py."
    return addons_from_paths(paths, known), PACKAGER in paths, ""


def copy_packages(built: list[Path], target: Path) -> None:
    """Copia los .ankiaddon generados a la carpeta indicada (artefacto de GitHub)."""
    target.mkdir(parents=True, exist_ok=True)
    for path in built:
        shutil.copy2(path, target / path.name)


def main(argv: list[str] | None = None) -> int:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Comprueba el taller de complementos.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--ci", action="store_true", help="solo revisa (GitHub Actions)")
    mode.add_argument("--gancho", action="store_true", help="modo del gancho Stop")
    mode.add_argument("--paquetes", type=Path, metavar="DIR", help="solo empaqueta los cambiados y los copia a DIR")
    parser.add_argument("--sin-paquete", action="store_true", help="no genera ningún .ankiaddon")
    parser.add_argument("--todos", action="store_true", help="revisa todos los complementos")
    args = parser.parse_args(argv)

    if args.paquetes is not None:
        addons, _, note = select_addons(args.todos)
        if not addons:
            print(note or "Ningún complemento cambiado: no hay paquetes que generar.")
            return 0
        built, failures = build_packages(addons)
        copy_packages(built, args.paquetes)
        print("\n".join([f"Paquete: {p.name}" for p in built] + failures))
        return 1 if failures else 0

    current = fingerprint()
    if args.gancho:
        read_hook_input()
        if not needs_check(current, load_state()):
            return 0
    missing = missing_tools()
    if missing:
        text = f"Faltan piezas: {', '.join(missing)}. Instálelas con: {INSTALL_HINT}"
        if args.gancho:
            save_state(fail=current)
            hook_feedback(text)
            return 0
        print(text)
        return 1

    fixes = "" if args.ci or args.gancho else apply_fixes()
    current = fingerprint()
    addons, tool_changed, note = select_addons(args.todos)
    results, warnings = run_checks(addons, tool_changed)
    ok, text = report(results, warnings)
    if not addons and not note:
        text += "\nComplementos: ninguno cambiado respecto a la rama principal."
    if note:
        text += "\n" + note
    if ok and addons and not (args.ci or args.gancho or args.sin_paquete):
        built, failures = build_packages(addons)
        if failures:
            ok, text = False, text + "\nEmpaquetado fallido:\n" + "\n".join(failures)
        else:
            text += "\nPaquetes: " + ", ".join(empaquetar_kit.readable(p) for p in built)
        current = fingerprint()
    if ok:
        save_state(ok=current)
    else:
        save_state(fail=current)

    if args.gancho:
        if not ok:
            hook_feedback(text)
        return 0
    print("\n".join(filter(None, [fixes, text])))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
