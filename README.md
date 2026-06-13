# Data Attribution at Scale - ICML 2024 Tutorial

Source Manim project for a Vietnamese academic video based on the ICML 2024 tutorial **Data Attribution at Scale: Connecting ML behavior to training data**.

The current production target is a compact 40-60 minute submission version that covers the main tutorial ideas:

- Part I: attribution taxonomy.
- Part II: theory, leave-one-out, influence functions, and datamodels.
- Part III: scaling and counterfactual evaluation.
- Part IV: applications.
- Epilogue: recap and credits.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Render One Scene

```bash
manim -ql scenes/part1_g2_corroborative.py CorroborativeAttribution
manim -qh scenes/part1_g2_corroborative.py CorroborativeAttribution
```

## Render All Scenes

```bash
python scripts/render_all.py --quality low
python scripts/render_all.py --quality high
```

Render logs are written to `outputs/render_logs/`.

## Check Subtitles And Timing

```bash
python scripts/check_srt.py subtitles/part1_g2_corroborative_bilingual.srt
python scripts/check_durations.py
```

## Project Layout

```text
scenes/       ManimCE scene source
docs/         voice scripts, coverage matrix, production docs
subtitles/    bilingual subtitle files
assets/audio/ AI voice files used for sync where available
scripts/      render and validation helpers
notebooks/    optional demos
```

## GitHub Notes

Do not commit heavy render artifacts. The `.gitignore` excludes Manim `media/`, generated videos, and audio/video binaries. Commit source `.py`, docs, scripts, and subtitle text files.
