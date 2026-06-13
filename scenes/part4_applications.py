from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from manim import *

try:
    from scripts.check_durations import audio_duration
except Exception:  # pragma: no cover - Manim import fallback
    audio_duration = None


# ============================================================
# ICML Tutorial: Data Attribution at Scale
# Part IV: Applications
# Timeline-driven build. Audio is NOT embedded.
# ============================================================

config.background_color = "#171717"
config.frame_width = 16
config.frame_height = 9

ROOT = Path(__file__).resolve().parents[1]

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

FALLBACK_DURATIONS = {
    "p4_00": 89.443,
    "p4_01": 127.922,
    "p4_02": 135.967,
    "p4_03": 130.351,
    "p4_04": 133.642,
    "p4_05": 97.280,
    "p4_06": 102.635,
    "p4_07": 121.757,
    "p4_08": 106.475,
    "p4_09": 123.794,
}


@dataclass(frozen=True)
class Section:
    key: str
    title: str
    color: str
    audio: str


SECTIONS = [
    Section("p4_00", "Từ estimator sang quyết định ứng dụng", CYAN_SOFT, "p4_00.mp3"),
    Section("p4_01", "Recipe chung cho mọi ứng dụng", BLUE_NEON, "p4_01.mp3"),
    Section("p4_02", "Model debugging", RED_NEON, "p4_02.mp3"),
    Section("p4_03", "Dataset selection", GREEN_NEON, "p4_03.mp3"),
    Section("p4_04", "Data valuation và fair credit", YELLOW_NEON, "p4_04.mp3"),
    Section("p4_05", "Data poisoning và security", RED_NEON, "p4_05.mp3"),
    Section("p4_06", "Machine unlearning", PURPLE_NEON, "p4_06.mp3"),
    Section("p4_07", "Citation, RAG, và copyright", BLUE_NEON, "p4_07.mp3"),
    Section("p4_08", "Pitfalls: dùng sai lens", ORANGE_SOFT, "p4_08.mp3"),
    Section("p4_09", "Recap và chuyển sang epilogue", GREEN_NEON, "p4_09.mp3"),
]


def section_duration(section: Section) -> float:
    path = ROOT / "assets" / "audio" / section.audio
    if audio_duration is not None and path.exists():
        duration = audio_duration(path)
        if duration is not None:
            return duration
    return FALLBACK_DURATIONS[section.key]


def make_text(text: str, color: str = WHITE_SOFT, font_size: int = 26, weight=NORMAL, max_width: float = 12.8) -> Text:
    label = Text(text, font="Arial", font_size=font_size, weight=weight, color=color, line_spacing=0.86)
    if label.width > max_width:
        label.scale_to_fit_width(max_width)
    return label


def make_title(text: str, font_size: int = 42, color: str = WHITE_SOFT) -> Text:
    return make_text(text, color, font_size, BOLD, 14.3)


def rounded_box(width: float, height: float, color: str, fill_opacity: float = 0.055, stroke_width: float = 2.0) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        color=color,
        stroke_width=stroke_width,
        fill_color=color,
        fill_opacity=fill_opacity,
    )


def label_box(text: str, color: str, width: float = 3.2, height: float = 0.9, font_size: int = 23) -> VGroup:
    frame = rounded_box(width, height, color, 0.06, 2)
    label = make_text(text, color, font_size, BOLD, width - 0.35)
    if label.height > height - 0.22:
        label.scale_to_fit_height(height - 0.22)
    label.move_to(frame)
    return VGroup(frame, label)


def chip(text: str, color: str, font_size: int = 19) -> VGroup:
    label = make_text(text, color, font_size, BOLD, 2.55)
    if label.height > 0.34:
        label.scale_to_fit_height(0.34)
    frame = rounded_box(label.width + 0.42, max(0.48, label.height + 0.17), color, 0.08, 1.6)
    label.move_to(frame)
    return VGroup(frame, label)


def data_dot(label: str, color: str, radius: float = 0.19) -> VGroup:
    outer = Circle(radius=radius * 1.35, color=color, stroke_width=2, fill_color=color, fill_opacity=0.10)
    dot = Dot(radius=radius, color=color)
    txt = make_text(label, WHITE_SOFT, 18, BOLD, 0.65).move_to(dot)
    return VGroup(outer, dot, txt)


def dots_grid(rows: int, cols: int, colors: list[str], radius: float = 0.06, buff: float = 0.13) -> VGroup:
    dots = VGroup()
    for idx in range(rows * cols):
        dots.add(Square(side_length=radius * 2.0, color=colors[idx % len(colors)], fill_color=colors[idx % len(colors)], fill_opacity=0.95))
    dots.arrange_in_grid(rows=rows, cols=cols, buff=buff)
    return dots


def equation(tex: str, color: str = YELLOW_NEON, font_size: int = 36, max_width: float = 8.8) -> MathTex:
    eq = MathTex(tex, color=color, font_size=font_size)
    if eq.width > max_width:
        eq.scale_to_fit_width(max_width)
    return eq


def stage_note(text: str, color: str) -> VGroup:
    note = make_text(text, color, 24, BOLD, 10.4)
    frame = rounded_box(note.width + 0.55, note.height + 0.28, color, 0.045, 1.7)
    note.move_to(frame)
    group = VGroup(frame, note)
    group.move_to(DOWN * 2.78)
    return group


class ApplicationsOfDataAttribution(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        players = {
            "p4_00": self.play_intro,
            "p4_01": self.play_recipe,
            "p4_02": self.play_debugging,
            "p4_03": self.play_selection,
            "p4_04": self.play_valuation,
            "p4_05": self.play_poisoning,
            "p4_06": self.play_unlearning,
            "p4_07": self.play_rag,
            "p4_08": self.play_pitfalls,
            "p4_09": self.play_recap,
        }
        for section in SECTIONS:
            self.play_section(section, players[section.key])
        self.wait(0.85)

    def section_header(self, section: Section) -> VGroup:
        title = make_title("Part IV: Applications", 43).to_edge(UP, buff=0.25)
        subtitle = make_text(section.title, section.color, 25, BOLD, 13.4).next_to(title, DOWN, buff=0.12)
        return VGroup(title, subtitle)

    def play_section(self, section: Section, beat_makers) -> None:
        duration = section_duration(section)
        start = self.time
        end = start + duration
        header = self.section_header(section)
        self.play(FadeIn(header, shift=UP * 0.15), run_time=0.65)

        beats = beat_makers(section)
        beat_start = self.time
        beat_end = end - 0.55
        previous: VGroup | None = None
        for index, maker in enumerate(beats, start=1):
            target = beat_start + (beat_end - beat_start) * index / len(beats)
            visual = maker()
            if previous is None:
                self.play(FadeIn(visual, shift=UP * 0.12), run_time=0.65)
            else:
                self.play(FadeOut(previous, shift=DOWN * 0.08), FadeIn(visual, shift=UP * 0.08), run_time=0.72)
            previous = visual
            self.animate_visual(visual, section.color)
            self.wait(max(0.0, target - self.time))

        if previous is not None:
            self.play(FadeOut(previous), FadeOut(header), run_time=0.55)
        else:
            self.play(FadeOut(header), run_time=0.55)
        if self.time < end:
            self.wait(end - self.time)

    def animate_visual(self, visual: VGroup, color: str) -> None:
        if len(visual) == 0:
            return
        focus = visual[-1]
        self.play(Circumscribe(focus, color=color, fade_out=True), run_time=1.0)

    # ------------------------------------------------------------------
    # p4_00
    # ------------------------------------------------------------------
    def play_intro(self, section: Section):
        def beat1() -> VGroup:
            estimators = VGroup(
                chip("Influence function", BLUE_NEON),
                chip("TracIn", ORANGE_SOFT),
                chip("TRAK", GREEN_NEON),
                chip("Datamodels", PURPLE_NEON),
                chip("proxy rẻ hơn", YELLOW_NEON),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(LEFT * 5.0 + DOWN * 0.15)
            question = label_box("counterfactual\nquá đắt", RED_NEON, 2.75, 1.25, 24).move_to(LEFT * 1.0 + DOWN * 0.15)
            apps = VGroup(
                chip("debug", RED_NEON),
                chip("select", GREEN_NEON),
                chip("poison", PURPLE_NEON),
                chip("unlearn", YELLOW_NEON),
                chip("cite", BLUE_NEON),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 4.45 + DOWN * 0.15)
            arrows = VGroup(
                Arrow(estimators.get_right(), question.get_left(), color=WHITE_SOFT, buff=0.2),
                Arrow(question.get_right(), apps.get_left(), color=WHITE_SOFT, buff=0.2),
            )
            note = stage_note("Part IV hỏi: score này giúp ta hành động gì?", section.color)
            return VGroup(estimators, question, apps, arrows, note)

        def beat2() -> VGroup:
            score = Circle(radius=1.1, color=YELLOW_NEON, stroke_width=3, fill_color=YELLOW_NEON, fill_opacity=0.08)
            score_label = make_text("score", YELLOW_NEON, 32, BOLD).move_to(score)
            actions = VGroup(
                label_box("debug lỗi", RED_NEON, 2.4, 0.72, 20),
                label_box("chọn data", GREEN_NEON, 2.4, 0.72, 20),
                label_box("phát hiện poison", PURPLE_NEON, 2.55, 0.72, 19),
                label_box("unlearn F", YELLOW_NEON, 2.4, 0.72, 20),
                label_box("trích dẫn nguồn", BLUE_NEON, 2.55, 0.72, 19),
            )
            positions = [LEFT * 5 + UP * 1.5, RIGHT * 4.7 + UP * 1.4, RIGHT * 5 + DOWN * 0.7, DOWN * 2.1, LEFT * 5 + DOWN * 0.9]
            for box, pos in zip(actions, positions, strict=True):
                box.move_to(pos)
            arrows = VGroup(*[Arrow(score.get_center(), box.get_center(), color=box[0].get_color(), buff=1.35, stroke_width=3) for box in actions])
            note = stage_note("Attribution score = tín hiệu để ra quyết định", section.color)
            return VGroup(score, score_label, actions, arrows, note)

        def beat3() -> VGroup:
            lenses = VGroup(
                label_box("evidence", BLUE_NEON, 3.0, 1.0, 25),
                label_box("credit", YELLOW_NEON, 3.0, 1.0, 25),
                label_box("counterfactual\nprediction", GREEN_NEON, 3.0, 1.05, 22),
            ).arrange(RIGHT, buff=0.55).move_to(UP * 0.25)
            questions = VGroup(
                make_text("source nào hỗ trợ output?", BLUE_NEON, 22, BOLD, 3.7),
                make_text("ai đóng góp utility?", YELLOW_NEON, 22, BOLD, 3.7),
                make_text("data đổi thì behavior đổi ra sao?", GREEN_NEON, 21, BOLD, 4.1),
            )
            for q, lens in zip(questions, lenses, strict=True):
                q.next_to(lens, DOWN, buff=0.34)
            selector = SurroundingRectangle(lenses, color=section.color, buff=0.18)
            note = stage_note("Ứng dụng quyết định ý nghĩa của attribution", section.color)
            return VGroup(lenses, questions, selector, note)

        return [beat1, beat2, beat3]

    # ------------------------------------------------------------------
    # p4_01
    # ------------------------------------------------------------------
    def play_recipe(self, section: Section):
        steps = [
            ("behavior", "ta đo điều gì?", BLUE_NEON),
            ("data unit", "đơn vị nào?", GREEN_NEON),
            ("intervention", "hành động nào?", YELLOW_NEON),
            ("notion", "lens nào?", PURPLE_NEON),
            ("evaluation", "kiểm tra ra sao?", RED_NEON),
        ]

        def pipeline(active: int) -> VGroup:
            boxes = VGroup()
            for idx, (title, body, color) in enumerate(steps):
                box = label_box(f"{title}\n{body}", color, 2.45, 1.1, 19).scale(1.0 if idx == active else 0.92)
                boxes.add(box)
            boxes.arrange(RIGHT, buff=0.28).move_to(UP * 0.35)
            arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), color=GRAY_SOFT, buff=0.08, stroke_width=3) for i in range(len(boxes) - 1)])
            highlight = SurroundingRectangle(boxes[active], color=steps[active][2], buff=0.09)
            note_texts = [
                "Behavior rõ thì score mới có nghĩa.",
                "Unit quá nhỏ thì nhiễu; quá lớn thì khó sửa.",
                "Remove, downweight, add, relabel, deduplicate?",
                "Evidence, credit, hay prediction?",
                "Không evaluation thì score chỉ là một đề xuất.",
            ]
            return VGroup(boxes, arrows, highlight, stage_note(note_texts[active], steps[active][2]))

        def beat1() -> VGroup:
            return pipeline(0)

        def beat2() -> VGroup:
            return pipeline(1)

        def beat3() -> VGroup:
            choices = VGroup(
                chip("remove", RED_NEON),
                chip("downweight", ORANGE_SOFT),
                chip("add", GREEN_NEON),
                chip("replace label", YELLOW_NEON),
                chip("deduplicate", BLUE_NEON),
                chip("retrain S \\ F", PURPLE_NEON),
            ).arrange_in_grid(rows=2, cols=3, buff=0.28).move_to(UP * 0.2)
            hook = Arrow(LEFT * 5.0 + DOWN * 1.35, choices.get_left(), color=YELLOW_NEON, stroke_width=4)
            return VGroup(choices, hook, stage_note("Intervention phải khớp câu hỏi ứng dụng", YELLOW_NEON))

        def beat4() -> VGroup:
            lens = VGroup(
                label_box("corroborative\n= evidence", BLUE_NEON, 3.25, 1.16, 22),
                label_box("game-theoretic\n= credit", YELLOW_NEON, 3.25, 1.16, 22),
                label_box("predictive\n= behavior shift", GREEN_NEON, 3.25, 1.16, 22),
            ).arrange(RIGHT, buff=0.45).move_to(UP * 0.18)
            note = stage_note("Một score đẹp vẫn có thể trả lời sai câu hỏi", section.color)
            return VGroup(lens, note)

        def beat5() -> VGroup:
            tests = VGroup(
                label_box("debug\nprecision@k", RED_NEON, 2.7, 1.0, 21),
                label_box("selection\nretrain + held-out", GREEN_NEON, 3.0, 1.0, 20),
                label_box("unlearning\nutility + forgetting", PURPLE_NEON, 3.2, 1.0, 19),
            ).arrange(RIGHT, buff=0.48).move_to(UP * 0.18)
            return VGroup(tests, stage_note("Evaluation là nơi score chạm đất", RED_NEON))

        return [beat1, beat2, beat3, beat4, beat5]

    # ------------------------------------------------------------------
    # p4_02
    # ------------------------------------------------------------------
    def play_debugging(self, section: Section):
        def beat1() -> VGroup:
            failure = label_box("output lỗi", RED_NEON, 2.7, 1.0, 26).move_to(LEFT * 5.2 + UP * 0.65)
            data = VGroup(*[data_dot(f"z{i}", color) for i, color in enumerate([BLUE_NEON, GRAY_SOFT, RED_NEON, GREEN_NEON, RED_NEON, GRAY_SOFT], 1)])
            data.arrange(RIGHT, buff=0.33).move_to(RIGHT * 2.4 + UP * 0.65)
            arrows = VGroup(*[Arrow(failure.get_right(), d.get_left(), color=d[0].get_color(), buff=0.12, stroke_width=3) for d in data[::2]])
            return VGroup(failure, data, arrows, stage_note("Debugging bắt đầu từ một behavior xấu đã quan sát", RED_NEON))

        def beat2() -> VGroup:
            labels = VGroup(
                label_box("mislabeled", RED_NEON, 2.5, 0.78, 21),
                label_box("ambiguous", YELLOW_NEON, 2.5, 0.78, 21),
                label_box("duplicated", BLUE_NEON, 2.5, 0.78, 21),
                label_box("subgroup gap", PURPLE_NEON, 2.5, 0.78, 21),
            ).arrange_in_grid(rows=2, cols=2, buff=0.34).move_to(LEFT * 2.8 + UP * 0.25)
            shortlist = label_box("top-k examples\nhuman inspection", GREEN_NEON, 3.2, 1.25, 22).move_to(RIGHT * 3.6 + UP * 0.25)
            arrow = Arrow(labels.get_right(), shortlist.get_left(), color=GREEN_NEON, buff=0.2, stroke_width=4)
            return VGroup(labels, shortlist, arrow, stage_note("Top-k hữu ích hơn một score tuyệt đối hoàn hảo", GREEN_NEON))

        def beat3() -> VGroup:
            test = label_box("test case", BLUE_NEON, 2.5, 0.86, 24).move_to(LEFT * 4.9 + UP * 0.65)
            evidence = label_box("semantic evidence", BLUE_NEON, 3.1, 0.86, 22).move_to(RIGHT * 0.0 + UP * 1.25)
            cause = label_box("causal influence", RED_NEON, 3.1, 0.86, 22).move_to(RIGHT * 4.4 + DOWN * 0.25)
            arrows = VGroup(
                Arrow(test.get_right(), evidence.get_left(), color=BLUE_NEON, buff=0.18),
                Arrow(evidence.get_right(), cause.get_left(), color=RED_NEON, buff=0.18),
            )
            warning = Cross(Line(LEFT * 0.55, RIGHT * 0.55, color=RED_NEON), stroke_width=6).move_to(RIGHT * 2.25 + UP * 0.48)
            return VGroup(test, evidence, cause, arrows, warning, stage_note("Semantic similarity chưa chắc là nguyên nhân", RED_NEON))

        def beat4() -> VGroup:
            left = label_box("brittle\nprediction", PURPLE_NEON, 3.1, 1.15, 24).move_to(LEFT * 3.8 + UP * 0.25)
            toggle = VGroup(
                chip("subset A", BLUE_NEON),
                Arrow(LEFT * 0.9, RIGHT * 0.9, color=WHITE_SOFT),
                chip("prediction flips", RED_NEON),
            ).arrange(RIGHT, buff=0.28).move_to(UP * 0.25)
            right = label_box("train-test\nleakage", YELLOW_NEON, 3.0, 1.15, 24).move_to(RIGHT * 4.2 + UP * 0.25)
            lines = VGroup(
                DashedLine(left.get_right(), toggle.get_left(), color=PURPLE_NEON),
                DashedLine(toggle.get_right(), right.get_left(), color=YELLOW_NEON),
            )
            return VGroup(left, toggle, right, lines, stage_note("Datamodels mở rộng debugging thành audit behavior", PURPLE_NEON))

        return [beat1, beat2, beat3, beat4]

    # ------------------------------------------------------------------
    # p4_03
    # ------------------------------------------------------------------
    def play_selection(self, section: Section):
        def beat1() -> VGroup:
            pool = dots_grid(6, 10, [GRAY_SOFT, GREEN_NEON, GRAY_SOFT, BLUE_NEON], 0.09, 0.11).move_to(LEFT * 4.4 + UP * 0.3)
            budget = label_box("budget hữu hạn", YELLOW_NEON, 2.9, 0.85, 23).move_to(RIGHT * 1.2 + UP * 0.8)
            selected = dots_grid(3, 6, [GREEN_NEON, BLUE_NEON, GREEN_NEON], 0.09, 0.11).move_to(RIGHT * 4.7 + DOWN * 0.15)
            arrows = VGroup(
                Arrow(pool.get_right(), budget.get_left(), color=YELLOW_NEON, buff=0.2),
                Arrow(budget.get_right(), selected.get_left(), color=GREEN_NEON, buff=0.2),
            )
            return VGroup(pool, budget, selected, arrows, stage_note("Không phải cứ gom càng nhiều data càng tốt", GREEN_NEON))

        def beat2() -> VGroup:
            target = label_box("target behavior", BLUE_NEON, 3.0, 0.85, 23).move_to(UP * 1.45)
            rare = chip("rare classes", GREEN_NEON).move_to(LEFT * 4.2 + DOWN * 0.2)
            hallucination = chip("hallucination giảm", RED_NEON).move_to(RIGHT * 0.0 + DOWN * 0.2)
            embedding = chip("embedding giống query", GRAY_SOFT).move_to(RIGHT * 4.2 + DOWN * 0.2)
            arrows = VGroup(
                Arrow(rare.get_top(), target.get_bottom(), color=GREEN_NEON, buff=0.13),
                Arrow(hallucination.get_top(), target.get_bottom(), color=RED_NEON, buff=0.13),
                Arrow(embedding.get_top(), target.get_bottom(), color=GRAY_SOFT, buff=0.13),
            )
            return VGroup(target, rare, hallucination, embedding, arrows, stage_note("Ta chọn theo expected behavior gain, không chỉ theo similarity", BLUE_NEON))

        def beat3() -> VGroup:
            value = VGroup(
                label_box("high Data Shapley", GREEN_NEON, 3.35, 0.85, 21),
                Arrow(LEFT * 0.8, RIGHT * 0.8, color=GREEN_NEON),
                label_box("acquire similar data", GREEN_NEON, 3.35, 0.85, 21),
            ).arrange(RIGHT, buff=0.34).move_to(UP * 0.85)
            low = VGroup(
                label_box("low / weird value", RED_NEON, 3.25, 0.85, 21),
                Arrow(LEFT * 0.8, RIGHT * 0.8, color=RED_NEON),
                label_box("outlier / bad label", RED_NEON, 3.35, 0.85, 21),
            ).arrange(RIGHT, buff=0.34).move_to(DOWN * 0.65)
            return VGroup(value, low, stage_note("Valuation cũng gợi ý acquire, clean, hoặc loại data", GREEN_NEON))

        def beat4() -> VGroup:
            loop = VGroup(
                label_box("score", BLUE_NEON, 1.8, 0.75, 22),
                label_box("subset", GREEN_NEON, 1.95, 0.75, 22),
                label_box("train", YELLOW_NEON, 1.8, 0.75, 22),
                label_box("evaluate", RED_NEON, 2.2, 0.75, 22),
            ).arrange(RIGHT, buff=0.36).move_to(UP * 0.25)
            arrows = VGroup(*[Arrow(loop[i].get_right(), loop[(i + 1) % len(loop)].get_left(), color=WHITE_SOFT, buff=0.1) for i in range(len(loop) - 1)])
            back = CurvedArrow(loop[-1].get_bottom(), loop[0].get_bottom(), angle=-TAU / 4, color=PURPLE_NEON)
            heldout = chip("held-out behaviors", PURPLE_NEON).next_to(loop, DOWN, buff=0.65)
            return VGroup(loop, arrows, back, heldout, stage_note("Selection là vòng lặp, không phải sort một lần rồi xong", PURPLE_NEON))

        return [beat1, beat2, beat3, beat4]

    # ------------------------------------------------------------------
    # p4_04
    # ------------------------------------------------------------------
    def play_valuation(self, section: Section):
        def beat1() -> VGroup:
            contributors = VGroup(
                label_box("A", BLUE_NEON, 0.95, 0.75, 28),
                label_box("B", GREEN_NEON, 0.95, 0.75, 28),
                label_box("C", YELLOW_NEON, 0.95, 0.75, 28),
                label_box("D", PURPLE_NEON, 0.95, 0.75, 28),
            ).arrange(DOWN, buff=0.22).move_to(LEFT * 5.2 + UP * 0.2)
            utility = label_box("utility\naccuracy / revenue / win rate", GREEN_NEON, 4.0, 1.35, 21).move_to(RIGHT * 3.9 + UP * 0.2)
            arrows = VGroup(*[Arrow(c.get_right(), utility.get_left(), color=c[0].get_color(), buff=0.14, stroke_width=3) for c in contributors])
            return VGroup(contributors, utility, arrows, stage_note("Data valuation hỏi: credit nên chia thế nào?", YELLOW_NEON))

        def beat2() -> VGroup:
            shapley = equation(r"\phi_i=\mathbb{E}_{S}\left[v(S\cup\{i\})-v(S)\right]", YELLOW_NEON, 40, 9.2).move_to(UP * 0.75)
            contexts = VGroup(
                chip("context 1", BLUE_NEON),
                chip("context 2", GREEN_NEON),
                chip("context 3", PURPLE_NEON),
            ).arrange(RIGHT, buff=0.35).next_to(shapley, DOWN, buff=0.55)
            return VGroup(shapley, contexts, stage_note("Shapley trung bình marginal contribution qua nhiều context", YELLOW_NEON))

        def beat3() -> VGroup:
            left = label_box("utility y tế", RED_NEON, 2.9, 0.9, 22).move_to(LEFT * 4.0 + UP * 0.7)
            right = label_box("utility dịch máy", BLUE_NEON, 2.9, 0.9, 22).move_to(RIGHT * 4.0 + UP * 0.7)
            data = label_box("same dataset", YELLOW_NEON, 2.7, 0.85, 23).move_to(DOWN * 0.35)
            arrows = VGroup(
                Arrow(data.get_top(), left.get_bottom(), color=RED_NEON, buff=0.1),
                Arrow(data.get_top(), right.get_bottom(), color=BLUE_NEON, buff=0.1),
            )
            scores = VGroup(make_text("high value", RED_NEON, 25, BOLD), make_text("low value", BLUE_NEON, 25, BOLD))
            scores[0].next_to(left, DOWN, buff=0.3)
            scores[1].next_to(right, DOWN, buff=0.3)
            return VGroup(left, right, data, arrows, scores, stage_note("Giá trị data phụ thuộc utility và context", YELLOW_NEON))

        def beat4() -> VGroup:
            duplicates = VGroup(*[data_dot("d", BLUE_NEON, 0.16) for _ in range(5)]).arrange(RIGHT, buff=0.18).move_to(LEFT * 3.8 + UP * 0.55)
            rare = VGroup(*[data_dot("r", GREEN_NEON, 0.16) for _ in range(2)]).arrange(RIGHT, buff=0.22).move_to(RIGHT * 3.9 + UP * 0.55)
            dup_label = make_text("nhiều duplicate\nmarginal thấp", BLUE_NEON, 23, BOLD, 3.8).next_to(duplicates, DOWN, buff=0.35)
            rare_label = make_text("ít nhưng hiếm\nmarginal cao", GREEN_NEON, 23, BOLD, 3.8).next_to(rare, DOWN, buff=0.35)
            return VGroup(duplicates, rare, dup_label, rare_label, stage_note("Fair credit khác predictive usefulness", section.color))

        return [beat1, beat2, beat3, beat4]

    # ------------------------------------------------------------------
    # p4_05
    # ------------------------------------------------------------------
    def play_poisoning(self, section: Section):
        def beat1() -> VGroup:
            clean = VGroup(*[data_dot(f"z{i}", BLUE_NEON, 0.15) for i in range(1, 7)]).arrange(RIGHT, buff=0.22)
            poison = data_dot("p", RED_NEON, 0.19)
            train = VGroup(clean, poison).arrange(RIGHT, buff=0.38).move_to(LEFT * 3.7 + UP * 0.55)
            model = label_box("model behavior\nbị kéo lệch", RED_NEON, 3.25, 1.15, 22).move_to(RIGHT * 3.8 + UP * 0.55)
            arrow = Arrow(train.get_right(), model.get_left(), color=RED_NEON, buff=0.2, stroke_width=4)
            return VGroup(train, model, arrow, stage_note("Poisoning: một vài điểm data có thể làm behavior xấu đi", RED_NEON))

        def beat2() -> VGroup:
            clean_label = label_box("clean-label", YELLOW_NEON, 2.8, 0.85, 25).move_to(LEFT * 4.5 + UP * 0.55)
            gradient = equation(r"\nabla_\theta \ell_{poison}\approx \nabla_\theta \ell_{target}", RED_NEON, 36, 6.4).move_to(RIGHT * 2.2 + UP * 0.55)
            target = chip("target sai", RED_NEON).next_to(gradient, DOWN, buff=0.55)
            arrow = Arrow(clean_label.get_right(), gradient.get_left(), color=YELLOW_NEON, buff=0.2)
            return VGroup(clean_label, gradient, target, arrow, stage_note("Gradient có thể bị dùng để thiết kế attack tinh vi", RED_NEON))

        def beat3() -> VGroup:
            heatmap = dots_grid(5, 9, [GRAY_SOFT, GRAY_SOFT, RED_NEON, GRAY_SOFT, BLUE_NEON], 0.095, 0.12).move_to(LEFT * 3.8 + UP * 0.35)
            audit = label_box("audit\nabnormal influence", GREEN_NEON, 3.4, 1.15, 22).move_to(RIGHT * 3.65 + UP * 0.35)
            arrow = Arrow(heatmap.get_right(), audit.get_left(), color=GREEN_NEON, buff=0.22, stroke_width=4)
            return VGroup(heatmap, audit, arrow, stage_note("Attribution giúp defender ưu tiên data cần kiểm tra", GREEN_NEON))

        def beat4() -> VGroup:
            defender = label_box("defender", GREEN_NEON, 2.8, 0.9, 24).move_to(LEFT * 3.6 + UP * 0.5)
            attacker = label_box("attacker", RED_NEON, 2.8, 0.9, 24).move_to(RIGHT * 3.6 + UP * 0.5)
            score = Circle(radius=0.72, color=YELLOW_NEON, stroke_width=3, fill_color=YELLOW_NEON, fill_opacity=0.07)
            score_text = make_text("score", YELLOW_NEON, 25, BOLD).move_to(score)
            arrows = VGroup(
                Arrow(score.get_left(), defender.get_right(), color=GREEN_NEON, buff=0.15),
                Arrow(score.get_right(), attacker.get_left(), color=RED_NEON, buff=0.15),
            )
            guard = VGroup(chip("access control", BLUE_NEON), chip("aggregation", PURPLE_NEON), chip("privacy", CYAN_SOFT)).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.2)
            return VGroup(defender, attacker, score, score_text, arrows, guard, stage_note("Security biến attribution thành bài toán governance", YELLOW_NEON))

        return [beat1, beat2, beat3, beat4]

    # ------------------------------------------------------------------
    # p4_06
    # ------------------------------------------------------------------
    def play_unlearning(self, section: Section):
        def beat1() -> VGroup:
            full = VGroup(*[data_dot(f"s{i}", BLUE_NEON, 0.15) for i in range(1, 9)]).arrange(RIGHT, buff=0.20).move_to(LEFT * 3.8 + UP * 0.55)
            forget = SurroundingRectangle(VGroup(full[2], full[3]), color=RED_NEON, buff=0.12)
            target = label_box("train on\nS \\ F ?", PURPLE_NEON, 2.85, 1.1, 24).move_to(RIGHT * 3.6 + UP * 0.55)
            arrow = Arrow(full.get_right(), target.get_left(), color=PURPLE_NEON, buff=0.18)
            return VGroup(full, forget, target, arrow, stage_note("Unlearning hỏi một counterfactual rất tự nhiên", PURPLE_NEON))

        def beat2() -> VGroup:
            shards = VGroup()
            for i, color in enumerate([BLUE_NEON, GREEN_NEON, YELLOW_NEON, PURPLE_NEON]):
                shard = VGroup(*[Square(0.28, color=color, fill_color=color, fill_opacity=0.25) for _ in range(5)]).arrange(RIGHT, buff=0.05)
                shards.add(shard)
            shards.arrange(DOWN, buff=0.22).move_to(LEFT * 3.4 + UP * 0.25)
            sisa = label_box("SISA\nshard + slice", YELLOW_NEON, 3.0, 1.15, 23).move_to(RIGHT * 3.6 + UP * 0.25)
            arrow = Arrow(shards.get_right(), sisa.get_left(), color=YELLOW_NEON, buff=0.22)
            return VGroup(shards, sisa, arrow, stage_note("SISA giảm chi phí quên bằng cách giới hạn phạm vi ảnh hưởng", YELLOW_NEON))

        def beat3() -> VGroup:
            predictors = VGroup(
                label_box("predictive\nattribution", GREEN_NEON, 3.2, 1.1, 21),
                label_box("influence-style\napproximation", BLUE_NEON, 3.2, 1.1, 21),
                label_box("datamodels\nsurrogate", PURPLE_NEON, 3.2, 1.1, 21),
            ).arrange(RIGHT, buff=0.42).move_to(UP * 0.2)
            return VGroup(predictors, stage_note("Attribution ước lượng behavior sau khi remove F", GREEN_NEON))

        def beat4() -> VGroup:
            checks = VGroup(
                label_box("utility giữ được?", GREEN_NEON, 3.0, 0.82, 21),
                label_box("privacy đạt không?", BLUE_NEON, 3.0, 0.82, 21),
                label_box("attack probes?", RED_NEON, 3.0, 0.82, 21),
                label_box("compliance?", YELLOW_NEON, 3.0, 0.82, 21),
            ).arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(UP * 0.25)
            stamp = Cross(checks, stroke_width=5).set_color(RED_NEON).scale(1.06)
            cert = make_text("not a certificate", RED_NEON, 31, BOLD).next_to(checks, DOWN, buff=0.45)
            return VGroup(checks, stamp, cert, stage_note("Attribution là triage/audit, không phải chứng nhận unlearning", RED_NEON))

        return [beat1, beat2, beat3, beat4]

    # ------------------------------------------------------------------
    # p4_07
    # ------------------------------------------------------------------
    def play_rag(self, section: Section):
        def beat1() -> VGroup:
            query = label_box("user query", BLUE_NEON, 2.4, 0.78, 22).move_to(LEFT * 5.3 + UP * 0.8)
            retrieval = label_box("retrieved docs", PURPLE_NEON, 3.0, 0.9, 22).move_to(LEFT * 1.3 + UP * 0.8)
            answer = label_box("generated answer", GREEN_NEON, 3.3, 0.9, 22).move_to(RIGHT * 3.7 + UP * 0.8)
            arrows = VGroup(
                Arrow(query.get_right(), retrieval.get_left(), color=BLUE_NEON, buff=0.15),
                Arrow(retrieval.get_right(), answer.get_left(), color=GREEN_NEON, buff=0.15),
            )
            docs = VGroup(*[chip(f"doc {i}", color) for i, color in enumerate([BLUE_NEON, GRAY_SOFT, GREEN_NEON, YELLOW_NEON], 1)]).arrange(RIGHT, buff=0.18).next_to(retrieval, DOWN, buff=0.7)
            return VGroup(query, retrieval, answer, arrows, docs, stage_note("RAG retrieval không tự động làm citation đúng", BLUE_NEON))

        def beat2() -> VGroup:
            claim = label_box("claim trong output", GREEN_NEON, 3.25, 0.9, 22).move_to(UP * 1.15)
            sources = VGroup(
                label_box("support", GREEN_NEON, 2.5, 0.75, 21),
                label_box("contradict", RED_NEON, 2.5, 0.75, 21),
                label_box("related", YELLOW_NEON, 2.5, 0.75, 21),
            ).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.35)
            arrows = VGroup(*[Arrow(source.get_top(), claim.get_bottom(), color=source[0].get_color(), buff=0.14) for source in sources])
            return VGroup(claim, sources, arrows, stage_note("Corroborative attribution nối claim với evidence candidates", GREEN_NEON))

        def beat3() -> VGroup:
            correctness = label_box("citation\ncorrectness", BLUE_NEON, 3.3, 1.15, 24).move_to(LEFT * 3.3 + UP * 0.35)
            faithfulness = label_box("citation\nfaithfulness", PURPLE_NEON, 3.3, 1.15, 24).move_to(RIGHT * 3.3 + UP * 0.35)
            versus = make_text("support != relied on", YELLOW_NEON, 29, BOLD).move_to(DOWN * 0.95)
            brace = DoubleArrow(correctness.get_right(), faithfulness.get_left(), color=YELLOW_NEON, buff=0.2)
            return VGroup(correctness, faithfulness, brace, versus, stage_note("Source có thể đúng nhưng chỉ được gắn vào sau", PURPLE_NEON))

        def beat4() -> VGroup:
            output = label_box("output", GREEN_NEON, 2.5, 0.82, 23).move_to(LEFT * 4.8 + UP * 0.35)
            source = label_box("source corpus", BLUE_NEON, 3.0, 0.82, 23).move_to(RIGHT * 4.0 + UP * 0.35)
            similar = equation(r"\text{too close?}", RED_NEON, 36, 4.2).move_to(UP * 0.35)
            evidence = chip("evidence span", YELLOW_NEON).move_to(DOWN * 1.15)
            arrows = VGroup(
                Arrow(output.get_right(), similar.get_left(), color=RED_NEON, buff=0.2),
                Arrow(similar.get_right(), source.get_left(), color=RED_NEON, buff=0.2),
                Arrow(similar.get_bottom(), evidence.get_top(), color=YELLOW_NEON, buff=0.15),
            )
            return VGroup(output, source, similar, evidence, arrows, stage_note("Copyright/citation cần lens evidence, không phải utility", RED_NEON))

        return [beat1, beat2, beat3, beat4]

    # ------------------------------------------------------------------
    # p4_08
    # ------------------------------------------------------------------
    def play_pitfalls(self, section: Section):
        pitfalls = [
            ("evidence", "cause", BLUE_NEON),
            ("similarity", "value", GREEN_NEON),
            ("fair credit", "predictive effect", YELLOW_NEON),
            ("document score", "paragraph effect", PURPLE_NEON),
            ("score", "evaluation", RED_NEON),
        ]

        def pitfall(index: int) -> VGroup:
            left, right, color = pitfalls[index]
            left_box = label_box(left, color, 3.1, 0.92, 23).move_to(LEFT * 3.4 + UP * 0.35)
            right_box = label_box(right, RED_NEON if index == 0 else color, 3.1, 0.92, 23).move_to(RIGHT * 3.4 + UP * 0.35)
            eq = make_text("!=", RED_NEON, 44, BOLD).move_to(UP * 0.35)
            cross = Cross(VGroup(left_box, right_box), stroke_width=4).set_color(RED_NEON).scale(1.05)
            notes = [
                "Một source support claim chưa chắc gây ra claim.",
                "Embedding gần không đồng nghĩa marginal contribution cao.",
                "Payment cần fairness; selection cần prediction.",
                "Unit thay đổi thì kết luận cũng đổi.",
                "Sau hành động, luôn đo lại.",
            ]
            return VGroup(left_box, right_box, eq, cross, stage_note(notes[index], color))

        def beat1() -> VGroup:
            return pitfall(0)

        def beat2() -> VGroup:
            return pitfall(1)

        def beat3() -> VGroup:
            return pitfall(2)

        def beat4() -> VGroup:
            return pitfall(3)

        def beat5() -> VGroup:
            return pitfall(4)

        return [beat1, beat2, beat3, beat4, beat5]

    # ------------------------------------------------------------------
    # p4_09
    # ------------------------------------------------------------------
    def play_recap(self, section: Section):
        def beat1() -> VGroup:
            rows = VGroup(
                label_box("debugging -> evidence + predictive", RED_NEON, 5.2, 0.62, 19),
                label_box("selection -> predictive", GREEN_NEON, 5.2, 0.62, 19),
                label_box("valuation -> game-theoretic", YELLOW_NEON, 5.2, 0.62, 19),
                label_box("poisoning -> predictive/security", PURPLE_NEON, 5.2, 0.62, 19),
                label_box("unlearning -> counterfactual", BLUE_NEON, 5.2, 0.62, 19),
                label_box("RAG/citation -> corroborative", CYAN_SOFT, 5.2, 0.62, 19),
            ).arrange(DOWN, buff=0.12).move_to(UP * 0.2)
            return VGroup(rows, stage_note("Mỗi ứng dụng cần một lens attribution khác nhau", GREEN_NEON))

        def beat2() -> VGroup:
            center = Circle(radius=1.05, color=WHITE_SOFT, stroke_width=2, fill_color=WHITE_SOFT, fill_opacity=0.03)
            label = make_text("application\nquestion", WHITE_SOFT, 24, BOLD, 2.2).move_to(center)
            lenses = VGroup(
                label_box("evidence?", BLUE_NEON, 2.35, 0.72, 21).move_to(LEFT * 4.6 + UP * 0.85),
                label_box("credit?", YELLOW_NEON, 2.35, 0.72, 21).move_to(RIGHT * 4.6 + UP * 0.85),
                label_box("behavior after\nintervention?", GREEN_NEON, 2.8, 1.0, 20).move_to(DOWN * 1.55),
            )
            arrows = VGroup(*[Arrow(center.get_center(), lens.get_center(), color=lens[0].get_color(), buff=1.25, stroke_width=3) for lens in lenses])
            return VGroup(center, label, lenses, arrows, stage_note("Đừng bắt đầu từ method; hãy bắt đầu từ câu hỏi", YELLOW_NEON))

        def beat3() -> VGroup:
            map_items = VGroup(
                label_box("3 lenses", BLUE_NEON, 2.6, 0.82, 24),
                label_box("2 scale lessons", PURPLE_NEON, 2.9, 0.82, 23),
                label_box("1 responsibility principle", GREEN_NEON, 3.8, 0.82, 22),
            ).arrange(RIGHT, buff=0.35).move_to(UP * 0.15)
            epilogue = make_title("Epilogue", 38, WHITE_SOFT).next_to(map_items, DOWN, buff=0.55)
            arrow = Arrow(map_items.get_bottom(), epilogue.get_top(), color=GREEN_NEON, buff=0.18, stroke_width=4)
            return VGroup(map_items, epilogue, arrow, stage_note("Data attribution at scale là cách đặt câu hỏi có kỷ luật", GREEN_NEON))

        return [beat1, beat2, beat3]
