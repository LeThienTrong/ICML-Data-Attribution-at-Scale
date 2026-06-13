from __future__ import annotations

import argparse
import re
from pathlib import Path


TIMESTAMP_RE = re.compile(
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2}),(\d{3})"
)


def srt_time_to_ass(value: str) -> str:
    hours, minutes, rest = value.split(":")
    seconds, milliseconds = rest.split(",")
    centiseconds = int(milliseconds) // 10
    return f"{int(hours)}:{minutes}:{seconds}.{centiseconds:02d}"


def escape_ass(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def parse_srt(path: Path) -> list[tuple[str, str, list[str]]]:
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip())
    cues: list[tuple[str, str, list[str]]] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 3:
            continue
        match = TIMESTAMP_RE.fullmatch(lines[1])
        if not match:
            continue
        start_raw, end_raw = lines[1].split("-->")
        cues.append((srt_time_to_ass(start_raw.strip()), srt_time_to_ass(end_raw.strip()), lines[2:]))
    return cues


def build_ass(cues: list[tuple[str, str, list[str]]]) -> str:
    header = """[Script Info]
ScriptType: v4.00+
ScaledBorderAndShadow: yes
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BilingualBox, Arial, 44, &H00FFFFFF, &H00FFFFFF, &H00000000, &H99000000, 0, 0, 0, 0, 100, 100, 0, 0, 3, 8, 0, 2, 110, 110, 62, 1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for start, end, lines in cues:
        vietnamese = escape_ass(lines[0])
        english = escape_ass(" ".join(lines[1:])) if len(lines) > 1 else ""
        text = r"{\fs48}" + vietnamese
        if english:
            text += r"\N{\fs34}" + english
        events.append(f"Dialogue: 0,{start},{end},BilingualBox,,0,0,0,,{text}")
    return header + "\n".join(events) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert bilingual SRT subtitles to styled ASS.")
    parser.add_argument("srt", type=Path)
    parser.add_argument("ass", type=Path, nargs="?")
    args = parser.parse_args()

    output = args.ass or args.srt.with_suffix(".ass")
    cues = parse_srt(args.srt)
    output.write_text(build_ass(cues), encoding="utf-8")
    print(f"Wrote {output} ({len(cues)} cues)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
