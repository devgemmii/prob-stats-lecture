from manim import *

class ExpectedValueAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#F5F7FA"

        title = Text("기댓값 E(X) — 확률분포의 무게중심", font="Malgun Gothic",
                     font_size=34, color="#1A3A6B")
        title.to_edge(UP, buff=0.35)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 0.3, 0.05],
            x_length=9,
            y_length=4.0,
            axis_config={"color": "#444455", "include_tip": True, "include_numbers": False},
        ).shift(DOWN * 0.6)

        self.play(Create(axes))

        for n in range(1, 7):
            lbl = Text(str(n), font="Malgun Gothic", font_size=20, color="#444455")
            lbl.next_to(axes.c2p(n, 0), DOWN, buff=0.15)
            self.add(lbl)

        p = 1 / 6
        col = "#2E6DB8"
        for x in range(1, 7):
            bar = Rectangle(
                width=0.5,
                height=axes.y_length * p / 0.3,
                fill_color=col, fill_opacity=0.8,
                stroke_color=col, stroke_width=1.5
            )
            bar.move_to(axes.c2p(x, p / 2))
            self.play(GrowFromEdge(bar, DOWN), run_time=0.3)

        self.wait(0.4)

        ev_x = 3.5
        ev_line = DashedLine(
            start=axes.c2p(ev_x, 0),
            end=axes.c2p(ev_x, 0.27),
            color="#E86A2C", stroke_width=3, dash_length=0.15
        )
        ev_label = Text("E(X) = 3.5", font="Malgun Gothic", font_size=26, color="#E86A2C")
        ev_label.next_to(axes.c2p(ev_x, 0.27), UP, buff=0.1)

        self.play(Create(ev_line), Write(ev_label))

        formula = Text(
            "E(X) = 1×(1/6) + 2×(1/6) + 3×(1/6) + 4×(1/6) + 5×(1/6) + 6×(1/6) = 3.5",
            font="Malgun Gothic", font_size=17, color="#1A3A6B"
        )
        formula.to_edge(DOWN, buff=0.35)
        self.play(Write(formula))
        self.wait(2)
