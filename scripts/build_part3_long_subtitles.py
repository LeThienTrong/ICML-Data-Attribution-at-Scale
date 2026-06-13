from __future__ import annotations

import argparse
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path

from build_part3_long_timeline import extract_sections
from srt_to_ass import escape_ass, srt_time_to_ass


ROOT = Path(__file__).resolve().parents[1]
VOICE_SCRIPT = ROOT / "docs" / "part3_scaling_and_evaluation_voice_script.md"
ENGLISH_LINES = ROOT / "subtitles" / "part3_scaling_and_evaluation_english_lines.txt"
SRT_OUTPUT = ROOT / "subtitles" / "part3_scaling_and_evaluation_bilingual.srt"
ASS_OUTPUT = ROOT / "subtitles" / "part3_scaling_and_evaluation_bilingual.ass"


@dataclass
class Cue:
    start: float
    end: float
    vietnamese: str
    english: str = ""


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+|(?<=:)\s+", text)
    return [part.strip() for part in parts if part.strip()]


def voice_to_cues(text: str, max_chars: int) -> list[str]:
    paragraphs = [re.sub(r"\s+", " ", part.strip()) for part in re.split(r"\n\s*\n", text) if part.strip()]
    cues: list[str] = []
    for paragraph in paragraphs:
        current = ""
        for sentence in split_sentences(paragraph):
            if len(sentence) > max_chars:
                if current:
                    cues.append(current)
                    current = ""
                cues.append(sentence)
                continue
            candidate = f"{current} {sentence}".strip() if current else sentence
            if current and len(candidate) > max_chars:
                cues.append(current)
                current = sentence
            else:
                current = candidate
        if current:
            cues.append(current)
    return cues


def merge_short_texts(texts: list[str], *, min_chars: int = 28, max_merged_chars: int = 180) -> list[str]:
    merged: list[str] = []
    for text in texts:
        if not merged:
            merged.append(text)
            continue
        if len(text) < min_chars and len(merged[-1]) + 1 + len(text) <= max_merged_chars:
            merged[-1] = f"{merged[-1]} {text}"
        else:
            merged.append(text)
    if len(merged) >= 2 and len(merged[-1]) < min_chars and len(merged[-2]) + 1 + len(merged[-1]) <= max_merged_chars:
        merged[-2] = f"{merged[-2]} {merged[-1]}"
        merged.pop()
    return merged


def allocate(section_start: float, duration: float, texts: list[str]) -> list[tuple[float, float, str]]:
    if not texts:
        return []
    weights = [max(1, len(text)) for text in texts]
    total = sum(weights)
    cursor = section_start
    allocated: list[tuple[float, float, str]] = []
    for index, (text, weight) in enumerate(zip(texts, weights, strict=True)):
        end = section_start + duration if index == len(texts) - 1 else cursor + duration * weight / total
        allocated.append((cursor, end, text))
        cursor = end
    return allocated


def timestamp(seconds: float) -> str:
    total_ms = max(0, round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def wrapped_lines(text: str, width: int) -> list[str]:
    return textwrap.wrap(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [text]


def read_english_lines(path: Path, count: int) -> list[str]:
    if not path.exists():
        return [""] * count
    lines = [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines()]
    lines = [line for line in lines if line and not line.startswith("#")]
    if len(lines) > count:
        raise ValueError(f"Expected at most {count} English subtitle lines, found {len(lines)} in {path}")
    if len(lines) < count:
        print(f"Warning: found {len(lines)}/{count} English subtitle lines; remaining cues stay Vietnamese-only.")
        lines.extend([""] * (count - len(lines)))
    return lines


def write_srt(cues: list[Cue], path: Path, wrap_width: int) -> None:
    blocks: list[str] = []
    for index, cue in enumerate(cues, start=1):
        lines = [
            str(index),
            f"{timestamp(cue.start)} --> {timestamp(cue.end)}",
            *wrapped_lines(cue.vietnamese, wrap_width),
        ]
        if cue.english:
            lines.extend(wrapped_lines(cue.english, wrap_width))
        blocks.append("\n".join(lines))
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def build_ass_from_cues(cues: list[Cue], wrap_width: int) -> str:
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
    events: list[str] = []
    for cue in cues:
        start = srt_time_to_ass(timestamp(cue.start))
        end = srt_time_to_ass(timestamp(cue.end))
        vi = r"\N".join(escape_ass(line) for line in wrapped_lines(cue.vietnamese, wrap_width))
        text = r"{\fs48}" + vi
        if cue.english:
            en = r"\N".join(escape_ass(line) for line in wrapped_lines(cue.english, wrap_width))
            text += r"\N{\fs34}" + en
        events.append(f"Dialogue: 0,{start},{end},BilingualBox,,0,0,0,,{text}")
    return header + "\n".join(events) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build long Part 3 subtitles from the detailed voice script.")
    parser.add_argument("--max-cue-chars", type=int, default=92)
    parser.add_argument("--wrap-width", type=int, default=88)
    parser.add_argument("--estimate-wpm", type=float, default=155.0)
    args = parser.parse_args()

    sections = extract_sections(VOICE_SCRIPT, args.estimate_wpm)
    raw_cues: list[tuple[float, float, str]] = []
    cursor = 0.0
    for section in sections:
        texts = merge_short_texts(voice_to_cues(section.voice, args.max_cue_chars))
        raw_cues.extend(allocate(cursor, section.duration, texts))
        cursor += section.duration

    english_lines = read_english_lines(ENGLISH_LINES, len(raw_cues))
    cues = [
        Cue(start=start, end=end, vietnamese=vietnamese, english=english)
        for (start, end, vietnamese), english in zip(raw_cues, english_lines, strict=True)
    ]

    SRT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    write_srt(cues, SRT_OUTPUT, args.wrap_width)
    ASS_OUTPUT.write_text(build_ass_from_cues(cues, args.wrap_width), encoding="utf-8")

    print(f"Wrote {SRT_OUTPUT.relative_to(ROOT)}")
    print(f"Wrote {ASS_OUTPUT.relative_to(ROOT)}")
    print(f"Cues: {len(cues)}")
    print(f"Duration: {cursor:.2f}s")
    if not ENGLISH_LINES.exists():
        print(f"Warning: {ENGLISH_LINES.relative_to(ROOT)} not found; generated Vietnamese-only subtitles.")
    elif any(cue.english for cue in cues):
        translated = sum(1 for cue in cues if cue.english)
        print(f"English cues: {translated}/{len(cues)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
