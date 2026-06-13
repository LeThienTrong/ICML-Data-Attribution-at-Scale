from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

from check_durations import audio_duration
from srt_to_ass import build_ass, parse_srt


ROOT = Path(__file__).resolve().parents[1]
FIELD_RE = re.compile(r"^(Audio|Voice VI|Subtitle EN|Visual|Must show):\s*(.*)$")
HEADING_RE = re.compile(r"^##\s+([a-z0-9_]+)\s*-\s*(.+?)\s*$", re.IGNORECASE)


@dataclass
class Beat:
    beat_id: str
    title: str
    audio: str
    voice_vi: str
    subtitle_en: str
    visual: str
    must_show: str
    duration: float
    raw_duration: float | None
    duration_source: str
    start: float = 0.0
    end: float = 0.0

    @property
    def group(self) -> str:
        parts = self.beat_id.split("_")
        return "_".join(parts[:2]) if len(parts) >= 2 else self.beat_id


def normalize_text(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines if line.strip())
    return re.sub(r"\s+", " ", text).strip()


def parse_beat_script(path: Path) -> tuple[str, list[dict[str, str]]]:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    title = path.stem
    beats: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    active_field: str | None = None
    field_lines: dict[str, list[str]] = {}

    def flush_field() -> None:
        nonlocal active_field
        if current is not None and active_field is not None:
            current[active_field] = normalize_text(field_lines.get(active_field, []))
        active_field = None

    def flush_beat() -> None:
        nonlocal current, active_field, field_lines
        if current is None:
            return
        flush_field()
        beats.append(current)
        current = None
        active_field = None
        field_lines = {}

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        heading = HEADING_RE.match(line)
        if heading:
            flush_beat()
            current = {"ID": heading.group(1).strip(), "Title": heading.group(2).strip()}
            field_lines = {}
            continue

        if current is None:
            if line.startswith("# "):
                title = line[2:].strip()
            continue

        field = FIELD_RE.match(line)
        if field:
            flush_field()
            active_field = field.group(1)
            field_lines[active_field] = [field.group(2).strip()] if field.group(2).strip() else []
            continue

        if active_field is not None and line.strip():
            field_lines.setdefault(active_field, []).append(line.strip())

    flush_beat()
    return title, beats


def estimate_duration(voice_vi: str, wpm: float, minimum: float) -> float:
    word_count = len(re.findall(r"\S+", voice_vi))
    duration = word_count / wpm * 60.0
    return max(minimum, duration)


def output_stem(script_path: Path) -> str:
    stem = script_path.stem
    return stem.removesuffix("_beat_script")


def relpath(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def srt_timestamp(seconds: float) -> str:
    total_ms = max(0, round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(beats: list[Beat], path: Path) -> None:
    blocks: list[str] = []
    for index, beat in enumerate(beats, start=1):
        blocks.append(
            "\n".join(
                [
                    str(index),
                    f"{srt_timestamp(beat.start)} --> {srt_timestamp(beat.end)}",
                    beat.voice_vi,
                    beat.subtitle_en,
                ]
            )
        )
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def validate_and_build(
    script_path: Path,
    *,
    allow_missing_audio: bool,
    speed: float,
    estimate_wpm: float,
    min_estimate_duration: float,
    min_duration_warn: float,
    max_duration_warn: float,
    subtitle_line_limit: int,
) -> tuple[dict[str, object], list[str], list[str]]:
    title, raw_beats = parse_beat_script(script_path)
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    beats: list[Beat] = []

    required_fields = ["Audio", "Voice VI", "Subtitle EN", "Visual", "Must show"]
    for raw in raw_beats:
        beat_id = raw["ID"]
        if beat_id in seen:
            errors.append(f"{beat_id}: duplicate beat ID")
        seen.add(beat_id)

        missing = [field for field in required_fields if not raw.get(field)]
        if missing:
            errors.append(f"{beat_id}: missing fields: {', '.join(missing)}")
            continue

        audio_rel = raw["Audio"]
        audio_path = ROOT / audio_rel
        raw_duration = audio_duration(audio_path) if audio_path.exists() else None
        duration_source = "audio"
        if raw_duration is None:
            if audio_path.exists():
                errors.append(f"{beat_id}: cannot read audio duration: {audio_rel}")
                continue
            if not allow_missing_audio:
                errors.append(f"{beat_id}: missing audio file: {audio_rel}")
                continue
            raw_duration = estimate_duration(raw["Voice VI"], estimate_wpm, min_estimate_duration)
            duration_source = "estimate"
            warnings.append(f"{beat_id}: missing audio, estimated {raw_duration:.2f}s from voice text")

        effective_duration = raw_duration / speed
        if effective_duration < min_duration_warn:
            warnings.append(f"{beat_id}: short beat duration {effective_duration:.2f}s")
        if effective_duration > max_duration_warn:
            warnings.append(f"{beat_id}: long beat duration {effective_duration:.2f}s")

        if len(raw["Voice VI"]) > subtitle_line_limit:
            warnings.append(f"{beat_id}: long Vietnamese subtitle line ({len(raw['Voice VI'])} chars)")
        if len(raw["Subtitle EN"]) > subtitle_line_limit:
            warnings.append(f"{beat_id}: long English subtitle line ({len(raw['Subtitle EN'])} chars)")

        beats.append(
            Beat(
                beat_id=beat_id,
                title=raw["Title"],
                audio=audio_rel,
                voice_vi=raw["Voice VI"],
                subtitle_en=raw["Subtitle EN"],
                visual=raw["Visual"],
                must_show=raw["Must show"],
                duration=effective_duration,
                raw_duration=raw_duration if duration_source == "audio" else None,
                duration_source=duration_source,
            )
        )

    cursor = 0.0
    for beat in beats:
        beat.start = cursor
        beat.end = cursor + beat.duration
        cursor = beat.end

    data: dict[str, object] = {
        "title": title,
        "source": relpath(script_path),
        "speed": speed,
        "total_duration": cursor,
        "pad_end": 0.8,
        "beats": [
            {
                "id": beat.beat_id,
                "group": beat.group,
                "title": beat.title,
                "audio": beat.audio,
                "start": round(beat.start, 3),
                "end": round(beat.end, 3),
                "duration": round(beat.duration, 3),
                "raw_duration": round(beat.raw_duration, 3) if beat.raw_duration is not None else None,
                "duration_source": beat.duration_source,
                "voice_vi": beat.voice_vi,
                "subtitle_en": beat.subtitle_en,
                "visual": beat.visual,
                "must_show": beat.must_show,
            }
            for beat in beats
        ],
    }
    return data, warnings, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Build beat-locked Manim timeline and bilingual subtitles.")
    parser.add_argument("beat_script", type=Path)
    parser.add_argument("--allow-missing-audio", action="store_true", help="Use estimated durations for missing audio.")
    parser.add_argument("--speed", type=float, default=1.0, help="Effective audio speed. Use 1.0 for CapCut speed 1.00.")
    parser.add_argument("--estimate-wpm", type=float, default=155.0)
    parser.add_argument("--min-estimate-duration", type=float, default=4.5)
    parser.add_argument("--min-duration-warn", type=float, default=3.0)
    parser.add_argument("--max-duration-warn", type=float, default=16.0)
    parser.add_argument("--subtitle-line-limit", type=int, default=110)
    args = parser.parse_args()

    script_path = (ROOT / args.beat_script).resolve() if not args.beat_script.is_absolute() else args.beat_script
    if not script_path.exists():
        print(f"Beat script not found: {script_path}")
        return 2
    if args.speed <= 0:
        print("--speed must be positive")
        return 2

    data, warnings, errors = validate_and_build(
        script_path,
        allow_missing_audio=args.allow_missing_audio,
        speed=args.speed,
        estimate_wpm=args.estimate_wpm,
        min_estimate_duration=args.min_estimate_duration,
        min_duration_warn=args.min_duration_warn,
        max_duration_warn=args.max_duration_warn,
        subtitle_line_limit=args.subtitle_line_limit,
    )

    if errors:
        print("Errors")
        for error in errors:
            print(f"- {error}")
        return 1

    stem = output_stem(script_path)
    timeline_path = ROOT / "timelines" / f"{stem}.json"
    srt_path = ROOT / "subtitles" / f"{stem}_bilingual.srt"
    ass_path = ROOT / "subtitles" / f"{stem}_bilingual.ass"
    timeline_path.parent.mkdir(parents=True, exist_ok=True)
    srt_path.parent.mkdir(parents=True, exist_ok=True)

    timeline_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_srt(
        [
            Beat(
                beat_id=str(item["id"]),
                title=str(item["title"]),
                audio=str(item["audio"]),
                voice_vi=str(item["voice_vi"]),
                subtitle_en=str(item["subtitle_en"]),
                visual=str(item["visual"]),
                must_show=str(item["must_show"]),
                duration=float(item["duration"]),
                raw_duration=float(item["raw_duration"]) if item["raw_duration"] is not None else None,
                duration_source=str(item["duration_source"]),
                start=float(item["start"]),
                end=float(item["end"]),
            )
            for item in data["beats"]  # type: ignore[index]
        ],
        srt_path,
    )
    ass_path.write_text(build_ass(parse_srt(srt_path)), encoding="utf-8")

    print(f"Wrote {relpath(timeline_path)}")
    print(f"Wrote {relpath(srt_path)}")
    print(f"Wrote {relpath(ass_path)}")
    print(f"Beats: {len(data['beats'])}")  # type: ignore[index]
    print(f"Total duration: {float(data['total_duration']):.2f}s")
    if warnings:
        print("\nWarnings")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
