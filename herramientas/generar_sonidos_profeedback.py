"""Genera los 18 sonidos de serie de ProFeedback con la receta del informe 2.4.0 (apartado 8.9).

Síntesis aditiva pura (sumas de senos, sin muestras grabadas), en Do mayor pentatónica, con
tres voces (madera, campanilla y suave). Cada archivo se escala a su pico y se codifica a .mp3
mono de 44.100 Hz y 128 kbps con ffmpeg, sin etiquetas.

Uso: python herramientas/generar_sonidos_profeedback.py [carpeta_destino]
Sin destino, escribe en complementos/profeedback/sonidos. Necesita ffmpeg (solo en el taller;
el complemento no lo usa).
"""

from __future__ import annotations

import math
import shutil
import subprocess
import sys
import tempfile
import wave
from array import array
from pathlib import Path

RATE = 44_100

# La4 = 440 Hz, temperamento igual.
NOTES: dict[str, float] = {
    "Do4": 261.63,
    "Mi4": 329.63,
    "Sol4": 392.00,
    "La4": 440.00,
    "Do5": 523.25,
    "Re5": 587.33,
    "Mi5": 659.26,
    "Sol5": 783.99,
    "La5": 880.00,
    "Do6": 1046.50,
    "Re6": 1174.66,
    "Mi6": 1318.51,
    "Sol6": 1567.98,
    "Do7": 2093.00,
}

# Voz: (ataque en segundos, parciales [(razón, peso, factor de caída)]).
VOICES: dict[str, tuple[float, list[tuple[float, float, float]]]] = {
    "madera": (0.003, [(1, 1.00, 1.00), (4, 0.22, 0.35), (9.2, 0.05, 0.15)]),
    "campanilla": (0.005, [(1, 1.00, 1.00), (2, 0.30, 0.60), (3, 0.10, 0.40), (5.4, 0.03, 0.20)]),
    "suave": (0.015, [(1, 1.00, 1.00), (2, 0.12, 0.70), (3, 0.03, 0.50)]),
}

Note = tuple[str, int, float, float]  # nombre, inicio en ms, fuerza, caída en s

# (subcarpeta, archivo, voz, notas, duración en s, pico en dBFS)
RECIPE: list[tuple[str, str, str, list[Note], float, float]] = [
    ("correcto", "acierto-1-madera", "madera", [("Sol5", 0, 0.8, 0.05), ("Do6", 70, 1.0, 0.07)], 0.35, -12),
    ("correcto", "acierto-2-campanilla", "campanilla", [("La5", 0, 0.8, 0.06), ("Mi6", 65, 1.0, 0.08)], 0.38, -12),
    ("correcto", "acierto-3-suave", "suave", [("Do5", 0, 1.0, 0.08), ("Sol5", 0, 0.7, 0.08)], 0.35, -14),
    ("fallo", "fallo-1-madera", "madera", [("Mi4", 0, 1.0, 0.07)], 0.30, -15),
    ("fallo", "fallo-2-campanilla", "campanilla", [("La4", 0, 0.9, 0.06), ("Sol4", 80, 1.0, 0.08)], 0.40, -15),
    ("fallo", "fallo-3-suave", "suave", [("Sol4", 0, 1.0, 0.08)], 0.35, -16),
    (
        "finalizado/mazo",
        "mazo-1-madera",
        "madera",
        [("Do5", 0, 0.8, 0.12), ("Mi5", 110, 0.8, 0.12), ("Sol5", 220, 0.8, 0.12), ("Do6", 330, 1.0, 0.30)],
        1.20,
        -10,
    ),
    (
        "finalizado/mazo",
        "mazo-2-campanilla",
        "campanilla",
        [("Sol5", 0, 0.8, 0.15), ("Do6", 130, 0.8, 0.15), ("Mi6", 260, 1.0, 0.35)],
        1.30,
        -10,
    ),
    (
        "finalizado/mazo",
        "mazo-3-suave",
        "suave",
        [("Do5", 0, 1.0, 0.25), ("Sol5", 0, 0.7, 0.25), ("Mi5", 280, 1.0, 0.40), ("Do6", 280, 0.7, 0.40)],
        1.40,
        -11,
    ),
    (
        "finalizado/todo",
        "todo-1-madera",
        "madera",
        [
            ("Do5", 0, 0.8, 0.12),
            ("Re5", 100, 0.8, 0.12),
            ("Mi5", 200, 0.8, 0.12),
            ("Sol5", 300, 0.8, 0.12),
            ("La5", 400, 0.8, 0.12),
            ("Do6", 500, 0.9, 0.15),
            ("Do5", 650, 0.7, 0.45),
            ("Mi5", 650, 0.7, 0.45),
            ("Sol5", 650, 0.7, 0.45),
            ("Do6", 650, 1.0, 0.45),
        ],
        2.20,
        -9,
    ),
    (
        "finalizado/todo",
        "todo-2-campanilla",
        "campanilla",
        [
            ("Sol5", 0, 0.8, 0.15),
            ("Do6", 140, 0.8, 0.15),
            ("Mi6", 280, 0.8, 0.15),
            ("Sol6", 420, 0.8, 0.18),
            ("Do6", 620, 1.0, 0.50),
            ("Mi6", 620, 0.7, 0.50),
            ("Sol6", 620, 0.5, 0.50),
        ],
        2.35,
        -9,
    ),
    (
        "finalizado/todo",
        "todo-3-suave",
        "suave",
        [
            ("Do4", 0, 1.0, 0.25),
            ("Sol4", 0, 0.7, 0.25),
            ("Mi4", 300, 1.0, 0.25),
            ("Do5", 300, 0.7, 0.25),
            ("Sol4", 600, 1.0, 0.25),
            ("Mi5", 600, 0.7, 0.25),
            ("Do5", 900, 1.0, 0.50),
            ("Sol5", 900, 0.7, 0.50),
            ("Do6", 900, 0.5, 0.50),
        ],
        2.65,
        -10,
    ),
    (
        "perfecto-mazo",
        "perfecto-mazo-1-madera",
        "madera",
        [
            ("Do5", 0, 0.8, 0.12),
            ("Mi5", 100, 0.8, 0.12),
            ("Sol5", 200, 0.8, 0.12),
            ("Do6", 300, 0.8, 0.12),
            ("Mi6", 400, 0.8, 0.12),
            ("Do6", 520, 1.0, 0.35),
            ("Sol6", 520, 0.6, 0.35),
        ],
        1.50,
        -9,
    ),
    (
        "perfecto-mazo",
        "perfecto-mazo-2-campanilla",
        "campanilla",
        [
            ("Sol5", 0, 0.8, 0.15),
            ("Do6", 120, 0.8, 0.15),
            ("Mi6", 240, 0.8, 0.15),
            ("Sol6", 360, 0.8, 0.15),
            ("Do7", 480, 0.6, 0.40),
            ("Do6", 480, 1.0, 0.40),
        ],
        1.50,
        -9,
    ),
    (
        "perfecto-mazo",
        "perfecto-mazo-3-suave",
        "suave",
        [
            ("Do5", 0, 1.0, 0.22),
            ("Sol5", 0, 0.7, 0.22),
            ("Mi5", 250, 1.0, 0.22),
            ("Do6", 250, 0.7, 0.22),
            ("Sol5", 500, 1.0, 0.50),
            ("Mi6", 500, 0.7, 0.50),
        ],
        1.60,
        -10,
    ),
    (
        "perfecto-todo",
        "perfecto-todo-1-madera",
        "madera",
        [
            ("Do5", 0, 0.8, 0.11),
            ("Re5", 90, 0.8, 0.11),
            ("Mi5", 180, 0.8, 0.11),
            ("Sol5", 270, 0.8, 0.11),
            ("La5", 360, 0.8, 0.11),
            ("Do6", 450, 0.8, 0.11),
            ("Re6", 540, 0.8, 0.11),
            ("Mi6", 630, 0.9, 0.14),
            ("Do5", 780, 0.7, 0.45),
            ("Sol5", 780, 0.7, 0.45),
            ("Do6", 780, 1.0, 0.45),
            ("Mi6", 780, 0.7, 0.45),
            ("Do6", 1200, 0.5, 0.45),
            ("Mi6", 1200, 0.4, 0.45),
            ("Sol6", 1200, 0.4, 0.45),
        ],
        2.80,
        -8,
    ),
    (
        "perfecto-todo",
        "perfecto-todo-2-campanilla",
        "campanilla",
        [
            ("Sol5", 0, 0.8, 0.15),
            ("Do6", 130, 0.8, 0.15),
            ("Mi6", 260, 0.8, 0.15),
            ("Sol6", 390, 0.8, 0.15),
            ("Do6", 560, 0.8, 0.15),
            ("Mi6", 690, 0.8, 0.15),
            ("Sol6", 820, 0.8, 0.15),
            ("Do7", 950, 0.7, 0.18),
            ("Do6", 1150, 1.0, 0.50),
            ("Mi6", 1150, 0.7, 0.50),
            ("Sol6", 1150, 0.5, 0.50),
            ("Do7", 1150, 0.3, 0.50),
        ],
        2.90,
        -8,
    ),
    (
        "perfecto-todo",
        "perfecto-todo-3-suave",
        "suave",
        [
            ("Do4", 0, 1.0, 0.24),
            ("Sol4", 0, 0.7, 0.24),
            ("Mi4", 280, 1.0, 0.24),
            ("Do5", 280, 0.7, 0.24),
            ("Sol4", 560, 1.0, 0.24),
            ("Mi5", 560, 0.7, 0.24),
            ("Do5", 840, 1.0, 0.24),
            ("Sol5", 840, 0.7, 0.24),
            ("Mi5", 1120, 1.0, 0.50),
            ("Do6", 1120, 0.7, 0.50),
            ("Sol6", 1120, 0.4, 0.50),
        ],
        2.90,
        -9,
    ),
]


def render(voice: str, notes: list[Note], seconds: float, peak_db: float) -> list[float]:
    attack, partials = VOICES[voice]
    total = round(seconds * RATE)
    out = [0.0] * total
    for name, start_ms, strength, decay in notes:
        freq = NOTES[name]
        start = round(start_ms / 1000 * RATE)
        attack_n = max(1, round(attack * RATE))
        for i in range(start, total):
            t = (i - start) / RATE
            env = 0.5 - 0.5 * math.cos(math.pi * (i - start) / attack_n) if i - start < attack_n else 1.0
            value = 0.0
            for ratio, weight, factor in partials:
                value += weight * math.exp(-t / (decay * factor)) * math.sin(2 * math.pi * freq * ratio * t)
            out[i] += strength * env * value
    # Atenuación final: 10 ms en los cortos, 40 ms en los demás.
    fade = int((0.010 if seconds < 0.6 else 0.040) * RATE)
    for k in range(fade):
        out[total - 1 - k] *= k / fade
    peak = max(abs(x) for x in out) or 1.0
    target = 10 ** (peak_db / 20)
    return [x * target / peak for x in out]


def write_mp3(samples: list[float], target: Path) -> None:
    data = array("h", (max(-32767, min(32767, round(x * 32767))) for x in samples))
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "s.wav"
        with wave.open(str(wav), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(RATE)
            handle.writeframes(data.tobytes())
        target.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-i",
                str(wav),
                "-ac",
                "1",
                "-ar",
                str(RATE),
                "-codec:a",
                "libmp3lame",
                "-b:a",
                "128k",
                "-map_metadata",
                "-1",
                "-id3v2_version",
                "0",
                "-write_xing",
                "0",
                str(target),
            ],
            check=True,
        )


def main() -> int:
    if shutil.which("ffmpeg") is None:
        print("Falta ffmpeg.", file=sys.stderr)
        return 1
    root = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else (Path(__file__).resolve().parent.parent / "complementos" / "profeedback" / "sonidos")
    )
    for folder, name, voice, notes, seconds, peak in RECIPE:
        write_mp3(render(voice, notes, seconds, peak), root / folder / f"{name}.mp3")
        print(f"{folder}/{name}.mp3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
