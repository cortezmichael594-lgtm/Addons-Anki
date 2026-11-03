"""Prepara la sesión: instala lo que falte y dice qué hay pendiente en el taller.

Lo lanza el gancho SessionStart de .claude/settings.json al empezar o retomar una sesión de
claude.ai/code. En los hilos de un proyecto de Claude no hay ganchos: allí CLAUDE.md pide
ejecutarlo a mano (python herramientas/preparar.py).

1. En la nube (CLAUDE_CODE_REMOTE=true), si falta algo de requirements-dev.txt o de
   requirements-anki.txt, o tiene otra versión, lo instala con pip; en Linux, si falta la pieza
   gráfica libEGL que necesita Qt, la instala con apt-get. El script de preparación del entorno de
   la nube hace lo mismo una vez y queda en caché (véase docs/preparar-entorno.md); esto es la red
   de seguridad para cuando cambian las versiones.
2. Dice dónde está el código de Anki instalado y lo pendiente según empaquetar.py --revision (solo
   avisos y errores). Lo que imprime un gancho SessionStart se añade al contexto de Claude y cada
   línea cuesta tokens: por eso la salida es corta.
"""

from __future__ import annotations

import ctypes.util
import importlib.metadata
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIREMENTS = ("requirements-dev.txt", "requirements-anki.txt")
PIN_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+)(?:\[[^\]]*\])?\s*==\s*([^\s;#]+)")
INSTALL_HINT = "python -m pip install -q -r requirements-dev.txt -r requirements-anki.txt"
PIP_TIMEOUT = 240  # segundos; el gancho tiene 300 en total
APT_TIMEOUT = 120
MAX_PENDING = 15


def pins(root: Path = ROOT) -> dict[str, str]:
    """Paquetes con versión fija en los requirements: {nombre en minúsculas: versión}."""
    found: dict[str, str] = {}
    for name in REQUIREMENTS:
        path = root / name
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            match = PIN_RE.match(line)
            if match:
                found[match.group(1).lower()] = match.group(2)
    return found


def outdated(required: dict[str, str]) -> list[str]:
    """Paquetes que faltan o tienen otra versión que la fijada."""
    wrong: list[str] = []
    for name, version in required.items():
        try:
            installed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            wrong.append(name)
            continue
        if installed != version:
            wrong.append(f"{name} {installed}")
    return wrong


def pip_install() -> str | None:
    """Instala los requirements con pip; devuelve el problema si falla."""
    command = [sys.executable, "-m", "pip", "install", "-q", "--disable-pip-version-check"]
    for name in REQUIREMENTS:
        if (ROOT / name).is_file():
            command += ["-r", str(ROOT / name)]
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=PIP_TIMEOUT)
    except (OSError, subprocess.TimeoutExpired):
        return "no se pudieron instalar los requirements (pip no responde o tardó demasiado)"
    if done.returncode != 0:
        last = (done.stderr.strip().splitlines() or ["sin detalle"])[-1]
        return f"pip no pudo instalar los requirements ({last[:200]})"
    return None


def egl_missing() -> bool:
    """En Linux, Qt (y con él aqt) no se importa sin la biblioteca libEGL."""
    return sys.platform.startswith("linux") and ctypes.util.find_library("EGL") is None


def apt_install_egl() -> str | None:
    """Instala libegl1 con apt-get; devuelve el problema si no puede."""
    apt = shutil.which("apt-get")
    if apt is None or os.geteuid() != 0:
        return "falta la pieza gráfica libEGL y aquí no se puede instalar (apt-get install -y libegl1)"
    env = {**os.environ, "DEBIAN_FRONTEND": "noninteractive"}

    def step(*args: str) -> bool:
        try:
            return subprocess.run([apt, *args], capture_output=True, timeout=APT_TIMEOUT, env=env).returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            return False

    if step("install", "-y", "-q", "libegl1") or (step("update", "-q") and step("install", "-y", "-q", "libegl1")):
        return None
    return "no se pudo instalar la pieza gráfica libegl1 (apt-get install -y libegl1)"


def anki_folder() -> Path | None:
    """Carpeta site-packages con aqt, _aqt y anki, sin importarlos."""
    spec = importlib.util.find_spec("aqt")
    if spec is None or not spec.submodule_search_locations:
        return None
    return Path(next(iter(spec.submodule_search_locations))).resolve().parent


def pending_items(report: str) -> list[str]:
    """Avisos y errores de un informe de empaquetar.py, sin lo ya comprobado."""
    items: list[str] = []
    section = ""
    for line in report.splitlines():
        if line.startswith(("COMPROBADO", "AVISOS", "ERRORES")):
            section = line.split()[0]
        elif line.startswith("  - ") and section in ("AVISOS", "ERRORES"):
            items.append(("Error: " if section == "ERRORES" else "Aviso: ") + line[4:])
        elif line.strip() and not line.startswith(" "):
            section = ""
    return items


def revision() -> list[str]:
    """Lo pendiente según empaquetar.py --revision."""
    try:
        done = subprocess.run(
            [sys.executable, str(ROOT / "herramientas" / "empaquetar.py"), "--revision"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            env={**os.environ, "PYTHONUTF8": "1"},
        )
    except (OSError, subprocess.TimeoutExpired):
        return ["Aviso: no se pudo ejecutar empaquetar.py --revision."]
    return pending_items(done.stdout)


def main() -> int:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    lines: list[str] = []
    if os.environ.get("CLAUDE_CODE_REMOTE") == "true":
        if outdated(pins()):
            problem = pip_install()
            if problem:
                lines.append(f"Aviso: {problem}. Antes de comprobar: {INSTALL_HINT}")
        if egl_missing():
            problem = apt_install_egl()
            if problem:
                lines.append(f"Aviso: {problem}.")
    folder = anki_folder()
    if folder is None:
        lines.append(f"Aviso: Anki no está instalado en este Python. Instálelo con: {INSTALL_HINT}")
    else:
        lines.append(f"Código de Anki instalado: {folder.as_posix()} (carpetas aqt, _aqt y anki).")
    pending = revision()
    if pending:
        lines.append("Pendiente en el taller (atiéndelo en esta sesión; véase docs/normas-del-taller.md):")
        lines += [f"- {item}" for item in pending[:MAX_PENDING]]
        if len(pending) > MAX_PENDING:
            lines.append(f"- [... y {len(pending) - MAX_PENDING} más: python herramientas/empaquetar.py --revision]")
    else:
        lines.append("Revisión del taller: nada pendiente.")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
