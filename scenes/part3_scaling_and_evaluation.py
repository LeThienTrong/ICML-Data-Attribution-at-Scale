from __future__ import annotations

import json
import os
from pathlib import Path

from manim import *


# ============================================================
# ICML Tutorial: Data Attribution at Scale
# Part III: Scaling and evaluation
# Timeline-driven build. Audio is NOT embedded.
# ============================================================

config.background_color = "#171717"
config.frame_width = 16
config.frame_height = 9

ROOT = Path(__file__).resolve().parents[1]
TIMELINE = ROOT / "timelines" / "part3_scaling_and_evaluation.json"

BG = "#171717"
WHITE_SOFT = "#E8E8E8"
GRAY_SOFT = "#9A9A9A"
BLUE_NEON = "#4DA6FF"
GREEN_NEON = "#42F59B"
YELLOW_NEON = "#FFD166"
RED_NEON = "#FF5C5C"
PURPLE_NEON = "#B388FF"
CYAN_SOFT = "#64E9FF"
ORANGE_SOFT = "#FFA657"

GROUP_TITLES = {
    "p3_00": ("Từ theory sạch sang modern ML", BLUE_NEON),
    "p3_01": ("Ba trục scale", CYAN_SOFT),
    "p3_02": ("Counterfactual ground truth", YELLOW_NEON),
    "p3_03": ("Influence functions ở scale lớn", PURPLE_NEON),
    "p3_04": ("Training dynamics và TracIn", ORANGE_SOFT),
    "p3_05": ("TRAK: behavior attribution at scale", GREEN_NEON),
    "p3_06": ("Datamodels: chính xác hơn, đắt hơn", BLUE_NEON),
    "p3_07": ("Method landscape", YELLOW_NEON),
    "p3_08": ("Counterfactual evaluation và LDS", GREEN_NEON),
    "p3_09": ("Failure modes và hygiene", RED_NEON),
    "p3_10": ("Future work", PURPLE_NEON),
    "p3_11": ("Takeaway và chuyển sang Part IV", CYAN_SOFT),
}


def make_title(text: str, font_size: int = 40, color: str = WHITE_SOFT) -> Text:
    title = Text(text, font="Arial", font_size=font_size, weight=BOLD, color=color)
    if title.width > 14.4:
        title.scale_to_fit_width(14.4)
    return title


def make_label(text: str, color: str = WHITE_SOFT, font_size: int = 25, weight=NORMAL) -> Text:
    label = Text(text, font="Arial", font_size=font_size, weight=weight, color=color, line_spacing=0.86)
    if label.width > 12.6:
        label.scale_to_fit_width(12.6)
    return label


def rounded_box(width: float, height: float, color: str, fill_opacity: float = 0.055, stroke_width: float = 2) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        color=color,
        stroke_width=stroke_width,
        fill_color=color,
        fill_opacity=fill_opacity,
    )


def chip(text: str, color: str, font_size: int = 20) -> VGroup:
    label = make_label(text, color, font_size, BOLD)
    max_width = 2.75
    if label.width > max_width:
        label.scale_to_fit_width(max_width)
    if label.height > 0.32:
        label.scale_to_fit_height(0.32)
    frame = rounded_box(label.width + 0.46, max(0.46, label.height + 0.18), color, 0.08, 1.7)
    return VGroup(frame, label.move_to(frame))


def labeled_box(text: str, color: str, width: float = 3.15, height: float = 1.0, font_size: int = 23) -> VGroup:
    frame = rounded_box(width, height, color, 0.06, 2)
    label = make_label(text, color, font_size, BOLD)
    if label.width > width - 0.32:
        label.scale_to_fit_width(width - 0.32)
    if label.height > height - 0.24:
        label.scale_to_fit_height(height - 0.24)
    label.move_to(frame)
    return VGroup(frame, label)


def equation(tex: str, color: str = YELLOW_NEON, font_size: int = 36, max_width: float = 7.2) -> MathTex:
    eq = MathTex(tex, color=color, font_size=font_size)
    if eq.width > max_width:
        eq.scale_to_fit_width(max_width)
    return eq


def split_terms(value: str) -> list[str]:
    terms = [term.strip() for term in value.replace(",", ";").split(";")]
    return [term for term in terms if term][:5]


def must_show_chips(beat: dict, color: str) -> VGroup:
    terms = split_terms(str(beat.get("must_show", "")))
    if not terms:
        return VGroup()
    chips = VGroup(*[chip(term, color, 16) for term in terms]).arrange(RIGHT, buff=0.16)
    if chips.width > 12.8:
        chips.scale_to_fit_width(12.8)
    chips.to_edge(DOWN, buff=0.76)
    return chips


def beat_index(beat: dict) -> int:
    try:
        return int(str(beat["id"]).split("_")[-1])
    except (KeyError, ValueError):
        return 1


def dots_grid(rows: int, cols: int, color: str, radius: float = 0.045, buff: float = 0.11) -> VGroup:
    dots = VGroup(*[Dot(radius=radius, color=color) for _ in range(rows * cols)])
    dots.arrange_in_grid(rows=rows, cols=cols, buff=buff)
    return dots


def base_frame(beat: dict) -> tuple[VGroup, str]:
    group = str(beat["group"])
    group_title, color = GROUP_TITLES.get(group, ("Scaling and Evaluation", WHITE_SOFT))
    title = make_title("Part III: Scaling and Evaluation", 42).to_edge(UP, buff=0.25)
    section = make_label(group_title, color, 25, BOLD).next_to(title, DOWN, buff=0.14)
    beat_title = make_label(str(beat["title"]), GRAY_SOFT, 20, BOLD).next_to(section, DOWN, buff=0.08)
    return VGroup(title, section, beat_title), color


def visual_intro(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    left = VGroup(
        labeled_box("weights", BLUE_NEON, 2.3, 0.78, 21),
        labeled_box("LOO", YELLOW_NEON, 2.3, 0.78, 21),
        labeled_box("IF", PURPLE_NEON, 2.3, 0.78, 21),
        labeled_box("datamodels", GREEN_NEON, 2.3, 0.78, 20),
    ).arrange(DOWN, buff=0.22).move_to(LEFT * 4.7 + DOWN * 0.1)
    data = dots_grid(8, 13, BLUE_NEON, 0.035, 0.075).move_to(RIGHT * 3.45 + DOWN * 0.05)
    model = labeled_box("modern ML", GREEN_NEON, 2.9, 1.15, 25).move_to(RIGHT * 0.15 + DOWN * 0.05)
    arrow1 = Arrow(left.get_right(), model.get_left(), color=WHITE_SOFT, buff=0.2, stroke_width=4)
    arrow2 = Arrow(model.get_right(), data.get_left(), color=WHITE_SOFT, buff=0.2, stroke_width=4)
    noisy = VGroup(
        chip("large", YELLOW_NEON),
        chip("noisy", RED_NEON),
        chip("many targets", CYAN_SOFT),
    ).arrange(DOWN, buff=0.18).move_to(RIGHT * 6.25 + DOWN * 0.1)
    highlight = SurroundingRectangle(left[min(idx - 1, len(left) - 1)], color=color, buff=0.08)
    if idx >= 3:
        highlight = SurroundingRectangle(VGroup(model, data), color=color, buff=0.16)
    return VGroup(header, left, model, data, arrow1, arrow2, noisy, highlight, must_show_chips(beat, color))


def visual_scale_axes(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    axes = VGroup()
    specs = [("n", "training points", BLUE_NEON), ("p", "parameters", PURPLE_NEON), ("m", "target behaviors", GREEN_NEON)]
    for label, body, axis_color in specs:
        line = Line(DOWN * 1.35, UP * 1.35, color=axis_color, stroke_width=5)
        arrow = Triangle(color=axis_color, fill_color=axis_color, fill_opacity=1).scale(0.16).next_to(line, UP, buff=0)
        name = make_label(label, axis_color, 44, BOLD).next_to(line, DOWN, buff=0.16)
        desc = make_label(body, WHITE_SOFT, 18, BOLD).next_to(name, DOWN, buff=0.08)
        axes.add(VGroup(line, arrow, name, desc))
    axes.arrange(RIGHT, buff=2.0).move_to(UP * 0.2)
    cost = [
        "n retrains",
        "2^n subsets",
        "p x p Hessian",
        "HVP / CG",
        "n x m scores",
        "behavior + budget",
    ]
    callout = labeled_box(cost[min(idx - 1, len(cost) - 1)], color, 4.6, 0.85, 25).move_to(DOWN * 2.15)
    active_axis = axes[0 if idx <= 3 else 1 if idx <= 5 else 2]
    highlight = SurroundingRectangle(active_axis, color=color, buff=0.18)
    return VGroup(header, axes, callout, highlight, must_show_chips(beat, color))


def visual_counterfactual(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    data = labeled_box("same data S", BLUE_NEON, 2.4, 0.8, 23).move_to(LEFT * 5.2 + UP * 0.7)
    paths = VGroup(
        labeled_box("seed A", GREEN_NEON, 2.1, 0.72, 21).move_to(LEFT * 1.6 + UP * 1.45),
        labeled_box("seed B", YELLOW_NEON, 2.1, 0.72, 21).move_to(LEFT * 1.6 + UP * 0.15),
        labeled_box("checkpoint", PURPLE_NEON, 2.45, 0.72, 21).move_to(LEFT * 1.6 + DOWN * 1.15),
    )
    arrows = VGroup(*[Arrow(data.get_right(), path.get_left(), color=WHITE_SOFT, buff=0.15) for path in paths])
    behavior = labeled_box("behavior distribution", RED_NEON, 3.2, 1.05, 22).move_to(RIGHT * 3.9 + UP * 0.15)
    out_arrows = VGroup(*[Arrow(path.get_right(), behavior.get_left(), color=WHITE_SOFT, buff=0.15) for path in paths])
    checklist_terms = ["retrain", "fine-tune", "seed", "checkpoint", "metric"]
    checklist = VGroup(
        *[
            VGroup(Square(0.18, color=GREEN_NEON), make_label(term, WHITE_SOFT, 18, BOLD)).arrange(RIGHT, buff=0.13)
            for term in checklist_terms
        ]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 0.2 + DOWN * 2.2)
    if idx <= len(checklist):
        highlight = SurroundingRectangle(checklist[idx - 1], color=color, buff=0.07)
    else:
        highlight = SurroundingRectangle(VGroup(data, behavior), color=color, buff=0.15)
    return VGroup(header, data, paths, arrows, behavior, out_arrows, checklist, highlight, must_show_chips(beat, color))


def visual_influence(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    formula = equation(
        r"\Delta f_j \approx -\nabla_\theta f^\top H^{-1}\nabla_\theta \ell_j",
        YELLOW_NEON,
        38,
        8.7,
    ).move_to(UP * 1.55)
    pieces = VGroup(
        labeled_box("grad behavior", BLUE_NEON, 2.65, 0.82, 20),
        labeled_box("H^-1", PURPLE_NEON, 1.65, 0.82, 25),
        labeled_box("grad sample", GREEN_NEON, 2.45, 0.82, 20),
    ).arrange(RIGHT, buff=0.38).move_to(UP * 0.35)
    hessian = VGroup(
        labeled_box("Hessian", RED_NEON, 2.2, 0.75, 22),
        labeled_box("HVP", CYAN_SOFT, 1.7, 0.7, 20),
        labeled_box("CG", YELLOW_NEON, 1.35, 0.7, 20),
        labeled_box("LiSSA", GREEN_NEON, 1.55, 0.7, 20),
    ).arrange(RIGHT, buff=0.24).move_to(DOWN * 1.1)
    slider = Line(LEFT * 3.0, RIGHT * 3.0, color=GRAY_SOFT, stroke_width=5).move_to(DOWN * 2.25)
    knob_x = [-2.5, -1.7, -0.6, 0.5, 1.5, 2.55][min(idx - 1, 5)]
    knob = Dot(slider.get_center() + RIGHT * knob_x, radius=0.13, color=color)
    labels = VGroup(make_label("theory", GRAY_SOFT, 17), make_label("evaluation", GRAY_SOFT, 17))
    labels[0].next_to(slider, LEFT, buff=0.18)
    labels[1].next_to(slider, RIGHT, buff=0.18)
    return VGroup(header, formula, pieces, hessian, slider, knob, labels, must_show_chips(beat, color))


def visual_tracin(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    points = [LEFT * 5.0 + DOWN * 1.1, LEFT * 3.1 + UP * 0.65, LEFT * 1.1 + DOWN * 0.2, RIGHT * 1.0 + UP * 0.9, RIGHT * 3.3 + DOWN * 0.2]
    path = VMobject(color=ORANGE_SOFT, stroke_width=4).set_points_smoothly(points)
    checkpoints = VGroup(*[Dot(point, radius=0.11, color=YELLOW_NEON) for point in points])
    model = labeled_box("training trajectory", ORANGE_SOFT, 3.5, 0.75, 22).next_to(path, UP, buff=0.4)
    z = chip("sample z", BLUE_NEON).move_to(LEFT * 5.2 + UP * 1.4)
    target = chip("target x", GREEN_NEON).move_to(RIGHT * 4.7 + UP * 1.45)
    arrows = VGroup(
        Arrow(z.get_bottom(), checkpoints[min(idx - 1, len(checkpoints) - 1)].get_center(), color=BLUE_NEON, buff=0.15),
        Arrow(target.get_bottom(), checkpoints[min(idx - 1, len(checkpoints) - 1)].get_center(), color=GREEN_NEON, buff=0.15),
    )
    formula = equation(
        r"\mathrm{score}(z,x)=\sum_t \eta_t\langle\nabla\ell_x(\theta_t),\nabla\ell_z(\theta_t)\rangle",
        WHITE_SOFT,
        29,
        8.8,
    ).move_to(DOWN * 2.18)
    warnings = VGroup(chip("checkpoint", RED_NEON), chip("loss scale", RED_NEON), chip("optimizer path", RED_NEON)).arrange(RIGHT, buff=0.22).move_to(DOWN * 1.45)
    if idx < 5:
        warnings.set_opacity(0.25)
    return VGroup(header, path, checkpoints, model, z, target, arrows, formula, warnings, must_show_chips(beat, color))


def visual_trak(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    model = labeled_box("large model", GREEN_NEON, 2.35, 1.05, 23).move_to(LEFT * 5.0 + UP * 0.35)
    features = labeled_box("gradient features", BLUE_NEON, 2.95, 0.9, 21).move_to(LEFT * 2.05 + UP * 0.35)
    projection = labeled_box("random projection", PURPLE_NEON, 3.1, 0.9, 20).move_to(RIGHT * 1.15 + UP * 0.35)
    score = labeled_box("TRAK scores", YELLOW_NEON, 2.45, 0.9, 22).move_to(RIGHT * 4.5 + UP * 0.35)
    arrows = VGroup(
        Arrow(model.get_right(), features.get_left(), color=WHITE_SOFT, buff=0.12),
        Arrow(features.get_right(), projection.get_left(), color=WHITE_SOFT, buff=0.12),
        Arrow(projection.get_right(), score.get_left(), color=WHITE_SOFT, buff=0.12),
    )
    rank_bars = VGroup()
    for i, width in enumerate([2.7, 2.25, 1.7, 1.2]):
        bar = Rectangle(width=width, height=0.18, fill_color=[GREEN_NEON, BLUE_NEON, YELLOW_NEON, RED_NEON][i], fill_opacity=0.85, stroke_width=0)
        label = make_label(f"z{i + 1}", WHITE_SOFT, 17, BOLD).next_to(bar, LEFT, buff=0.18)
        rank_bars.add(VGroup(label, bar))
    rank_bars.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 1.55)
    focus_objects = [model, features, projection, score, rank_bars, score]
    highlight = SurroundingRectangle(focus_objects[min(idx - 1, len(focus_objects) - 1)], color=color, buff=0.12)
    return VGroup(header, model, features, projection, score, arrows, rank_bars, highlight, must_show_chips(beat, color))


def visual_datamodels(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    masks = VGroup()
    for row in range(5):
        dots = VGroup(*[Square(0.22, fill_color=(GREEN_NEON if (row + col) % 2 else GRAY_SOFT), fill_opacity=0.9, stroke_width=0) for col in range(6)])
        dots.arrange(RIGHT, buff=0.08)
        masks.add(dots)
    masks.arrange(DOWN, buff=0.14).move_to(LEFT * 4.6 + UP * 0.1)
    train_runs = labeled_box("many training runs", RED_NEON, 3.25, 0.95, 21).move_to(LEFT * 1.25 + UP * 0.1)
    surrogate = labeled_box("surrogate", PURPLE_NEON, 2.45, 0.95, 23).move_to(RIGHT * 1.7 + UP * 0.1)
    behavior = labeled_box("behavior", GREEN_NEON, 2.25, 0.95, 23).move_to(RIGHT * 4.85 + UP * 0.1)
    arrows = VGroup(
        Arrow(masks.get_right(), train_runs.get_left(), color=WHITE_SOFT, buff=0.12),
        Arrow(train_runs.get_right(), surrogate.get_left(), color=WHITE_SOFT, buff=0.12),
        Arrow(surrogate.get_right(), behavior.get_left(), color=WHITE_SOFT, buff=0.12),
    )
    formula = equation(
        r"\widehat f(S)=\beta_0+\sum_i m_i\tau_i",
        YELLOW_NEON,
        42,
        7.4,
    ).move_to(DOWN * 1.48)
    cost = VGroup(chip("upfront cost", RED_NEON), chip("amortize", GREEN_NEON), chip("many queries", BLUE_NEON)).arrange(RIGHT, buff=0.24).move_to(DOWN * 2.22)
    focus = [masks, train_runs, formula, surrogate, cost, behavior]
    highlight = SurroundingRectangle(focus[min(idx - 1, len(focus) - 1)], color=color, buff=0.12)
    return VGroup(header, masks, train_runs, surrogate, behavior, arrows, formula, cost, highlight, must_show_chips(beat, color))


def visual_landscape(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    axes = Axes(
        x_range=[0, 10, 2],
        y_range=[0, 10, 2],
        x_length=8.2,
        y_length=4.8,
        axis_config={"color": GRAY_SOFT, "stroke_width": 2},
    ).move_to(DOWN * 0.1)
    x_label = make_label("cost", GRAY_SOFT, 19, BOLD).next_to(axes.x_axis, RIGHT, buff=0.1)
    y_label = make_label("counterfactual accuracy", GRAY_SOFT, 19, BOLD).next_to(axes.y_axis, UP, buff=0.1)
    methods = [
        ("similarity", 1.2, 2.0, BLUE_NEON),
        ("grad", 2.5, 3.5, CYAN_SOFT),
        ("TracIn", 3.4, 4.7, ORANGE_SOFT),
        ("IF", 4.1, 5.0, PURPLE_NEON),
        ("TRAK", 5.6, 6.8, GREEN_NEON),
        ("Shapley", 7.3, 7.3, YELLOW_NEON),
        ("datamodels", 8.7, 8.4, RED_NEON),
    ]
    dots = VGroup()
    for label, x, y, dot_color in methods:
        dot = Dot(axes.c2p(x, y), radius=0.11, color=dot_color)
        text = make_label(label, dot_color, 15, BOLD).next_to(dot, UP, buff=0.08)
        dots.add(VGroup(dot, text))
    active = dots[min(idx - 1, len(dots) - 1)]
    selector = SurroundingRectangle(active, color=color, buff=0.09)
    note_text = ["landscape", "cheap", "learning", "theory", "middle", "expensive", "choose by use case"][min(idx - 1, 6)]
    note = labeled_box(note_text, color, 3.4, 0.78, 22).to_edge(DOWN, buff=1.05)
    return VGroup(header, axes, x_label, y_label, dots, selector, note, must_show_chips(beat, color))


def visual_evaluation(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    axes = Axes(
        x_range=[0, 1, 0.25],
        y_range=[0, 1, 0.25],
        x_length=5.2,
        y_length=3.45,
        axis_config={"color": GRAY_SOFT, "stroke_width": 2},
    ).move_to(LEFT * 3.25 + DOWN * 0.1)
    diagonal = Line(axes.c2p(0, 0), axes.c2p(1, 1), color=GREEN_NEON, stroke_width=3)
    pts = VGroup(*[Dot(axes.c2p(x, y), radius=0.07, color=c) for x, y, c in [(0.15, 0.19, BLUE_NEON), (0.32, 0.28, YELLOW_NEON), (0.45, 0.52, GREEN_NEON), (0.66, 0.57, RED_NEON), (0.82, 0.8, GREEN_NEON)]])
    axis_labels = VGroup(make_label("actual", GRAY_SOFT, 17), make_label("predicted", GRAY_SOFT, 17))
    axis_labels[0].next_to(axes.x_axis, DOWN, buff=0.13)
    axis_labels[1].next_to(axes.y_axis, LEFT, buff=0.13)
    lds_panel = rounded_box(5.95, 3.45, PURPLE_NEON, 0.045, 2).move_to(RIGHT * 3.45 + DOWN * 0.1)
    lds_title = make_label("LDS", PURPLE_NEON, 32, BOLD).move_to(lds_panel.get_top() + DOWN * 0.42)
    mask = dots_grid(3, 5, BLUE_NEON, 0.055, 0.13)
    mask_label = make_label("subset S", BLUE_NEON, 16, BOLD).next_to(mask, DOWN, buff=0.14)
    panel_center = lds_panel.get_center()
    mask_group = VGroup(mask, mask_label).move_to(panel_center + LEFT * 1.55 + UP * 0.25)
    sum_formula = equation(r"\sum_{i\in S}\tau_i", YELLOW_NEON, 30, 1.55)
    sum_frame = rounded_box(1.82, 0.78, YELLOW_NEON, 0.06, 2)
    sum_box = VGroup(sum_frame, sum_formula.move_to(sum_frame)).move_to(panel_center + RIGHT * 0.58 + UP * 0.25)
    behavior_formula = equation(r"\widehat y(S)\leftrightarrow y(S)", GREEN_NEON, 28, 2.35)
    behavior_frame = rounded_box(2.95, 0.78, GREEN_NEON, 0.06, 2)
    behavior = VGroup(behavior_frame, behavior_formula.move_to(behavior_frame)).move_to(panel_center + RIGHT * 1.05 + DOWN * 0.72)
    lds_arrows = VGroup(
        Arrow(mask_group.get_right(), sum_box.get_left(), color=WHITE_SOFT, buff=0.1, stroke_width=3.5),
        Arrow(sum_box.get_bottom(), behavior.get_top(), color=WHITE_SOFT, buff=0.12, stroke_width=3.5),
    )
    lds_formula = equation(r"\mathrm{LDS}=\mathrm{corr}\left(\widehat y(S),y(S)\right)", PURPLE_NEON, 27, 4.55)
    lds_formula.move_to(lds_panel.get_bottom() + UP * 0.42)
    metric_terms = ["intervention", "delta", "calibration", "top-k", "sign", "LDS", "prediction vs truth", "interaction", "use case"]
    metric = labeled_box(metric_terms[min(idx - 1, len(metric_terms) - 1)], color, 3.35, 0.7, 20).move_to(DOWN * 2.38)
    return VGroup(header, axes, diagonal, pts, axis_labels, lds_panel, lds_title, mask_group, sum_box, behavior, lds_arrows, lds_formula, metric, must_show_chips(beat, color))


def visual_failure(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    items = [
        ("duplicates", BLUE_NEON),
        ("correlated data", PURPLE_NEON),
        ("target mismatch", YELLOW_NEON),
        ("seed noise", RED_NEON),
        ("OOD intervention", ORANGE_SOFT),
        ("metric hygiene", GREEN_NEON),
    ]
    grid = VGroup(*[labeled_box(text, item_color, 3.25, 0.82, 21) for text, item_color in items]).arrange_in_grid(rows=2, cols=3, buff=0.38)
    grid.move_to(UP * 0.2)
    heatmap = dots_grid(5, 9, GREEN_NEON, 0.04, 0.07).move_to(DOWN * 2.0 + LEFT * 2.7)
    cracks = VGroup(*[Line(ORIGIN, UP * 0.55, color=RED_NEON, stroke_width=4).rotate(angle) for angle in [-0.55, 0.2, 0.75]])
    cracks.arrange(RIGHT, buff=0.35).move_to(heatmap)
    checklist = labeled_box("target + intervention + seed + metric", GREEN_NEON, 4.9, 0.8, 20).move_to(DOWN * 2.0 + RIGHT * 2.6)
    highlight = SurroundingRectangle(grid[min(idx - 1, len(grid) - 1)], color=color, buff=0.1)
    return VGroup(header, grid, heatmap, cracks, checklist, highlight, must_show_chips(beat, color))


def visual_future(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    doors = [
        ("beyond\nlinear", BLUE_NEON),
        ("pair\ninteraction", CYAN_SOFT),
        ("multiple\nstages", YELLOW_NEON),
        ("better\nsurrogate", GREEN_NEON),
        ("single-model\ncounterfactual", PURPLE_NEON),
        ("efficient\nproxies", ORANGE_SOFT),
        ("evaluated\ncorrectly", RED_NEON),
        ("know\nlimits", WHITE_SOFT),
    ]
    door_group = VGroup()
    for text, door_color in doors:
        frame = rounded_box(1.86, 1.45, door_color, 0.065, 2)
        label = make_label(text, door_color, 15, BOLD)
        if label.width > 1.52:
            label.scale_to_fit_width(1.52)
        if label.height > 1.08:
            label.scale_to_fit_height(1.08)
        label.move_to(frame)
        door_group.add(VGroup(frame, label))
    door_group.arrange_in_grid(rows=2, cols=4, buff=0.34).move_to(UP * 0.12)
    pipeline = VGroup(
        chip("pretrain", BLUE_NEON, 17),
        chip("filter", YELLOW_NEON, 17),
        chip("SFT", GREEN_NEON, 17),
        chip("alignment", PURPLE_NEON, 17),
        chip("RAG", CYAN_SOFT, 17),
    ).arrange(RIGHT, buff=0.2).move_to(DOWN * 2.3)
    highlight = SurroundingRectangle(door_group[min(idx - 1, len(door_group) - 1)], color=color, buff=0.12)
    return VGroup(header, door_group, pipeline, highlight, must_show_chips(beat, color))


def visual_takeaway(beat: dict) -> VGroup:
    idx = beat_index(beat)
    header, color = base_frame(beat)
    cards = VGroup(
        labeled_box("scale changes\nthe problem", RED_NEON, 3.25, 1.15, 21),
        labeled_box("scalable methods\nare estimators", YELLOW_NEON, 3.25, 1.15, 21),
        labeled_box("pretty score\nis not enough", GREEN_NEON, 3.25, 1.15, 21),
        labeled_box("choose by use case\nand compute", BLUE_NEON, 3.25, 1.15, 21),
    ).arrange_in_grid(rows=2, cols=2, buff=0.45).move_to(LEFT * 2.7 + DOWN * 0.15)
    part4 = labeled_box("Part IV\napplications", PURPLE_NEON, 3.1, 1.45, 25).move_to(RIGHT * 4.4 + DOWN * 0.15)
    arrow = Arrow(cards.get_right(), part4.get_left(), color=WHITE_SOFT, stroke_width=5, buff=0.22)
    highlight = SurroundingRectangle(cards[min(idx - 1, len(cards) - 1)] if idx <= 4 else part4, color=color, buff=0.12)
    return VGroup(header, cards, part4, arrow, highlight, must_show_chips(beat, color))


def visual_for_beat(beat: dict) -> VGroup:
    group = str(beat["group"])
    if group == "p3_00":
        return visual_intro(beat)
    if group == "p3_01":
        return visual_scale_axes(beat)
    if group == "p3_02":
        return visual_counterfactual(beat)
    if group == "p3_03":
        return visual_influence(beat)
    if group == "p3_04":
        return visual_tracin(beat)
    if group == "p3_05":
        return visual_trak(beat)
    if group == "p3_06":
        return visual_datamodels(beat)
    if group == "p3_07":
        return visual_landscape(beat)
    if group == "p3_08":
        return visual_evaluation(beat)
    if group == "p3_09":
        return visual_failure(beat)
    if group == "p3_10":
        return visual_future(beat)
    if group == "p3_11":
        return visual_takeaway(beat)
    header, color = base_frame(beat)
    return VGroup(header, labeled_box(str(beat["title"]), color, 5, 1.2), must_show_chips(beat, color))


class ScalingAndEvaluation(Scene):
    max_beats: int | None = None
    duration_scale: float = 1.0

    def construct(self) -> None:
        self.camera.background_color = BG
        if not TIMELINE.exists():
            raise FileNotFoundError(f"Missing timeline: {TIMELINE}")

        timeline = json.loads(TIMELINE.read_text(encoding="utf-8"))
        beats = timeline["beats"]
        max_beats = self.max_beats or int(os.environ.get("PART3_MAX_BEATS", "0") or "0")
        if max_beats > 0:
            beats = beats[:max_beats]
        current: VGroup | None = None

        for beat in beats:
            duration = float(beat["duration"]) * self.duration_scale
            visual = visual_for_beat(beat)
            transition = min(0.48, max(0.24, duration * 0.16))
            if current is None:
                self.play(FadeIn(visual, shift=UP * 0.1), run_time=transition)
            else:
                self.play(FadeOut(current, shift=UP * 0.06), FadeIn(visual, shift=UP * 0.06), run_time=transition)
            hold = max(0.0, duration - transition)
            if hold:
                self.wait(hold)
            current = visual

        pad_end = float(timeline.get("pad_end", 0.8))
        if current is not None:
            fade_time = min(0.6, max(0.1, pad_end)) if pad_end > 0 else 0.6
            if pad_end > fade_time:
                self.wait(pad_end - fade_time)
            self.play(FadeOut(current), run_time=fade_time)
        elif pad_end > 0:
            self.wait(pad_end)


class ScalingAndEvaluationPreview(ScalingAndEvaluation):
    max_beats = 10
    duration_scale = 0.08
