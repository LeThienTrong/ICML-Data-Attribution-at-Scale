#!/usr/bin/env bash
set -e

SCENE_FILE=${1:-scenes/part1_g1_intro_taxonomy.py}
SCENE_NAME=${2:-IntroTaxonomy}
QUALITY=${3:-pqh}

manim -$QUALITY "$SCENE_FILE" "$SCENE_NAME"
