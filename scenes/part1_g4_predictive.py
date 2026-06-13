from manim import *

# ============================================================
# ICML Tutorial: Data Attribution at Scale
# Part I - Goi 4: Predictive Attribution
# Style: dark background, neon colors, 3Blue1Brown-inspired
# Audio is not embedded; sync voice manually in CapCut.
# ============================================================

config.background_color = "#171717"
config.frame_width = 16
config.frame_height = 9


BG = "#171717"
WHITE_SOFT = "#E8E8E8"
GRAY_SOFT = "#9A9A9A"
BLUE_NEON = "#4DA6FF"
GREEN_NEON = "#42F59B"
YELLOW_NEON = "#FFD166"
RED_NEON = "#FF5C5C"
PURPLE_NEON = "#B388FF"
CYAN_SOFT = "#64E9FF"


def make_title(text, font_size=44):
    return Text(text, font="Arial", font_size=font_size, weight=BOLD, color=WHITE_SOFT)


def make_label(text, color=WHITE_SOFT, font_size=26, weight=NORMAL):
    return Text(
        text,
        font="Arial",
        font_size=font_size,
        weight=weight,
        color=color,
        line_spacing=0.86,
    )


def rounded_box(width, height, color=BLUE_NEON, fill_opacity=0.07, stroke_width=2):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        color=color,
        stroke_width=stroke_width,
        fill_color=color,
        fill_opacity=fill_opacity,
    )


def chip(text, color=BLUE_NEON, font_size=22, pad_x=0.5, pad_y=0.25):
    text_obj = make_label(text, color, font_size, BOLD)
    frame = rounded_box(text_obj.width + pad_x, text_obj.height + pad_y, color, 0.055, 2)
    text_obj.move_to(frame)
    return VGroup(frame, text_obj)


def bit_grid(bits, active_color=BLUE_NEON, inactive_color=GRAY_SOFT, side=0.34):
    group = VGroup()
    for bit in bits:
        color = active_color if bit else inactive_color
        cell = Square(side_length=side, color=color, stroke_width=2)
        cell.set_fill(color, opacity=0.24 if bit else 0.06)
        label = make_label("1" if bit else "0", color, int(side * 42), BOLD).move_to(cell)
        group.add(VGroup(cell, label))
    group.arrange(RIGHT, buff=0.06)
    return group


def neural_net(width=1.7, height=2.0, color=WHITE_SOFT):
    layers = [3, 4, 3]
    x_positions = [-width / 2, 0, width / 2]
    nodes = []
    group = VGroup()
    for layer_idx, n_nodes in enumerate(layers):
        layer_nodes = []
        y_positions = [height / 2 - i * height / (n_nodes - 1) for i in range(n_nodes)]
        for y in y_positions:
            dot = Dot([x_positions[layer_idx], y, 0], radius=0.05, color=color)
            layer_nodes.append(dot)
            group.add(dot)
        nodes.append(layer_nodes)
    for layer_idx in range(len(nodes) - 1):
        for a in nodes[layer_idx]:
            for b in nodes[layer_idx + 1]:
                group.add(Line(a.get_center(), b.get_center(), color=color, stroke_width=1, stroke_opacity=0.4))
    return group


def metric_card(name, value, color=GREEN_NEON, width=3.65):
    frame = rounded_box(width, 1.0, color, 0.045)
    label = make_label(name, WHITE_SOFT, 21)
    number = make_label(value, color, 28, BOLD)
    content = VGroup(label, number).arrange(RIGHT, buff=0.28)
    if content.width > width - 0.35:
        content.scale_to_fit_width(width - 0.35)
    content.move_to(frame)
    return VGroup(frame, content)


def subset_row(bits, value, color=GREEN_NEON):
    vector = bit_grid(bits, side=0.3)
    arrow = Arrow(ORIGIN, RIGHT * 0.55, color=WHITE_SOFT, buff=0, stroke_width=3)
    metric = make_label(value, color, 21, BOLD)
    return VGroup(vector, arrow, metric).arrange(RIGHT, buff=0.24)


def knob(label, color):
    arc = Arc(radius=0.38, start_angle=215 * DEGREES, angle=250 * DEGREES, color=color, stroke_width=4)
    dot = Dot(arc.point_from_proportion(0.72), radius=0.055, color=color)
    text = make_label(label, color, 19, BOLD).next_to(arc, DOWN, buff=0.12)
    return VGroup(arc, dot, text)


def voice_wait(scene, seconds):
    scene.wait(seconds)


class PredictiveAttribution(Scene):
    def construct(self):
        self.camera.background_color = BG

        # =====================================================
        # g4_00, 47.673s - Opening: from credit to what-if.
        # =====================================================
        title = make_title("Predictive Attribution", 50).to_edge(UP, buff=0.35)
        subtitle = make_label(
            "Nếu training data thay đổi, model behavior sẽ thay đổi thế nào?",
            GREEN_NEON,
            28,
            BOLD,
        ).next_to(title, DOWN, buff=0.22)

        credit = chip("credit chia thế nào?", YELLOW_NEON, 25).move_to(LEFT * 4.4 + UP * 0.7)
        predictive = chip("behavior sẽ đổi ra sao?", GREEN_NEON, 25).move_to(RIGHT * 4.4 + UP * 0.7)
        lens_arrow = Arrow(credit.get_right(), predictive.get_left(), color=WHITE_SOFT, buff=0.25)

        data_cloud = VGroup(*[Dot(radius=0.065, color=BLUE_NEON if i % 3 else GREEN_NEON) for i in range(30)])
        data_cloud.arrange_in_grid(rows=5, cols=6, buff=0.18).move_to(LEFT * 4.6 + DOWN * 1.0)
        model = VGroup(rounded_box(2.55, 1.45, PURPLE_NEON, 0.045), neural_net(color=WHITE_SOFT).scale(0.55)).move_to(ORIGIN + DOWN * 1.0)
        behavior = metric_card("accuracy", "0.82", GREEN_NEON, 3.1).move_to(RIGHT * 4.45 + DOWN * 1.0)
        flow = VGroup(
            Arrow(data_cloud.get_right(), model.get_left(), color=WHITE_SOFT, buff=0.25),
            Arrow(model.get_right(), behavior.get_left(), color=WHITE_SOFT, buff=0.25),
        )

        scenarios = VGroup(
            chip("remove subset", RED_NEON, 21),
            chip("add new data", BLUE_NEON, 21),
            chip("change weights", PURPLE_NEON, 21),
        ).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.55)
        controls = VGroup(knob("on/off", GREEN_NEON), knob("weight", YELLOW_NEON), knob("shift", RED_NEON))
        controls.arrange(RIGHT, buff=0.65).move_to(DOWN * 0.05)

        self.play(FadeIn(title, shift=UP * 0.18), FadeIn(subtitle), run_time=1.0)
        self.play(FadeIn(credit), Create(lens_arrow), FadeIn(predictive), run_time=1.0)
        self.play(FadeIn(data_cloud), FadeIn(model), Create(flow[0]), Create(flow[1]), FadeIn(behavior), run_time=1.0)
        self.play(behavior[1][1].animate.set_color(YELLOW_NEON).scale(1.12), rate_func=there_and_back, run_time=1.0)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in scenarios], lag_ratio=0.12), run_time=1.1)
        self.play(TransformFromCopy(scenarios, controls), run_time=1.0)
        self.play(FadeOut(credit), FadeOut(lens_arrow), predictive.animate.move_to(UP * 1.15), run_time=0.9)
        voice_wait(self, 39.87)
        self.play(FadeOut(VGroup(subtitle, predictive, data_cloud, model, behavior, flow, scenarios, controls)), run_time=0.8)

        # =====================================================
        # g4_01, 43.886s - Counterfactual question.
        # =====================================================
        counter_title = make_title("Counterfactual: một thế giới khác", 43).to_edge(UP, buff=0.35)
        self.play(Transform(title, counter_title), run_time=0.75)

        current = VGroup(
            rounded_box(4.25, 2.0, BLUE_NEON, 0.04),
            make_label("world A\ntraining data gốc", BLUE_NEON, 25, BOLD),
        ).move_to(LEFT * 4.3 + UP * 0.6)
        current[1].move_to(current[0])
        alternate = VGroup(
            rounded_box(4.25, 2.0, GREEN_NEON, 0.04),
            make_label("world B\nbỏ / thêm / reweight", GREEN_NEON, 25, BOLD),
        ).move_to(RIGHT * 4.3 + UP * 0.6)
        alternate[1].move_to(alternate[0])
        compare = Arrow(current.get_right(), alternate.get_left(), color=WHITE_SOFT, buff=0.3)

        retrains = VGroup()
        for label, color in [("keep all", BLUE_NEON), ("remove i", RED_NEON), ("remove subset", YELLOW_NEON), ("upweight group", PURPLE_NEON)]:
            retrains.add(chip(label, color, 20))
        retrains.arrange(RIGHT, buff=0.26).move_to(DOWN * 1.15)
        cost = VGroup(
            make_label("train lại model lớn nhiều lần", RED_NEON, 29, BOLD),
            make_label("quá đắt", RED_NEON, 36, BOLD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.55)
        surrogate_hint = chip("learn a surrogate for counterfactual behavior", GREEN_NEON, 23).move_to(DOWN * 2.55)

        self.play(FadeIn(current), FadeIn(alternate), Create(compare), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.08) for item in retrains], lag_ratio=0.12), run_time=1.2)
        self.play(retrains.animate.arrange(RIGHT, buff=0.18).scale(1.08), rate_func=there_and_back, run_time=1.2)
        self.play(FadeIn(cost, shift=UP * 0.12), run_time=1.0)
        self.play(Transform(cost[1], surrogate_hint), run_time=1.1)
        self.play(current.animate.set_opacity(0.55), alternate.animate.set_opacity(0.55), run_time=0.9)
        voice_wait(self, 35.94)
        self.play(FadeOut(VGroup(current, alternate, compare, retrains, cost)), run_time=0.8)

        # =====================================================
        # g4_02, 56.686s - Training subsets and indicators.
        # =====================================================
        subset_title = make_title("Training subsets -> observed behavior", 42).to_edge(UP, buff=0.35)
        self.play(Transform(title, subset_title), run_time=0.75)

        rows = VGroup(
            subset_row([1, 0, 1, 1, 0, 0, 1, 0], "accuracy = 0.82", GREEN_NEON),
            subset_row([0, 1, 1, 0, 1, 0, 1, 1], "accuracy = 0.76", YELLOW_NEON),
            subset_row([1, 1, 0, 0, 1, 1, 0, 0], "loss down, edge worse", RED_NEON),
            subset_row([0, 0, 1, 1, 1, 0, 0, 1], "robustness = 0.88", CYAN_SOFT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to(LEFT * 3.35 + DOWN * 0.1)
        indicator_note = chip("subset indicator: 1 = giữ, 0 = bỏ", BLUE_NEON, 24).next_to(rows, UP, buff=0.35)

        map_box = VGroup(
            rounded_box(4.25, 3.2, PURPLE_NEON, 0.035),
            make_label("learn a map\nsubset -> behavior", PURPLE_NEON, 27, BOLD),
        ).move_to(RIGHT * 4.25 + DOWN * 0.05)
        map_box[1].move_to(map_box[0].get_top() + DOWN * 0.75)
        dots = VGroup()
        dot_specs = [
            (-1.0, -0.85, BLUE_NEON),
            (-0.55, -0.2, GREEN_NEON),
            (-0.05, -0.62, RED_NEON),
            (0.55, -0.18, CYAN_SOFT),
            (1.0, -0.9, YELLOW_NEON),
        ]
        for x, y, color in dot_specs:
            dots.add(Dot(map_box.get_center() + RIGHT * x + UP * y, radius=0.07, color=color))
        map_arrow = Arrow(rows.get_right(), map_box.get_left(), color=WHITE_SOFT, buff=0.28)

        self.play(FadeIn(indicator_note), LaggedStart(*[FadeIn(row, shift=RIGHT * 0.12) for row in rows], lag_ratio=0.15), run_time=1.8)
        self.play(rows[0][0][0].animate.set_fill(GREEN_NEON, opacity=0.45), rows[1][0][0].animate.set_fill(RED_NEON, opacity=0.2), rate_func=there_and_back, run_time=1.0)
        self.play(LaggedStart(*[row[2].animate.scale(1.08) for row in rows], lag_ratio=0.1), rate_func=there_and_back, run_time=1.1)
        self.play(Create(map_arrow), FadeIn(map_box), LaggedStart(*[FadeIn(dot, scale=0.75) for dot in dots], lag_ratio=0.08), run_time=1.2)
        self.play(dots.animate.scale(1.12), rate_func=there_and_back, run_time=1.2)
        voice_wait(self, 48.84)
        self.play(FadeOut(VGroup(indicator_note, rows, map_arrow, map_box, dots)), run_time=0.8)

        # =====================================================
        # g4_03, 57.078s - Datamodel as surrogate.
        # =====================================================
        datamodel_title = make_title("Datamodel: surrogate cho counterfactual behavior", 40).to_edge(UP, buff=0.35)
        self.play(Transform(title, datamodel_title), run_time=0.75)

        subset = bit_grid([1, 1, 1, 1, 1, 1, 1, 1], side=0.42).move_to(LEFT * 5.0 + UP * 0.55)
        subset_label = make_label("subset indicator", BLUE_NEON, 24, BOLD).next_to(subset, DOWN, buff=0.22)
        datamodel = VGroup(
            rounded_box(3.4, 2.35, PURPLE_NEON, 0.045),
            neural_net(color=WHITE_SOFT).scale(0.78),
        ).move_to(ORIGIN + UP * 0.45)
        datamodel_label = make_label("datamodel", PURPLE_NEON, 26, BOLD).next_to(datamodel, DOWN, buff=0.22)
        prediction = metric_card("predicted behavior", "0.82", GREEN_NEON, 4.0).move_to(RIGHT * 5.0 + UP * 0.55)
        arrow_in = Arrow(subset.get_right(), datamodel.get_left(), color=WHITE_SOFT, buff=0.22)
        arrow_out = Arrow(datamodel.get_right(), prediction.get_left(), color=WHITE_SOFT, buff=0.22)
        formula = MathTex(r"g(\mathbf{1}_S)\approx \text{behavior}", font_size=40, color=YELLOW_NEON).move_to(DOWN * 2.5)

        toggled = subset.copy()
        toggled[3][0].set_fill(RED_NEON, opacity=0.35)
        toggled[3][1].become(make_label("0", RED_NEON, 18, BOLD).move_to(toggled[3][0]))
        toggled_label = chip("turn off data point i", RED_NEON, 21).next_to(toggled, UP, buff=0.28)
        new_prediction = metric_card("predicted behavior", "0.77", YELLOW_NEON, 4.0).move_to(prediction)
        diff = make_label("signal: 0.82 - 0.77 = +0.05", YELLOW_NEON, 28, BOLD).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(subset), FadeIn(subset_label), FadeIn(datamodel), FadeIn(datamodel_label), FadeIn(prediction), run_time=1.5)
        self.play(Create(arrow_in), Create(arrow_out), run_time=1.1)
        self.play(Write(formula), run_time=1.0)
        self.play(Transform(subset, toggled), FadeIn(toggled_label), run_time=1.2)
        self.play(Transform(prediction, new_prediction), run_time=1.2)
        self.play(FadeIn(diff, shift=UP * 0.12), run_time=1.0)
        voice_wait(self, 48.53)
        self.play(FadeOut(VGroup(subset, subset_label, toggled_label, datamodel, datamodel_label, prediction, arrow_in, arrow_out, formula, diff)), run_time=0.8)

        # =====================================================
        # g4_04, 53.864s - Attribution as sensitivity.
        # =====================================================
        sensitivity_title = make_title("Attribution = sensitivity với từng data point", 40).to_edge(UP, buff=0.35)
        self.play(Transform(title, sensitivity_title), run_time=0.75)

        base_vector = bit_grid([1, 1, 1, 1, 1, 1, 1, 1], GREEN_NEON, GRAY_SOFT, side=0.38).move_to(UP * 1.55)
        bars = VGroup()
        values = [0.10, -0.04, 0.16, 0.03, -0.11, 0.12, 0.05, -0.02]
        for idx, value in enumerate(values):
            color = GREEN_NEON if value >= 0 else RED_NEON
            bg = Line(DOWN * 0.9, UP * 0.9, color=GRAY_SOFT, stroke_width=2, stroke_opacity=0.45)
            zero = Dot(ORIGIN, radius=0.025, color=WHITE_SOFT, fill_opacity=0.65)
            fg_height = max(abs(value) * 10.0, 0.22)
            if value >= 0:
                fg = Line(ORIGIN, UP * fg_height, color=color, stroke_width=12)
            else:
                fg = Line(ORIGIN, DOWN * fg_height, color=color, stroke_width=12)
            label = make_label(f"d{idx + 1}", WHITE_SOFT, 16, BOLD)
            val = make_label(f"{value:+.2f}", color, 16, BOLD)
            meter = VGroup(bg, zero, fg)
            bar = VGroup(meter, val, label).arrange(DOWN, buff=0.08)
            bars.add(bar)
        bars.arrange(RIGHT, aligned_edge=DOWN, buff=0.34).move_to(DOWN * 0.65)
        behavior_choices = VGroup(
            chip("accuracy", GREEN_NEON, 21),
            chip("fairness", YELLOW_NEON, 21),
            chip("robustness", CYAN_SOFT, 21),
        ).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.62)
        toggle_note = chip("toggle one point -> prediction changes", PURPLE_NEON, 23).move_to(UP * 2.45)
        warning = make_label(
            "score chỉ có nghĩa khi ta biết behavior nào đang được đo",
            YELLOW_NEON,
            27,
            BOLD,
        ).next_to(behavior_choices, UP, buff=0.28)

        self.play(FadeIn(base_vector), FadeIn(toggle_note), run_time=1.0)
        self.play(
            LaggedStart(
                *[GrowFromEdge(bar[0][1], DOWN if values[i] >= 0 else UP) for i, bar in enumerate(bars)],
                lag_ratio=0.08,
            ),
            FadeIn(bars),
            run_time=1.4,
        )
        self.play(base_vector[2].animate.set_color(YELLOW_NEON), bars[2].animate.scale(1.12), rate_func=there_and_back, run_time=1.2)
        self.play(FadeIn(behavior_choices, shift=UP * 0.12), run_time=1.1)
        self.play(FadeIn(warning, shift=UP * 0.1), run_time=1.0)
        voice_wait(self, 46.61)
        self.play(FadeOut(VGroup(base_vector, toggle_note, bars, behavior_choices, warning)), run_time=0.8)

        # =====================================================
        # g4_05, 53.629s - Scale and evaluation.
        # =====================================================
        scale_title = make_title("Scale: amortize cost, rồi kiểm tra counterfactual", 38).to_edge(UP, buff=0.35)
        self.play(Transform(title, scale_title), run_time=0.75)

        expensive = VGroup(
            rounded_box(4.6, 2.15, RED_NEON, 0.045),
            make_label("train lại model\ncho mọi câu hỏi", RED_NEON, 27, BOLD),
            make_label("too expensive", RED_NEON, 28, BOLD),
        ).move_to(LEFT * 4.25 + UP * 0.8)
        expensive[1:].arrange(DOWN, buff=0.22).move_to(expensive[0])
        amortized = VGroup(
            rounded_box(4.6, 2.15, GREEN_NEON, 0.045),
            make_label("học datamodel\nmột lần", GREEN_NEON, 27, BOLD),
            make_label("answer many what-ifs", GREEN_NEON, 24, BOLD),
        ).move_to(RIGHT * 4.25 + UP * 0.8)
        amortized[1:].arrange(DOWN, buff=0.22).move_to(amortized[0])
        arrow = Arrow(expensive.get_right(), amortized.get_left(), color=WHITE_SOFT, buff=0.3)

        prediction_eval = VGroup(
            metric_card("datamodel predicts", "-5%", YELLOW_NEON, 3.8),
            metric_card("actual retrain", "0%", RED_NEON, 3.8),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.9)
        mismatch = make_label("score đẹp chưa đủ: phải predict đúng behavior chưa thấy", YELLOW_NEON, 27, BOLD).to_edge(DOWN, buff=0.58)

        path = VGroup(
            chip("theory", PURPLE_NEON, 21),
            chip("datamodels", GREEN_NEON, 21),
            chip("scaling", BLUE_NEON, 21),
            chip("evaluation", YELLOW_NEON, 21),
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 2.55)

        self.play(FadeIn(expensive, shift=UP * 0.12), FadeIn(amortized, shift=UP * 0.12), Create(arrow), run_time=1.2)
        self.play(amortized.animate.scale(1.06), rate_func=there_and_back, run_time=1.3)
        self.play(FadeIn(prediction_eval, shift=UP * 0.12), run_time=1.2)
        self.play(prediction_eval[0].animate.set_opacity(0.45), prediction_eval[1].animate.scale(1.08), rate_func=there_and_back, run_time=1.1)
        self.play(FadeIn(mismatch, shift=UP * 0.08), run_time=1.0)
        self.play(FadeIn(path), run_time=0.9)
        voice_wait(self, 45.38)
        self.play(FadeOut(VGroup(expensive, amortized, arrow, prediction_eval, mismatch, path)), run_time=0.8)

        # =====================================================
        # g4_06, 43.546s - Recap Part I and transition.
        # =====================================================
        recap_title = make_title("Ba lens chính của data attribution", 40).to_edge(UP, buff=0.35)
        self.play(Transform(title, recap_title), run_time=0.75)

        lens_cards = VGroup(
            VGroup(rounded_box(4.15, 1.65, BLUE_NEON, 0.045), make_label("Corroborative\nevidence nào?", BLUE_NEON, 24, BOLD)),
            VGroup(rounded_box(4.15, 1.65, YELLOW_NEON, 0.045), make_label("Game-theoretic\ncredit chia thế nào?", YELLOW_NEON, 24, BOLD)),
            VGroup(rounded_box(4.15, 1.65, GREEN_NEON, 0.045), make_label("Predictive\ncounterfactual gì?", GREEN_NEON, 24, BOLD)),
        )
        for card in lens_cards:
            card[1].move_to(card[0])
        lens_cards.arrange(RIGHT, buff=0.32).move_to(UP * 0.85)

        trio = VGroup(
            chip("evidence", BLUE_NEON, 22),
            chip("credit", YELLOW_NEON, 22),
            chip("counterfactual prediction", GREEN_NEON, 22),
        ).arrange(RIGHT, buff=0.45).move_to(DOWN * 0.85)

        part2 = VGroup(
            rounded_box(7.1, 1.35, PURPLE_NEON, 0.045),
            make_label("Tiếp theo: M-estimation, leave-one-out,\ninfluence functions, datamodels", PURPLE_NEON, 25, BOLD),
        ).to_edge(DOWN, buff=0.55)
        part2[1].move_to(part2[0])

        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in lens_cards], lag_ratio=0.14), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.1) for item in trio], lag_ratio=0.12), run_time=1.2)
        self.play(FadeIn(part2, shift=UP * 0.12), run_time=1.1)
        voice_wait(self, 38.45)
        self.play(FadeOut(VGroup(title, lens_cards, trio, part2)), run_time=1.0)
