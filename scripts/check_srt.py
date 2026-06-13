from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


TIMESTAMP_RE = re.compile(
    r"(?P<h1>\d{2}):(?P<m1>\d{2}):(?P<s1>\d{2}),(?P<ms1>\d{3})\s+-->\s+"
    r"(?P<h2>\d{2}):(?P<m2>\d{2}):(?P<s2>\d{2}),(?P<ms2>\d{3})"
)


@dataclass
class Cue:
    index: int
    start: float
    end: float
    text: list[str]


def to_seconds(match: re.Match[str], prefix: str) -> float:
    return (
        int(match[f"h{prefix}"]) * 3600
        + int(match[f"m{prefix}"]) * 60
        + int(match[f"s{prefix}"])
        + int(match[f"ms{prefix}"]) / 1000
    )


def parse_srt(path: Path) -> tuple[list[Cue], list[str]]:
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    blocks = [block.strip() for block in raw.split("\n\n") if block.strip()]
    cues: list[Cue] = []
    warnings: list[str] = []
    for block_no, block in enumerate(blocks, start=1):
        lines = block.splitlines()
        if len(lines) < 3:
            warnings.append(f"Block {block_no}: expected index, timestamp, and text")
            continue
        try:
            index = int(lines[0].strip())
        except ValueError:
            warnings.append(f"Block {block_no}: invalid index {lines[0]!r}")
            continue
        match = TIMESTAMP_RE.fullmatch(lines[1].strip())
        if not match:
            warnings.append(f"Cue {index}: invalid timestamp line")
            continue
        start = to_seconds(match, "1")
        end = to_seconds(match, "2")
        cues.append(Cue(index=index, start=start, end=end, text=lines[2:]))
    return cues, warnings


def check(path: Path) -> int:
    cues, warnings = parse_srt(path)
    previous_end = -1.0
    expected_index = 1
    for cue in cues:
        if cue.index != expected_index:
            warnings.append(f"Cue {cue.index}: expected index {expected_index}")
        if cue.end <= cue.start:
            warnings.append(f"Cue {cue.index}: end must be after start")
        if cue.start < previous_end - 0.05:
            warnings.append(f"Cue {cue.index}: overlaps previous cue by more than 0.05s")
        for line in cue.text:
            if len(line) > 92:
                warnings.append(f"Cue {cue.index}: long subtitle line ({len(line)} chars)")
        previous_end = max(previous_end, cue.end)
        expected_index += 1

    print(f"File: {path}")
    print(f"Cues: {len(cues)}")
    if cues:
        print(f"Duration from SRT: {cues[-1].end:.2f}s")

    if warnings:
        print("\nWarnings")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("No SRT issues found.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SRT structure and basic readability.")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    exit_code = 0
    for path in args.paths:
        exit_code = max(exit_code, check(path))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
