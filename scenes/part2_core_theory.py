from __future__ import annotations

from manim import *

# ============================================================
# ICML Tutorial: Data Attribution at Scale
# Part II: Core theory, influence functions, datamodels
# ============================================================

config.background_color = "#171717"
config.frame_width = 16
config.frame_height = 9

BG = "#171717"
WHITE_SOFT = "#E8E8E8"
GRAY_SOFT = "#9A9A9A"
GRAY_DARK = "#343434"
BLUE_NEON = "#4DA6FF"
GREEN_NEON = "#42F59B"
YELLOW_NEON = "#FFD166"
RED_NEON = "#FF5C5C"
PURPLE_NEON = "#B388FF"
CYAN_SOFT = "#64E9FF"
ORANGE = "#FFB86B"


AUDIO_DURATIONS = [
    71.419,
    102.217,
    78.106,
    69.982,
    62.119,
    64.183,
    65.437,
    113.868,
    92.918,
    98.900,
    72.986,
    99.709,
    107.128,
]


def make_title(text: str, font_size: int = 43) -> Text:
    return Text(text, font="Arial", font_size=font_size, weight=BOLD, color=WHITE_SOFT)


def make_label(text: str, color=WHITE_SOFT, font_size: int = 26, weight=NORMAL) -> Text:
    return Text(
        text,
        font="Arial",
        font_size=font_size,
        weight=weight,
        color=color,
        line_spacing=0.84,
    )


def rounded_box(width: float, height: float, color=BLUE_NEON, fill_opacity=0.055, stroke_width=2):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        color=color,
        stroke_width=stroke_width,
        fill_color=color,
        fill_opacity=fill_opacity,
    )


def chip(text: str, color=BLUE_NEON, font_size: int = 22, width: float | None = None):
    label = make_label(text, color, font_size, BOLD)
    if width is not None and label.width > width - 0.5:
        label.scale((width - 0.5) / label.width)
    frame = rounded_box(width or label.width + 0.45, label.height + 0.26, color, 0.055, 2)
    label.move_to(frame)
    return VGroup(frame, label)


def boxed_label(
    text: str,
    color=BLUE_NEON,
    font_size: int = 26,
    width: float = 4.0,
    height: float = 1.2,
    fill_opacity: float = 0.055,
    stroke_width: int = 2,
):
    frame = rounded_box(width, height, color, fill_opacity, stroke_width)
    label = make_label(text, color, font_size, BOLD)
    max_width = width - 0.55
    max_height = height - 0.34
    fit = min(
        1.0,
        max_width / label.width if label.width else 1.0,
        max_height / label.height if label.height else 1.0,
    )
    if fit < 1.0:
        label.scale(fit)
    label.move_to(frame)
    return VGroup(frame, label)


def card(title: str, body: str, color=BLUE_NEON, width=3.8, height=1.75, title_size=25, body_size=20):
    frame = rounded_box(width, height, color, 0.05, 2)
    title_obj = make_label(title, color, title_size, BOLD)
    body_obj = make_label(body, WHITE_SOFT, body_size)
    content = VGroup(title_obj, body_obj).arrange(DOWN, buff=0.22)
    content.move_to(frame)
    return VGroup(frame, content)


def bit_cell(bit: int, color=GREEN_NEON, side=0.36):
    active = bool(bit)
    cell_color = color if active else GRAY_SOFT
    square = Square(side_length=side, color=cell_color, stroke_width=1.6)
    square.set_fill(cell_color, opacity=0.24 if active else 0.06)
    label = make_label("1" if active else "0", cell_color, int(side * 42), BOLD).move_to(square)
    return VGroup(square, label)


def bit_row(bits: list[int], color=GREEN_NEON, side=0.36, buff=0.06):
    row = VGroup(*[bit_cell(bit, color, side) for bit in bits]).arrange(RIGHT, buff=buff)
    return row


def neural_net(color=GREEN_NEON):
    layers = [3, 5, 4, 2]
    x_positions = [-1.45, -0.45, 0.55, 1.45]
    nodes = []
    edges = VGroup()
    for layer_idx, count in enumerate(layers):
        y_positions = [0] if count == 1 else [1.1 - i * (2.2 / (count - 1)) for i in range(count)]
        layer_nodes = []
        for y in y_positions:
            dot = Dot([x_positions[layer_idx], y, 0], radius=0.045, color=WHITE_SOFT)
            layer_nodes.append(dot)
        nodes.append(layer_nodes)
    for left, right in zip(nodes[:-1], nodes[1:]):
        for a in left:
            for b in right:
                edges.add(Line(a.get_center(), b.get_center(), color=GRAY_SOFT, stroke_width=0.8, stroke_opacity=0.45))
    dots = VGroup(*[dot for layer in nodes for dot in layer])
    return VGroup(edges, dots).set_color(color)


def mini_dataset(rows=4, cols=5, color=BLUE_NEON, highlight_index: int | None = None):
    dots = VGroup()
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            dot_color = RED_NEON if idx == highlight_index else color
            dots.add(Dot(radius=0.075, color=dot_color).move_to(RIGHT * c * 0.36 + DOWN * r * 0.34))
    dots.center()
    return dots


class CoreTheory(Scene):
    def construct(self):
        self.camera.background_color = BG

        def tracker():
            return [0.0]

        def playt(t, *animations, run_time=1.0, **kwargs):
            self.play(*animations, run_time=run_time, **kwargs)
            t[0] += run_time

        def wait_until(t, target, reserve=0.0):
            remain = target - t[0] - reserve
            if remain > 0:
                self.wait(remain)
                t[0] += remain

        def fade_segment(t, target, *mobjects, run_time=0.7, extra=0.0):
            wait_until(t, target + extra, reserve=run_time if mobjects else 0.0)
            if mobjects:
                playt(t, FadeOut(VGroup(*mobjects)), run_time=run_time)

        def retitle(t, title_obj: Text, text: str, size=42):
            new_title = make_title(text, size).to_edge(UP, buff=0.32)
            playt(t, Transform(title_obj, new_title), run_time=0.65)

        # ------------------------------------------------------------
        # p2_00 - Why theory.
        # ------------------------------------------------------------
        t = tracker()
        title = make_title("Part II: Core Theory", 50).to_edge(UP, buff=0.32)
        subtitle = make_label("Từ trực giác attribution đến counterfactual prediction", BLUE_NEON, 28, BOLD)
        subtitle.next_to(title, DOWN, buff=0.28)

        center = VGroup(
            Circle(radius=0.72, color=WHITE_SOFT, stroke_width=2, fill_color=WHITE_SOFT, fill_opacity=0.03),
            make_label("model\nbehavior", WHITE_SOFT, 24, BOLD),
        ).move_to(ORIGIN + DOWN * 0.1)
        center[1].move_to(center[0])
        lenses = VGroup(
            chip("evidence", BLUE_NEON, 24).move_to(LEFT * 4.9 + UP * 1.25),
            chip("credit", YELLOW_NEON, 24).move_to(LEFT * 4.65 + DOWN * 1.35),
            chip("counterfactual", GREEN_NEON, 24).move_to(RIGHT * 4.55 + UP * 0.95),
        )
        lens_arrows = VGroup(
            Arrow(lenses[0].get_right(), center.get_left(), color=BLUE_NEON, buff=0.18),
            Arrow(lenses[1].get_right(), center.get_left() + DOWN * 0.22, color=YELLOW_NEON, buff=0.18),
            Arrow(lenses[2].get_left(), center.get_right() + UP * 0.14, color=GREEN_NEON, buff=0.18),
        )
        question = VGroup(
            rounded_box(7.25, 1.15, GREEN_NEON, 0.045, 2),
            make_label("Nếu training data thay đổi,\nmodel behavior sẽ đổi ra sao?", GREEN_NEON, 28, BOLD),
        ).move_to(DOWN * 2.6)
        question[1].move_to(question[0])
        score_warning = chip("score đẹp chưa đủ: phải kiểm chứng được", RED_NEON, 24).move_to(UP * 2.35)

        playt(t, FadeIn(title, shift=UP * 0.2), FadeIn(subtitle), run_time=0.9)
        playt(t, FadeIn(center), LaggedStart(*[FadeIn(lens, shift=UP * 0.15) for lens in lenses], lag_ratio=0.12), run_time=1.4)
        playt(t, LaggedStart(*[Create(arrow) for arrow in lens_arrows], lag_ratio=0.1), run_time=1.1)
        playt(t, lenses[2].animate.scale(1.12), lens_arrows[2].animate.set_stroke(width=6), rate_func=there_and_back, run_time=1.2)
        playt(t, FadeIn(question, shift=UP * 0.16), run_time=0.9)
        playt(t, FadeIn(score_warning, shift=DOWN * 0.12), run_time=0.8)
        fade_segment(t, AUDIO_DURATIONS[0], subtitle, center, lenses, lens_arrows, question, score_warning)

        # ------------------------------------------------------------
        # p2_01 - Statistical analog.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "Statistical analog: từ estimator đến behavior", 40)
        timeline = VGroup()
        stages = [
            ("weighted\nre-fitting", BLUE_NEON),
            ("leave-one-out\ndiagnostics", YELLOW_NEON),
            ("infinitesimal\njackknife", PURPLE_NEON),
            ("influence\nfunctions", RED_NEON),
            ("datamodeling", GREEN_NEON),
        ]
        for i, (name, color) in enumerate(stages):
            dot = Dot(radius=0.09, color=color)
            label = make_label(name, color, 20, BOLD).next_to(dot, DOWN, buff=0.18)
            timeline.add(VGroup(dot, label))
        timeline.arrange(RIGHT, buff=1.0).move_to(UP * 1.35)
        timeline_line = Line(timeline[0][0].get_center(), timeline[-1][0].get_center(), color=GRAY_SOFT, stroke_width=2)
        split = VGroup(
            card("parameter prediction", "theta thay đổi\nnhư thế nào?", BLUE_NEON, 4.6, 1.85, 25, 22),
            card("behavior prediction", "output, loss,\naccuracy, fairness", GREEN_NEON, 4.6, 1.85, 25, 22),
        ).arrange(RIGHT, buff=1.15).move_to(DOWN * 0.72)
        bridge = Arrow(split[0].get_right(), split[1].get_left(), color=WHITE_SOFT, buff=0.25)
        note = make_label("Trong ML, parameter chỉ là tầng trung gian.", YELLOW_NEON, 29, BOLD).move_to(DOWN * 2.55)

        playt(t, Create(timeline_line), LaggedStart(*[FadeIn(item, shift=UP * 0.12) for item in timeline], lag_ratio=0.12), run_time=1.8)
        playt(t, FadeIn(split[0], shift=RIGHT * 0.12), run_time=0.8)
        playt(t, Create(bridge), FadeIn(split[1], shift=LEFT * 0.12), run_time=1.0)
        playt(t, FadeIn(note, shift=UP * 0.12), run_time=0.8)
        playt(t, split[1].animate.scale(1.08), rate_func=there_and_back, run_time=1.2)
        fade_segment(t, AUDIO_DURATIONS[1], timeline, timeline_line, split, bridge, note)

        # ------------------------------------------------------------
        # p2_02 - M-estimation.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "M-estimation: data đi vào bằng trọng số", 40)
        formula = MathTex(
            r"\theta^*(w)=\arg\min_{\theta}\sum_{i=1}^{n} w_i\,\ell_i(\theta)",
            font_size=44,
            color=WHITE_SOFT,
        ).move_to(UP * 1.8)
        bars = VGroup()
        heights = [1.0, 0.95, 0.35, 1.12, 0.62, 1.0, 0.0, 1.18]
        for idx, height in enumerate(heights):
            bar = Rectangle(width=0.42, height=max(1.8 * height, 0.06), stroke_width=0)
            color = RED_NEON if height == 0 else YELLOW_NEON if height < 0.8 else BLUE_NEON if height <= 1 else GREEN_NEON
            bar.set_fill(color, opacity=0.9).align_to(ORIGIN, DOWN)
            label = make_label(f"w{idx + 1}", GRAY_SOFT, 15, BOLD).next_to(bar, DOWN, buff=0.12)
            bars.add(VGroup(bar, label))
        bars.arrange(RIGHT, aligned_edge=DOWN, buff=0.25).move_to(LEFT * 4.4 + DOWN * 1.05)
        legend = VGroup(
            chip("w_i = 1: dùng sample", BLUE_NEON, 22, 3.35),
            chip("w_j = 0: bỏ sample", RED_NEON, 22, 3.35),
            chip("w_i > 1: upweight", GREEN_NEON, 22, 3.35),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to(RIGHT * 3.55 + DOWN * 0.8)
        map_note = make_label("w thay đổi -> objective thay đổi -> theta* thay đổi", YELLOW_NEON, 27, BOLD)
        map_note.move_to(DOWN * 2.55)

        playt(t, Write(formula), run_time=1.3)
        playt(t, FadeIn(bars, shift=UP * 0.16), run_time=1.0)
        playt(t, LaggedStart(*[FadeIn(item, shift=LEFT * 0.12) for item in legend], lag_ratio=0.12), run_time=1.2)
        playt(t, bars[6].animate.scale(1.35), legend[1].animate.scale(1.06), rate_func=there_and_back, run_time=1.2)
        playt(t, FadeIn(map_note, shift=UP * 0.12), run_time=0.8)
        fade_segment(t, AUDIO_DURATIONS[2], formula, bars, legend, map_note)

        # ------------------------------------------------------------
        # p2_03 - Leave-one-out.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "Leave-one-out: counterfactual rõ nhưng đắt", 39)
        dataset = mini_dataset(4, 6, BLUE_NEON, highlight_index=15).move_to(LEFT * 5.35 + UP * 0.75)
        data_frame = rounded_box(2.65, 2.15, BLUE_NEON, 0.035).move_to(dataset)
        data_label = make_label("training set S", BLUE_NEON, 23, BOLD).next_to(data_frame, DOWN, buff=0.22)
        full = card("train trên S", "theta*(S)\nbehavior f(S)", GREEN_NEON, 3.05, 1.85, 24, 20).move_to(LEFT * 0.9 + UP * 0.75)
        remove = card("bỏ z_j", "theta*(S \\ {z_j})\nbehavior mới", RED_NEON, 3.55, 1.85, 24, 20).move_to(RIGHT * 4.25 + UP * 0.75)
        arrows = VGroup(
            Arrow(data_frame.get_right(), full.get_left(), color=WHITE_SOFT, buff=0.2),
            Arrow(full.get_right(), remove.get_left(), color=RED_NEON, buff=0.2),
        )
        loo_formula = MathTex(
            r"\mathrm{LOO}(j)=f(S)-f(S\setminus\{z_j\})",
            font_size=42,
            color=YELLOW_NEON,
        ).move_to(DOWN * 1.45)
        cost = VGroup(
            make_label("n data points", GRAY_SOFT, 23),
            Arrow(LEFT * 1.0, RIGHT * 1.0, color=RED_NEON),
            make_label("n retrains", RED_NEON, 27, BOLD),
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 2.55)

        playt(t, FadeIn(data_frame), FadeIn(dataset), FadeIn(data_label), run_time=0.9)
        playt(t, Create(arrows[0]), FadeIn(full, shift=LEFT * 0.12), run_time=0.9)
        playt(t, dataset[15].animate.scale(1.75).set_color(RED_NEON), run_time=0.8)
        playt(t, Create(arrows[1]), FadeIn(remove, shift=LEFT * 0.12), run_time=1.0)
        playt(t, Write(loo_formula), run_time=1.0)
        playt(t, FadeIn(cost, shift=UP * 0.12), run_time=0.8)
        fade_segment(t, AUDIO_DURATIONS[3], data_frame, dataset, data_label, full, remove, arrows, loo_formula, cost)

        # ------------------------------------------------------------
        # p2_04 - Linear regression warmup.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "Warmup: linear regression có cấu trúc đẹp", 38)
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 5, 1],
            x_length=5.2,
            y_length=3.15,
            axis_config={"color": GRAY_SOFT, "stroke_width": 2, "include_tip": False},
        ).move_to(LEFT * 3.9 + DOWN * 0.35)
        points_data = [(0.7, 0.95), (1.2, 1.35), (1.8, 1.62), (2.4, 2.0), (3.1, 2.25), (3.7, 2.82), (4.4, 3.05), (5.2, 4.2)]
        points = VGroup(*[Dot(axes.c2p(x, y), radius=0.065, color=BLUE_NEON) for x, y in points_data])
        outlier = points[-1].copy().set_color(RED_NEON).scale(1.2)
        line_full = Line(axes.c2p(0.45, 0.75), axes.c2p(5.55, 4.05), color=GREEN_NEON, stroke_width=4)
        line_removed = Line(axes.c2p(0.45, 0.78), axes.c2p(5.55, 3.55), color=YELLOW_NEON, stroke_width=4)
        closed_form = MathTex(
            r"\theta^*(w)=\left(\sum_i w_i x_i x_i^\top\right)^{-1}\left(\sum_i w_i y_i x_i\right)",
            font_size=34,
            color=WHITE_SOFT,
        ).move_to(RIGHT * 3.2 + UP * 1.35)
        sm = VGroup(
            chip("remove one point", RED_NEON, 22, 3.4),
            make_label("rank-one update\nkhông cần retrain từ đầu", YELLOW_NEON, 24, BOLD),
        ).arrange(DOWN, buff=0.32).move_to(RIGHT * 3.55 + DOWN * 0.85)
        geom = make_label("influence = nghiệm hiện tại + geometry của data", GREEN_NEON, 25, BOLD).move_to(DOWN * 2.55)

        playt(t, Create(axes), FadeIn(points), run_time=1.0)
        playt(t, Create(line_full), run_time=0.9)
        playt(t, Transform(points[-1], outlier), run_time=0.6)
        playt(t, Write(closed_form), run_time=1.2)
        playt(t, Transform(line_full, line_removed), FadeIn(sm, shift=UP * 0.12), run_time=1.2)
        playt(t, FadeIn(geom, shift=UP * 0.12), run_time=0.8)
        fade_segment(t, AUDIO_DURATIONS[4], axes, points, line_full, closed_form, sm, geom)

        # ------------------------------------------------------------
        # p2_05 - Residual and leverage.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "Residual + leverage: loss cao chưa đủ", 39)
        base_line = Line(LEFT * 5.4 + DOWN * 0.4, RIGHT * 0.2 + UP * 1.0, color=GREEN_NEON, stroke_width=4)
        cloud = VGroup(*[
            Dot(LEFT * 4.8 + RIGHT * (i % 4) * 0.55 + UP * (0.65 - (i // 4) * 0.36), radius=0.055, color=BLUE_NEON)
            for i in range(12)
        ])
        residual_point = Dot(LEFT * 2.1 + UP * 1.35, radius=0.085, color=RED_NEON)
        residual_drop = DashedLine(residual_point.get_center(), LEFT * 2.1 + UP * 0.48, color=RED_NEON, dash_length=0.08)
        edge_point = Dot(RIGHT * 4.35 + UP * 1.55, radius=0.085, color=YELLOW_NEON)
        leverage_line = Line(RIGHT * 1.65 + UP * 1.05, edge_point.get_center(), color=YELLOW_NEON, stroke_width=3)
        labels = VGroup(
            chip("residual: model đang sai bao nhiêu?", RED_NEON, 22, 5.85).move_to(LEFT * 3.35 + DOWN * 1.7),
            chip("leverage: vị trí nhạy đến đâu?", YELLOW_NEON, 22, 5.05).move_to(RIGHT * 3.25 + DOWN * 1.7),
        )
        influence = MathTex(
            r"\Delta_j \;\propto\; \text{residual}_j \times \text{leverage}_j",
            font_size=40,
            color=WHITE_SOFT,
        ).move_to(DOWN * 2.55)
        gradient_hessian = VGroup(
            make_label("gradient: hướng kéo", BLUE_NEON, 24, BOLD),
            make_label("Hessian: độ cong / độ cứng", PURPLE_NEON, 24, BOLD),
        ).arrange(RIGHT, buff=0.6).move_to(UP * 2.25)

        playt(t, Create(base_line), FadeIn(cloud), run_time=1.0)
        playt(t, FadeIn(residual_point), Create(residual_drop), FadeIn(labels[0]), run_time=1.0)
        playt(t, FadeIn(edge_point), Create(leverage_line), FadeIn(labels[1]), run_time=1.0)
        playt(t, Write(influence), run_time=1.0)
        playt(t, FadeIn(gradient_hessian, shift=DOWN * 0.12), run_time=0.8)
        fade_segment(t, AUDIO_DURATIONS[5], base_line, cloud, residual_point, residual_drop, edge_point, leverage_line, labels, influence, gradient_hessian)

        # ------------------------------------------------------------
        # p2_06 - Quadratic approximation.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "Quadratic approximation: nhìn gần loss landscape", 37)
        ax = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[0, 5, 1],
            x_length=6.2,
            y_length=3.45,
            axis_config={"color": GRAY_SOFT, "include_tip": False},
        ).move_to(LEFT * 3.35 + DOWN * 0.3)
        true_curve = ax.plot(lambda x: 0.075 * (x + 1.6) ** 4 + 0.18 * (x - 0.7) ** 2 + 0.35, x_range=[-3.0, 2.7], color=BLUE_NEON)
        quad_curve = ax.plot(lambda x: 0.42 * (x + 0.45) ** 2 + 0.55, x_range=[-2.15, 1.35], color=YELLOW_NEON)
        theta_star = Dot(ax.c2p(-0.45, 0.55), color=GREEN_NEON, radius=0.08)
        theta_new = Dot(ax.c2p(0.25, 0.73), color=RED_NEON, radius=0.08)
        quad_formula = MathTex(
            r"L_{-j}(\theta)\approx L_{-j}(\theta^*)+\nabla L^\top(\theta-\theta^*)+\frac{1}{2}(\theta-\theta^*)^\top H(\theta-\theta^*)",
            font_size=30,
            color=WHITE_SOFT,
        ).move_to(RIGHT * 3.0 + UP * 1.2)
        local = VGroup(
            chip("không có closed form", RED_NEON, 22, 3.7),
            chip("thay bằng parabol gần theta*", YELLOW_NEON, 22, 4.25),
            chip("dự đoán đáy mới", GREEN_NEON, 22, 3.55),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 3.65 + DOWN * 1.05)

        playt(t, Create(ax), Create(true_curve), run_time=1.0)
        playt(t, FadeIn(theta_star), FadeIn(local[0]), run_time=0.8)
        playt(t, Create(quad_curve), FadeIn(local[1]), run_time=1.0)
        playt(t, FadeIn(theta_new), FadeIn(local[2]), run_time=0.8)
        playt(t, Write(quad_formula), run_time=1.3)
        playt(t, theta_new.animate.scale(1.45), rate_func=there_and_back, run_time=0.9)
        fade_segment(t, AUDIO_DURATIONS[6], ax, true_curve, quad_curve, theta_star, theta_new, quad_formula, local)

        # ------------------------------------------------------------
        # p2_07 - Influence functions.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "Influence function: đạo hàm theo data weight", 38)
        opt = MathTex(
            r"\sum_{i=1}^{n} w_i\,\nabla_\theta \ell_i(\theta^*(w))=0",
            font_size=44,
            color=WHITE_SOFT,
        ).move_to(UP * 2.0)
        force_center = Dot(LEFT * 4.8 + UP * 0.05, radius=0.08, color=WHITE_SOFT)
        force_arrows = VGroup(
            Arrow(force_center.get_center(), force_center.get_center() + RIGHT * 1.0 + UP * 0.45, color=BLUE_NEON, buff=0),
            Arrow(force_center.get_center(), force_center.get_center() + LEFT * 0.75 + UP * 0.5, color=YELLOW_NEON, buff=0),
            Arrow(force_center.get_center(), force_center.get_center() + RIGHT * 0.1 + DOWN * 1.05, color=PURPLE_NEON, buff=0),
            Arrow(force_center.get_center(), force_center.get_center() + LEFT * 0.35 + DOWN * 0.25, color=GREEN_NEON, buff=0),
        )
        force_label = make_label("gradient forces cân bằng", GRAY_SOFT, 23, BOLD).move_to(LEFT * 4.75 + DOWN * 1.55)
        assumptions = VGroup(
            chip("smooth loss", BLUE_NEON, 20, 2.5),
            chip("strong convexity", YELLOW_NEON, 20, 3.25),
            chip("unique minimizer", GREEN_NEON, 20, 3.25),
            chip("invertible Hessian", PURPLE_NEON, 20, 3.35),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 4.2 + DOWN * 0.1)
        derivative = MathTex(
            r"\frac{d\theta^*(w)}{dw_j}=-H^{-1}\nabla_\theta\ell_j(\theta^*)",
            font_size=44,
            color=YELLOW_NEON,
        ).move_to(DOWN * 1.35)
        explain = VGroup(
            make_label("gradient_j: sample kéo theo hướng nào", BLUE_NEON, 23, BOLD),
            make_label("H^{-1}: loss landscape cho phép dịch bao nhiêu", PURPLE_NEON, 23, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(DOWN * 2.45)

        playt(t, Write(opt), run_time=1.2)
        playt(t, FadeIn(force_center), LaggedStart(*[GrowArrow(a) for a in force_arrows], lag_ratio=0.12), FadeIn(force_label), run_time=1.4)
        playt(t, LaggedStart(*[FadeIn(item, shift=LEFT * 0.12) for item in assumptions], lag_ratio=0.12), run_time=1.3)
        playt(t, Write(derivative), run_time=1.4)
        playt(t, FadeIn(explain, shift=UP * 0.12), run_time=0.9)
        playt(t, assumptions[1].animate.scale(1.08), assumptions[2].animate.scale(1.08), rate_func=there_and_back, run_time=1.0)
        fade_segment(t, AUDIO_DURATIONS[7], opt, force_center, force_arrows, force_label, assumptions, derivative, explain)

        # ------------------------------------------------------------
        # p2_08 - Parameter prediction to behavior prediction.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "Parameter prediction != behavior prediction", 39)
        train_point = chip("training point z_j", BLUE_NEON, 23, 3.6).move_to(LEFT * 5.55 + UP * 0.8)
        param = VGroup(
            rounded_box(3.2, 1.55, PURPLE_NEON, 0.045),
            make_label("parameter\nchange", PURPLE_NEON, 25, BOLD),
        ).move_to(LEFT * 0.9 + UP * 0.8)
        param[1].move_to(param[0])
        behavior = VGroup(
            rounded_box(3.5, 1.55, GREEN_NEON, 0.045),
            make_label("behavior\nchange", GREEN_NEON, 25, BOLD),
        ).move_to(RIGHT * 4.35 + UP * 0.8)
        behavior[1].move_to(behavior[0])
        chain = VGroup(
            Arrow(train_point.get_right(), param.get_left(), color=WHITE_SOFT, buff=0.22),
            Arrow(param.get_right(), behavior.get_left(), color=WHITE_SOFT, buff=0.22),
        )
        metrics = VGroup(
            chip("output", GREEN_NEON, 20, 2.2),
            chip("loss", YELLOW_NEON, 20, 2.2),
            chip("accuracy", BLUE_NEON, 20, 2.2),
            chip("fairness", PURPLE_NEON, 20, 2.2),
            chip("robustness", CYAN_SOFT, 20, 2.2),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 0.95)
        behavior_formula = MathTex(
            r"\Delta f_j \approx -\nabla_\theta f(\theta^*)^\top H^{-1}\nabla_\theta\ell_j(\theta^*)",
            font_size=40,
            color=YELLOW_NEON,
        ).move_to(DOWN * 2.45)
        question = make_label("Method đang dự đoán theta change hay behavior change?", RED_NEON, 27, BOLD).move_to(UP * 2.35)

        playt(t, FadeIn(train_point, shift=RIGHT * 0.12), FadeIn(param), FadeIn(behavior), run_time=1.0)
        playt(t, Create(chain[0]), run_time=0.7)
        playt(t, Create(chain[1]), run_time=0.7)
        playt(t, FadeIn(metrics, shift=UP * 0.12), run_time=0.9)
        playt(t, Write(behavior_formula), run_time=1.3)
        playt(t, FadeIn(question, shift=DOWN * 0.12), run_time=0.8)
        playt(t, behavior.animate.scale(1.08), rate_func=there_and_back, run_time=1.0)
        fade_segment(t, AUDIO_DURATIONS[8], train_point, param, behavior, chain, metrics, behavior_formula, question)

        # ------------------------------------------------------------
        # p2_09 - IF fragility for DNNs.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "Khi nào influence function dễ gãy?", 40)
        checklist = VGroup(
            chip("differentiable loss", BLUE_NEON, 21, 3.55),
            chip("strong convexity", YELLOW_NEON, 21, 3.55),
            chip("unique minimizer", GREEN_NEON, 21, 3.55),
            chip("converged training", PURPLE_NEON, 21, 3.55),
            chip("stable Hessian", CYAN_SOFT, 21, 3.55),
            chip("small perturbation", ORANGE, 21, 3.55),
        ).arrange(DOWN, buff=0.18).move_to(LEFT * 4.85 + DOWN * 0.05)
        dnn_box = VGroup(
            rounded_box(4.4, 3.55, RED_NEON, 0.035, 2),
            neural_net(WHITE_SOFT).scale(0.95),
            make_label("DNN training", RED_NEON, 27, BOLD),
        ).move_to(RIGHT * 3.55 + UP * 0.05)
        dnn_box[1].move_to(dnn_box[0].get_center() + DOWN * 0.02)
        dnn_box[2].next_to(dnn_box[0], DOWN, buff=0.22)
        break_tag = chip("assumptions break", RED_NEON, 19, 3.15).move_to(dnn_box[0].get_top() + DOWN * 0.34)
        warnings = VGroup(
            make_label("non-convex", RED_NEON, 23, BOLD),
            make_label("random seed", RED_NEON, 23, BOLD),
            make_label("non-convergence", RED_NEON, 23, BOLD),
            make_label("Hessian khó xử lý", RED_NEON, 23, BOLD),
        ).arrange(RIGHT, buff=0.32).move_to(DOWN * 2.55)
        caution = make_label("IF là baseline mạnh, không phải bằng chứng cuối cùng.", YELLOW_NEON, 28, BOLD).move_to(UP * 2.35)

        playt(t, LaggedStart(*[FadeIn(item, shift=RIGHT * 0.12) for item in checklist], lag_ratio=0.08), run_time=1.4)
        playt(t, FadeIn(dnn_box, shift=LEFT * 0.12), run_time=1.0)
        playt(t, FadeIn(break_tag, shift=DOWN * 0.08), dnn_box[0].animate.set_stroke(RED_NEON, width=4), run_time=0.9)
        playt(t, dnn_box.animate.shift(LEFT * 0.07), break_tag.animate.shift(LEFT * 0.07), rate_func=there_and_back, run_time=0.6)
        playt(t, FadeIn(warnings, shift=UP * 0.12), run_time=0.9)
        playt(t, FadeIn(caution, shift=DOWN * 0.12), run_time=0.8)
        fade_segment(t, AUDIO_DURATIONS[9], checklist, dnn_box, break_tag, warnings, caution)

        # ------------------------------------------------------------
        # p2_10 - Datamodel supervised learning.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "Datamodel: học map từ subset sang behavior", 39)
        rows = [
            [1, 0, 1, 1, 0, 1, 0, 1],
            [1, 1, 0, 1, 1, 0, 0, 1],
            [0, 1, 1, 0, 1, 1, 1, 0],
            [1, 0, 0, 1, 0, 1, 1, 1],
        ]
        subset_rows = VGroup(*[bit_row(row, GREEN_NEON, side=0.28, buff=0.04) for row in rows]).arrange(DOWN, buff=0.18)
        subset_rows.move_to(LEFT * 5.1 + UP * 0.65)
        subset_label = make_label("subset indicators", GREEN_NEON, 23, BOLD).next_to(subset_rows, UP, buff=0.28)
        behaviors = VGroup(
            make_label("0.82", YELLOW_NEON, 23, BOLD),
            make_label("0.76", YELLOW_NEON, 23, BOLD),
            make_label("0.68", YELLOW_NEON, 23, BOLD),
            make_label("0.91", YELLOW_NEON, 23, BOLD),
        ).arrange(DOWN, buff=0.29).move_to(RIGHT * 5.2 + UP * 0.65)
        behavior_label = make_label("measured behavior", YELLOW_NEON, 23, BOLD).next_to(behaviors, UP, buff=0.28)
        surrogate = VGroup(
            rounded_box(3.65, 2.25, PURPLE_NEON, 0.045),
            neural_net(PURPLE_NEON).scale(0.72),
            make_label("surrogate\n/datamodel", PURPLE_NEON, 24, BOLD),
        ).move_to(ORIGIN + UP * 0.2)
        surrogate[1].move_to(surrogate[0].get_center() + UP * 0.12)
        surrogate[2].next_to(surrogate[0], DOWN, buff=0.2)
        flow = VGroup(
            Arrow(subset_rows.get_right(), surrogate[0].get_left(), color=WHITE_SOFT, buff=0.25),
            Arrow(surrogate[0].get_right(), behaviors.get_left(), color=WHITE_SOFT, buff=0.25),
        )
        supervised = make_label("Datamodeling = supervised learning trên counterfactual runs", BLUE_NEON, 27, BOLD)
        supervised.move_to(DOWN * 2.55)

        playt(t, FadeIn(subset_rows), FadeIn(subset_label), run_time=0.9)
        playt(t, Create(flow[0]), FadeIn(surrogate, shift=LEFT * 0.12), run_time=1.0)
        playt(t, Create(flow[1]), FadeIn(behaviors), FadeIn(behavior_label), run_time=1.0)
        playt(t, FadeIn(supervised, shift=UP * 0.12), run_time=0.8)
        playt(t, subset_rows[1].animate.scale(1.08), behaviors[1].animate.scale(1.18), rate_func=there_and_back, run_time=1.1)
        fade_segment(t, AUDIO_DURATIONS[10], subset_rows, subset_label, behaviors, behavior_label, surrogate, flow, supervised)

        # ------------------------------------------------------------
        # p2_11 - Linear datamodel and evaluation.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "Linear datamodel: coefficient thành attribution", 38)
        linear_formula = MathTex(
            r"\hat f_\beta(m)=\beta_0+\sum_i m_i\tau_i",
            font_size=46,
            color=WHITE_SOFT,
        ).move_to(UP * 2.0)
        coef_bars = VGroup()
        coefs = [0.18, -0.06, 0.24, 0.04, -0.13, 0.16, 0.08, -0.03]
        for idx, value in enumerate(coefs):
            color = GREEN_NEON if value >= 0 else RED_NEON
            bg = Line(DOWN * 0.8, UP * 0.8, color=GRAY_SOFT, stroke_width=2, stroke_opacity=0.5)
            fg = Line(ORIGIN, UP * (value * 4.0) if value >= 0 else DOWN * (abs(value) * 4.0), color=color, stroke_width=10)
            val = make_label(f"{value:+.2f}", color, 15, BOLD)
            lab = make_label(f"z{idx + 1}", WHITE_SOFT, 15, BOLD)
            coef_bars.add(VGroup(VGroup(bg, fg), val, lab).arrange(DOWN, buff=0.08))
        coef_bars.arrange(RIGHT, aligned_edge=DOWN, buff=0.26).move_to(LEFT * 4.75 + DOWN * 0.6)
        coef_label = make_label("tau_i = attribution coefficient", YELLOW_NEON, 24, BOLD).next_to(coef_bars, UP, buff=0.3)
        scatter_frame = rounded_box(4.25, 3.1, BLUE_NEON, 0.025).move_to(RIGHT * 3.8 + DOWN * 0.2)
        scatter_axes = VGroup(
            Line(scatter_frame.get_left() + RIGHT * 0.45 + DOWN * 1.1, scatter_frame.get_left() + RIGHT * 0.45 + UP * 1.1, color=GRAY_SOFT, stroke_width=2),
            Line(scatter_frame.get_left() + RIGHT * 0.45 + DOWN * 1.1, scatter_frame.get_right() + LEFT * 0.35 + DOWN * 1.1, color=GRAY_SOFT, stroke_width=2),
        )
        scatter_points = VGroup()
        for x, y in [(0.2, 0.25), (0.45, 0.52), (0.7, 0.64), (0.95, 0.93), (1.15, 1.05), (1.45, 1.36), (1.7, 1.55), (2.0, 1.92)]:
            scatter_points.add(Dot(scatter_axes[1].get_start() + RIGHT * x + UP * y, radius=0.055, color=GREEN_NEON))
        diag = Line(scatter_axes[1].get_start(), scatter_frame.get_right() + LEFT * 0.5 + UP * 0.95, color=YELLOW_NEON, stroke_width=3)
        rho = make_label("predicted vs actual\nrho cao -> score đáng tin hơn", BLUE_NEON, 22, BOLD).next_to(scatter_frame, DOWN, buff=0.24)
        eval_note = chip("hold-out test", GREEN_NEON, 20, 2.85).move_to(RIGHT * 4.15 + UP * 1.55)

        playt(t, Write(linear_formula), run_time=1.0)
        playt(t, FadeIn(coef_label), FadeIn(coef_bars, shift=UP * 0.12), run_time=1.1)
        playt(t, Create(scatter_frame), Create(scatter_axes), run_time=0.8)
        playt(t, LaggedStart(*[FadeIn(point) for point in scatter_points], lag_ratio=0.05), Create(diag), run_time=1.2)
        playt(t, FadeIn(rho, shift=UP * 0.1), FadeIn(eval_note, shift=UP * 0.1), run_time=1.0)
        playt(t, scatter_points.animate.set_color(CYAN_SOFT), rate_func=there_and_back, run_time=0.9)
        fade_segment(t, AUDIO_DURATIONS[11], linear_formula, coef_label, coef_bars, scatter_frame, scatter_axes, scatter_points, diag, rho, eval_note)

        # ------------------------------------------------------------
        # p2_12 - Recap and transition.
        # ------------------------------------------------------------
        t = tracker()
        retitle(t, title, "Takeaway Part II: score phải dự đoán được", 39)
        recap_items = [
            ("1", "statistical analog", BLUE_NEON),
            ("2", "weights -> M-estimation", GREEN_NEON),
            ("3", "LOO = counterfactual chuẩn", YELLOW_NEON),
            ("4", "IF cần giả định mạnh", RED_NEON),
            ("5", "datamodels predict behavior", PURPLE_NEON),
        ]
        recap = VGroup()
        for num, text, color in recap_items:
            num_circle = Circle(radius=0.28, color=color, stroke_width=2, fill_color=color, fill_opacity=0.16)
            num_label = make_label(num, color, 21, BOLD).move_to(num_circle)
            item_text = make_label(text, WHITE_SOFT, 24, BOLD)
            item = VGroup(VGroup(num_circle, num_label), item_text).arrange(RIGHT, buff=0.28)
            recap.add(item)
        recap.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(LEFT * 3.85 + DOWN * 0.15)
        predictive_test = boxed_label(
            "Nếu data thay đổi,\nbehavior có đổi như dự đoán không?",
            GREEN_NEON,
            27,
            6.35,
            2.35,
            0.045,
        ).move_to(RIGHT * 3.25 + UP * 0.25)
        part3 = boxed_label(
            "Part III: scaling + evaluation",
            CYAN_SOFT,
            27,
            5.95,
            1.25,
            0.045,
        ).move_to(RIGHT * 2.55 + DOWN * 2.25)
        bridge_arrow = Arrow(predictive_test.get_bottom(), part3.get_top(), color=CYAN_SOFT, buff=0.16)

        playt(t, LaggedStart(*[FadeIn(item, shift=RIGHT * 0.16) for item in recap], lag_ratio=0.1), run_time=1.5)
        playt(t, FadeIn(predictive_test, shift=LEFT * 0.12), run_time=1.0)
        playt(t, Create(bridge_arrow), FadeIn(part3, shift=UP * 0.12), run_time=1.0)
        playt(t, recap[3].animate.scale(1.06), predictive_test.animate.scale(1.05), rate_func=there_and_back, run_time=1.1)
        fade_segment(t, AUDIO_DURATIONS[12], recap, predictive_test, bridge_arrow, part3, run_time=0.85, extra=0.9)
        self.play(FadeOut(title), run_time=0.7)
