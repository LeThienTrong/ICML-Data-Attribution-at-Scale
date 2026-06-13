from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

from check_durations import audio_duration
from build_beat_timeline import parse_beat_script, relpath


ROOT = Path(__file__).resolve().parents[1]
VOICE_SCRIPT = ROOT / "docs" / "part3_scaling_and_evaluation_voice_script.md"
VISUAL_BEATS = ROOT / "docs" / "part3_scaling_and_evaluation_beat_script.md"
TIMELINE = ROOT / "timelines" / "part3_scaling_and_evaluation.json"


@dataclass
class Section:
    code: str
    title: str
    visual: str
    voice: str
    duration: float
    raw_duration: float | None
    duration_source: str


def extract_sections(path: Path, estimate_wpm: float) -> list[Section]:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    matches = list(re.finditer(r"^## (p3_\d+) - (.+)$", text, re.MULTILINE))
    sections: list[Section] = []
    for index, match in enumerate(matches):
        code = match.group(1)
        title = match.group(2).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else text.find("\n## Research Notes", start)
        if end == -1:
            end = len(text)
        block = text[start:end]
        if "Visual:" not in block or "Voice:" not in block:
            raise ValueError(f"{code}: missing Visual or Voice field")
        visual = block.split("Visual:", 1)[1].split("Voice:", 1)[0].strip()
        voice = block.split("Voice:", 1)[1].strip()
        voice = re.sub(r"\n## Research Notes.*$", "", voice, flags=re.S).strip()
        audio_path = ROOT / "assets" / "audio" / f"{code}.mp3"
        raw_duration = audio_duration(audio_path) if audio_path.exists() else None
        if raw_duration is None:
            words = len(re.findall(r"\S+", voice))
            duration = max(18.0, words / estimate_wpm * 60.0)
            duration_source = "section_estimate"
        else:
            duration = raw_duration
            duration_source = "audio"
        sections.append(
            Section(
                code=code,
                title=title,
                visual=visual,
                voice=voice,
                duration=duration,
                raw_duration=raw_duration,
                duration_source=duration_source,
            )
        )
    return sections


def group_visual_beats(path: Path) -> dict[str, list[dict[str, str]]]:
    _, beats = parse_beat_script(path)
    grouped: dict[str, list[dict[str, str]]] = {}
    for beat in beats:
        beat_id = beat["ID"]
        parts = beat_id.split("_")
        group = "_".join(parts[:2])
        grouped.setdefault(group, []).append(beat)
    return grouped


def word_weight(text: str) -> float:
    return max(1.0, float(len(re.findall(r"\S+", text))))


def build_timeline(estimate_wpm: float, pad_end: float) -> dict[str, object]:
    sections = extract_sections(VOICE_SCRIPT, estimate_wpm)
    visual_groups = group_visual_beats(VISUAL_BEATS)
    beats: list[dict[str, object]] = []
    cursor = 0.0

    for section in sections:
        visuals = visual_groups.get(section.code, [])
        if not visuals:
            visuals = [
                {
                    "ID": f"{section.code}_01",
                    "Title": section.title,
                    "Audio": f"assets/audio/{section.code}.mp3",
                    "Voice VI": section.title,
                    "Subtitle EN": section.title,
                    "Visual": section.visual,
                    "Must show": section.code,
                }
            ]
        weights = [word_weight(item.get("Voice VI", "")) for item in visuals]
        total_weight = sum(weights)

        for local_index, (visual, weight) in enumerate(zip(visuals, weights, strict=True), start=1):
            duration = section.duration * weight / total_weight
            beat_id = str(visual["ID"])
            start = cursor
            end = cursor + duration
            beats.append(
                {
                    "id": beat_id,
                    "group": section.code,
                    "section": section.code,
                    "section_title": section.title,
                    "title": visual.get("Title", section.title),
                    "audio": f"assets/audio/{section.code}.mp3",
                    "start": round(start, 3),
                    "end": round(end, 3),
                    "duration": round(duration, 3),
                    "raw_duration": round(section.raw_duration, 3) if section.raw_duration is not None else None,
                    "duration_source": section.duration_source,
                    "voice_vi": visual.get("Voice VI", section.title),
                    "subtitle_en": visual.get("Subtitle EN", section.title),
                    "visual": visual.get("Visual", section.visual),
                    "must_show": visual.get("Must show", section.code),
                    "section_voice_words": len(re.findall(r"\S+", section.voice)),
                    "section_visual_index": local_index,
                    "section_visual_count": len(visuals),
                }
            )
            cursor = end

    return {
        "title": "Part 3 - Scaling and Evaluation Long Timeline",
        "source": relpath(VOICE_SCRIPT),
        "visual_scaffold": relpath(VISUAL_BEATS),
        "audio_mode": "section",
        "speed": 1.0,
        "total_duration": cursor,
        "pad_end": pad_end,
        "beats": beats,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the long Part 3 visual timeline from the detailed voice script.")
    parser.add_argument("--estimate-wpm", type=float, default=155.0)
    parser.add_argument("--pad-end", type=float, default=1.4)
    args = parser.parse_args()

    data = build_timeline(args.estimate_wpm, args.pad_end)
    TIMELINE.parent.mkdir(parents=True, exist_ok=True)
    TIMELINE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sources = sorted({str(item["duration_source"]) for item in data["beats"]})  # type: ignore[index]
    print(f"Wrote {relpath(TIMELINE)}")
    print(f"Visual beats: {len(data['beats'])}")  # type: ignore[index]
    print(f"Total duration: {float(data['total_duration']):.2f}s")
    print(f"Duration sources: {', '.join(sources)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
