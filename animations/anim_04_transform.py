from manim import *
import numpy as np

class LinearTransformAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#F5F7FA"

        title = Text("선형변환  Y = aX + b", font="Malgun Gothic", font_size=36, color="#1A3A6B")
        title.to_edge(UP, buff=0.35)
        self.play(Write(title))

        axes = Axes(
            x_range=[-1, 11, 1],
            y_range=[0, 0.5, 0.1],
            x_length=10,
            y_length=4.5,
            axis_config={"color": "#444455", "include_tip": True},
        ).shift(DOWN * 0.5)
        self.play(Create(axes))

        def normal(x, mu, sigma):
            return np.exp(-0.5 * ((x - mu) / sigma)**2) / (sigma * np.sqrt(2 * np.pi))

        # 원래 분포 X ~ N(2, 1)
        curve_x = axes.plot(lambda x: normal(x, 2, 1), color="#2E6DB8", stroke_width=4)
        lbl_x = Text("X ~ N(2, 1)", font="Malgun Gothic", font_size=22, color="#2E6DB8")
        lbl_x.next_to(axes.c2p(2, 0.42), UP, buff=0.08)

        self.play(Create(curve_x), Write(lbl_x))
        self.wait(0.7)

        # Y = 2X + 1 → N(5, 4)  σ=2
        curve_y = axes.plot(lambda x: normal(x, 5, 2), color="#E86A2C", stroke_width=4)
        lbl_y = Text("Y = 2X+1  ~  N(5, 4)", font="Malgun Gothic", font_size=22, color="#E86A2C")
        lbl_y.next_to(axes.c2p(5, 0.22), UP, buff=0.08)

        arrow = CurvedArrow(axes.c2p(3, 0.35), axes.c2p(4.3, 0.28),
                            color="#1A7A4A", tip_length=0.2)
        arrow_lbl = Text("Y = 2X + 1", font="Malgun Gothic", font_size=18, color="#1A7A4A")
        arrow_lbl.next_to(arrow, UP, buff=0.05)

        self.play(Create(arrow), Write(arrow_lbl))
        self.play(TransformFromCopy(curve_x, curve_y), Write(lbl_y), run_time=1.5)

        rules = VGroup(
            Text("E(Y) = 2·E(X) + 1 = 2×2 + 1 = 5",
                 font="Malgun Gothic", font_size=20, color="#1A3A6B"),
            Text("V(Y) = 2²·V(X) = 4×1 = 4",
                 font="Malgun Gothic", font_size=20, color="#1A3A6B"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)

        self.play(Write(rules))
        self.wait(2)
