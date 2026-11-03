"""Genera el ZIP del taller entero (este repositorio), sin carpetas pesadas, secretos ni colecciones.

Uso:
    python herramientas/empaquetar_kit.py [--salida CARPETA] [--nombre NOMBRE] [--conservar N]

No confundir con empaquetar.py, que comprueba y empaqueta un complemento (.ankiaddon). Este ZIP
sirve para entregar o mover el taller completo; en el día a día no hace falta.

Las exclusiones están aquí, en código, para que se cumplan siempre sin depender de que alguien
las recuerde. Si el proyecto es un repositorio git, además se respeta su .gitignore. El ZIP lleva
una sola carpeta raíz con el nombre del proyecto y se verifica después de crearlo; si algo no
cuadra, se descarta.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent

# Carpetas que nunca entran, estén donde estén.
EXCLUDED_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "venv",
        "env",
        ".tox",
        ".nox",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".cache",
        "htmlcov",
        "dist",
        "build",
        "entregas",
        ".idea",
        ".vscode",
        ".ipynb_checkpoints",
        "site-packages",
        "collection.media",
    }
)
EXCLUDED_DIR_PATTERNS = ("*.egg-info",)

# Archivos que nunca entran: compilados, basura del sistema, registros,
# secretos y ajustes personales de Claude Code.
EXCLUDED_FILE_PATTERNS = (
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    "*.log",
    ".coverage",
    "coverage.xml",
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "settings.local.json",
    "CLAUDE.local.md",
    # Colecciones y copias de Anki: son datos de la persona y nunca viajan.
    "*.anki2",
    "*.anki21",
    "*.anki21b",
    "*.colpkg",
)
ALLOWED_FILES = frozenset({".env.example"})


def is_excluded(relative: PurePosixPath) -> bool:
    """Indica si una ruta relativa a la raíz del proyecto debe quedar fuera del ZIP."""
    *dirs, name = relative.parts
    for directory in dirs:
        if directory in EXCLUDED_DIRS:
            return True
        if any(fnmatch.fnmatch(directory, p) for p in EXCLUDED_DIR_PATTERNS):
            return True
    if name in ALLOWED_FILES:
        return False
    return any(fnmatch.fnmatch(name, p) for p in EXCLUDED_FILE_PATTERNS)


def _list_with_git(root: Path) -> list[Path] | None:
    """Archivos versionados o nuevos no ignorados; None si no hay git o repositorio."""
    command = [
        "git",
        "-C",
        str(root),
        "ls-files",
        "-z",
        "--cached",
        "--others",
        "--exclude-standard",
    ]
    try:
        result = subprocess.run(command, capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    names = result.stdout.decode("utf-8", errors="replace").split("\0")
    return [root / n for n in names if n]


def _list_by_walking(root: Path) -> list[Path]:
    """Todos los archivos bajo la raíz, sin entrar en las carpetas excluidas."""
    files: list[Path] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in directory.iterdir():
            if entry.is_symlink():
                continue
            if entry.is_dir():
                if entry.name not in EXCLUDED_DIRS:
                    pending.append(entry)
            elif entry.is_file():
                files.append(entry)
    return files


def project_files(root: Path) -> list[Path]:
    """Lista ordenada de los archivos que entran en el ZIP."""
    candidates = _list_with_git(root)
    if candidates is None:
        candidates = _list_by_walking(root)
    chosen = [
        p
        for p in candidates
        if p.is_file() and not p.is_symlink() and not is_excluded(PurePosixPath(p.relative_to(root).as_posix()))
    ]
    return sorted(chosen)


def project_name(root: Path) -> str:
    """Nombre de pyproject.toml; si no hay, el de la carpeta."""
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        with pyproject.open("rb") as f:
            data = tomllib.load(f)
        name = data.get("project", {}).get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return root.name


def write_zip(root: Path, target: Path, top_folder: str) -> list[Path]:
    """Escribe el ZIP con una sola carpeta raíz y devuelve los archivos incluidos."""
    files = project_files(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, strict_timestamps=False
    ) as archive:
        for file in files:
            archive.write(file, f"{top_folder}/{file.relative_to(root).as_posix()}")
    return files


def verify_zip(target: Path, top_folder: str, expected: int) -> list[str]:
    """Comprueba integridad, recuento, carpeta raíz única y ausencia de excluidos."""
    problems: list[str] = []
    with zipfile.ZipFile(target) as archive:
        broken = archive.testzip()
        names = archive.namelist()
    if broken:
        problems.append(f"archivo dañado dentro del ZIP: {broken}")
    if len(names) != expected:
        problems.append(f"el ZIP tiene {len(names)} archivos y se esperaban {expected}")
    for name in names:
        path = PurePosixPath(name)
        if path.parts[0] != top_folder:
            problems.append(f"fuera de la carpeta raíz: {name}")
        elif is_excluded(PurePosixPath(*path.parts[1:])):
            problems.append(f"no debería estar: {name}")
    return problems


def prune(output: Path, name: str, keep: int) -> None:
    """Deja solo los `keep` ZIP más recientes de este proyecto."""
    archives = sorted(output.glob(f"{name}_*.zip"))
    for old in archives[: max(0, len(archives) - keep)]:
        old.unlink()


def build_package(root: Path, output: Path, name: str, keep: int) -> tuple[Path, int]:
    """Crea y verifica el ZIP; devuelve su ruta y el número de archivos."""
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    target = output / f"{name}_{stamp}.zip"
    files = write_zip(root, target, name)
    problems = verify_zip(target, name, len(files))
    if problems:
        target.unlink(missing_ok=True)
        raise RuntimeError("ZIP descartado: " + "; ".join(problems[:5]))
    prune(output, name, keep)
    return target, len(files)


def readable(path: Path) -> str:
    """Ruta relativa al proyecto si es posible, para mensajes cortos."""
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Genera el ZIP del taller entero.")
    parser.add_argument("--salida", type=Path, default=ROOT / "entregas")
    parser.add_argument("--nombre", default=None, help="carpeta raíz y prefijo del ZIP")
    parser.add_argument("--conservar", type=int, default=5, help="ZIP que se guardan")
    args = parser.parse_args(argv)
    name = args.nombre or project_name(ROOT)
    try:
        target, total = build_package(ROOT, args.salida.resolve(), name, args.conservar)
    except (OSError, RuntimeError, zipfile.BadZipFile) as error:
        print(f"Empaquetado fallido: {error}", file=sys.stderr)
        return 1
    size_kb = target.stat().st_size // 1024 + 1
    print(f"ZIP: {readable(target)} ({total} archivos, {size_kb} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
