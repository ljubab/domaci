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

class SineAndCosineCurveUnitCircle(Scene):
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
        self.cosine_start = np.array([-3, 1, 0])
        self.sine_start = np.array([-3, 0, 0])

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

        # Funkcija za pomeranje tacke oko kruga, ne diraj!!!
        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            mob.move_to(circle.point_from_proportion(self.t_offset % 1))

        # Poluprecnik koji se vrti, ne diraj!!!
        def get_line_to_circle():
            return Line(self.origin_point, dot.get_center(), color=BLUE)

        def get_cosine_line_to_curve():
            x = self.cosine_start[0] + self.t_offset * 4
            y = dot.get_center()[0] - self.origin_point[0]
            return Line(dot.get_center(), np.array([x, y, 0]), color=YELLOW_A, stroke_width=2)
        
        def get_sine_line_to_curve():
            x = self.sine_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(dot.get_center(), np.array([x, y, 0]), color=YELLOW_A, stroke_width=2)

        def cos_updater():
            return Line([self.origin_point[0], dot.get_center()[1], 0], dot.get_center(), color=GREEN)

        def sine_updater():
            newLine = Line([dot.get_center()[0], 0, 0], dot.get_center(), color=BLUE)
            return newLine

        self.cos_curve = VGroup()
        self.cos_curve.add(Line(self.cosine_start, self.cosine_start))
    
        # Ovde moras da radis tempTacku
        def add_cos_curve():
            last_line = self.cos_curve[-1]
            x = self.cosine_start[0] + self.t_offset * 4
            y = dot.get_center()[0] - self.origin_point[0]
            new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=GREEN)
            self.cos_curve.add(new_line)

            return self.cos_curve
        
        self.sine_curve = VGroup()
        self.sine_curve.add(Line(self.sine_start, self.sine_start))

        def add_sin_curve():
            last_line = self.sine_curve[-1]
            x = self.sine_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=BLUE)
            self.sine_curve.add(new_line)

            return self.sine_curve


        dot.add_updater(go_around_circle)

        cos_line = always_redraw(cos_updater)
        sine_line = always_redraw(sine_updater)

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_cosine_line_to_curve)
        dot_to_curve_line2 = always_redraw(get_sine_line_to_curve)
        cos_curve_line = always_redraw(add_cos_curve)
        sine_curve_line = always_redraw(add_sin_curve)

        self.add(dot)
        self.add(cos_line, sine_line, origin_to_circle_line, circle, dot_to_curve_line, sine_curve_line, cos_curve_line, dot_to_curve_line2)
        self.wait(8.5)

        dot.remove_updater(go_around_circle)

class Tangens(Scene):
    def construct(self):
        self.axes = Axes()
        self.add(self.axes)
        self.tangens_pocetak = np.array([2, 0, 0])

        self.trig_krug = Circle(radius=2, color=RED)
        self.play(GrowFromCenter(self.trig_krug))
        self.tackica = Dot(color=WHITE).shift(2 * RIGHT)  # tackica koja pokazuje na krugu koliki je ugao theta

        def tangens_updater(linija):
            sinus = self.tackica.get_center()[1]
            kosinus = self.tackica.get_center()[0]

            if kosinus == 0:
                linija.become(Line(self.tangens_pocetak, [2, 9, 0], color=BLUE_C))
            else:
                tangens = sinus/kosinus
                linija.become(Line(self.tangens_pocetak, [2, 2*tangens, 0], color=BLUE_C))

        def produzena_linija_updater(linija):
            sinus = self.tackica.get_center()[1]
            kosinus = self.tackica.get_center()[0]

            if kosinus == 0:
                linija.become(Line(self.tackica.get_center(), [0, 10, 0]))
            else:
                tangens = sinus/kosinus
                linija.become(Line(self.tackica.get_center(), [2, 2*tangens, 0]))

        self.produzena_linija = Line(self.tackica.get_center(), self.tackica.get_center()).add_updater(produzena_linija_updater)

        self.ugao_linijax = Line(ORIGIN, 2 * RIGHT)
        self.ugao_linijay = Line(ORIGIN, 2 * RIGHT)
        self.tangensna_osa = Line([2, -3, 0], [2, 3, 0])
        self.tangens_linija = Line([2, 0, 0], [2, 0, 0], color=BLUE_C).add_updater(tangens_updater)

        #text promenljive
        self.tangens_text = MathTex("tg \\theta", color=BLUE_C).add_updater(
            lambda t: t.next_to(self.tangens_linija.get_center(), RIGHT)
        )
        self.tg_vrednost = 0
        self.theta = MathTex("\\theta = 0").shift(4*RIGHT + 3*UP)
        self.tg_text_vrednost = MathTex("tg \\theta = " + str(self.tg_vrednost), color=BLUE_C).next_to(self.theta, DOWN)


        self.play(FadeIn(self.tackica), GrowFromCenter(self.ugao_linijax),
                  GrowFromCenter(self.ugao_linijay), FadeIn(self.tangensna_osa),
                  FadeIn(self.produzena_linija)
        )

        self.prvi_slucaj()
        self.drugi_slucaj()
        self.treci_slucaj()
        self.cetvrti_slucaj()
        self.obrisi()

    def prvi_slucaj(self):
        self.tg_vrednost = 0
        self.tg_text_vrednost = MathTex("tg\\theta = " + str(self.tg_vrednost), color=BLUE_C).next_to(self.theta, DOWN)

        self.play(Write(self.tg_text_vrednost), Write(self.theta), Write(self.tangens_text))
        self.wait(1.5)

    def drugi_slucaj(self):
        self.add(self.tangens_linija)

        #definisanje potrebnih promenljivih
        self.tg_vrednost = "?"
        theta_temp = MathTex("\\theta = \\frac{\\pi}{2}").shift(4*RIGHT+3*UP)
        tg_text_vrednost_temp = MathTex("tg\\theta = " + self.tg_vrednost, color=BLUE_C).next_to(theta_temp, DOWN)

        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2)
                  )

        self.ugao = Angle(self.ugao_linijax, self.ugao_linijay)
        self.theta_ugao = MathTex("\\theta").add_updater(
            lambda u: u.next_to(self.ugao)
        )

        self.play(FadeIn(self.ugao), Write(self.theta_ugao),
                  Transform(self.theta, theta_temp),
                  Transform(self.tg_text_vrednost, tg_text_vrednost_temp)
        )
        self.wait(1.5)

    def treci_slucaj(self):
        self.ugao.add_updater(lambda u: u.become(Angle(self.ugao_linijax, self.ugao_linijay)))
        self.add(self.ugao)

        self.tg_vrednost = 0
        theta_temp = MathTex("\\theta = \\pi").shift(4 * RIGHT + 3 * UP)
        tg_text_vrednost_temp = MathTex("tg\\theta = " + str(self.tg_vrednost), color=BLUE_C).next_to(theta_temp, DOWN)

        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Transform(self.theta, theta_temp)
                  )

        self.play(Transform(self.tg_text_vrednost, tg_text_vrednost_temp))
        self.wait(1.5)

    def cetvrti_slucaj(self):
        self.tg_vrednost = "?"
        theta_temp = MathTex("\\theta = \\frac{3\\pi}{2}").shift(4 * RIGHT + 3 * UP)
        tg_text_vrednost_temp = MathTex("tg\\theta = " + self.tg_vrednost, color=BLUE_C).next_to(theta_temp, DOWN)

        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Transform(self.theta, theta_temp)
                  )

        self.play(Transform(self.tg_text_vrednost, tg_text_vrednost_temp))
        self.wait(1.5)

    def obrisi(self):
        self.remove(self.ugao, self.tangens_linija, self.produzena_linija)
        self.play(FadeOut(self.tg_text_vrednost), FadeOut(self.theta))
        self.play(FadeOut(self.ugao_linijax), FadeOut(self.ugao_linijay),
                  FadeOut(self.theta_ugao), FadeOutToPoint(self.tackica, ORIGIN),
                  FadeOutToPoint(self.tangensna_osa, self.tangens_pocetak),
                  FadeOut(self.trig_krug), FadeOut(self.axes)
                  )


class Kotangens(Scene):
    def construct(self):
        self.axes = Axes()
        self.add(self.axes)
        self.kotangens_pocetak = np.array([0, 2, 0])

        self.trig_krug = Circle(radius=2, color=RED)
        self.play(GrowFromCenter(self.trig_krug))
        self.tackica = Dot(color=WHITE).shift(2 * RIGHT)  # tackica koja pokazuje na krugu koliki je ugao theta

        def kotangens_updater(linija):
            sinus = self.tackica.get_center()[1]
            kosinus = self.tackica.get_center()[0]

            if sinus == 0:
                linija.become(Line(self.kotangens_pocetak, [9, 2, 0], color=RED_A))
            else:
                kotangens = kosinus / sinus
                linija.become(Line(self.kotangens_pocetak, [2 * kotangens, 2, 0], color=RED_A))

        def produzena_linija_updater(linija):
            sinus = self.tackica.get_center()[1]
            kosinus = self.tackica.get_center()[0]

            if sinus == 0:
                linija.become(Line(self.tackica.get_center(), [10, 0, 0]))
            else:
                kotangens = kosinus / sinus
                linija.become(Line(self.tackica.get_center(), [2 * kotangens, 2, 0]))

        self.produzena_linija = Line(self.tackica.get_center(), self.tackica.get_center()).add_updater(
            produzena_linija_updater)

        self.ugao_linijax = Line(ORIGIN, 2 * RIGHT)
        self.ugao_linijay = Line(ORIGIN, 2 * RIGHT)
        self.kotangensna_osa = Line([-3, 2, 0], [3, 2, 0])
        self.kotangens_linija = Line([0, 2, 0], [0, 2, 0], color=RED_A).add_updater(kotangens_updater)

        # text promenljive
        self.kotangens_text = MathTex("ctg \\theta", color=RED_A).add_updater(
            lambda t: t.next_to(self.kotangens_linija.get_center(), UP)
        )
        self.ctg_vrednost = "?"
        self.theta = MathTex("\\theta = 0").shift(4 * RIGHT + 3 * UP)
        self.ctg_text_vrednost = MathTex("ctg \\theta = " + str(self.ctg_vrednost), color=BLUE_C).next_to(self.theta, DOWN)

        self.play(FadeIn(self.tackica), GrowFromCenter(self.ugao_linijax),
                  GrowFromCenter(self.ugao_linijay), FadeIn(self.kotangensna_osa),
                  FadeIn(self.produzena_linija)
                  )

        self.prvi_slucaj()
        self.drugi_slucaj()
        self.treci_slucaj()
        self.cetvrti_slucaj()
        self.obrisi()

    def prvi_slucaj(self):
        self.ctg_vrednost = "?"
        self.ctg_text_vrednost = MathTex("ctg\\theta = " + str(self.ctg_vrednost), color=RED_A).next_to(self.theta, DOWN)

        self.play(Write(self.ctg_text_vrednost), Write(self.theta), Write(self.kotangens_text))
        self.wait(1.5)

    def drugi_slucaj(self):
        self.add(self.kotangens_linija)

        # definisanje potrebnih promenljivih
        self.ctg_vrednost = 0
        theta_temp = MathTex("\\theta = \\frac{\\pi}{2}").shift(4 * RIGHT + 3 * UP)
        ctg_text_vrednost_temp = MathTex("ctg\\theta = " + str(self.ctg_vrednost), color=RED_A).next_to(theta_temp, DOWN)

        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2)
                  )

        self.ugao = Angle(self.ugao_linijax, self.ugao_linijay)
        self.theta_ugao = MathTex("\\theta").add_updater(
            lambda u: u.next_to(self.ugao)
        )

        self.play(FadeIn(self.ugao), Write(self.theta_ugao),
                  Transform(self.theta, theta_temp),
                  Transform(self.ctg_text_vrednost, ctg_text_vrednost_temp)
                  )
        self.wait(1.5)

    def treci_slucaj(self):
        self.ugao.add_updater(lambda u: u.become(Angle(self.ugao_linijax, self.ugao_linijay)))
        self.add(self.ugao)

        self.ctg_vrednost = "?"
        theta_temp = MathTex("\\theta = \\pi").shift(4 * RIGHT + 3 * UP)
        ctg_text_vrednost_temp = MathTex("ctg\\theta = " + str(self.ctg_vrednost), color=RED_A).next_to(theta_temp, DOWN)

        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Transform(self.theta, theta_temp)
                  )

        self.play(Transform(self.ctg_text_vrednost, ctg_text_vrednost_temp))
        self.wait(1.5)
    
    def cetvrti_slucaj(self):
        self.ctg_vrednost = 0
        theta_temp = MathTex("\\theta = \\frac{3\\pi}{2}").shift(4 * RIGHT + 3 * UP)
        ctg_text_vrednost_temp = MathTex("ctg\\theta = " + str(self.ctg_vrednost), color=RED_A).next_to(theta_temp, DOWN)

        self.play(Rotating(self.tackica, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Rotating(self.ugao_linijay, about_point=ORIGIN, radians=PI / 2, run_time=2),
                  Transform(self.theta, theta_temp)
                  )

        self.play(Transform(self.ctg_text_vrednost, ctg_text_vrednost_temp))
        self.wait(1.5)

    def obrisi(self):
        self.remove(self.ugao, self.kotangens_linija, self.produzena_linija)
        self.play(FadeOut(self.ctg_text_vrednost), FadeOut(self.theta))
        self.play(FadeOut(self.ugao_linijax), FadeOut(self.ugao_linijay),
                  FadeOut(self.theta_ugao), FadeOutToPoint(self.tackica, ORIGIN),
                  FadeOutToPoint(self.kotangensna_osa, self.kotangens_pocetak),
                  FadeOut(self.trig_krug), FadeOut(self.axes)
                  )

class Kosinus(Scene):
    def construct(self):
        self.axes = Axes()
        self.add(self.axes)

        #definicija promenljivih
        self.trig_krug = Circle(radius=2, color=RED)
        self.play(GrowFromCenter(self.trig_krug))
        self.tackica = Dot(color=WHITE).shift(2*RIGHT) #tackica koja pokazuje na krugu koliki je ugao theta

        self.ugao_linijax = Line(ORIGIN, 2*RIGHT)
        self.ugao_linijay = Line(ORIGIN, 2*RIGHT)

        self.add(self.ugao_linijax, self.ugao_linijay)

        def cos_updater(linija): #updater funkcija za liniju koja prikazuje duzinu kosinusa
            linija.become(Line(ORIGIN, [self.tackica.get_center()[0], 0, 0], color = YELLOW))

        #kosinus linija i odgovarajuci text
        self.cos_linija = Line(ORIGIN, 2*RIGHT, color = YELLOW).add_updater(cos_updater)
        self.cos_text_linija = MathTex("\\cos\\theta", color=YELLOW).add_updater(
            lambda c: c.next_to(self.cos_linija.get_center(), DOWN)
        )

        #text u gornjem desnom uglu
        self.cos_vrednost = 1
        self.theta_text = MathTex("\\theta = 0").shift(3*RIGHT+3*UP)
        self.cos_text_vrednost = MathTex("\\cos\\theta = " + str(self.cos_vrednost), color=YELLOW).next_to(self.theta_text, DOWN)

        self.prvi_slucaj()
        self.drugi_slucaj()
        self.treci_slucaj()
        self.cetvrti_slucaj()
        self.obrisi()
        self.prikazi_grafik()


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

    def obrisi(self):
        self.remove(self.ugao, self.theta)
        self.play(FadeOut(self.cos_text_vrednost), FadeOut(self.theta_text))
        self.play(FadeOut(self.ugao_linijax), FadeOut(self.ugao_linijay),
                  FadeOut(self.cos_text_linija), FadeOut(self.cos_linija), FadeOutToPoint(self.tackica, ORIGIN),
                  FadeOut(self.trig_krug), FadeOut(self.axes)
                  )
        self.wait(1)

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

        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            mob.move_to(circle.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(self.origin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[0] - self.origin_point[0]
            return Line(dot.get_center(), np.array([x, y, 0]), color=YELLOW_A, stroke_width=2)

        def cos_updater():
            return Line(self.origin_point, [dot.get_center()[0], 0, 0], color=GREEN)

        self.curve = VGroup().move_to([-1, 0, 0])
        self.curve.add(Line(self.curve_start, self.curve_start))

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

    def add_x_labels(self):
        x_labels = [
            MathTex("\pi"), MathTex("2 \pi"),
            MathTex("3 \pi"), MathTex("4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-1 + 2 * i, 0, 0]), DOWN)
            self.add(x_labels[i])

class TangensGrafik(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            y_min=-10,
            y_max=10,
            x_max=10,
            x_min=-10,
            x_axis_config={"tick_frequency": 1},
            y_axis_config={"tick_frequency": 1},
            graph_origin= ORIGIN,
            **kwargs
        )
    def construct(self):
        self.setup_axes()
        tan_function = lambda x: np.tan(x)
        tan_graph = VGroup()
        approx_factor = 0.934
        for n in range(-1,2):
            graph = self.get_graph(tan_function, 
                                    color = RED,
                                    x_min = (-PI/2)*approx_factor+n*PI,
                                    x_max = (PI/2)*approx_factor+n*PI
                                    )
            tan_graph.add(graph)
        
        self.play(
            Create(tan_graph),
        )
        self.wait()

class KotangensGrafik(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            y_min=-10,
            y_max=10,
            x_max=10,
            x_min=-10,
            x_axis_config={"tick_frequency": 1},
            y_axis_config={"tick_frequency": 1},
            graph_origin= ORIGIN,
            **kwargs
        )
    def construct(self):
        self.setup_axes()
        tan_function = lambda x: -np.tan(x)
        tan_graph = VGroup()
        approx_factor = 0.934
        for n in range(-1,2):
            graph = self.get_graph(tan_function, 
                                    color = RED,
                                    x_min = (-PI/2)*approx_factor+n*PI,
                                    x_max = (PI/2)*approx_factor+n*PI
                                    )
            tan_graph.add(graph)
        
        self.play(
            Create(tan_graph),
        )
        self.wait()