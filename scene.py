from manim import *

class SineCurveUnitCircle(Scene):
    def construct(self):
        self.show_axis()
        self.show_circle()
        self.prikazi_grafik()
    
    def show_axis(self):
        # Kreira pocetnu i krajnju kordinatu x ose
        x_start = np.array([-6, 0, 0])
        x_end = np.array([6, 0, 0])

        # Analogno kao za x osu
        y_start = np.array([-4, -2, 0])
        y_end = np.array([-4, 2, 0])

        # Prikazuje na ekraj linije kreirane povlacenjem ovih tacaka
        self.add(Line(x_start, x_end), Line(y_start, y_end))
        self.add_x_labels()

        # U objekat self, stavljamo vrednost origin_point i curve_start za dalje koriscenje
        self.origin_point = np.array([-4, 0, 0])
        self.curve_start = np.array([-3, 0, 0])
    
    def add_x_labels(self):
        # Ova funkcija dodaje pi, 2*pi ispod x ose
        x_labels = [
            MathTex("\pi"), MathTex("2 \pi"),
            MathTex("3 \pi"), MathTex("4 \pi")
        ]

        for i in range(len(x_labels)):
            # np.array je zapravo mobject, sto znaci u odnosu na tu kordinatu on spusta mobject ka dole
            x_labels[i].next_to(np.array([-1 + 2*i, 0, 0]), DOWN)
            self.add(x_labels[i])
    
    def show_circle(self):
        # Kreira krug
        circle = Circle(radius=1)
        circle.move_to(self.origin_point)
        self.play(GrowFromCenter(circle))
        self.circle = circle
    
    def prikazi_grafik(self):
        self.origin_point = np.array([-4, 0, 0])
        self.curve_start = np.array([-3, 0, 0])

        x_start = np.array([-6, 0, 0])
        x_end = np.array([6, 0, 0])

        y_start = np.array([-4, -2, 0])
        y_end = np.array([-4, 2, 0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        circle = Circle(radius=1)
        circle.move_to(self.origin_point)

        self.play(FadeIn(circle), FadeIn(x_axis), FadeIn(y_axis))

        self.add_x_labels()
        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(circle.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            mob.move_to(circle.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(self.origin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(dot.get_center(), np.array([x, y, 0]), color=YELLOW_A, stroke_width=2)

        def sine_updater():
            newLine = Line([dot.get_center()[0], 0, 0], dot.get_center(), color=GREEN)
            return newLine

        self.curve = VGroup()
        self.curve.add(Line(self.curve_start, self.curve_start))
        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=GREEN)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)

        sine_line = always_redraw(sine_updater)
        sin_theta = MathTex("\\sin\\theta", color=BLUE).next_to(sine_line, RIGHT).scale(0.8)
        sin_theta.add_updater(lambda s: s.next_to(sine_line, RIGHT)).scale(0.8)

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(dot)
        self.add(sine_line, sin_theta, origin_to_circle_line, circle, dot_to_curve_line, sine_curve_line)
        self.wait(8.5)

        dot.remove_updater(go_around_circle)
    
class KosinusGranicniSlucajevi(Scene):
    def construct(self):
        axes = Axes()
        self.add(axes)

        #definicija promenljivih
        trig_krug = Circle(radius=2, color=RED)
        self.play(GrowFromCenter(trig_krug))
        self.tackica = Dot(color=WHITE).shift(2*RIGHT) #tackica koja pokazuje na krugu koliki je ugao theta

        self.ugao_linijax = Line(ORIGIN, 2*RIGHT)
        self.ugao_linijay = Line(ORIGIN, 2*RIGHT)

        self.add(self.ugao_linijax, self.ugao_linijay)

        def cos_updater(linija): #updater funkcija za liniju koja prikazuje duzinu kosinusa
            linija.become(Line(ORIGIN, [self.tackica.get_center()[0], 0, 0], color = YELLOW))

        #kosinus linija i odgovarajuci text
        self.cos_linija = Line(ORIGIN, 2*RIGHT, color = YELLOW).add_updater(cos_updater)
        self.cos_text_linija = MathTex("\\cos\\theta", color=YELLOW).add_updater(lambda c: c.next_to(self.cos_linija.get_center(), DOWN))

        #text u gornjem desnom uglu
        self.cos_vrednost = 1
        self.theta_text = MathTex("\\theta = 0").shift(3*RIGHT+3*UP)
        self.cos_text_vrednost = MathTex("\\cos\\theta = " + str(self.cos_vrednost), color=YELLOW).next_to(self.theta_text, DOWN)

        self.prvi_slucaj()
        self.drugi_slucaj()
        self.treci_slucaj()
        self.cetvrti_slucaj()

    def prvi_slucaj(self):
        self.play(GrowFromPoint(self.cos_linija, ORIGIN), Write(self.cos_text_linija), FadeIn(self.tackica))
        self.play(Write(self.theta_text), Write(self.cos_text_vrednost))
        self.wait(1.5)


    def drugi_slucaj(self):
        #rotiramo tacku do ugla od pi/2
        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2)
        )

        self.ugao = Angle(self.ugao_linijax, self.ugao_linijay) #definisemo ugao

        #pomocne promenljive u koje pretvaramo text kako bi animacije lepse izgledale
        self.cos_vrednost = 0
        self.theta = MathTex("\\theta").next_to(self.ugao)
        theta_text_temp = MathTex("\\theta = \\frac{\\pi}{2}").shift(3*RIGHT+3*UP)
        cos_text_vrednost_temp = MathTex("\\cos\\theta = " + str(self.cos_vrednost), color=YELLOW).next_to(theta_text_temp, DOWN)

        self.play(FadeIn(self.ugao), Write(self.theta), Transform(self.theta_text, theta_text_temp))
        self.play(Transform(self.cos_text_vrednost, cos_text_vrednost_temp))

        self.wait(1.5)

    def treci_slucaj(self):
        self.ugao.add_updater(lambda u: u.become(Angle(self.ugao_linijax, self.ugao_linijay)))
        self.theta.add_updater(
            lambda t: t.next_to(self.ugao)
        )
        self.add(self.ugao, self.theta)

        self.cos_vrednost = -1
        theta_text_temp = MathTex("\\theta = \\pi").shift(3*RIGHT+3*UP)
        cos_text_vrednost_temp = MathTex("\\cos\\theta = " + str(self.cos_vrednost), color=YELLOW).next_to(theta_text_temp, DOWN)

        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI/2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Transform(self.theta_text, theta_text_temp)
                  )
        self.play(Transform(self.cos_text_vrednost, cos_text_vrednost_temp))
        self.wait(1.5)

    def cetvrti_slucaj(self):
        self.ugao.add_updater(lambda u: u.become(Angle(self.ugao_linijax, self.ugao_linijay)))
        self.theta.add_updater(
            lambda t: t.next_to(self.ugao)
        )
        self.add(self.ugao, self.theta)

        self.cos_vrednost = 0
        theta_text_temp = MathTex("\\theta = \\frac{3\\pi}{2}").shift(3 * RIGHT + 3 * UP)
        cos_text_vrednost_temp = MathTex("\\cos\\theta = " + str(self.cos_vrednost), color=YELLOW).next_to(
            theta_text_temp, DOWN)

        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Transform(self.theta_text, theta_text_temp)
                  )
        self.play(Transform(self.cos_text_vrednost, cos_text_vrednost_temp))
        self.wait(1.5)

class CosineCurveUnitCircle(Scene):
    def construct(self):
        self.show_axis()
        self.show_circle()
        self.prikazi_grafik()
    
    def show_axis(self):
        # Kreira pocetnu i krajnju kordinatu x ose
        x_start = np.array([-6, 0, 0])
        x_end = np.array([6, 0, 0])

        # Analogno kao za x osu
        y_start = np.array([-4, -2, 0])
        y_end = np.array([-4, 2, 0])

        # Prikazuje na ekraj linije kreirane povlacenjem ovih tacaka
        self.add(Line(x_start, x_end), Line(y_start, y_end))
        self.add_x_labels()

        # U objekat self, stavljamo vrednost origin_point i curve_start za dalje koriscenje
        self.origin_point = np.array([-4, 0, 0])
        self.curve_start = np.array([-3, 10, 0])
    
    def add_x_labels(self):
        # Ova funkcija dodaje pi, 2*pi ispod x ose
        x_labels = [
            MathTex("\pi"), MathTex("2 \pi"),
            MathTex("3 \pi"), MathTex("4 \pi")
        ]

        for i in range(len(x_labels)):
            # np.array je zapravo mobject, sto znaci u odnosu na tu kordinatu on spusta mobject ka dole
            x_labels[i].next_to(np.array([-1 + 2*i, 0, 0]), DOWN)
            self.add(x_labels[i])
    
    def show_circle(self):
        # Kreira krug
        circle = Circle(radius=1)
        circle.move_to(self.origin_point)
        self.play(GrowFromCenter(circle))
        self.circle = circle
    
    def prikazi_grafik(self):
        self.origin_point = np.array([-4, 0, 0])
        self.curve_start = np.array([-3, 1, 0])

        x_start = np.array([-6, 0, 0])
        x_end = np.array([6, 0, 0])

        y_start = np.array([-4, -2, 0])
        y_end = np.array([-4, 2, 0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        circle = Circle(radius=1)
        circle.move_to(self.origin_point)

        self.play(FadeIn(circle), FadeIn(x_axis), FadeIn(y_axis))

        self.add_x_labels()
        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(circle.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        # def dajTacku():
        #     temp = self.t_offset + 0.25;
        #     temp %= 1
        #     return circle.point_from_proportion(temp)

        # Funkcija za pomeranje tacke oko kruga, ne diraj!!!
        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            mob.move_to(circle.point_from_proportion(self.t_offset % 1))

        # Poluprecnik koji se vrti, ne diraj!!!
        def get_line_to_circle():
            return Line(self.origin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[0] - self.origin_point[0]
            return Line(dot.get_center(), np.array([x, y, 0]), color=YELLOW_A, stroke_width=2)

        def cos_updater():
            return Line(self.origin_point, [dot.get_center()[0], 0, 0], color=GREEN)

        self.curve = VGroup()
        self.curve.add(Line(self.curve_start, self.curve_start))
    
        # Ovde moras da radis tempTacku
        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[0] - self.origin_point[0]
            new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=GREEN)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)

        cos_line = always_redraw(cos_updater)
        cos_theta = MathTex("\\cos\\theta", color=BLUE).next_to(cos_line, RIGHT).scale(0.8)
        cos_theta.add_updater(lambda s: s.next_to(cos_line, RIGHT)).scale(0.8)

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(dot)
        self.add(cos_line, cos_theta, origin_to_circle_line, circle, dot_to_curve_line, sine_curve_line)
        self.wait(8.5)

        dot.remove_updater(go_around_circle)

class SinusGranicniSlucajevi(Scene):
    def construct(self):
        axes = Axes()
        self.add(axes)

        #definicija promenljivih
        trig_krug = Circle(radius=2, color=RED)
        self.play(GrowFromCenter(trig_krug))
        self.tackica = Dot(color=WHITE).shift(2*RIGHT) #tackica koja pokazuje na krugu koliki je ugao theta

        self.ugao_linijax = Line(ORIGIN, 2*RIGHT)
        self.ugao_linijay = Line(ORIGIN, 2*RIGHT)

        self.add(self.ugao_linijax, self.ugao_linijay)

        def sin_updater(linija): #updater funkcija za liniju koja prikazuje duzinu kosinusa
            linija.become(Line(ORIGIN, [0, self.tackica.get_center()[1], 0], color = YELLOW))

        #kosinus linija i odgovarajuci text
        self.sin_linija = Line(ORIGIN, 2*RIGHT, color = YELLOW).add_updater(sin_updater)
        self.sin_text_linija = MathTex("\\sin\\theta", color=YELLOW).add_updater(lambda c: c.next_to(self.sin_linija.get_center(), DOWN))

        #text u gornjem desnom uglu
        self.sin_vrednost = 0
        self.theta_text = MathTex("\\theta = 0").shift(3*RIGHT+3*UP)
        self.sin_text_vrednost = MathTex("\\sin\\theta = " + str(self.sin_vrednost), color=YELLOW).next_to(self.theta_text, DOWN)

        self.prvi_slucaj()
        self.drugi_slucaj()
        self.treci_slucaj()
        self.cetvrti_slucaj()

    def prvi_slucaj(self):
        self.play(GrowFromPoint(self.sin_linija, ORIGIN), Write(self.sin_text_linija), FadeIn(self.tackica))
        self.play(Write(self.theta_text), Write(self.sin_text_vrednost))
        self.wait(1.5)


    def drugi_slucaj(self):
        #rotiramo tacku do ugla od pi/2
        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2)
        )

        self.ugao = Angle(self.ugao_linijax, self.ugao_linijay) #definisemo ugao

        #pomocne promenljive u koje pretvaramo text kako bi animacije lepse izgledale
        self.sin_vrednost = 1
        self.theta = MathTex("\\theta").next_to(self.ugao)
        theta_text_temp = MathTex("\\theta = \\frac{\\pi}{2}").shift(3*RIGHT+3*UP)
        sin_text_vrednost_temp = MathTex("\\sin\\theta = " + str(self.sin_vrednost), color=YELLOW).next_to(theta_text_temp, DOWN)

        self.play(FadeIn(self.ugao), Write(self.theta), Transform(self.theta_text, theta_text_temp))
        self.play(Transform(self.sin_text_vrednost, sin_text_vrednost_temp))

        self.wait(1.5)

    def treci_slucaj(self):
        self.ugao.add_updater(lambda u: u.become(Angle(self.ugao_linijax, self.ugao_linijay)))
        self.theta.add_updater(
            lambda t: t.next_to(self.ugao)
        )
        self.add(self.ugao, self.theta)

        self.sin_vrednost = 0
        theta_text_temp = MathTex("\\theta = \\pi").shift(3*RIGHT+3*UP)
        sin_text_vrednost_temp = MathTex("\\sin\\theta = " + str(self.sin_vrednost), color=YELLOW).next_to(theta_text_temp, DOWN)

        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI/2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Transform(self.theta_text, theta_text_temp)
                  )
        self.play(Transform(self.sin_text_vrednost, sin_text_vrednost_temp))
        self.wait(1.5)

    def cetvrti_slucaj(self):
        self.ugao.add_updater(lambda u: u.become(Angle(self.ugao_linijax, self.ugao_linijay)))
        self.theta.add_updater(
            lambda t: t.next_to(self.ugao)
        )
        self.add(self.ugao, self.theta)

        self.sin_vrednost = -1
        theta_text_temp = MathTex("\\theta = \\frac{3\\pi}{2}").shift(3 * RIGHT + 3 * UP)
        sin_text_vrednost_temp = MathTex("\\sin\\theta = " + str(self.sin_vrednost), color=YELLOW).next_to(
            theta_text_temp, DOWN)

        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Transform(self.theta_text, theta_text_temp)
                  )
        self.play(Transform(self.sin_text_vrednost, sin_text_vrednost_temp))
        self.wait(1.5)