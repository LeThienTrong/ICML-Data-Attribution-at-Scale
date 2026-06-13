from manim import *

# ============================================================
# ICML Tutorial: Data Attribution at Scale
# Part I - Gói 2: Corroborative Attribution
# Visual direction: 3Blue1Brown-inspired, but more kinetic than p1_g1.
# Voice target: ~150 seconds, synced to assets/audio/g2_*.mp3.
# ============================================================

config.background_color = "#171717"
config.frame_width = 16
config.frame_height = 9


# ---------- Color palette ----------
BG = "#171717"
WHITE_SOFT = "#E8E8E8"
GRAY_SOFT = "#9A9A9A"
BLUE_NEON = "#4DA6FF"
GREEN_NEON = "#42F59B"
YELLOW_NEON = "#FFD166"
RED_NEON = "#FF5C5C"
PURPLE_NEON = "#B388FF"
CYAN_SOFT = "#64E9FF"


# ---------- Helper functions ----------
def make_title(text, font_size=44):
    return Text(
        text,
        font="Arial",
        font_size=font_size,
        weight=BOLD,
        color=WHITE_SOFT,
    )


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


def doc_card(text, color=BLUE_NEON, width=2.55, height=0.88, font_size=20):
    frame = rounded_box(width, height, color, fill_opacity=0.05, stroke_width=2)
    text_obj = make_label(text, WHITE_SOFT, font_size)
    return VGroup(frame, text_obj)


def chip(text, color=BLUE_NEON, font_size=22):
    text_obj = make_label(text, color, font_size, BOLD)
    frame = rounded_box(text_obj.width + 0.55, text_obj.height + 0.28, color, 0.06, 2)
    return VGroup(frame, text_obj)


def neural_net(width=1.7, height=2.2, color=WHITE_SOFT):
    layers = [3, 4, 3]
    x_positions = [-width / 2, 0, width / 2]
    nodes = []
    group = VGroup()

    for layer_idx, n_nodes in enumerate(layers):
        layer_nodes = []
        y_positions = [
            height / 2 - i * height / (n_nodes - 1)
            for i in range(n_nodes)
        ]
        for y in y_positions:
            dot = Dot([x_positions[layer_idx], y, 0], radius=0.052, color=color)
            layer_nodes.append(dot)
            group.add(dot)
        nodes.append(layer_nodes)

    for layer_idx in range(len(nodes) - 1):
        for a in nodes[layer_idx]:
            for b in nodes[layer_idx + 1]:
                group.add(
                    Line(
                        a.get_center(),
                        b.get_center(),
                        color=color,
                        stroke_width=1,
                        stroke_opacity=0.42,
                    )
                )

    return group


def score_bar(name, value, color, width=3.15):
    label = make_label(name, WHITE_SOFT, 19)
    bg = Rectangle(
        width=width,
        height=0.19,
        stroke_width=0,
        fill_color=GRAY_SOFT,
        fill_opacity=0.24,
    )
    fg = Rectangle(
        width=width * value,
        height=0.19,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.95,
    )
    fg.align_to(bg, LEFT)
    pct = make_label(f"{int(value * 100)}%", color, 18, BOLD)
    row = VGroup(label, bg, pct).arrange(RIGHT, buff=0.22)
    fg.move_to(bg).align_to(bg, LEFT)
    return VGroup(row, fg)


def particle_stream(start, end, color=YELLOW_NEON, count=5):
    particles = VGroup(*[Dot(radius=0.05, color=color) for _ in range(count)])
    for dot in particles:
        dot.move_to(start)
    path = Line(start, end)
    return particles, [MoveAlongPath(dot, path) for dot in particles]


def voice_wait(scene, seconds):
    scene.wait(seconds)


class CorroborativeAttribution(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Schedule all narration at fixed timestamps. Calling add_sound
        # mid-scene can be unreliable with cached Manim renders.
        self.add_sound("assets/audio/g2_00_intro.mp3", time_offset=0.0)
        self.add_sound("assets/audio/g2_01_continue.mp3", time_offset=14.341)
        self.add_sound("assets/audio/g2_02_rest.mp3", time_offset=37.747)

        # =====================================================
        # 00:00-00:14.34 Voice: introduce the evidence question.
        # =====================================================
        title = make_title("Corroborative Attribution", 50).to_edge(UP, buff=0.35)
        lens = Circle(radius=0.86, color=BLUE_NEON, stroke_width=5).move_to(LEFT * 4.9)
        lens_glass = Circle(radius=0.52, color=BLUE_NEON, stroke_width=1.5, stroke_opacity=0.5).move_to(lens)
        handle = Line(lens.get_bottom() + RIGHT * 0.48, lens.get_bottom() + RIGHT * 1.18 + DOWN * 0.7,
                      color=BLUE_NEON, stroke_width=5)
        lens_group = VGroup(lens, lens_glass, handle)

        output = doc_card("output của model", YELLOW_NEON, 3.0, 1.05, 22)
        output.move_to(RIGHT * 3.7 + UP * 0.7)
        question = make_label(
            "Có bằng chứng nào trong dữ liệu cho output này không?",
            RED_NEON,
            31,
            BOLD,
        ).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.9)
        self.play(GrowFromCenter(lens_group), FadeIn(output, shift=LEFT * 0.2), run_time=1.1)
        self.play(lens_group.animate.move_to(output.get_left() + LEFT * 1.4), run_time=1.2)
        self.play(FadeIn(question, shift=UP * 0.12), run_time=0.7)
        voice_wait(self, 10.441)

        # =====================================================
        # 00:14.34-00:37.75 Voice: toy search through a corpus.
        # =====================================================
        toy_title = make_title("Tìm evidence, không tìm thủ phạm", 42).to_edge(UP, buff=0.35)
        self.play(Transform(title, toy_title), FadeOut(question), run_time=0.8)

        corpus = VGroup()
        corpus_texts = [
            "doc A: định nghĩa",
            "doc B: ví dụ gần giống",
            "doc C: nhiễu",
            "doc D: nguồn hỗ trợ",
            "doc E: không liên quan",
            "doc F: trích đoạn mạnh",
        ]
        for idx, text in enumerate(corpus_texts):
            color = BLUE_NEON if idx not in [2, 4] else GRAY_SOFT
            corpus.add(doc_card(text, color, 3.35, 0.62, 17))
        corpus.arrange(DOWN, buff=0.08).move_to(LEFT * 4.7 + DOWN * 0.15)

        output.generate_target()
        output.target.move_to(RIGHT * 4.4 + UP * 1.2)
        output.target.scale(0.95)
        output_label = make_label("claim / generation", YELLOW_NEON, 22)
        output_label.next_to(output.target, DOWN, buff=0.18)

        scanner = Line(corpus.get_left(), corpus.get_right(), color=YELLOW_NEON, stroke_width=4)
        scanner.move_to(corpus[0].get_center())
        scan_label = chip("scan corpus", YELLOW_NEON, 20).next_to(corpus, RIGHT, buff=0.55)

        self.play(MoveToTarget(output), FadeOut(lens_group), FadeIn(output_label), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(doc, shift=RIGHT * 0.12) for doc in corpus], lag_ratio=0.06), run_time=1.3)
        self.play(Create(scanner), FadeIn(scan_label), run_time=0.6)
        self.play(scanner.animate.move_to(corpus[5].get_center()), run_time=2.0)

        ev_d = corpus[3].copy()
        ev_f = corpus[5].copy()
        ev_d.generate_target()
        ev_f.generate_target()
        ev_d.target.move_to(RIGHT * 1.0 + DOWN * 0.15)
        ev_f.target.move_to(RIGHT * 1.0 + DOWN * 1.0)

        link_d = Arrow(ev_d.target.get_right(), output.get_left(), color=GREEN_NEON, buff=0.18)
        link_f = Arrow(ev_f.target.get_right(), output.get_left(), color=YELLOW_NEON, buff=0.18)
        evidence_tag = chip("evidence candidates", GREEN_NEON, 22)
        evidence_tag.next_to(VGroup(ev_d.target, ev_f.target), DOWN, buff=0.24)

        self.play(
            corpus[3].animate.set_color(GREEN_NEON),
            corpus[5].animate.set_color(YELLOW_NEON),
            FadeOut(scanner),
            FadeOut(scan_label),
            run_time=0.7,
        )
        self.play(MoveToTarget(ev_d), MoveToTarget(ev_f), run_time=1.0)
        self.play(Create(link_d), Create(link_f), FadeIn(evidence_tag), run_time=0.8)
        voice_wait(self, 14.606)

        self.play(FadeOut(VGroup(corpus, output, output_label, ev_d, ev_f, link_d, link_f, evidence_tag)), run_time=0.8)

        # =====================================================
        # 00:37.75-00:59.92 Voice: two motivations with one shared core.
        # =====================================================
        motivation_title = make_title("Hai use case rất thực tế", 44).to_edge(UP, buff=0.35)
        self.play(Transform(title, motivation_title), run_time=0.75)

        citation = VGroup(
            rounded_box(4.6, 2.0, BLUE_NEON, fill_opacity=0.05),
            make_label("Citation", BLUE_NEON, 30, BOLD),
            make_label("Câu trả lời cần\nnguồn hỗ trợ", WHITE_SOFT, 24),
        )
        citation[1:].arrange(DOWN, buff=0.24)
        citation[1:].move_to(citation[0])
        citation.move_to(LEFT * 4.15 + UP * 0.35)

        copyright_box = VGroup(
            rounded_box(4.6, 2.0, PURPLE_NEON, fill_opacity=0.05),
            make_label("Copyright detection", PURPLE_NEON, 28, BOLD),
            make_label("Output có quá giống\ndữ liệu gốc?", WHITE_SOFT, 24),
        )
        copyright_box[1:].arrange(DOWN, buff=0.24)
        copyright_box[1:].move_to(copyright_box[0])
        copyright_box.move_to(RIGHT * 4.15 + UP * 0.35)

        core = chip("output -> dữ liệu liên quan nhất", YELLOW_NEON, 28)
        core.to_edge(DOWN, buff=0.6)
        motivation_arrows = VGroup(
            Arrow(citation.get_bottom(), core.get_top() + LEFT * 1.6, color=BLUE_NEON, buff=0.15),
            Arrow(copyright_box.get_bottom(), core.get_top() + RIGHT * 1.6, color=PURPLE_NEON, buff=0.15),
        )

        self.play(FadeIn(citation, shift=UP * 0.18), run_time=0.8)
        self.play(FadeIn(copyright_box, shift=UP * 0.18), run_time=0.8)
        self.play(
            Create(motivation_arrows),
            FadeIn(core),
            run_time=1.0,
        )
        voice_wait(self, 18.021)
        self.play(FadeOut(VGroup(citation, copyright_box, core, motivation_arrows)), run_time=0.8)

        # =====================================================
        # 00:59.92-01:23.80 Voice: definition and score.
        # =====================================================
        definition_title = make_title("Định nghĩa bằng một score", 43).to_edge(UP, buff=0.35)
        self.play(Transform(title, definition_title), run_time=0.75)

        behavior = VGroup(
            rounded_box(3.45, 1.2, YELLOW_NEON, fill_opacity=0.06),
            make_label("output y", YELLOW_NEON, 27, BOLD),
        ).move_to(LEFT * 4.7 + UP * 0.7)
        similarity = VGroup(
            Circle(radius=0.78, color=CYAN_SOFT, stroke_width=4),
            make_label("s", CYAN_SOFT, 38, BOLD),
        ).move_to(ORIGIN + UP * 0.7)
        item = VGroup(
            rounded_box(3.45, 1.2, GREEN_NEON, fill_opacity=0.06),
            make_label("item z trong corpus", GREEN_NEON, 25, BOLD),
        ).move_to(RIGHT * 4.7 + UP * 0.7)

        formula = MathTex(
            r"a(z, x) = s\left(f_{\theta(S)}(x), z\right)",
            font_size=42,
            color=WHITE_SOFT,
        ).move_to(DOWN * 1.65)
        note = make_label("a cao nghĩa là z corroborate tốt cho output", GRAY_SOFT, 24)
        note.next_to(formula, DOWN, buff=0.22)
        definition_arrows = VGroup(
            Arrow(behavior.get_right(), similarity.get_left(), color=WHITE_SOFT, buff=0.2),
            Arrow(item.get_left(), similarity.get_right(), color=WHITE_SOFT, buff=0.2),
        )

        self.play(FadeIn(behavior), FadeIn(item), run_time=0.75)
        self.play(
            Create(definition_arrows),
            GrowFromCenter(similarity),
            run_time=1.0,
        )
        self.play(Write(formula), FadeIn(note), run_time=1.1)
        self.play(similarity.animate.scale(1.15).set_color(YELLOW_NEON), rate_func=there_and_back, run_time=0.9)
        voice_wait(self, 18.577)
        self.play(FadeOut(VGroup(behavior, similarity, item, definition_arrows, formula, note)), run_time=0.8)

        # =====================================================
        # 01:23.80-01:54.49 Voice: pipeline with particle flow and ranking.
        # =====================================================
        pipeline_title = make_title("Pipeline: train, generate, then search", 41).to_edge(UP, buff=0.35)
        self.play(Transform(title, pipeline_title), run_time=0.75)

        train_dots = VGroup()
        for i in range(16):
            color = BLUE_NEON if i in [2, 6, 10, 13] else GRAY_SOFT
            train_dots.add(Dot(radius=0.07, color=color))
        train_dots.arrange_in_grid(rows=4, cols=4, buff=0.24)
        train = VGroup(rounded_box(2.35, 1.72, BLUE_NEON, 0.035), train_dots).move_to(LEFT * 5.55 + UP * 0.65)
        train_label = make_label("train set S", BLUE_NEON, 22).next_to(train, DOWN, buff=0.18)

        model = VGroup(rounded_box(2.35, 2.08, GREEN_NEON, 0.04), neural_net(color=WHITE_SOFT).scale(0.92)).move_to(LEFT * 1.95 + UP * 0.65)
        model_label = make_label("model", GREEN_NEON, 22).next_to(model, DOWN, buff=0.18)

        out = doc_card("output y", YELLOW_NEON, 2.15, 0.8, 20).move_to(RIGHT * 1.4 + UP * 1.65)
        search_docs = VGroup(*[doc_card(f"z{i + 1}", PURPLE_NEON, 1.25, 0.48, 17) for i in range(5)])
        search_docs.arrange(DOWN, buff=0.09).move_to(RIGHT * 5.6 + UP * 0.8)
        search_label = make_label("search set", PURPLE_NEON, 21).next_to(search_docs, DOWN, buff=0.18)

        bars = VGroup(
            score_bar("z1", 0.34, GRAY_SOFT),
            score_bar("z2", 0.87, YELLOW_NEON),
            score_bar("z3", 0.51, BLUE_NEON),
            score_bar("z4", 0.76, GREEN_NEON),
            score_bar("z5", 0.18, GRAY_SOFT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        bars.move_to(RIGHT * 1.85 + DOWN * 1.55)
        rank_title = make_label("rank by score", YELLOW_NEON, 22, BOLD).next_to(bars, UP, buff=0.22)

        arrow_tm = Arrow(train.get_right(), model.get_left(), color=WHITE_SOFT, buff=0.22)
        arrow_mo = Arrow(model.get_right(), out.get_left(), color=WHITE_SOFT, buff=0.22)
        arrow_os = Arrow(out.get_right(), search_docs.get_left(), color=WHITE_SOFT, buff=0.22)

        p1, moves1 = particle_stream(train.get_right(), model.get_left(), BLUE_NEON, 5)
        p2, moves2 = particle_stream(model.get_right(), out.get_left(), GREEN_NEON, 5)
        p3, moves3 = particle_stream(out.get_right(), search_docs.get_left(), YELLOW_NEON, 5)

        self.play(FadeIn(train), FadeIn(train_label), run_time=0.7)
        self.play(Create(arrow_tm), FadeIn(p1), *moves1, FadeIn(model), FadeIn(model_label), run_time=1.15)
        self.play(FadeOut(p1), Create(arrow_mo), FadeIn(p2), *moves2, FadeIn(out), run_time=1.1)
        self.play(FadeOut(p2), Create(arrow_os), FadeIn(p3), *moves3, FadeIn(search_docs), FadeIn(search_label), run_time=1.1)
        bar_rows = VGroup(*[bar[0] for bar in bars])
        bar_fills = VGroup(*[bar[1] for bar in bars])
        self.play(FadeOut(p3), FadeIn(rank_title), FadeIn(bar_rows), run_time=0.5)
        self.play(
            LaggedStart(*[GrowFromEdge(fill, LEFT) for fill in bar_fills], lag_ratio=0.12),
            run_time=1.1,
        )

        winner_doc = SurroundingRectangle(search_docs[1], color=YELLOW_NEON, buff=0.08)
        winner_bar = SurroundingRectangle(bars[1], color=YELLOW_NEON, buff=0.06)
        runner_doc = SurroundingRectangle(search_docs[3], color=GREEN_NEON, buff=0.08)
        runner_bar = SurroundingRectangle(bars[3], color=GREEN_NEON, buff=0.06)
        winner_link = DashedLine(search_docs[1].get_left(), bars[1].get_right(), color=YELLOW_NEON, stroke_width=2)
        runner_link = DashedLine(search_docs[3].get_left(), bars[3].get_right(), color=GREEN_NEON, stroke_width=2)
        self.play(Create(winner_doc), Create(winner_bar), Create(winner_link), run_time=0.55)
        self.play(Create(runner_doc), Create(runner_bar), Create(runner_link), run_time=0.55)
        voice_wait(self, 22.399)
        self.play(
            FadeOut(VGroup(train, train_label, model, model_label, out, search_docs, search_label,
                           bars, rank_title, arrow_tm, arrow_mo, arrow_os, winner_doc, winner_bar,
                           runner_doc, runner_bar, winner_link, runner_link)),
            run_time=0.8,
        )

        # =====================================================
        # 01:54.49-02:16.67 Voice: embedding retrieval demo.
        # =====================================================
        retrieval_title = make_title("Ví dụ: Information Retrieval", 43).to_edge(UP, buff=0.35)
        self.play(Transform(title, retrieval_title), run_time=0.75)

        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6.2,
            y_length=3.8,
            background_line_style={"stroke_color": GRAY_SOFT, "stroke_opacity": 0.22, "stroke_width": 1},
            axis_config={"stroke_color": GRAY_SOFT, "stroke_opacity": 0.55, "stroke_width": 1.5},
        ).move_to(LEFT * 2.55 + DOWN * 0.15)
        plane_frame = rounded_box(6.55, 4.2, BLUE_NEON, 0.025, 1.5).move_to(plane)

        chunk_points = [
            (-2.2, 1.2), (-1.6, -0.6), (-0.8, 0.55),
            (0.7, -1.1), (1.55, 0.25), (2.05, 1.1),
        ]
        chunks = VGroup()
        for idx, (x, y) in enumerate(chunk_points):
            point = Dot(plane.c2p(x, y), radius=0.085, color=BLUE_NEON)
            label = make_label(f"z{idx + 1}", BLUE_NEON, 17).next_to(point, UP, buff=0.08)
            chunks.add(VGroup(point, label))

        out_point = Dot(plane.c2p(1.3, 0.45), radius=0.13, color=YELLOW_NEON)
        out_label = make_label("output", YELLOW_NEON, 20, BOLD).next_to(out_point, RIGHT, buff=0.12)
        rings = VGroup(
            Circle(radius=0.38, color=YELLOW_NEON, stroke_width=2, stroke_opacity=0.45).move_to(out_point),
            Circle(radius=0.74, color=YELLOW_NEON, stroke_width=2, stroke_opacity=0.25).move_to(out_point),
        )

        nearest_lines = VGroup(
            Line(out_point.get_center(), chunks[4][0].get_center(), color=YELLOW_NEON, stroke_width=3),
            Line(out_point.get_center(), chunks[5][0].get_center(), color=GREEN_NEON, stroke_width=3),
        )
        callout = VGroup(
            rounded_box(4.1, 2.2, YELLOW_NEON, 0.05),
            make_label("Top evidence", YELLOW_NEON, 29, BOLD),
            make_label("nearest chunks\ntrong embedding space", WHITE_SOFT, 24),
        )
        callout[1:].arrange(DOWN, buff=0.24)
        callout[1:].move_to(callout[0])
        callout.move_to(RIGHT * 4.7 + DOWN * 0.15)

        self.play(FadeIn(plane_frame), Create(plane), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in chunks], lag_ratio=0.08), run_time=1.0)
        self.play(FadeIn(out_point, scale=1.4), FadeIn(out_label), Create(rings), run_time=0.9)
        self.play(Create(nearest_lines), FadeIn(callout), chunks[4].animate.set_color(YELLOW_NEON), chunks[5].animate.set_color(GREEN_NEON), run_time=1.1)
        voice_wait(self, 16.721)
        self.play(FadeOut(VGroup(plane_frame, plane, chunks, out_point, out_label, rings, nearest_lines, callout)), run_time=0.8)

        # =====================================================
        # 02:16.67-02:30.31 Voice: limitation and transition.
        # =====================================================
        limit_title = make_title("Nhớ giới hạn", 44).to_edge(UP, buff=0.35)
        self.play(Transform(title, limit_title), run_time=0.75)

        evidence = VGroup(
            rounded_box(4.55, 1.65, BLUE_NEON, 0.055),
            make_label("evidence\nhỗ trợ output", BLUE_NEON, 28, BOLD),
        ).move_to(LEFT * 3.7 + UP * 0.25)
        causal = VGroup(
            rounded_box(4.55, 1.65, RED_NEON, 0.055),
            make_label("causal claim\nhoặc fair credit", RED_NEON, 28, BOLD),
        ).move_to(RIGHT * 3.7 + UP * 0.25)
        not_equal = MathTex(r"\neq", font_size=68, color=WHITE_SOFT).move_to(UP * 0.25)
        next_line = make_label(
            "Muốn phân bổ credit? Chuyển sang Game-theoretic Attribution.",
            YELLOW_NEON,
            30,
            BOLD,
        ).to_edge(DOWN, buff=0.58)

        self.play(FadeIn(evidence), run_time=0.65)
        self.play(FadeIn(causal), Write(not_equal), run_time=0.8)
        self.play(FadeIn(next_line), run_time=0.75)
        # Keep the final card on screen until after the narration finishes.
        # Without this small buffer, some editors trim the last audio tail on import.
        voice_wait(self, 10.75)
        self.play(FadeOut(VGroup(title, evidence, causal, not_equal, next_line)), run_time=1.0)
