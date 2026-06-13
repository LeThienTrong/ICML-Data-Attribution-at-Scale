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
# Part V: Epilogue recap
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
    "p5_00": 61.153,
    "p5_01": 98.534,
    "p5_02": 84.976,
    "p5_03": 95.190,
    "p5_04": 104.438,
    "p5_05": 96.575,
}


@dataclass(frozen=True)
class Section:
    key: str
    title: str
    color: str
    audio: str


SECTIONS = [
    Section("p5_00", "Epilogue: bản đồ cuối", CYAN_SOFT, "p5_00.mp3"),
    Section("p5_01", "Nhìn lại bốn phần", BLUE_NEON, "p5_01.mp3"),
    Section("p5_02", "Ba lens cần nhớ", GREEN_NEON, "p5_02.mp3"),
    Section("p5_03", "Hai bài học về scale", YELLOW_NEON, "p5_03.mp3"),
    Section("p5_04", "Responsible attribution", PURPLE_NEON, "p5_04.mp3"),
    Section("p5_05", "Closing", WHITE_SOFT, "p5_05.mp3"),
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
    return make_text(text, color, font_size, BOLD, 14.2)


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


def label_box(text: str, color: str, width: float = 3.25, height: float = 0.95, font_size: int = 22) -> VGroup:
    frame = rounded_box(width, height, color, 0.06, 2)
    label = make_text(text, color, font_size, BOLD, width - 0.35)
    if label.height > height - 0.22:
        label.scale_to_fit_height(height - 0.22)
    label.move_to(frame)
    return VGroup(frame, label)


def chip(text: str, color: str, font_size: int = 19) -> VGroup:
    label = make_text(text, color, font_size, BOLD, 2.75)
    if label.height > 0.34:
        label.scale_to_fit_height(0.34)
    frame = rounded_box(label.width + 0.44, max(0.48, label.height + 0.18), color, 0.08, 1.6)
    label.move_to(frame)
    return VGroup(frame, label)


def data_dot(label: str, color: str, radius: float = 0.18) -> VGroup:
    ring = Circle(radius=radius * 1.33, color=color, stroke_width=2, fill_color=color, fill_opacity=0.10)
    dot = Dot(radius=radius, color=color)
    txt = make_text(label, WHITE_SOFT, 17, BOLD, 0.55).move_to(dot)
    return VGroup(ring, dot, txt)


def stage_note(text: str, color: str) -> VGroup:
    note = make_text(text, color, 24, BOLD, 10.6)
    frame = rounded_box(note.width + 0.58, note.height + 0.28, color, 0.045, 1.7)
    note.move_to(frame)
    group = VGroup(frame, note).move_to(DOWN * 2.78)
    return group


def arc_arrow(radius: float, start_angle: float, angle: float, color: str) -> CurvedArrow:
    start = radius * np.array([np.cos(start_angle), np.sin(start_angle), 0])
    end = radius * np.array([np.cos(start_angle + angle), np.sin(start_angle + angle), 0])
    return CurvedArrow(start, end, angle=angle / 2, color=color, stroke_width=4)


class EpilogueRecap(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        players = {
            "p5_00": self.play_opening,
            "p5_01": self.play_four_parts,
            "p5_02": self.play_three_lenses,
            "p5_03": self.play_scale_lessons,
            "p5_04": self.play_responsible,
            "p5_05": self.play_closing,
        }
        for section in SECTIONS:
            self.play_section(section, players[section.key])
        self.wait(0.8)

    def section_header(self, section: Section) -> VGroup:
        title = make_title("Part V: Epilogue", 43).to_edge(UP, buff=0.25)
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
                self.play(FadeIn(visual, shift=UP * 0.10), run_time=0.65)
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
        self.play(Circumscribe(visual[-1], color=color, fade_out=True), run_time=0.95)

    # ------------------------------------------------------------------
    # p5_00
    # ------------------------------------------------------------------
    def play_opening(self, section: Section):
        def beat1() -> VGroup:
            center = label_box("data attribution\nat scale", WHITE_SOFT, 3.25, 1.18, 25).move_to(UP * 0.35)
            glow = SurroundingRectangle(center, color=section.color, buff=0.22, stroke_width=2)
            glow.set_opacity(0.65)

            def map_card(title: str, items: list[str], color: str, width: float = 3.25) -> VGroup:
                frame = rounded_box(width, 1.46, color, 0.055, 2)
                title_text = make_text(title, color, 23, BOLD, width - 0.35).move_to(frame.get_top() + DOWN * 0.33)
                item_row = VGroup(*[chip(item, color, 14) for item in items]).arrange(RIGHT, buff=0.09)
                if item_row.width > width - 0.35:
                    item_row.scale_to_fit_width(width - 0.35)
                item_row.move_to(frame.get_center() + DOWN * 0.32)
                return VGroup(frame, title_text, item_row)

            lens = map_card("lens", ["evidence", "credit", "predict"], BLUE_NEON).move_to(LEFT * 4.55 + UP * 0.85)
            scale = map_card("scale", ["cost", "proxy", "eval"], YELLOW_NEON).move_to(RIGHT * 4.55 + UP * 0.85)
            responsibility = map_card("responsibility", ["decision", "limits", "audit"], PURPLE_NEON, 4.05).move_to(DOWN * 1.48)

            connectors = VGroup(
                Arrow(lens.get_right(), center.get_left(), color=BLUE_NEON, buff=0.16, stroke_width=3.2, max_tip_length_to_length_ratio=0.08),
                Arrow(scale.get_left(), center.get_right(), color=YELLOW_NEON, buff=0.16, stroke_width=3.2, max_tip_length_to_length_ratio=0.08),
                Arrow(responsibility.get_top(), center.get_bottom(), color=PURPLE_NEON, buff=0.18, stroke_width=3.2, max_tip_length_to_length_ratio=0.10),
            )
            triangle = VGroup(
                DashedLine(lens.get_bottom(), responsibility.get_left(), color=GRAY_SOFT, dash_length=0.16),
                DashedLine(scale.get_bottom(), responsibility.get_right(), color=GRAY_SOFT, dash_length=0.16),
                DashedLine(lens.get_right(), scale.get_left(), color=GRAY_SOFT, dash_length=0.16),
            ).set_opacity(0.32)

            caption = stage_note("Epilogue gom tutorial thành một bản đồ: lens, scale, rồi trách nhiệm", section.color)
            caption.scale(0.92).move_to(DOWN * 3.02)
            return VGroup(triangle, connectors, center, glow, lens, scale, responsibility, caption)

        def beat2() -> VGroup:
            magic = label_box("magic score?", RED_NEON, 3.0, 0.9, 25).move_to(LEFT * 3.5 + UP * 0.4)
            question = label_box("disciplined\nquestion", GREEN_NEON, 3.3, 1.1, 24).move_to(RIGHT * 3.5 + UP * 0.4)
            cross = Cross(magic, stroke_width=5).set_color(RED_NEON)
            arrow = Arrow(magic.get_right(), question.get_left(), color=GREEN_NEON, buff=0.2, stroke_width=4)
            relation = make_text("training data  ↔  model behavior", YELLOW_NEON, 31, BOLD, 7.5).move_to(DOWN * 1.1)
            return VGroup(magic, cross, question, arrow, relation, stage_note("Không hỏi data nào quan trọng nhất; hỏi quan trọng theo nghĩa nào", GREEN_NEON))

        def beat3() -> VGroup:
            questions = VGroup(
                label_box("behavior nào?", BLUE_NEON, 3.0, 0.76, 21),
                label_box("intervention nào?", YELLOW_NEON, 3.0, 0.76, 21),
                label_box("data unit nào?", GREEN_NEON, 3.0, 0.76, 21),
                label_box("evaluation nào?", PURPLE_NEON, 3.0, 0.76, 21),
            ).arrange_in_grid(rows=2, cols=2, buff=0.32).move_to(UP * 0.25)
            compass = VGroup(
                chip("3 lenses", BLUE_NEON),
                chip("2 scale lessons", YELLOW_NEON),
                chip("1 responsibility principle", PURPLE_NEON),
            ).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.45)
            return VGroup(questions, compass, stage_note("Ba lens, hai bài học scale, một nguyên tắc trách nhiệm", section.color))

        return [beat1, beat2, beat3]

    # ------------------------------------------------------------------
    # p5_01
    # ------------------------------------------------------------------
    def play_four_parts(self, section: Section):
        def timeline(active: int) -> VGroup:
            specs = [
                ("Part I", "taxonomy", BLUE_NEON),
                ("Part II", "theory", GREEN_NEON),
                ("Part III", "scale", YELLOW_NEON),
                ("Part IV", "applications", RED_NEON),
            ]
            nodes = VGroup()
            for idx, (part, body, color) in enumerate(specs):
                box = label_box(f"{part}\n{body}", color, 2.55, 1.05, 22)
                if idx != active:
                    box.set_opacity(0.45)
                nodes.add(box)
            nodes.arrange(RIGHT, buff=0.55).move_to(UP * 0.35)
            arrows = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), color=GRAY_SOFT, buff=0.12) for i in range(3)])
            highlight = SurroundingRectangle(nodes[active], color=specs[active][2], buff=0.10)
            notes = [
                "Part I phân biệt evidence, credit, prediction.",
                "Part II biến trực giác thành weights, LOO, IF, datamodels.",
                "Part III hỏi estimator nào scale được và được evaluate ra sao.",
                "Part IV đưa score vào debugging, selection, valuation, security, RAG.",
            ]
            return VGroup(nodes, arrows, highlight, stage_note(notes[active], specs[active][2]))

        def beat1() -> VGroup:
            return timeline(0)

        def beat2() -> VGroup:
            return timeline(1)

        def beat3() -> VGroup:
            return timeline(2)

        def beat4() -> VGroup:
            return timeline(3)

        def beat5() -> VGroup:
            center = label_box("application\nquestion", WHITE_SOFT, 3.2, 1.15, 24)
            parts = VGroup(
                chip("taxonomy", BLUE_NEON).move_to(LEFT * 4.4 + UP * 1.15),
                chip("theory", GREEN_NEON).move_to(RIGHT * 4.0 + UP * 1.15),
                chip("scale", YELLOW_NEON).move_to(LEFT * 4.1 + DOWN * 0.75),
                chip("applications", RED_NEON).move_to(RIGHT * 4.0 + DOWN * 0.75),
            )
            arrows = VGroup(*[Arrow(part.get_center(), center.get_center(), color=part[0].get_color(), buff=1.0, stroke_width=3) for part in parts])
            return VGroup(center, parts, arrows, stage_note("Ứng dụng quyết định câu hỏi attribution", section.color))

        return [beat1, beat2, beat3, beat4, beat5]

    # ------------------------------------------------------------------
    # p5_02
    # ------------------------------------------------------------------
    def play_three_lenses(self, section: Section):
        def lens_map(active: int) -> VGroup:
            specs = [
                ("evidence", "output được hỗ trợ bởi gì?", BLUE_NEON),
                ("credit", "utility nên chia thế nào?", YELLOW_NEON),
                ("prediction", "intervention đổi behavior ra sao?", GREEN_NEON),
            ]
            center = label_box("model\nbehavior", WHITE_SOFT, 2.5, 1.0, 23)
            lenses = VGroup()
            positions = [LEFT * 4.4 + UP * 0.75, RIGHT * 4.2 + UP * 0.75, DOWN * 1.35]
            for idx, (name, body, color) in enumerate(specs):
                box = label_box(f"{name}\n{body}", color, 3.45, 1.08, 19).move_to(positions[idx])
                if idx != active:
                    box.set_opacity(0.42)
                lenses.add(box)
            arrows = VGroup(*[Arrow(center.get_center(), lens.get_center(), color=lens[0].get_color(), buff=1.15, stroke_width=3) for lens in lenses])
            warning = [
                "Evidence hỗ trợ output, nhưng không tự động là cause.",
                "Credit phụ thuộc utility và data context.",
                "Prediction phải đúng trong counterfactual chưa thấy.",
            ][active]
            return VGroup(center, lenses, arrows, stage_note(warning, specs[active][2]))

        def beat1() -> VGroup:
            return lens_map(0)

        def beat2() -> VGroup:
            return lens_map(1)

        def beat3() -> VGroup:
            return lens_map(2)

        def beat4() -> VGroup:
            lines = VGroup(
                label_box("Evidence -> support", BLUE_NEON, 3.6, 0.75, 22),
                label_box("Credit -> utility share", YELLOW_NEON, 3.6, 0.75, 22),
                label_box("Prediction -> behavior shift", GREEN_NEON, 3.9, 0.75, 22),
            ).arrange(DOWN, buff=0.24).move_to(UP * 0.15)
            return VGroup(lines, stage_note("Ba lens không cạnh tranh; chúng trả lời ba loại câu hỏi khác nhau", section.color))

        return [beat1, beat2, beat3, beat4]

    # ------------------------------------------------------------------
    # p5_03
    # ------------------------------------------------------------------
    def play_scale_lessons(self, section: Section):
        def beat1() -> VGroup:
            data = VGroup(*[data_dot(str(i), BLUE_NEON, 0.11) for i in range(1, 13)]).arrange_in_grid(rows=3, cols=4, buff=0.16).move_to(LEFT * 4.2 + UP * 0.55)
            retrain = label_box("retrain\nx millions?", RED_NEON, 3.1, 1.05, 23).move_to(RIGHT * 3.8 + UP * 0.55)
            arrow = Arrow(data.get_right(), retrain.get_left(), color=RED_NEON, buff=0.2, stroke_width=4)
            return VGroup(data, retrain, arrow, stage_note("Clean counterfactuals thường rất đắt", RED_NEON))

        def beat2() -> VGroup:
            methods = VGroup(
                label_box("Influence\nlinearize", BLUE_NEON, 2.7, 0.96, 20),
                label_box("TracIn\ntrajectory", ORANGE_SOFT, 2.7, 0.96, 20),
                label_box("TRAK\nprojection", GREEN_NEON, 2.7, 0.96, 20),
                label_box("Datamodels\nupfront runs", PURPLE_NEON, 2.7, 0.96, 20),
            ).arrange_in_grid(rows=2, cols=2, buff=0.42).move_to(UP * 0.25)
            return VGroup(methods, stage_note("Mỗi method mua tốc độ bằng một giả định hoặc proxy", section.color))

        def beat3() -> VGroup:
            evals = VGroup(
                chip("debug -> precision@k", RED_NEON),
                chip("selection -> retrain", GREEN_NEON),
                chip("unlearning -> forgetting", PURPLE_NEON),
                chip("citation -> support + faithfulness", BLUE_NEON),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(LEFT * 3.8 + UP * 0.2)
            score = label_box("score đẹp\nchưa đủ", YELLOW_NEON, 3.05, 1.1, 24).move_to(RIGHT * 3.6 + UP * 0.2)
            arrow = Arrow(evals.get_right(), score.get_left(), color=YELLOW_NEON, buff=0.22)
            return VGroup(evals, score, arrow, stage_note("Evaluation là một phần của định nghĩa method", YELLOW_NEON))

        def beat4() -> VGroup:
            question = make_text("Does this score support the right decision?", WHITE_SOFT, 33, BOLD, 10.5).move_to(UP * 0.4)
            setting = VGroup(chip("setting", BLUE_NEON), chip("behavior", GREEN_NEON), chip("decision", YELLOW_NEON), chip("risk", RED_NEON)).arrange(RIGHT, buff=0.25).next_to(question, DOWN, buff=0.7)
            return VGroup(question, setting, stage_note("Ở scale lớn, score phải phục vụ quyết định đúng", section.color))

        return [beat1, beat2, beat3, beat4]

    # ------------------------------------------------------------------
    # p5_04
    # ------------------------------------------------------------------
    def play_responsible(self, section: Section):
        checklist_items = [
            ("1", "behavior?", BLUE_NEON),
            ("2", "data unit?", GREEN_NEON),
            ("3", "intervention?", YELLOW_NEON),
            ("4", "attribution notion?", PURPLE_NEON),
            ("5", "who sees score?", RED_NEON),
            ("6", "evaluation?", CYAN_SOFT),
        ]

        def checklist(active: int) -> VGroup:
            rows = VGroup()
            for idx, (num, text, color) in enumerate(checklist_items):
                circle = Circle(radius=0.23, color=color, stroke_width=2, fill_color=color, fill_opacity=0.10)
                number = make_text(num, color, 19, BOLD, 0.4).move_to(circle)
                bullet = VGroup(circle, number)
                row = VGroup(
                    bullet,
                    make_text(text, WHITE_SOFT if idx == active else GRAY_SOFT, 24, BOLD, 4.2),
                )
                row.arrange(RIGHT, buff=0.18)
                if idx != active:
                    row.set_opacity(0.48)
                rows.add(row)
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(LEFT * 3.7 + UP * 0.15)
            principle = label_box("start from\napplication question", section.color, 4.0, 1.2, 23).move_to(RIGHT * 3.5 + UP * 0.15)
            arrow = Arrow(rows.get_right(), principle.get_left(), color=section.color, buff=0.2)
            return VGroup(rows, principle, arrow, stage_note(f"Câu hỏi {checklist_items[active][0]}: {checklist_items[active][1]}", checklist_items[active][2]))

        def beat1() -> VGroup:
            return checklist(0)

        def beat2() -> VGroup:
            return checklist(2)

        def beat3() -> VGroup:
            risk = VGroup(
                label_box("defender", GREEN_NEON, 2.5, 0.8, 22),
                label_box("attacker", RED_NEON, 2.5, 0.8, 22),
                label_box("false certainty", YELLOW_NEON, 3.1, 0.8, 21),
                label_box("not a certificate", PURPLE_NEON, 3.2, 0.8, 21),
            ).arrange_in_grid(rows=2, cols=2, buff=0.34).move_to(UP * 0.15)
            return VGroup(risk, stage_note("Score mạnh phải đi kèm governance và giới hạn rõ", RED_NEON))

        def beat4() -> VGroup:
            return checklist(5)

        def beat5() -> VGroup:
            compass = VGroup(
                chip("right lens", BLUE_NEON),
                chip("right limits", YELLOW_NEON),
                chip("right audience", PURPLE_NEON),
                chip("right evaluation", GREEN_NEON),
            ).arrange_in_grid(rows=2, cols=2, buff=0.32).move_to(UP * 0.25)
            return VGroup(compass, stage_note("Responsible attribution = dùng score đúng cách, không thần thánh hóa score", section.color))

        return [beat1, beat2, beat3, beat4, beat5]

    # ------------------------------------------------------------------
    # p5_05
    # ------------------------------------------------------------------
    def play_closing(self, section: Section):
        def beat1() -> VGroup:
            lines = VGroup(
                label_box("Evidence is not cause.", BLUE_NEON, 5.0, 0.78, 25),
                label_box("Credit is utility-dependent.", YELLOW_NEON, 5.0, 0.78, 25),
                label_box("Prediction must be evaluated counterfactually.", GREEN_NEON, 6.3, 0.78, 22),
            ).arrange(DOWN, buff=0.24).move_to(UP * 0.25)
            return VGroup(lines, stage_note("Ba câu này ngăn rất nhiều nhầm lẫn thực tế", GREEN_NEON))

        def beat2() -> VGroup:
            contexts = VGroup(
                label_box("hallucination", RED_NEON, 2.8, 0.78, 22),
                label_box("data contributors", YELLOW_NEON, 3.2, 0.78, 22),
                label_box("remove / select / unlearn", PURPLE_NEON, 4.0, 0.78, 21),
            ).arrange(DOWN, buff=0.25).move_to(LEFT * 3.7 + UP * 0.15)
            questions = VGroup(
                chip("evidence, cause, or neighbor?", BLUE_NEON),
                chip("utility + context + fairness?", YELLOW_NEON),
                chip("counterfactual behavior correct?", GREEN_NEON),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.45 + UP * 0.15)
            arrows = VGroup(*[Arrow(contexts[i].get_right(), questions[i].get_left(), color=questions[i][0].get_color(), buff=0.2) for i in range(3)])
            return VGroup(contexts, questions, arrows, stage_note("Trước khi hành động, hỏi score đang mang nghĩa nào", section.color))

        def beat3() -> VGroup:
            center = label_box("training data\n↔\nmodel behavior", WHITE_SOFT, 3.5, 1.55, 25)
            clarity = chip("clearer", BLUE_NEON).move_to(LEFT * 4.4 + UP * 1.2)
            testable = chip("testable", GREEN_NEON).move_to(RIGHT * 4.3 + UP * 1.2)
            responsible = chip("responsible", PURPLE_NEON).move_to(DOWN * 1.35)
            arrows = VGroup(
                Arrow(center.get_left(), clarity.get_right(), color=BLUE_NEON, buff=0.15),
                Arrow(center.get_right(), testable.get_left(), color=GREEN_NEON, buff=0.15),
                Arrow(center.get_bottom(), responsible.get_top(), color=PURPLE_NEON, buff=0.15),
            )
            return VGroup(center, clarity, testable, responsible, arrows, stage_note("Không phải magic score, mà là quan hệ được làm rõ và kiểm chứng", WHITE_SOFT))

        def beat4() -> VGroup:
            credit = VGroup(
                make_text("Based on", GRAY_SOFT, 24, BOLD),
                make_text("ICML 2024 Tutorial", BLUE_NEON, 31, BOLD),
                make_text("Data Attribution at Scale", WHITE_SOFT, 38, BOLD),
                make_text("Before asking which data is important,", GRAY_SOFT, 24, BOLD),
                make_text("ask important in what sense.", YELLOW_NEON, 30, BOLD),
            ).arrange(DOWN, buff=0.18).move_to(UP * 0.25)
            return VGroup(credit, stage_note("Và đó là nơi data attribution thật sự bắt đầu.", YELLOW_NEON))

        return [beat1, beat2, beat3, beat4]
