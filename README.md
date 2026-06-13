# ICML Data Attribution at Scale - Manim Video Project

Source code for a Vietnamese Manim video series based on the ICML 2024 tutorial
**Data Attribution at Scale: Connecting ML Behavior to Training Data**.

The project turns the tutorial into an animated academic explainer with:

- Vietnamese narration scripts for ElevenLabs or similar AI voice tools.
- Manim scenes inspired by the visual style of mathematical explainers.
- Bilingual Vietnamese-English subtitles in `.srt` and styled `.ass` formats.
- Utility scripts for rendering, subtitle generation, and duration checks.
- A coverage matrix that maps each video section to the tutorial concepts it covers.

The repository intentionally stores source files, scripts, docs, and subtitles only.
Rendered videos and audio files are treated as local production assets and should not be
committed to GitHub.

## Project Scope

The video is organized as a compact but complete walkthrough of data attribution:

| Block | Scene file | Manim class | Main role |
|---|---|---|---|
| Part I - Intro and taxonomy | `scenes/part1_g1_intro_taxonomy.py` | `IntroTaxonomy` | Introduces the problem, roadmap, and attribution taxonomy. |
| Part I - Corroborative attribution | `scenes/part1_g2_corroborative.py` | `CorroborativeAttribution` | Explains evidence-style attribution: search, citation, retrieval, similarity, and limitations. |
| Part I - Game-theoretic attribution | `scenes/part1_g3_game_theoretic.py` | `GameTheoreticAttribution` | Explains credit allocation through coalitions, marginal contribution, and Shapley-style intuition. |
| Part I - Predictive attribution | `scenes/part1_g4_predictive.py` | `PredictiveAttribution` | Introduces datamodel-style prediction from subset indicators to behavior. |
| Part II - Core theory | `scenes/part2_core_theory.py` | `CoreTheory` | Covers M-estimation, leave-one-out, influence functions, assumptions, and datamodels. |
| Part III - Scaling and evaluation | `scenes/part3_scaling_and_evaluation.py` | `ScalingAndEvaluation` | Covers scaling challenges, estimator landscape, LDS/counterfactual evaluation, and future work. |
| Part IV - Applications | `scenes/part4_applications.py` | `ApplicationsOfDataAttribution` | Covers debugging, dataset selection, poisoning, unlearning, valuation, citation, and RAG. |
| Part V - Epilogue | `scenes/part5_epilogue_recap.py` | `EpilogueRecap` | Recaps the full arc: lens, scale, responsibility, and final takeaways. |

More detail is available in [`docs/coverage_matrix.md`](docs/coverage_matrix.md).

## Repository Layout

```text
.
├── scenes/          Manim scene source files
├── docs/            Voice scripts, coverage notes, production notes, YouTube template
├── subtitles/       Bilingual subtitle files in SRT and ASS formats
├── scripts/         Render, subtitle, duration, and timeline helper scripts
├── timelines/       Timeline JSON generated for selected sections
├── assets/audio/    Local audio input directory, ignored by Git
├── outputs/         Local render logs/output artifacts, ignored by Git
├── media/           Manim render output directory, ignored by Git
├── requirements.txt Python dependencies
└── README.md
```

## Setup

Use Python 3.10+ if possible. The project has been developed on Windows with
Manim Community Edition.

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

You also need a working Manim installation. If the `manim` command is available,
the scene commands below will work directly.

Optional dependencies in `requirements.txt`, such as Jupyter, are kept for local
experimentation. They are not required for the main video rendering pipeline.

## Rendering

Render one scene in low quality:

```powershell
manim -ql scenes\part1_g1_intro_taxonomy.py IntroTaxonomy
```

Render one scene in high quality:

```powershell
manim -qh scenes\part5_epilogue_recap.py EpilogueRecap
```

Render all discovered Manim scenes:

```powershell
python scripts\render_all.py --quality low
python scripts\render_all.py --quality high
```

Render a single scene class through the helper:

```powershell
python scripts\render_all.py --quality low --scene CoreTheory
```

Render logs are written to:

```text
outputs/render_logs/
```

Rendered videos are written by Manim under:

```text
media/videos/
```

The `media/` directory is ignored by Git because rendered videos are large generated artifacts.

## Audio Workflow

The repo does not commit `.mp3`, `.wav`, or other audio files.

For local production, place AI voice files in:

```text
assets/audio/
```

The current naming convention is:

```text
g1_full_afterfixed.mp3
g2_*.mp3
g3_*.mp3
g4_*.mp3
p2_*.mp3
p3_*.mp3
p4_*.mp3
p5_*.mp3
```

Most Manim scenes are rendered as silent video. Audio is intended to be assembled
manually in CapCut or another editor. This avoids inconsistent audio embedding
behavior during Manim rendering and keeps GitHub clean.

Part G2 may keep audio-specific local workflow details, but the general pipeline is:

1. Generate voice in short or section-based chunks.
2. Put the audio files in `assets/audio/`.
3. Generate or validate subtitles.
4. Render silent Manim video.
5. Import video, voice, and `.ass` subtitles into CapCut.
6. Keep voice speed at `1.00` unless the corresponding video/subtitle timing is also updated.

## Subtitle Workflow

Subtitles are stored in two forms:

- `.srt`: plain subtitle timing, useful for validation and general video tools.
- `.ass`: styled subtitle format, useful for bilingual subtitles with a dark translucent box.

The intended subtitle layout is:

- Vietnamese subtitle on the first line.
- English subtitle on the second line.
- Vietnamese text is larger than English text.
- White text on a semi-transparent black background.

Useful subtitle scripts:

| Script | Purpose |
|---|---|
| `scripts/build_g1_subtitles.py` | Builds G1 bilingual subtitles from the voice script. |
| `scripts/build_g3_subtitles.py` | Builds G3 bilingual subtitles. |
| `scripts/build_g4_subtitles.py` | Builds G4 bilingual subtitles. |
| `scripts/build_part2_subtitles.py` | Builds Part II bilingual subtitles. |
| `scripts/build_part3_long_subtitles.py` | Builds Part III bilingual subtitles. |
| `scripts/build_part4_subtitles.py` | Builds Part IV bilingual subtitles. |
| `scripts/build_part5_subtitles.py` | Builds Part V bilingual subtitles. |
| `scripts/srt_to_ass.py` | Converts SRT subtitles into ASS styling when needed. |
| `scripts/check_srt.py` | Validates subtitle timing and formatting. |

Validate one subtitle file:

```powershell
python scripts\check_srt.py subtitles\part5_epilogue_recap_bilingual.srt
```

Check audio and subtitle duration alignment:

```powershell
python scripts\check_durations.py --threshold 1.5
```

This duration check works only when the matching local audio files exist in
`assets/audio/`.

## Timeline And Beat Scripts

Part III includes an experimental beat/timeline workflow:

```powershell
python scripts\build_beat_timeline.py docs\part3_scaling_and_evaluation_beat_script.md
```

This generates:

```text
timelines/part3_scaling_and_evaluation.json
subtitles/part3_scaling_and_evaluation_bilingual.srt
subtitles/part3_scaling_and_evaluation_bilingual.ass
```

The goal of this workflow is to make audio, subtitles, and animation beats easier
to align when a section becomes too long for a single continuous script.

## Documentation Files

Important docs:

| File | Purpose |
|---|---|
| `docs/coverage_matrix.md` | Maps tutorial content to the implemented video scenes. |
| `docs/*_voice_script.md` | Human-readable narration scripts. |
| `docs/*_voice_script_elevenlabs.txt` | Voice text prepared for ElevenLabs input. |
| `docs/part4_applications_research_notes.md` | Research notes for application coverage. |
| `docs/production_checklist.md` | Final production checklist. |
| `docs/youtube_description_template.md` | Template for the final YouTube description. |

## Production Checks

Before publishing or submitting the final video, run:

```powershell
python -m py_compile scenes\part1_g1_intro_taxonomy.py scenes\part1_g2_corroborative.py scenes\part1_g3_game_theoretic.py scenes\part1_g4_predictive.py scenes\part2_core_theory.py scenes\part3_scaling_and_evaluation.py scenes\part4_applications.py scenes\part5_epilogue_recap.py
python scripts\check_srt.py subtitles\part5_epilogue_recap_bilingual.srt
python scripts\check_durations.py --threshold 1.5
python scripts\render_all.py --quality low
```

For final export, render individual scenes in high quality:

```powershell
manim -qh scenes\part1_g1_intro_taxonomy.py IntroTaxonomy
manim -qh scenes\part1_g2_corroborative.py CorroborativeAttribution
manim -qh scenes\part1_g3_game_theoretic.py GameTheoreticAttribution
manim -qh scenes\part1_g4_predictive.py PredictiveAttribution
manim -qh scenes\part2_core_theory.py CoreTheory
manim -qh scenes\part3_scaling_and_evaluation.py ScalingAndEvaluation
manim -qh scenes\part4_applications.py ApplicationsOfDataAttribution
manim -qh scenes\part5_epilogue_recap.py EpilogueRecap
```

## Git Policy

Commit these files:

- Manim source files in `scenes/`.
- Documentation in `docs/`.
- Subtitle text files in `subtitles/`.
- Helper scripts in `scripts/`.
- Timeline metadata in `timelines/`.
- Project metadata such as `README.md`, `.gitignore`, and `requirements.txt`.

Do not commit these files:

- Rendered videos in `media/`.
- Audio files in `assets/audio/`.
- Large video/audio exports such as `.mp4`, `.mp3`, `.wav`, `.mov`.
- Local virtual environments.
- Temporary editor or OS files.

The `.gitignore` is configured to keep these generated and heavy assets out of Git.

## Attribution

This project is an independent Vietnamese educational video adaptation based on
the ICML 2024 tutorial:

**Data Attribution at Scale: Connecting ML Behavior to Training Data**

Tutorial website:

```text
https://ml-data-tutorial.org
```

Use the original tutorial as the academic reference, and use this repository as
the Manim production source for the Vietnamese video.
