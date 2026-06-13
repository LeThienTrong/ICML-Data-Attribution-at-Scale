from __future__ import annotations

import argparse
import re
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TIMESTAMP_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2}),(\d{3})")
CHUNK_RE = re.compile(r"^((?:g|p)\d+)_[0-9]+(?:_|$)")
AUDIO_GROUP_MAP = {
    "g1": "part1_g1_intro_taxonomy",
    "g2": "part1_g2_corroborative",
    "g3": "part1_g3_game_theoretic",
    "g4": "part1_g4_predictive",
    "p2": "part2_core_theory",
    "p3": "part3_scaling_and_evaluation",
    "p4": "part4_applications",
    "p5": "part5_epilogue_recap",
}
FULL_AUDIO_MAP = {
    "g1_full_afterfixed": "part1_g1_intro_taxonomy",
}


def srt_duration(path: Path) -> float | None:
    last_end: float | None = None
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    for match in TIMESTAMP_RE.finditer(text):
        h, m, s, ms = [int(part) for part in match.groups()[4:]]
        last_end = h * 3600 + m * 60 + s + ms / 1000
    return last_end


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as handle:
        return handle.getnframes() / float(handle.getframerate())


def mp3_duration_with_mutagen(path: Path) -> float | None:
    try:
        from mutagen.mp3 import MP3
    except ImportError:
        return None
    try:
        return float(MP3(path).info.length)
    except Exception:
        return None


def _skip_id3v2(data: bytes) -> int:
    if len(data) < 10 or data[:3] != b"ID3":
        return 0
    size = 0
    for byte in data[6:10]:
        size = (size << 7) | (byte & 0x7F)
    footer = 10 if data[5] & 0x10 else 0
    return min(len(data), 10 + size + footer)


def mp3_duration_from_frames(path: Path) -> float | None:
    data = path.read_bytes()
    pos = _skip_id3v2(data)
    duration = 0.0
    frames = 0

    bitrates = {
        ("1", "I"): [None, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448],
        ("1", "II"): [None, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384],
        ("1", "III"): [None, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
        ("2", "I"): [None, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256],
        ("2", "II"): [None, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
        ("2", "III"): [None, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
    }
    sample_rates = {
        "1": [44100, 48000, 32000],
        "2": [22050, 24000, 16000],
        "2.5": [11025, 12000, 8000],
    }

    while pos + 4 <= len(data):
        header = int.from_bytes(data[pos : pos + 4], "big")
        if (header & 0xFFE00000) != 0xFFE00000:
            pos += 1
            continue

        version_bits = (header >> 19) & 0b11
        layer_bits = (header >> 17) & 0b11
        bitrate_index = (header >> 12) & 0b1111
        sample_rate_index = (header >> 10) & 0b11
        padding = (header >> 9) & 0b1

        version = {0b00: "2.5", 0b10: "2", 0b11: "1"}.get(version_bits)
        layer = {0b01: "III", 0b10: "II", 0b11: "I"}.get(layer_bits)
        if (
            version is None
            or layer is None
            or bitrate_index in {0, 15}
            or sample_rate_index == 3
        ):
            pos += 1
            continue

        table_version = "1" if version == "1" else "2"
        bitrate = bitrates[(table_version, layer)][bitrate_index]
        sample_rate = sample_rates[version][sample_rate_index]
        if bitrate is None:
            pos += 1
            continue

        if layer == "I":
            samples = 384
            frame_length = int((12 * bitrate * 1000 / sample_rate + padding) * 4)
        elif layer == "III" and version != "1":
            samples = 576
            frame_length = int(72 * bitrate * 1000 / sample_rate + padding)
        else:
            samples = 1152
            frame_length = int(144 * bitrate * 1000 / sample_rate + padding)

        if frame_length <= 4:
            pos += 1
            continue

        duration += samples / sample_rate
        frames += 1
        pos += frame_length

    return duration if frames else None


def audio_duration(path: Path) -> float | None:
    if path.suffix.lower() == ".wav":
        return wav_duration(path)
    if path.suffix.lower() == ".mp3":
        return mp3_duration_with_mutagen(path) or mp3_duration_from_frames(path)
    return None


def normalize_stem(stem: str) -> str:
    for suffix in ("_bilingual", ".bilingual", "_vi", "_en"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return stem


def collect_audio() -> dict[str, tuple[Path, float | None]]:
    result: dict[str, tuple[Path, float | None]] = {}
    grouped: dict[str, tuple[Path, float | None]] = {}
    for directory in [ROOT / "assets" / "audio"]:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*")):
            if path.suffix.lower() in {".mp3", ".wav"}:
                key = normalize_stem(path.stem)
                key = FULL_AUDIO_MAP.get(key, key)
                duration = audio_duration(path)
                chunk_match = CHUNK_RE.match(key)
                if chunk_match:
                    group_key = AUDIO_GROUP_MAP.get(chunk_match.group(1), chunk_match.group(1))
                    first_path, previous_duration = grouped.get(group_key, (path, 0.0))
                    if previous_duration is None or duration is None:
                        grouped[group_key] = (first_path, None)
                    else:
                        grouped[group_key] = (first_path, previous_duration + duration)
                else:
                    result[key] = (path, duration)
    for key, value in grouped.items():
        result.setdefault(key, value)
    return result


def collect_srt() -> dict[str, tuple[Path, float | None]]:
    result: dict[str, tuple[Path, float | None]] = {}
    for directory in [ROOT / "subtitles", ROOT / "assets" / "subtitles"]:
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.srt")):
            result[normalize_stem(path.stem)] = (path, srt_duration(path))
    return result


def fmt_seconds(value: float | None) -> str:
    return f"{value:9.2f}" if value is not None else f"{'-':>9}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare available audio and SRT durations.")
    parser.add_argument("--threshold", type=float, default=3.0)
    args = parser.parse_args()

    audio = collect_audio()
    srts = collect_srt()
    keys = sorted(set(audio) | set(srts))

    print(f"{'stem':34} {'audio':>9} {'srt':>9} status")
    print("-" * 70)
    warning_count = 0
    for key in keys:
        audio_path, audio_len = audio.get(key, (None, None))
        srt_path, srt_len = srts.get(key, (None, None))
        status = "OK"
        if audio_path is None:
            status = "missing audio"
        elif srt_path is None:
            status = "missing srt"
        elif audio_len is None:
            status = "audio duration unavailable"
        elif srt_len is None:
            status = "srt duration unavailable"
        elif abs(audio_len - srt_len) > args.threshold:
            status = f"WARNING diff={abs(audio_len - srt_len):.2f}s"
            warning_count += 1
        print(f"{key[:34]:34} {fmt_seconds(audio_len)} {fmt_seconds(srt_len)} {status}")

    return 1 if warning_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
