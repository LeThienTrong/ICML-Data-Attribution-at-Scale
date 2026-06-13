from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass
from pathlib import Path

from check_durations import audio_duration
from srt_to_ass import escape_ass, srt_time_to_ass


ROOT = Path(__file__).resolve().parents[1]
SENTENCE_RE = re.compile(r"(?:(?<=[.!?])|(?<=[.!?][\"'”’]))\s+")


@dataclass
class Cue:
    start: float
    end: float
    vietnamese: str
    english: str


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def read_paragraphs(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig")
    return [normalize_spaces(part) for part in re.split(r"\n\s*\n", text) if part.strip()]


def split_sentences(paragraph: str) -> list[str]:
    return [part.strip() for part in SENTENCE_RE.split(paragraph.strip()) if part.strip()]


def paragraphs_to_sentence_pairs(vietnamese: list[str], english: list[str]) -> list[tuple[str, str]]:
    if len(vietnamese) != len(english):
        raise ValueError(f"Vietnamese paragraphs: {len(vietnamese)}, English paragraphs: {len(english)}")

    pairs: list[tuple[str, str]] = []
    for index, (vi_para, en_para) in enumerate(zip(vietnamese, english, strict=True), start=1):
        vi_sentences = split_sentences(vi_para)
        en_sentences = split_sentences(en_para)
        if len(vi_sentences) != len(en_sentences):
            raise ValueError(
                f"Paragraph {index}: Vietnamese sentences={len(vi_sentences)}, "
                f"English sentences={len(en_sentences)}"
            )
        pairs.extend(zip(vi_sentences, en_sentences, strict=True))
    return pairs


def audio_durations(audio_files: list[str]) -> list[float]:
    durations: list[float] = []
    for name in audio_files:
        path = ROOT / "assets" / "audio" / name
        duration = audio_duration(path)
        if duration is None:
            raise ValueError(f"Could not read audio duration: {path}")
        durations.append(duration)
    return durations


def segment_pairs(pairs: list[tuple[str, str]], paragraph_counts: list[int], paragraphs: list[str]) -> list[list[tuple[str, str]]]:
    sentence_counts = [len(split_sentences(paragraph)) for paragraph in paragraphs]
    result: list[list[tuple[str, str]]] = []
    paragraph_cursor = 0
    pair_cursor = 0
    for count in paragraph_counts:
        segment_sentence_count = sum(sentence_counts[paragraph_cursor : paragraph_cursor + count])
        result.append(pairs[pair_cursor : pair_cursor + segment_sentence_count])
        paragraph_cursor += count
        pair_cursor += segment_sentence_count
    if paragraph_cursor != len(paragraphs) or pair_cursor != len(pairs):
        raise ValueError("Segment paragraph counts do not cover the full script.")
    return result


def allocate_segment(start: float, duration: float, pairs: list[tuple[str, str]]) -> list[Cue]:
    weights = [max(len(vi) + 0.5 * len(en), 36) for vi, en in pairs]
    total = sum(weights)
    cursor = start
    cues: list[Cue] = []
    for index, ((vi, en), weight) in enumerate(zip(pairs, weights, strict=True)):
        end = start + duration if index == len(pairs) - 1 else cursor + duration * weight / total
        cues.append(Cue(cursor, end, vi, en))
        cursor = end
    return cues


def build_cues(
    *,
    voice_script: Path,
    english_text: str,
    audio_files: list[str],
    paragraph_counts: list[int],
) -> list[Cue]:
    vi_paragraphs = read_paragraphs(voice_script)
    en_paragraphs = [normalize_spaces(part) for part in re.split(r"\n\s*\n", english_text.strip()) if part.strip()]
    pairs = paragraphs_to_sentence_pairs(vi_paragraphs, en_paragraphs)
    segments = segment_pairs(pairs, paragraph_counts, vi_paragraphs)
    durations = audio_durations(audio_files)
    if len(segments) != len(durations):
        raise ValueError(f"Segments: {len(segments)}, audio files: {len(durations)}")

    cues: list[Cue] = []
    cursor = 0.0
    for duration, segment in zip(durations, segments, strict=True):
        cues.extend(allocate_segment(cursor, duration, segment))
        cursor += duration

    original = normalize_spaces(" ".join(vi_paragraphs))
    rebuilt = normalize_spaces(" ".join(cue.vietnamese for cue in cues))
    if original != rebuilt:
        raise ValueError("Vietnamese cues do not exactly rebuild the ElevenLabs script.")
    return cues


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
    return textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False) or [text]


def write_srt(cues: list[Cue], path: Path, wrap_width: int = 88) -> None:
    blocks: list[str] = []
    for index, cue in enumerate(cues, start=1):
        lines = [
            str(index),
            f"{timestamp(cue.start)} --> {timestamp(cue.end)}",
            *wrapped_lines(cue.vietnamese, wrap_width),
            *wrapped_lines(cue.english, wrap_width),
        ]
        blocks.append("\n".join(lines))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def write_ass(cues: list[Cue], path: Path, wrap_width: int = 72) -> None:
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
        en = r"\N".join(escape_ass(line) for line in wrapped_lines(cue.english, wrap_width))
        text = r"{\fs48}" + vi + r"\N{\fs34}" + en
        events.append(f"Dialogue: 0,{start},{end},BilingualBox,,0,0,0,,{text}")
    path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


def write_outputs(cues: list[Cue], srt_path: Path) -> None:
    write_srt(cues, srt_path)
    write_ass(cues, srt_path.with_suffix(".ass"))
    print(f"Wrote {srt_path} ({len(cues)} cues, {cues[-1].end:.3f}s)")
    print(f"Wrote {srt_path.with_suffix('.ass')}")
