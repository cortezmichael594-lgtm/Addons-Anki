"""Pruebas de las herramientas: qué entra en el ZIP del taller, qué complementos se revisan y cuándo
comprueba el gancho."""

from __future__ import annotations

import zipfile
from pathlib import Path, PurePosixPath

import pytest

import comprobar
import empaquetar_kit
import preparar


@pytest.mark.parametrize(
    "path",
    [
        ".git/config",
        ".venv/Lib/site-packages/x.py",
        "web/node_modules/lib/index.js",
        "complementos/gritmap/__pycache__/logic.cpython-313.pyc",
        ".pytest_cache/v/cache/nodeids",
        ".cache/comprobar.json",
        "entregas/gritmap-3.5.0.ankiaddon",
        ".env",
        "config/.env.production",
        "certs/server.pem",
        ".claude/settings.local.json",
        "paquete.egg-info/PKG-INFO",
        "debug.log",
        "perfil/collection.anki2",
        "perfil/collection.anki21b",
        "perfil/collection.media/foto.jpg",
        "copias/backup-2026-11-03.colpkg",
    ],
)
def test_excluded_paths(path: str) -> None:
    assert empaquetar_kit.is_excluded(PurePosixPath(path))


@pytest.mark.parametrize(
    "path",
    [
        "CLAUDE.md",
        ".claude/settings.json",
        ".github/workflows/comprobar.yml",
        ".gitignore",
        ".gitattributes",
        ".env.example",
        "complementos/gritmap/__init__.py",
        "paquetes/gritmap-3.5.0.ankiaddon",
    ],
)
def test_included_paths(path: str) -> None:
    assert not empaquetar_kit.is_excluded(PurePosixPath(path))


def test_zip_has_one_top_folder_and_no_heavy_dirs(tmp_path: Path) -> None:
    project = tmp_path / "demo"
    for relative in ["CLAUDE.md", ".claude/settings.json", "complementos/a/__init__.py", ".venv/x.py", ".env"]:
        file = project / relative
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("x", encoding="utf-8")
    target, total = empaquetar_kit.build_package(project, tmp_path / "out", "demo", keep=5)
    with zipfile.ZipFile(target) as archive:
        names = sorted(archive.namelist())
    assert total == 3
    assert names == ["demo/.claude/settings.json", "demo/CLAUDE.md", "demo/complementos/a/__init__.py"]


def test_prune_keeps_latest(tmp_path: Path) -> None:
    for stamp in ["2026-01-01_000000", "2026-01-02_000000", "2026-01-03_000000"]:
        (tmp_path / f"demo_{stamp}.zip").write_bytes(b"")
    empaquetar_kit.prune(tmp_path, "demo", keep=2)
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "demo_2026-01-02_000000.zip",
        "demo_2026-01-03_000000.zip",
    ]


def test_hook_checks_only_new_states() -> None:
    assert comprobar.needs_check("nueva", {})
    assert not comprobar.needs_check("a", {"ok": "a"})
    assert not comprobar.needs_check("b", {"fail": "b"})
    assert comprobar.needs_check("c", {"ok": "a", "fail": "b"})


def test_trim_keeps_head_and_tail() -> None:
    text = "\n".join(f"línea {n}" for n in range(100))
    trimmed = comprobar.trim(text)
    assert "línea 0" in trimmed
    assert "línea 99" in trimmed
    assert "omitidas" in trimmed


def test_changed_addons_come_from_code_tests_and_docs() -> None:
    paths = [
        "complementos/gritmap/logic.py",
        "pruebas/nocturne/test_paleta.py",
        "docs/hider/que-hace.md",
        "docs/guia-interfaz.md",
        "complementos/LEEME.txt",
        "herramientas/empaquetar.py",
        "complementos/ajeno/__init__.py",
    ]
    known = ["gritmap", "hider", "nocturne", "restart"]
    assert comprobar.addons_from_paths(paths, known) == ["gritmap", "hider", "nocturne"]


def test_packager_report_is_read() -> None:
    report = (
        "COMPROBADO\n  - Pruebas: 37 correctas (colección temporal, nunca la real).\n"
        "AVISOS (revíselos uno a uno: corríjalos o explíquelos en la entrega)\n  - Primer aviso.\n  - Segundo aviso.\n"
        "\nRESULTADO: CORRECTO (2 aviso(s)) (solo comprobación).\n"
    )
    assert comprobar.packager_warnings(report) == ["Primer aviso.", "Segundo aviso."]
    assert comprobar.addon_tests(report) == 37
    assert comprobar.addon_tests("RESULTADO: CORRECTO") is None
    assert preparar.pending_items(report) == ["Aviso: Primer aviso.", "Aviso: Segundo aviso."]


def test_pins_read_both_requirements(tmp_path: Path) -> None:
    (tmp_path / "requirements-dev.txt").write_text("# comentario\nruff==0.17.3\npyyaml==6.0.3\n", encoding="utf-8")
    (tmp_path / "requirements-anki.txt").write_text("aqt[qt]==26.9.3\n", encoding="utf-8")
    assert preparar.pins(tmp_path) == {"ruff": "0.17.3", "pyyaml": "6.0.3", "aqt": "26.9.3"}
