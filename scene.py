from manim import *

# Ovo je manje vise kopi pejstovan kod, medjutim doradicemo ga

class SineCurveUnitCircle(Scene):
    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()
    
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
    
    def move_dot_and_draw_curve(self):
        # varijabla orbit sluzi samo da bismo izbegli stalo pisanje self.circle
        orbit = self.circle
        origin_point = self.origin_point

        dot = Dot(radius=0.08, color=YELLOW)
        # Neki mudri ljudi sa redita su rekli da je funkcija point_from_proportion zapravo prati ivice odredjenog mobjecta
        # point_from_proportion(0) zapravo pokazuje 0 stepeni, a point_from_proportion(1) pokazuje na 360 
        dot.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            # dt varijabla zapravo kaze koliko cesto cemo da pomeramo objekat
            # moze da ima dve vrednost: 0 i 1
            # Ovo (dt * rate) zapravo kaze pomeri ga za rate ako pomeras
            self.t_offset += (dt * rate)
            self.t_offset %= 1
            # modulo 1 u pajtonu zapravo izvlaci decimale iz broja
            mob.move_to(orbit.point_from_proportion(self.t_offset))
        
        def sine_updater():
            newLine = Line([dot.get_center()[0], 0, 0], dot.get_center(), color=BLUE)
            return newLine
        
        def get_line_to_circle():
            return Line(origin_point, dot.get_center(), color=PINK)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(dot.get_center(), np.array([x, y, 0]), color=ORANGE, stroke_width=3)

        self.curve = VGroup()
        self.curve.add(Line(self.curve_start, self.curve_start))

        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=BLUE)
            self.curve.add(new_line)

            return self.curve
        

        sine_line = always_redraw(sine_updater)
        sin_theta = MathTex("\\sin\\theta", color=BLUE).next_to(sine_line, RIGHT).scale(0.8)
        sin_theta.add_updater(lambda s: s.next_to(sine_line, RIGHT)).scale(0.8)

        lajna = Line(origin_point, [origin_point[0]+1, origin_point[1], origin_point[2]], color=GREEN)
        origin_to_circle_line = Line(origin_point, [origin_point[0]+1.5, origin_point[1]+0.5, origin_point[2]])
        origin_to_circle_line = always_redraw(get_line_to_curve)
        angle = Angle(origin_to_circle_line, lajna)

        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        angle = Angle(origin_to_circle_line, lajna)
        dot.add_updater(go_around_circle)

        self.add(origin_to_circle_line, sine_line, angle, sin_theta, dot, dot_to_curve_line, sine_curve_line)

        self.wait(8.5)

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