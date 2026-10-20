from manim import *
import numpy as np

class PDFAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#F5F7FA"

        title = Text("연속확률변수: 넓이 = 확률", font="Malgun Gothic", font_size=36, color="#1A3A6B")
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))

        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[0, 0.5, 0.1],
            x_length=10,
            y_length=4.5,
            axis_config={"color": "#444455", "include_tip": True, "include_numbers": False},
        ).shift(DOWN * 0.5)

        self.play(Create(axes))

        def normal(x):
            return np.exp(-0.5 * x**2) / np.sqrt(2 * np.pi)

        curve = axes.plot(normal, color="#2E6DB8", stroke_width=4)
        self.play(Create(curve), run_time=1.5)

        area1 = axes.get_area(curve, x_range=[-1, 1], color="#2E6DB8", opacity=0.4)
        label1 = Text("P(-1 ≤ X ≤ 1) ≈ 68.3%", font="Malgun Gothic",
                      font_size=24, color="#1A3A6B")
        label1.move_to(axes.c2p(0, 0.22))
        self.play(FadeIn(area1), Write(label1))
        self.wait(1)

        area2L = axes.get_area(curve, x_range=[-2, -1], color="#E86A2C", opacity=0.45)
        area2R = axes.get_area(curve, x_range=[1, 2], color="#E86A2C", opacity=0.45)
        label2 = Text("P(-2 ≤ X ≤ 2) ≈ 95.4%", font="Malgun Gothic",
                      font_size=24, color="#E86A2C")
        label2.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(area2L), FadeIn(area2R), Write(label2))
        self.wait(1)

        note = Text("전체 넓이 = 1  (전체 확률의 합)", font="Malgun Gothic",
                    font_size=20, color="#1A7A4A")
        note.next_to(label2, UP, buff=0.25)
        self.play(Write(note))
        self.wait(2)
