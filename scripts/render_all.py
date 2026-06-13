from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCENES_DIR = ROOT / "scenes"
LOG_DIR = ROOT / "outputs" / "render_logs"

QUALITY_FLAGS = {
    "low": "-ql",
    "medium": "-qm",
    "high": "-qh",
    "1080p": "-qh",
}


def manim_command(scene_path: Path, class_name: str, quality_flag: str) -> list[str]:
    uv_tool_python = Path.home() / "AppData" / "Roaming" / "uv" / "tools" / "manim" / "Scripts" / "python.exe"
    try:
        has_uv_tool_python = uv_tool_python.exists()
    except PermissionError:
        has_uv_tool_python = True
    if has_uv_tool_python:
        return [str(uv_tool_python), "-m", "manim", quality_flag, str(scene_path), class_name]
    return ["manim", quality_flag, str(scene_path), class_name]


@dataclass
class SceneTarget:
    file: Path
    class_name: str


def is_scene_base(base: ast.expr) -> bool:
    if isinstance(base, ast.Name):
        return base.id == "Scene"
    if isinstance(base, ast.Attribute):
        return base.attr == "Scene"
    return False


def discover_scenes() -> list[SceneTarget]:
    targets: list[SceneTarget] = []
    for path in sorted(SCENES_DIR.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and any(is_scene_base(base) for base in node.bases):
                targets.append(SceneTarget(path, node.name))
    return targets


def render(target: SceneTarget, quality_flag: str) -> tuple[bool, Path]:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{target.file.stem}_{target.class_name}.log"
    scene_path = target.file.relative_to(ROOT)
    command = manim_command(scene_path, target.class_name, quality_flag)
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    log_path.write_text(
        "$ " + " ".join(f'"{part}"' if " " in part else part for part in command) + "\n\n"
        + "STDOUT\n"
        + result.stdout
        + "\nSTDERR\n"
        + result.stderr,
        encoding="utf-8",
    )
    return result.returncode == 0, log_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render all Manim scenes in scenes/*.py")
    parser.add_argument("--quality", choices=QUALITY_FLAGS, default="low")
    parser.add_argument("--scene", help="Optional class name filter")
    args = parser.parse_args()

    targets = discover_scenes()
    if args.scene:
        targets = [target for target in targets if target.class_name == args.scene]

    if not targets:
        print("No scene classes found.")
        return 1

    failures: list[tuple[SceneTarget, Path]] = []
    for target in targets:
        rel = target.file.relative_to(ROOT)
        print(f"Rendering {rel}::{target.class_name}")
        ok, log_path = render(target, QUALITY_FLAGS[args.quality])
        if ok:
            print(f"  OK   log: {log_path.relative_to(ROOT)}")
        else:
            print(f"  FAIL log: {log_path.relative_to(ROOT)}")
            failures.append((target, log_path))

    print("\nSummary")
    print(f"  Total: {len(targets)}")
    print(f"  OK:    {len(targets) - len(failures)}")
    print(f"  Fail:  {len(failures)}")
    for target, log_path in failures:
        print(f"  - {target.file.name}::{target.class_name} ({log_path.relative_to(ROOT)})")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
