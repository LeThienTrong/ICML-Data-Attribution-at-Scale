from manim import *

config.background_color = "#171717"
config.frame_width = 16
config.frame_height = 9

WHITE_SOFT = "#E8E8E8"
GRAY_SOFT = "#9A9A9A"
BLUE_NEON = "#4DA6FF"
GREEN_NEON = "#42F59B"
YELLOW_NEON = "#FFD166"
RED_NEON = "#FF5C5C"


def title_text(text: str, size: int = 46) -> Text:
    return Text(text, font_size=size, weight=BOLD, color=WHITE_SOFT)


def label_text(text: str, color=WHITE_SOFT, size: int = 28) -> Text:
    return Text(text, font_size=size, color=color)


class IntroTaxonomy(Scene):
    def construct(self):
        title = title_text("Data Attribution at Scale", 54)
        subtitle = label_text("Connecting ML behavior to training data", BLUE_NEON, 30)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(title, shift=UP * 0.2), FadeIn(subtitle), run_time=1.2)
        self.wait(2)
        self.play(title.animate.to_edge(UP).scale(0.65), FadeOut(subtitle))

        boxes = VGroup()
        labels = [
            ("Corroborative\nEvidence", BLUE_NEON),
            ("Game-theoretic\nCredit", YELLOW_NEON),
            ("Predictive\nPrediction", GREEN_NEON),
        ]
        for text, color in labels:
            rect = RoundedRectangle(width=4.0, height=2.4, corner_radius=0.2, color=color, fill_color=color, fill_opacity=0.06)
            lab = label_text(text, color, 30)
            boxes.add(VGroup(rect, lab))
        boxes.arrange(RIGHT, buff=0.55).move_to(ORIGIN)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.25))
        self.wait(2)

        note = label_text("Different applications require different notions of attribution", WHITE_SOFT, 28)
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(2)
        self.play(FadeOut(VGroup(title, boxes, note)))
