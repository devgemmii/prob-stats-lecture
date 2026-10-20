from manim import *

class PMFAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#F5F7FA"

        title = Text("이산확률변수의 확률분포", font="Malgun Gothic", font_size=36, color="#1A3A6B")
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))

        axes = Axes(
            x_range=[-0.5, 5, 1],
            y_range=[0, 0.45, 0.1],
            x_length=9,
            y_length=4.5,
            axis_config={"color": "#444455", "include_tip": True,
                         "include_numbers": False},
        ).shift(DOWN * 0.4)

        self.play(Create(axes))

        x_nums = [0, 1, 2, 3, 4]
        for n in x_nums:
            lbl = Text(str(n), font="Malgun Gothic", font_size=20, color="#444455")
            lbl.next_to(axes.c2p(n, 0), DOWN, buff=0.15)
            self.add(lbl)

        x_label = Text("X (앞면 횟수)", font="Malgun Gothic", font_size=22, color="#444455")
        x_label.next_to(axes.x_axis, DOWN, buff=0.6)
        y_label = Text("P(X=x)", font="Malgun Gothic", font_size=20, color="#444455")
        y_label.next_to(axes.y_axis, LEFT, buff=0.15).rotate(PI / 2)
        self.add(x_label, y_label)

        data = [(0, 0.0625), (1, 0.25), (2, 0.375), (3, 0.25), (4, 0.0625)]
        colors = ["#5B9BD5", "#E86A2C", "#1A7A4A", "#E86A2C", "#5B9BD5"]
        prob_str = ["1/16", "4/16", "6/16", "4/16", "1/16"]

        for (x, p), col, pstr in zip(data, colors, prob_str):
            bar = Rectangle(
                width=0.55,
                height=axes.y_length * p / 0.45,
                fill_color=col, fill_opacity=0.85,
                stroke_color=col, stroke_width=1.5
            )
            bar.move_to(axes.c2p(x, p / 2))
            lbl = Text(pstr, font="Malgun Gothic", font_size=18, color=col)
            lbl.next_to(axes.c2p(x, p), UP, buff=0.1)
            self.play(GrowFromEdge(bar, DOWN), Write(lbl), run_time=0.55)

        note = Text("동전 4개를 던질 때 앞면 횟수 X ~ B(4, 0.5)",
                    font="Malgun Gothic", font_size=20, color="#1A3A6B")
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note))
        self.wait(2)
