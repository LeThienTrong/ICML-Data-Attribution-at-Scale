from manim import *

# ============================================================
# ICML Tutorial: Data Attribution at Scale
# Part I - Goi 1: Intro & Taxonomy
# Style: dark background, neon colors, 3Blue1Brown-inspired
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


def voice_wait(scene, seconds):
    scene.wait(seconds)


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


def neural_net(width=2.0, height=2.55, color=WHITE_SOFT):
    layers = [4, 5, 4, 2]
    x_positions = [-width / 2, -width / 6, width / 6, width / 2]
    nodes = []
    group = VGroup()

    for layer_idx, n_nodes in enumerate(layers):
        layer_nodes = []
        y_positions = [height / 2 - i * height / (n_nodes - 1) for i in range(n_nodes)]
        for y in y_positions:
            dot = Dot([x_positions[layer_idx], y, 0], radius=0.055, color=color)
            layer_nodes.append(dot)
            group.add(dot)
        nodes.append(layer_nodes)

    for layer_idx in range(len(nodes) - 1):
        for a in nodes[layer_idx]:
            for b in nodes[layer_idx + 1]:
                group.add(Line(a.get_center(), b.get_center(), color=color, stroke_width=1, stroke_opacity=0.34))

    return group


def data_cloud(rows=5, cols=7, active=None, color=BLUE_NEON, inactive=GRAY_SOFT, radius=0.065):
    active = set(active or [])
    dots = VGroup()
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            dot_color = color if idx in active else inactive
            dot = Dot(radius=radius, color=dot_color)
            dot.set_opacity(1.0 if idx in active else 0.48)
            dots.add(dot)
    dots.arrange_in_grid(rows=rows, cols=cols, buff=0.19)
    return dots


def mini_document(name, color=BLUE_NEON, width=1.25, height=1.55):
    page = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.045,
    )
    lines = VGroup()
    for i, w in enumerate([0.82, 0.62, 0.75]):
        line = Line(LEFT * w / 2, RIGHT * w / 2, color=color, stroke_width=2, stroke_opacity=0.8)
        line.move_to(page.get_center() + UP * (0.28 - i * 0.24))
        lines.add(line)
    label = make_label(name, color, 18, BOLD).next_to(page, DOWN, buff=0.12)
    return VGroup(page, lines, label)


def lens(label, color, radius=0.78):
    outer = Circle(radius=radius, color=color, stroke_width=4)
    inner = Circle(radius=radius * 0.62, color=color, stroke_width=1.5, stroke_opacity=0.42)
    glass = VGroup(outer, inner)
    text = make_label(label, color, 24, BOLD).next_to(glass, DOWN, buff=0.18)
    return VGroup(glass, text)


def capsule_label(text, color, font_size=24, pad_x=0.6, pad_y=0.3):
    label = make_label(text, color, font_size, BOLD)
    frame = rounded_box(
        label.width + pad_x,
        label.height + pad_y,
        color,
        fill_opacity=0.055,
        stroke_width=2.6,
    )
    label.move_to(frame)
    return VGroup(frame, label)


def pulse_ring(mobject, color, scale=1.35):
    ring = Circle(radius=max(mobject.width, mobject.height) / 2, color=color, stroke_width=3, stroke_opacity=0.7)
    ring.move_to(mobject)
    ring.generate_target()
    ring.target.scale(scale).set_stroke(opacity=0.0)
    return ring


class IntroTaxonomy(Scene):
    def construct(self):
        self.camera.background_color = BG

        # =====================================================
        # 00:00-01:05 Opening: data becomes behavior.
        # =====================================================
        title = make_title("Data Attribution ở quy mô lớn", 52).move_to(UP * 2.55)
        subtitle = make_label("Kết nối hành vi của model với dữ liệu huấn luyện", GRAY_SOFT, 29)
        subtitle.next_to(title, DOWN, buff=0.22)

        cloud = data_cloud(rows=6, cols=9, active={2, 8, 11, 18, 27, 33, 41, 49}, radius=0.06)
        cloud.move_to(LEFT * 5.2 + DOWN * 0.1)
        model_frame = rounded_box(2.55, 3.15, GREEN_NEON, 0.035)
        model = neural_net(color=WHITE_SOFT).move_to(model_frame)
        model_group = VGroup(model_frame, model).move_to(ORIGIN + DOWN * 0.05)

        output = VGroup(
            rounded_box(3.15, 1.28, YELLOW_NEON, 0.07),
            make_label("output y", YELLOW_NEON, 30, BOLD),
        ).move_to(RIGHT * 5.15 + UP * 0.15)
        output[1].move_to(output[0])

        flow1 = Arrow(cloud.get_right(), model_group.get_left(), color=WHITE_SOFT, buff=0.35)
        flow2 = Arrow(model_group.get_right(), output.get_left(), color=WHITE_SOFT, buff=0.35)

        self.play(FadeIn(title, shift=UP * 0.2), FadeIn(subtitle), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in cloud], lag_ratio=0.015), run_time=1.6)
        self.play(Create(flow1), FadeIn(model_group, shift=RIGHT * 0.15), run_time=1.3)
        self.play(Create(flow2), FadeIn(output, shift=RIGHT * 0.15), run_time=1.1)

        packets = VGroup(*[Dot(radius=0.055, color=BLUE_NEON) for _ in range(7)])
        path_a = Line(cloud.get_right() + RIGHT * 0.15, model_group.get_left() + LEFT * 0.15)
        for packet in packets:
            packet.move_to(path_a.get_start())
        self.play(
            LaggedStart(*[MoveAlongPath(packet, path_a) for packet in packets], lag_ratio=0.16),
            run_time=2.0,
            rate_func=linear,
        )
        self.play(FadeOut(packets), run_time=0.3)

        question_arrow = CurvedArrow(
            output.get_bottom() + DOWN * 0.1,
            cloud.get_bottom() + DOWN * 0.1,
            angle=-TAU / 4,
            color=RED_NEON,
            stroke_width=5,
        )
        question = make_label("Data nào giải thích hành vi này?", RED_NEON, 32, BOLD)
        question.to_edge(DOWN, buff=0.48)
        ring = pulse_ring(output[0], YELLOW_NEON)
        self.play(MoveToTarget(ring), Create(question_arrow), FadeIn(question), run_time=1.45)
        self.play(FadeOut(ring), run_time=0.25)
        voice_wait(self, 36.0)

        self.play(
            FadeOut(VGroup(subtitle, cloud, model_group, output, flow1, flow2, question_arrow, question)),
            title.animate.to_edge(UP, buff=0.35).scale(0.78),
            run_time=1.0,
        )

        # =====================================================
        # 01:05-01:58 Data, model, behavior as a loop.
        # =====================================================
        section_title = make_title("Không chỉ hỏi model đúng hay sai", 43).to_edge(UP, buff=0.35)
        self.play(Transform(title, section_title), run_time=0.8)

        data_pool = data_cloud(rows=5, cols=8, active={3, 6, 10, 14, 22, 25, 31, 36}, radius=0.07)
        data_pool.move_to(LEFT * 5.2 + UP * 0.55)
        model_frame = rounded_box(2.65, 2.85, GREEN_NEON, 0.035)
        model = neural_net(color=WHITE_SOFT).scale(0.88).move_to(model_frame)
        model_node = VGroup(model_frame, model).move_to(ORIGIN + UP * 0.35)
        behavior_dot = Dot(radius=0.38, color=YELLOW_NEON).move_to(RIGHT * 5.1 + UP * 0.65)
        behavior_label = make_label("behavior", YELLOW_NEON, 26, BOLD).next_to(behavior_dot, DOWN, buff=0.28)
        bad_case = make_label("test case sai", RED_NEON, 27, BOLD).move_to(RIGHT * 5.05 + DOWN * 1.15)

        arrows = VGroup(
            Arrow(data_pool.get_right(), model_node.get_left(), color=WHITE_SOFT, buff=0.35),
            Arrow(model_node.get_right(), behavior_dot.get_left(), color=WHITE_SOFT, buff=0.35),
            CurvedArrow(behavior_dot.get_bottom(), data_pool.get_bottom(), angle=-TAU / 5, color=RED_NEON, stroke_width=4),
        )
        labels = VGroup(
            make_label("training data", BLUE_NEON, 24, BOLD).next_to(data_pool, DOWN, buff=0.28),
            make_label("model", GREEN_NEON, 25, BOLD).next_to(model_node, DOWN, buff=0.25),
        )

        self.play(FadeIn(data_pool), FadeIn(labels[0]), run_time=1.0)
        self.play(Create(arrows[0]), FadeIn(model_node), FadeIn(labels[1]), run_time=1.1)
        self.play(Create(arrows[1]), GrowFromCenter(behavior_dot), FadeIn(behavior_label), run_time=0.9)
        self.play(behavior_dot.animate.set_color(RED_NEON), FadeIn(bad_case, shift=UP * 0.1), run_time=0.9)
        self.play(Create(arrows[2]), run_time=1.1)

        suspicious = VGroup(data_pool[3], data_pool[10], data_pool[25]).copy()
        suspicious.generate_target()
        suspicious.target.arrange(RIGHT, buff=0.28).move_to(DOWN * 2.25)
        suspect_label = make_label("ta muốn truy ngược về dữ liệu", RED_NEON, 28, BOLD).next_to(suspicious.target, DOWN, buff=0.28)
        self.play(MoveToTarget(suspicious), FadeIn(suspect_label), run_time=1.2)
        voice_wait(self, 29.9)

        self.play(FadeOut(VGroup(data_pool, model_node, behavior_dot, behavior_label, bad_case, arrows, labels, suspicious, suspect_label)), run_time=0.9)

        # =====================================================
        # 01:58-03:04 Main goals without bullet pages.
        # =====================================================
        goals_title = make_title("Bốn việc video này sẽ làm", 42).to_edge(UP, buff=0.35)
        self.play(Transform(title, goals_title), run_time=0.8)

        compass = Circle(radius=1.05, color=WHITE_SOFT, stroke_width=2, stroke_opacity=0.65).move_to(ORIGIN)
        needle = Line(ORIGIN, UP * 0.82, color=YELLOW_NEON, stroke_width=5).move_to(compass)
        center_label = make_label("attribution", WHITE_SOFT, 25, BOLD).move_to(compass)

        goal_specs = [
            ("khái niệm", BLUE_NEON, LEFT * 4.6 + UP * 1.7),
            ("taxonomy", GREEN_NEON, RIGHT * 4.55 + UP * 1.7),
            ("theory", YELLOW_NEON, LEFT * 4.5 + DOWN * 1.65),
            ("scale & app", RED_NEON, RIGHT * 4.55 + DOWN * 1.65),
        ]
        goals = VGroup()
        rays = VGroup()
        for text, color, pos in goal_specs:
            node = capsule_label(text, color, font_size=25, pad_x=0.7, pad_y=0.38).move_to(pos)
            ray = Line(compass.get_center(), node.get_center(), color=color, stroke_width=2.5, stroke_opacity=0.55)
            goals.add(node)
            rays.add(ray)

        self.play(Create(compass), GrowFromCenter(needle), FadeIn(center_label), run_time=1.0)
        for idx, node in enumerate(goals):
            self.play(Create(rays[idx]), FadeIn(node, scale=0.86), Rotate(needle, angle=PI / 2, about_point=compass.get_center()), run_time=0.85)
        orbit = Circle(radius=2.3, color=GRAY_SOFT, stroke_width=1.5, stroke_opacity=0.25).move_to(compass)
        tracer = Dot(radius=0.08, color=CYAN_SOFT).move_to(orbit.point_from_proportion(0))
        self.play(Create(orbit), MoveAlongPath(tracer, orbit), run_time=3.0, rate_func=linear)
        voice_wait(self, 37.4)
        self.play(FadeOut(VGroup(compass, needle, center_label, goals, rays, orbit, tracer)), run_time=0.9)

        # =====================================================
        # 03:04-04:12 Roadmap as a moving path.
        # =====================================================
        roadmap_title = make_title("Lộ trình: từ câu hỏi đến ứng dụng", 42).to_edge(UP, buff=0.35)
        self.play(Transform(title, roadmap_title), run_time=0.8)

        path_points = [
            LEFT * 5.7 + DOWN * 1.3,
            LEFT * 2.2 + UP * 1.3,
            RIGHT * 1.8 + DOWN * 0.35,
            RIGHT * 5.45 + UP * 1.3,
        ]
        path = VMobject(color=GRAY_SOFT, stroke_width=4, stroke_opacity=0.55)
        path.set_points_smoothly(path_points)
        stop_specs = [
            ("I", "taxonomy", BLUE_NEON),
            ("II", "theory", GREEN_NEON),
            ("III", "scaling", YELLOW_NEON),
            ("IV", "applications", RED_NEON),
        ]
        stops = VGroup()
        for point, (roman, label, color) in zip(path_points, stop_specs):
            stop = VGroup(
                Circle(radius=0.46, color=color, stroke_width=3, fill_color=color, fill_opacity=0.06),
                make_label(roman, color, 26, BOLD),
                make_label(label, WHITE_SOFT, 23, BOLD),
            )
            stop[1].move_to(stop[0])
            stop[2].next_to(stop[0], DOWN, buff=0.2)
            stop.move_to(point)
            stops.add(stop)

        traveler = Dot(radius=0.13, color=CYAN_SOFT).move_to(path_points[0])
        self.play(Create(path), run_time=1.1)
        self.play(FadeIn(stops[0], scale=0.8), run_time=0.5)
        for idx in range(1, len(stops)):
            segment = Line(path_points[idx - 1], path_points[idx])
            self.play(MoveAlongPath(traveler, segment), FadeIn(stops[idx], scale=0.82), run_time=1.35)

        focus = Circle(radius=0.72, color=BLUE_NEON, stroke_width=4).move_to(stops[0][0])
        now = make_label("bắt đầu bằng Part I", BLUE_NEON, 29, BOLD).to_edge(DOWN, buff=0.55)
        self.play(Create(focus), FadeIn(now, shift=UP * 0.12), run_time=0.9)
        self.play(focus.animate.scale(1.16).set_stroke(opacity=0.25), rate_func=there_and_back, run_time=1.0)
        voice_wait(self, 39.1)
        self.play(FadeOut(VGroup(path, stops, traveler, focus, now)), run_time=0.9)

        # =====================================================
        # 04:12-05:15 Data problems orbiting the same model.
        # =====================================================
        problems_title = make_title("Rất nhiều bài toán, cùng một cấu trúc", 38).to_edge(UP, buff=0.35)
        self.play(Transform(title, problems_title), run_time=0.8)

        core_frame = rounded_box(2.55, 2.8, GREEN_NEON, 0.035)
        core_model = neural_net(color=WHITE_SOFT).scale(0.88).move_to(core_frame)
        core = VGroup(core_frame, core_model).move_to(ORIGIN + DOWN * 0.05)
        core_label = make_label("model behavior", GREEN_NEON, 25, BOLD).next_to(core, DOWN, buff=0.24)

        problem_specs = [
            ("debug", RED_NEON, RIGHT * 4.75 + UP * 1.55),
            ("trust", GREEN_NEON, RIGHT * 1.7 + UP * 2.05),
            ("select", BLUE_NEON, LEFT * 4.75 + UP * 1.15),
            ("pay", YELLOW_NEON, LEFT * 4.9 + DOWN * 1.35),
            ("copyright", PURPLE_NEON, LEFT * 1.9 + DOWN * 2.05),
            ("attack", RED_NEON, RIGHT * 4.45 + DOWN * 1.25),
        ]
        orbit = Ellipse(width=11.4, height=4.9, color=GRAY_SOFT, stroke_width=1.5, stroke_opacity=0.22)
        problem_nodes = VGroup()
        beams = VGroup()
        for text, color, pos in problem_specs:
            node = capsule_label(text, color, font_size=21, pad_x=0.48, pad_y=0.32).move_to(pos)
            beam = Line(node.get_center(), core.get_center(), color=color, stroke_width=2, stroke_opacity=0.42)
            problem_nodes.add(node)
            beams.add(beam)

        self.play(FadeIn(core), FadeIn(core_label), Create(orbit), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(node, scale=0.82) for node in problem_nodes], lag_ratio=0.08), run_time=1.2)
        self.play(LaggedStart(*[Create(beam) for beam in beams], lag_ratio=0.08), run_time=1.1)
        self.play(
            LaggedStart(
                *[node.animate.scale(1.06).set_stroke(opacity=0.95) for node in problem_nodes],
                lag_ratio=0.08,
            ),
            run_time=1.4,
            rate_func=there_and_back,
        )
        common = make_label("behavior của model  →  dữ liệu liên quan", YELLOW_NEON, 27, BOLD)
        common.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(common, shift=UP * 0.12), run_time=0.8)
        voice_wait(self, 36.5)
        self.play(FadeOut(VGroup(core, core_label, orbit, problem_nodes, beams, common)), run_time=0.9)

        # =====================================================
        # 05:15-06:16 Definition by a relation lens.
        # =====================================================
        definition_title = make_title("Data attribution là chọn một quan hệ", 42).to_edge(UP, buff=0.35)
        self.play(Transform(title, definition_title), run_time=0.8)

        behavior = VGroup(
            Circle(radius=0.78, color=YELLOW_NEON, stroke_width=4, fill_color=YELLOW_NEON, fill_opacity=0.06),
            make_label("behavior", YELLOW_NEON, 24, BOLD),
        ).move_to(LEFT * 5.0 + UP * 0.5)
        behavior[1].move_to(behavior[0])
        data = data_cloud(rows=4, cols=6, active={1, 4, 7, 10, 18, 22}, radius=0.075)
        data.move_to(RIGHT * 5.0 + UP * 0.5)
        data_label = make_label("training data", BLUE_NEON, 24, BOLD).next_to(data, DOWN, buff=0.28)

        relation_lens = lens("relation", PURPLE_NEON, radius=0.82).move_to(ORIGIN + UP * 0.5)
        beam_a = Arrow(behavior.get_right(), relation_lens.get_left(), color=WHITE_SOFT, buff=0.25)
        beam_b = Arrow(relation_lens.get_right(), data.get_left(), color=WHITE_SOFT, buff=0.25)

        relation_words = VGroup(
            make_label("evidence", BLUE_NEON, 24, BOLD),
            make_label("credit", YELLOW_NEON, 24, BOLD),
            make_label("counterfactual prediction", GREEN_NEON, 24, BOLD),
        ).arrange(RIGHT, buff=0.55)
        relation_words.to_edge(DOWN, buff=0.72)

        self.play(FadeIn(behavior, scale=0.9), FadeIn(data), FadeIn(data_label), run_time=1.0)
        self.play(Create(beam_a), FadeIn(relation_lens, scale=0.9), Create(beam_b), run_time=1.2)
        for word in relation_words:
            self.play(FadeIn(word, shift=UP * 0.08), relation_lens[0].animate.set_color(word.color), run_time=0.65)
        quote = make_label("Một attribution score chỉ có nghĩa khi ta biết nó đang đo quan hệ nào.", WHITE_SOFT, 28)
        quote.next_to(relation_words, UP, buff=0.42)
        self.play(FadeIn(quote), run_time=0.8)
        voice_wait(self, 37.0)
        self.play(FadeOut(VGroup(behavior, data, data_label, relation_lens, beam_a, beam_b, relation_words, quote)), run_time=0.9)

        # =====================================================
        # 06:16-07:21 Taxonomy as three lenses on one output.
        # =====================================================
        taxonomy_title = make_title("Ba lens chính của data attribution", 40).to_edge(UP, buff=0.35)
        self.play(Transform(title, taxonomy_title), run_time=0.8)

        output_claim = VGroup(
            rounded_box(3.65, 1.15, WHITE_SOFT, 0.035),
            make_label("output y", WHITE_SOFT, 30, BOLD),
        ).move_to(ORIGIN + UP * 1.85)
        output_claim[1].move_to(output_claim[0])

        corpus_docs = VGroup(*[mini_document(f"z{i+1}", BLUE_NEON if i in {1, 3} else GRAY_SOFT, 0.68, 0.88) for i in range(5)])
        corpus_docs.arrange(RIGHT, buff=0.18).move_to(LEFT * 4.75 + DOWN * 1.1)
        players = VGroup(*[Circle(radius=0.2, color=YELLOW_NEON, stroke_width=2, fill_color=YELLOW_NEON, fill_opacity=0.08) for _ in range(6)])
        players.arrange_in_grid(rows=2, cols=3, buff=0.22).move_to(DOWN * 1.1)
        toggles = data_cloud(rows=2, cols=5, active={0, 2, 3, 6, 8}, color=GREEN_NEON, radius=0.08)
        toggles.move_to(RIGHT * 4.75 + DOWN * 1.1)

        lens_specs = [
            ("corroborative", BLUE_NEON, corpus_docs, "evidence?"),
            ("game-theoretic", YELLOW_NEON, players, "credit?"),
            ("predictive", GREEN_NEON, toggles, "counterfactual?"),
        ]

        self.play(FadeIn(output_claim, shift=UP * 0.12), run_time=0.8)
        visual_groups = VGroup(corpus_docs, players, toggles)
        self.play(LaggedStart(*[FadeIn(group, shift=UP * 0.15) for group in visual_groups], lag_ratio=0.14), run_time=1.4)

        for name, color, group, question_text in lens_specs:
            current_label = capsule_label(name, color, font_size=23, pad_x=0.55, pad_y=0.3)
            current_label.next_to(group, UP, buff=0.32)
            question_label = make_label(question_text, color, 25, BOLD)
            question_label.next_to(current_label, UP, buff=0.18)
            beam = Line(output_claim.get_bottom(), group.get_top(), color=color, stroke_width=4, stroke_opacity=0.75)
            focus = SurroundingRectangle(VGroup(group, current_label), color=color, buff=0.18)
            self.play(FadeIn(current_label, scale=0.88), Create(beam), Create(focus), FadeIn(question_label), run_time=0.9)
            self.play(group.animate.set_opacity(1.0), run_time=0.25)
            voice_wait(self, 2.5)
            self.play(FadeOut(VGroup(current_label, beam, focus, question_label)), run_time=0.45)

        takeaway = make_label("Không có một score duy nhất trả lời tốt mọi câu hỏi.", PURPLE_NEON, 30, BOLD)
        takeaway.to_edge(DOWN, buff=0.75)
        self.play(FadeIn(takeaway, shift=UP * 0.12), run_time=0.8)
        voice_wait(self, 28.0)
        self.play(FadeOut(VGroup(output_claim, visual_groups, takeaway)), run_time=0.9)

        # =====================================================
        # 07:21-08:26 Transition to the next scene.
        # =====================================================
        final_title = make_title("Lens đầu tiên: Evidence", 42).to_edge(UP, buff=0.35)
        self.play(Transform(title, final_title), run_time=0.8)

        lens_ring = Circle(radius=1.25, color=BLUE_NEON, stroke_width=5)
        inner_ring = Circle(radius=0.78, color=BLUE_NEON, stroke_width=2, stroke_opacity=0.45)
        output_seed = VGroup(
            rounded_box(3.0, 1.05, YELLOW_NEON, 0.055),
            make_label("output y", YELLOW_NEON, 28, BOLD),
        ).move_to(LEFT * 3.9 + UP * 0.1)
        output_seed[1].move_to(output_seed[0])
        next_scene = capsule_label("Corroborative Attribution", BLUE_NEON, font_size=27, pad_x=0.65, pad_y=0.42)
        next_scene.move_to(RIGHT * 3.45 + UP * 0.1)
        arrow = Arrow(output_seed.get_right(), next_scene.get_left(), color=WHITE_SOFT, buff=0.35)
        bridge = make_label("ở phần tiếp theo, ta chỉ tập trung vào câu hỏi evidence", BLUE_NEON, 28, BOLD)
        bridge.to_edge(DOWN, buff=0.85)

        lens_group = VGroup(lens_ring, inner_ring).move_to(ORIGIN + DOWN * 1.45)
        self.play(FadeIn(output_seed, shift=RIGHT * 0.12), GrowFromCenter(lens_group), run_time=1.0)
        self.play(Create(arrow), FadeIn(next_scene, shift=LEFT * 0.12), run_time=1.0)
        self.play(FadeIn(bridge, shift=UP * 0.12), run_time=0.8)
        self.play(lens_group.animate.scale(1.16).set_stroke(opacity=0.45), rate_func=there_and_back, run_time=1.2)
        voice_wait(self, 40.5)
        self.play(FadeOut(VGroup(title, output_seed, next_scene, arrow, bridge, lens_group)), run_time=1.0)
