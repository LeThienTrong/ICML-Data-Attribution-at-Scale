from manim import *

# ============================================================
# ICML Tutorial: Data Attribution at Scale
# Part I - Goi 3: Game-theoretic Attribution
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


def rounded_box(width, height, color=BLUE_NEON, fill_opacity=0.06, stroke_width=2):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        color=color,
        stroke_width=stroke_width,
        fill_color=color,
        fill_opacity=fill_opacity,
    )


def capsule_label(text, color, font_size=24, pad_x=0.55, pad_y=0.28):
    label = make_label(text, color, font_size, BOLD)
    frame = rounded_box(label.width + pad_x, label.height + pad_y, color, 0.055, 2.4)
    label.move_to(frame)
    return VGroup(frame, label)


def data_token(name, color=BLUE_NEON, radius=0.28):
    halo = Circle(radius=radius * 1.35, color=color, stroke_width=2, stroke_opacity=0.35)
    dot = Circle(radius=radius, color=color, stroke_width=3, fill_color=color, fill_opacity=0.12)
    label = make_label(name, WHITE_SOFT, 19, BOLD).move_to(dot)
    return VGroup(halo, dot, label)


def utility_meter(value=0.7, color=GREEN_NEON, label="utility v(S)", width=4.45):
    frame = rounded_box(width, 1.0, color, 0.035, 2)
    title_size = 23 if len(label) <= 12 else 20
    title = make_label(label, color, title_size, BOLD)
    pct = make_label(f"{int(value * 100)}%", color, 20, BOLD)
    bg = Rectangle(width=width * 0.36, height=0.18, stroke_width=0, fill_color=GRAY_SOFT, fill_opacity=0.28)

    row = VGroup(title, bg, pct).arrange(RIGHT, buff=0.22)
    if row.width > width - 0.34:
        row.scale_to_fit_width(width - 0.34)
    row.move_to(frame)

    fg = Rectangle(width=bg.width * value, height=bg.height, stroke_width=0, fill_color=color, fill_opacity=0.95)
    fg.move_to(bg).align_to(bg, LEFT)
    return VGroup(frame, title, bg, fg, pct)


def contribution_bar(name, value, color):
    value_label = make_label(f"{value:+.2f}", color, 21, BOLD)
    bar_bg = Rectangle(width=1.65, height=0.15, stroke_width=0, fill_color=GRAY_SOFT, fill_opacity=0.3)
    bar_fg = Rectangle(
        width=1.65 * min(abs(value) / 0.35, 1.0),
        height=0.15,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.9,
    )
    bar_fg.move_to(bar_bg).align_to(bar_bg, LEFT)
    name_label = make_label(name, WHITE_SOFT, 17, BOLD)
    VGroup(value_label, VGroup(bar_bg, bar_fg), name_label).arrange(DOWN, buff=0.12)
    return VGroup(value_label, bar_bg, bar_fg, name_label)


def voice_wait(scene, seconds):
    scene.wait(seconds)


class GameTheoreticAttribution(Scene):
    def construct(self):
        self.camera.background_color = BG

        # =====================================================
        # g3_00, 50.390s - Opening: evidence vs credit.
        # =====================================================
        title = make_title("Game-theoretic Attribution", 50).to_edge(UP, buff=0.35)
        subtitle = make_label("Từ câu hỏi evidence sang câu hỏi credit", YELLOW_NEON, 30, BOLD)
        subtitle.next_to(title, DOWN, buff=0.22)

        output = VGroup(
            rounded_box(3.4, 1.15, WHITE_SOFT, 0.035),
            make_label("model utility", WHITE_SOFT, 28, BOLD),
        ).move_to(RIGHT * 4.25 + UP * 0.15)
        output[1].move_to(output[0])

        coins = VGroup()
        coin_specs = [("d1", BLUE_NEON), ("d2", GREEN_NEON), ("d3", YELLOW_NEON), ("d4", PURPLE_NEON), ("d5", RED_NEON)]
        for name, color in coin_specs:
            coin = data_token(name, color, radius=0.24)
            coins.add(coin)
        coins.arrange_in_grid(rows=2, cols=3, buff=0.45).move_to(LEFT * 4.6 + UP * 0.1)
        arrow = Arrow(coins.get_right(), output.get_left(), color=WHITE_SOFT, buff=0.35)
        credit_line = make_label("ai đóng góp bao nhiêu?", YELLOW_NEON, 31, BOLD).to_edge(DOWN, buff=0.65)

        self.play(FadeIn(title, shift=UP * 0.18), FadeIn(subtitle), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(coin, scale=0.82) for coin in coins], lag_ratio=0.08), run_time=1.25)
        self.play(Create(arrow), FadeIn(output, shift=LEFT * 0.12), run_time=1.0)
        self.play(FadeIn(credit_line, shift=UP * 0.12), run_time=0.8)
        self.play(coins.animate.arrange(RIGHT, buff=0.28).move_to(LEFT * 3.95 + DOWN * 1.55), run_time=1.25)
        credit_shares = VGroup()
        for coin in coins:
            share = Dot(output.get_center(), radius=0.06, color=coin[1].get_color())
            credit_shares.add(share)
        self.play(
            LaggedStart(
                *[
                    share.animate.move_to(coin.get_top() + UP * 0.22)
                    for share, coin in zip(credit_shares, coins)
                ],
                lag_ratio=0.08,
            ),
            run_time=1.4,
        )
        self.play(FadeOut(credit_shares), run_time=0.35)
        voice_wait(self, 42.44)
        self.play(FadeOut(VGroup(subtitle, coins, output, arrow, credit_line)), run_time=0.9)

        # =====================================================
        # g3_01, 43.128s - Data as players and coalition value.
        # =====================================================
        players_title = make_title("Data point như người chơi trong một cooperative game", 39).to_edge(UP, buff=0.35)
        self.play(Transform(title, players_title), run_time=0.8)

        pool = VGroup(*[data_token(f"d{i+1}", color) for i, color in enumerate([BLUE_NEON, GREEN_NEON, YELLOW_NEON, PURPLE_NEON, RED_NEON, CYAN_SOFT])])
        pool.arrange(RIGHT, buff=0.32).move_to(LEFT * 4.0 + UP * 1.15)
        pool_label = capsule_label("players = data points", BLUE_NEON, 23).next_to(pool, UP, buff=0.35)

        table = rounded_box(5.25, 2.35, PURPLE_NEON, 0.04, 2.4).move_to(RIGHT * 3.45 + UP * 0.35)
        table_label = make_label("coalition S", PURPLE_NEON, 28, BOLD).next_to(table, UP, buff=0.24)
        utility = utility_meter(0.66, GREEN_NEON, width=4.75).move_to(RIGHT * 3.45 + DOWN * 2.0)

        selected = VGroup(pool[0].copy(), pool[2].copy(), pool[4].copy())
        selected.generate_target()
        selected.target.arrange(RIGHT, buff=0.42).move_to(table)
        movers = VGroup(
            CurvedArrow(
                pool[0].get_bottom() + DOWN * 0.12,
                table.get_left() + RIGHT * 1.15 + UP * 0.58,
                angle=-0.38,
                color=BLUE_NEON,
                stroke_width=4,
            ),
            CurvedArrow(
                pool[2].get_bottom() + DOWN * 0.12,
                table.get_center() + UP * 0.72,
                angle=-0.26,
                color=YELLOW_NEON,
                stroke_width=4,
            ),
            CurvedArrow(
                pool[4].get_bottom() + DOWN * 0.12,
                table.get_right() + LEFT * 1.15 + UP * 0.58,
                angle=-0.34,
                color=RED_NEON,
                stroke_width=4,
            ),
        )

        self.play(FadeIn(pool_label), LaggedStart(*[FadeIn(p, scale=0.82) for p in pool], lag_ratio=0.06), run_time=1.1)
        self.play(FadeIn(table), FadeIn(table_label), Create(movers), run_time=1.1)
        self.play(MoveToTarget(selected), FadeOut(movers), run_time=1.1)
        self.play(FadeIn(utility, shift=UP * 0.1), run_time=0.9)
        value_text = make_label("v(S): utility của coalition S", YELLOW_NEON, 29, BOLD).to_edge(DOWN, buff=0.72)
        self.play(Write(value_text), run_time=1.0)
        voice_wait(self, 36.23)
        self.play(FadeOut(VGroup(pool, pool_label, table, table_label, selected, utility, value_text)), run_time=0.9)

        # =====================================================
        # g3_02, 45.140s - Marginal contribution.
        # =====================================================
        marginal_title = make_title("Marginal contribution: credit phụ thuộc vào context", 39).to_edge(UP, buff=0.35)
        self.play(Transform(title, marginal_title), run_time=0.8)

        before_set = VGroup(data_token("d1", BLUE_NEON, 0.23), data_token("d3", YELLOW_NEON, 0.23))
        before_set.arrange(RIGHT, buff=0.34)
        before_frame = rounded_box(3.3, 1.45, BLUE_NEON, 0.04).move_to(LEFT * 4.75 + UP * 1.0)
        before_set.move_to(before_frame)
        before_label = make_label("coalition S", BLUE_NEON, 25, BOLD).next_to(before_frame, UP, buff=0.22)

        candidate = data_token("i", GREEN_NEON, 0.27).move_to(ORIGIN + UP * 1.0)
        after_set = VGroup(before_set.copy(), candidate.copy()).arrange(RIGHT, buff=0.26)
        after_frame = rounded_box(3.8, 1.45, GREEN_NEON, 0.04).move_to(RIGHT * 4.55 + UP * 1.0)
        after_set.move_to(after_frame)
        after_label = make_label("S + i", GREEN_NEON, 25, BOLD).next_to(after_frame, UP, buff=0.22)

        before_meter = utility_meter(0.54, BLUE_NEON, label="v(S)", width=3.75).move_to(LEFT * 3.75 + DOWN * 1.6)
        after_meter = utility_meter(0.78, GREEN_NEON, label="v(S+i)", width=4.25).move_to(RIGHT * 3.65 + DOWN * 1.6)
        formula = MathTex(r"\Delta_i(S)=v(S\cup\{i\})-v(S)", font_size=42, color=YELLOW_NEON).move_to(DOWN * 0.15)
        delta = make_label("+0.24", GREEN_NEON, 34, BOLD).next_to(formula, DOWN, buff=0.28)
        arrows = VGroup(
            Arrow(before_frame.get_right(), candidate.get_left(), color=WHITE_SOFT, buff=0.22),
            Arrow(candidate.get_right(), after_frame.get_left(), color=WHITE_SOFT, buff=0.22),
        )

        self.play(FadeIn(before_frame), FadeIn(before_set), FadeIn(before_label), FadeIn(before_meter), run_time=1.0)
        self.play(Create(arrows[0]), GrowFromCenter(candidate), run_time=0.8)
        self.play(Create(arrows[1]), FadeIn(after_frame), FadeIn(after_set), FadeIn(after_label), FadeIn(after_meter), run_time=1.0)
        self.play(Write(formula), FadeIn(delta, shift=UP * 0.1), run_time=1.1)
        self.play(after_meter[3].animate.set_fill(GREEN_NEON, opacity=1.0), delta.animate.scale(1.12), rate_func=there_and_back, run_time=1.0)
        voice_wait(self, 38.54)
        self.play(FadeOut(VGroup(before_frame, before_set, before_label, before_meter, candidate, after_frame, after_set, after_label, after_meter, formula, delta, arrows)), run_time=0.9)

        # =====================================================
        # g3_04, 41.979s - Context dependence.
        # =====================================================
        context_title = make_title("Cùng một data point, hai context khác nhau", 40).to_edge(UP, buff=0.35)
        self.play(Transform(title, context_title), run_time=0.8)

        sparse = rounded_box(5.35, 2.65, BLUE_NEON, 0.035).move_to(LEFT * 4.0 + UP * 0.35)
        redundant = rounded_box(5.35, 2.65, RED_NEON, 0.035).move_to(RIGHT * 4.0 + UP * 0.35)
        sparse_label = capsule_label("context A: ít data tương tự", BLUE_NEON, 23).next_to(sparse, UP, buff=0.24)
        redundant_label = capsule_label("context B: đã có nhiều data giống nhau", RED_NEON, 23).next_to(redundant, UP, buff=0.24)

        point_i_left = data_token("i", GREEN_NEON, 0.25).move_to(sparse.get_center() + LEFT * 1.55)
        point_i_right = data_token("i", GREEN_NEON, 0.25).move_to(redundant.get_center() + LEFT * 1.55)
        sparse_neighbors = VGroup(data_token("d1", BLUE_NEON, 0.2), data_token("d2", YELLOW_NEON, 0.2)).arrange(RIGHT, buff=0.28).move_to(sparse.get_center() + RIGHT * 1.2)
        redundant_neighbors = VGroup(*[data_token(f"d{k}", GRAY_SOFT, 0.18) for k in range(1, 6)])
        redundant_neighbors.arrange_in_grid(rows=2, cols=3, buff=0.18).move_to(redundant.get_center() + RIGHT * 1.25)

        high_bar = contribution_bar("delta i", 0.31, GREEN_NEON).move_to(LEFT * 4.0 + DOWN * 2.3)
        low_bar = contribution_bar("delta i", 0.05, RED_NEON).move_to(RIGHT * 4.0 + DOWN * 2.3)
        note = make_label(
            "credit không phải nhãn cố định của data point;\n"
            "nó phụ thuộc coalition xung quanh.",
            YELLOW_NEON,
            25,
            BOLD,
        )
        note.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(sparse), FadeIn(redundant), FadeIn(sparse_label), FadeIn(redundant_label), run_time=1.0)
        self.play(FadeIn(point_i_left, scale=0.85), FadeIn(point_i_right, scale=0.85), FadeIn(sparse_neighbors), FadeIn(redundant_neighbors), run_time=1.1)
        self.play(FadeIn(high_bar, shift=UP * 0.08), FadeIn(low_bar, shift=UP * 0.08), run_time=1.1)
        self.play(FadeIn(note, shift=UP * 0.12), run_time=0.8)
        self.play(point_i_left.animate.scale(1.18), point_i_right.animate.scale(0.92), rate_func=there_and_back, run_time=1.2)
        voice_wait(self, 35.08)
        self.play(FadeOut(VGroup(sparse, redundant, sparse_label, redundant_label, point_i_left, point_i_right, sparse_neighbors, redundant_neighbors, high_bar, low_bar, note)), run_time=0.9)

        # =====================================================
        # g3_05, 56.033s - Shapley value as average over orders.
        # =====================================================
        shapley_title = make_title("Shapley value: trung bình hóa nhiều thứ tự", 41).to_edge(UP, buff=0.35)
        self.play(Transform(title, shapley_title), run_time=0.8)

        order_rows = VGroup()
        i_tokens = VGroup()
        order_specs = [
            (["d2", "i", "d1", "d4"], 0.32, BLUE_NEON),
            (["d1", "d3", "i", "d4"], 0.14, GREEN_NEON),
            (["d4", "d2", "d3", "i"], 0.04, RED_NEON),
            (["i", "d1", "d2", "d3"], 0.38, YELLOW_NEON),
        ]
        for names, value, color in order_specs:
            tokens = VGroup()
            for name in names:
                token_color = GREEN_NEON if name == "i" else GRAY_SOFT
                token = capsule_label(name, token_color, font_size=20, pad_x=0.35, pad_y=0.2)
                tokens.add(token)
                if name == "i":
                    i_tokens.add(token)
            tokens.arrange(RIGHT, buff=0.12)
            bar_bg = Rectangle(width=1.85, height=0.16, stroke_width=0, fill_color=GRAY_SOFT, fill_opacity=0.24)
            bar_fg = Rectangle(width=1.85 * value / 0.4, height=0.16, stroke_width=0, fill_color=color, fill_opacity=0.9)
            bar_fg.move_to(bar_bg).align_to(bar_bg, LEFT)
            value_label = make_label(f"+{value:.2f}", color, 22, BOLD)
            row = VGroup(tokens, bar_bg, bar_fg, value_label).arrange(RIGHT, buff=0.34)
            order_rows.add(row)
        order_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(LEFT * 3.6 + DOWN * 0.15)

        average = VGroup(
            rounded_box(4.25, 2.25, YELLOW_NEON, 0.05),
            MathTex(r"\phi_i=\mathbb{E}_{\pi}[\Delta_i]", font_size=43, color=YELLOW_NEON),
            make_label("credit trung bình", WHITE_SOFT, 25, BOLD),
        )
        average[1:].arrange(DOWN, buff=0.22).move_to(average[0])
        average.move_to(RIGHT * 4.45 + DOWN * 0.1)
        avg_arrow = Arrow(order_rows.get_right(), average.get_left(), color=YELLOW_NEON, buff=0.26)

        self.play(LaggedStart(*[FadeIn(row[0], shift=RIGHT * 0.08) for row in order_rows], lag_ratio=0.1), run_time=1.1)
        self.play(LaggedStart(*[token.animate.scale(1.12) for token in i_tokens], lag_ratio=0.08), rate_func=there_and_back, run_time=1.1)
        self.play(LaggedStart(*[GrowFromEdge(row[2], LEFT) for row in order_rows], lag_ratio=0.1), FadeIn(VGroup(*[row[3] for row in order_rows])), run_time=1.1)
        self.play(Create(avg_arrow), FadeIn(average, shift=LEFT * 0.1), run_time=1.1)
        self.play(average[1].animate.scale(1.08), rate_func=there_and_back, run_time=1.0)
        voice_wait(self, 48.93)
        self.play(FadeOut(VGroup(order_rows, average, avg_arrow)), run_time=0.9)

        # =====================================================
        # g3_06, 32.601s - Scale and approximation.
        # =====================================================
        scale_title = make_title("Vấn đề: số coalition tăng quá nhanh", 42).to_edge(UP, buff=0.35)
        self.play(Transform(title, scale_title), run_time=0.8)

        left = VGroup(
            rounded_box(4.4, 1.5, GREEN_NEON, 0.045),
            make_label("n = 4", GREEN_NEON, 30, BOLD),
            MathTex(r"2^4=16", font_size=38, color=GREEN_NEON),
        )
        left[1:].arrange(DOWN, buff=0.1).move_to(left[0])
        left.move_to(LEFT * 4.55 + UP * 0.9)

        right = VGroup(
            rounded_box(4.4, 1.5, RED_NEON, 0.045),
            make_label("n = 10^6", RED_NEON, 30, BOLD),
            MathTex(r"2^n\ \text{coalitions}", font_size=38, color=RED_NEON),
        )
        right[1:].arrange(DOWN, buff=0.1).move_to(right[0])
        right.move_to(RIGHT * 4.55 + UP * 0.9)

        explosion = VGroup()
        for i in range(40):
            dot = Dot(radius=0.035, color=YELLOW_NEON if i % 5 == 0 else GRAY_SOFT)
            explosion.add(dot)
        explosion.arrange_in_grid(rows=5, cols=8, buff=0.13).move_to(DOWN * 0.55)
        sample_path = Arrow(LEFT * 4.0 + DOWN * 2.3, RIGHT * 4.0 + DOWN * 2.3, color=PURPLE_NEON, buff=0)
        sample_label = make_label("thực tế: sampling / approximation", PURPLE_NEON, 29, BOLD).next_to(sample_path, UP, buff=0.26)

        self.play(FadeIn(left, shift=UP * 0.12), run_time=0.8)
        self.play(FadeIn(right, shift=UP * 0.12), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(dot, scale=0.7) for dot in explosion], lag_ratio=0.01), run_time=1.0)
        self.play(Create(sample_path), FadeIn(sample_label), run_time=0.9)
        self.play(explosion.animate.scale(1.15).set_opacity(0.75), rate_func=there_and_back, run_time=1.2)
        voice_wait(self, 26.20)
        self.play(FadeOut(VGroup(left, right, explosion, sample_path, sample_label)), run_time=0.9)

        # =====================================================
        # g3_07, 34.691s - Recap and transition.
        # =====================================================
        recap_title = make_title("Tóm lại", 46).to_edge(UP, buff=0.35)
        self.play(Transform(title, recap_title), run_time=0.8)

        summary = VGroup(
            capsule_label("question: credit chia thế nào?", YELLOW_NEON, 25),
            capsule_label("tool: marginal contribution", GREEN_NEON, 25),
            capsule_label("ideal: Shapley value", PURPLE_NEON, 25),
            capsule_label("cost: cần approximation ở scale lớn", RED_NEON, 25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        summary.move_to(LEFT * 3.2 + DOWN * 0.05)

        next_box = VGroup(
            rounded_box(4.55, 2.0, GREEN_NEON, 0.045),
            make_label("Tiếp theo:\nPredictive Attribution", GREEN_NEON, 29, BOLD),
        ).move_to(RIGHT * 3.95 + DOWN * 0.05)
        next_box[1].move_to(next_box[0])
        next_arrow = Arrow(summary.get_right(), next_box.get_left(), color=WHITE_SOFT, buff=0.3)

        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT * 0.12) for item in summary], lag_ratio=0.12), run_time=1.2)
        self.play(Create(next_arrow), FadeIn(next_box, shift=LEFT * 0.12), run_time=1.0)
        voice_wait(self, 30.26)
        self.play(FadeOut(VGroup(title, summary, next_box, next_arrow)), run_time=1.0)
