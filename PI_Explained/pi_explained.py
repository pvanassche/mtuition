#-----------------------------------------------------------------------------
# 
#  Copyright (c) 2025 - Piet Vanassche
#
#  Explainer on how to derive the PI control law from first principles.
#  Created using the community version of Manim.
#
#-----------------------------------------------------------------------------

from manim import *
from manim_voiceover import VoiceoverScene
#from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.azure import AzureService

class PIExplained(VoiceoverScene):
    def add_title(self, title):
        self.title = title
        self.add(title)

    def clear_canvas(self):
        fade_scene = Group(*self.mobjects)
        fade_scene.remove(self.title)
        self.play(FadeOut(fade_scene))

    def construct(self):
        #self.set_speech_service(GTTSService(lang="en", tld="com"))
        self.set_speech_service(
            AzureService(
                voice="en-US-AlloyTurboMultilingualNeural",
                style="default",  
                global_speed=1.0,
            )
        )
        fs = 90

        title = Title("PI Control Explained")

        #--------------------------------------------------------------------
        # SCENE 1
        #--------------------------------------------------------------------
        # Core equations of PI control algorithm
        #
        eq1 = Tex(r'$\frac{\text{d}x}{\text{d}t}$', r'=', r'$u_{cmd}$', r'$-u_{load}$', font_size=fs)
        eq2 = Tex(r'$\left.\frac{\text{d}x}{\text{d}t}\right|_{sp}$', r'=', r'$\frac{x_{sp}-x}{\tau}$', font_size=fs)
        eq12 = Tex(r'$\frac{\text{d}x}{\text{d}t}$', r'$\left.\frac{\text{d}x}{\text{d}t}\right|_{sp}$', font_size=fs)
        eq3 = Tex(r'$u_{cmd}$', r'$-u_{load}$', r'=', r'$\frac{x_{sp}-x}{\tau}$', font_size=fs)
        eq4 = Tex(r'$+\hat{u}_{load}$', font_size=fs)

        #self.add(index_labels(t3[0]))
        #self.add(index_labels(t3[1]))

        eq1[2].set_color(BLUE)
        eq1[3].set_color(RED)
        eq2[2].set_color(YELLOW)
        eq3[0].set_color(BLUE)
        eq3[1].set_color(RED)
        eq3[3].set_color(YELLOW)
        eq4[0].set_color(RED)

        eq1.shift(1.5*UP)
        eq2.next_to(eq1, 1.5*DOWN)
        eq3.next_to(eq2, 2.5*DOWN)

        eq1g1 = VGroup(eq1[0],eq1[1],eq1[2])
        eq1g2 = VGroup(eq1[2],eq1[3])
        eq3g = VGroup(eq3[0],eq3[1])
        res = VGroup(eq3[0], eq3[2], eq3[3], eq4[0])

        eq1[1].shift(1.5*RIGHT)
        eq2[1].align_to(eq1[1], LEFT)
        eq3[2].align_to(eq2[1], LEFT)

        eq1[0].next_to(eq1[1], LEFT)
        eq1g2.next_to(eq1[1], RIGHT)
        eq2[0].next_to(eq2[1], LEFT)
        eq2[2].next_to(eq2[1], RIGHT)
        eq3g.next_to(eq3[2], LEFT)
        eq3[3].next_to(eq3[2], RIGHT)
        eq4[0].next_to(eq3[3], RIGHT)
        eq12[0].next_to(eq3[2], LEFT)
        eq12[1].next_to(eq3[2], RIGHT)

        self.add_title(title)
        self.wait(1.0)
        with self.voiceover(text=
                """This clip introduces a simple and intuitive derivation of the control law
                    governing a P-I controller. To do so, we model both the actual,
                    open-loop behaviour of the system to-be-controlled as well as the desired, closed-loop
                    behaviour of system and controller combined. The control law derives from the
                    requirement that actual and desired behavior must conincide.
                """
            ):
            self.wait(0.1)
        self.wait(1.0)
        with self.voiceover(text=
                """So, Let's start with the equation that models the actual, 
                   open-loop behavior of the system to-be-controlled.
                   A P-I controller assumes this to be an integrator with 
                   <bookmark mark='X'/>x capturing the
                   system's output behaviour and 
                   <bookmark mark='U'/>u the input that is applied.
                   The input can be further decomposed in a command imposed by the controller
                   <bookmark mark='L'/>and a load component which the controller will need to compensate for."""
            ):
            self.play(Write(eq1g1))
            self.wait_until_bookmark("X")
            self.play(Indicate(eq1g1[0], color=WHITE))
            self.wait_until_bookmark("U")
            self.play(Indicate(eq1g1[2], color=BLUE))
            self.wait_until_bookmark("L")
            self.play(Write(eq1[3]))
        self.wait(1.0)
        with self.voiceover(text=
                """Our second equation models the desired closed-loop behavior.
                   The P-I controller shapes this to be a simple first-order response."""
            ):
            self.play(Write(eq2))
        self.wait(0.5)
        with self.voiceover(text=
                """The control law derives from requiring the actual and desired behavior to equal 
                   each other."""
            ):
            self.play(Write(eq3[2]))
            self.play(TransformFromCopy(eq1[0],eq12[0]))
            self.play(TransformFromCopy(eq2[0],eq12[1]))
        self.wait(0.5)
        with self.voiceover(text=
                """Through substitution 
                   <bookmark mark='A'/>and rearranging the result 
                   <bookmark mark='B'/>we get the fundamental law governing the PI controller."""
            ):
            self.play(FadeOut(eq12[0]), TransformFromCopy(eq1g2,eq3g))
            self.play(FadeOut(eq12[1]), TransformFromCopy(eq2[2],eq3[3]))
            self.wait_until_bookmark("A")
            self.play(Transform(eq3[1],eq4[0]))
            self.play(eq3[0].animate.next_to(eq3[2], LEFT))

            box = SurroundingRectangle(res, color=WHITE, buff=MED_LARGE_BUFF)
            self.wait_until_bookmark("B")
            self.play(Create(box))
        self.wait(0.5)
        with self.voiceover(text=
            """"Let's have a closer look at the components in the command applied by the controller.
                <bookmark mark="P"/>The yellow component is proportional to the error between the
                desired output and the actual output. This is the controller's 
                proportional action which is designed to get the system on track.
                <bookmark mark="I"/>The red component compensates for any external load. This component 
                corresponds to the controller's integral action which is designed to keep the system 
                on track. The hat on top of this variable indicates that it represents a
                best effort estimate of the load. The details on how this estimate is derived will be
                explained later. 
            """):
            box_c = box.copy().set_color(DARK_BLUE)
            self.play(ShowPassingFlash(box_c, run_time=2, time_width=0.5))
            self.wait_until_bookmark("P")
            self.play(Indicate(eq3[3], color=YELLOW))
            self.wait_until_bookmark("I")
            self.play(Indicate(eq4[0], color=RED))
        self.wait(1.0)

        #--------------------------------------------------------------------
        # SCENE 2
        #--------------------------------------------------------------------
        # Core equations blockdiagram using TikZ
        #
        self.next_section()
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{tikz}")
        template.add_to_preamble(r"\usetikzlibrary{shapes,arrows,positioning,calc}")
        template.add_to_document(
        r"""\tikzset{
                block/.style = {draw, rectangle, minimum height=3em, minimum width=3em},
                gain/.style  = {draw, thick, isosceles triangle, minimum height = 3em, isosceles triangle apex angle=60},                
                tmp/.style  = {coordinate}, 
                sum/.style= {draw, circle, node distance=1cm},
                input/.style = {coordinate},
                output/.style= {coordinate},
                pinstyle/.style = {pin edge={to-,thin,black}}
            }""")

        diagram = MathTex(r"""[auto, node distance=2cm,>=latex]
            \node (sp) {\LARGE{$x_{sp}$}};
            \node [below of=sp, node distance=1.5cm] (pv) {\LARGE{$x$}};
            \node [sum, right of=sp, node distance=1.5cm] (err) {};
            \draw [->] (sp) -- node[pos=0.99]{$+$} (err);
            \draw [->] (pv) -| node[pos=0.99]{$-$} (err);

            \node [gain, right of=err, node distance=1.5cm] (p_action) {\Large{$\frac{1}{\tau}$}};
            \draw [->] (err) -- (p_action);

            \node [sum, right of=p_action, node distance=2.0cm] (mv_aux) {};
            \node [input, below of=mv_aux, node distance=1.25cm] (mv_i) {};
            \node [output, right of=mv_aux, node distance=2.0cm] (mv) {};

            \draw [->] (p_action) -- node[pos=0.99]{$+$} (mv_aux);
            \draw [->] (mv_i) node[below]{\LARGE{$\hat{u}_{load}$}} -- node[pos=0.99]{$+$} (mv_aux);
            \draw [->] (mv_aux) --  (mv) node[right]{\LARGE{$u_{cmd}$}};                                       
                                      
            %\node [block, above of=controller,node distance=1.3cm] (up){$\frac{k_{i\beta}}{s}$};
            %\node [block, below of=controller,node distance=1.3cm] (rate) {$sk_{d\beta}$};
            %\node [block, above = 2cm of sum2](extra){$\frac{1}{\alpha_{\beta2}}$};
            %\node [block, right of=sum2,node distance=2cm] (system){$\frac{a_{\beta 2}}{s+a_{\beta 1}}$};
            %\node [output, right of=system, node distance=2cm] (output) {};
            %\node [tmp, below of=controller] (tmp1){$H(s)$};
            """,
            stroke_width=2, 
            tex_environment="tikzpicture", 
            tex_template=template )

        diagram.scale(0.7)
        diagram.shift(0.5*DOWN)

        labels = index_labels(diagram[0])
        labels.z_index = 1
        #self.add(labels)

        p_action = VGroup(diagram[0][0:11], diagram[0][15:17], diagram[0][11:15], diagram[0][18:21])
        p_action.set_color(YELLOW)
        i_action = VGroup(diagram[0][23:29], diagram[0][23:29], diagram[0][21:23], diagram[0][29])
        i_action.set_color(RED)
        u_cmd = VGroup(diagram[0][17], diagram[0][30:])
        u_cmd.set_color(BLUE)

        with self.voiceover(text=
                """It is straightforward to draw these equations as a block diagram.
                   <bookmark mark='P'/>There is the proportional action that acts on the control error to get the 
                      system on track.
                   <bookmark mark='I'/>There is the integral action that adds an estimate for the external load.
                   <bookmark mark='U'/>Combined together, they produce the actuator's command value. 
                """
            ):
            self.clear_canvas()
            self.wait_until_bookmark("P")
            self.play(Create(p_action), run_time=2.5)
            self.wait_until_bookmark("I")
            self.play(Create(i_action), run_time=2.0)
            self.wait_until_bookmark("U")
            self.play(Create(u_cmd), run_time=1.5)
        self.wait(1)

        #--------------------------------------------------------------------
        # SCENE 3
        #--------------------------------------------------------------------
        # Equations explaining estimator 
        #
        self.next_section()
        fs = 90
        eq1 = Tex(r'$\frac{\text{d}x}{\text{d}t}$', r'=', r'$u_{cmd}$', r'$-$', r'$u_{load}$', font_size=fs)
        eq1b = Tex(r'$\hat{u}_{load}$', font_size=fs)
        eq1c = Tex(r'$H\big[$', r'$\big]$', font_size=fs)
        eq1d = VGroup(eq1[2], eq1[3], eq1[0])
        eq1e = VGroup(eq1c[0], eq1[2])

        eq2 = Tex(r'$H\left(s\right)$', r'$=$', r'$\frac{1}{1+s\tau_{n}}$', r'$,\,\tau_{n}\gg\tau$', font_size=fs)
        eq2a = VGroup(eq2[0:3])

        eq3 = Tex(r'$u_{cmd}$', r'$=$', r'$\frac{x_{sp}-x}{\tau}$', r'$+$', r'$\hat{u}_{load}$', font_size=fs)
        eq3b = VGroup(eq3[2:5])
        eq3c = Tex(r'$H\big[u_{cmd}$', r'$\big]$', font_size=fs)

        eq1[2].set_color(BLUE)
        eq1[3].set_color(RED)
        eq1[4].set_color(RED)
        eq1b[0].set_color(RED)
        eq1c.set_color(RED)

        eq2.set_color(RED)
        eq2[3].set_color(YELLOW)

        eq3[0].set_color(BLUE)
        eq3[1].set_color(BLUE)
        eq3[2].set_color(YELLOW)
        eq3[3].set_color(RED)
        eq3[4].set_color(RED)
        eq3c.set_color(RED)
        eq3c[0][2:6].set_color(BLUE)

        eq1.shift(1.5*UP)
        eq1b.next_to(eq1[1], LEFT)
        eq1c[0].next_to(eq1[1], RIGHT)

        eq2.next_to(eq1, 1.75*DOWN)
        eq2[1].align_to(eq1[1], LEFT)
        eq2[0].next_to(eq2[1], LEFT)
        eq2[2].next_to(eq2[1], RIGHT)
        eq2[3].next_to(eq2[2], RIGHT)

        eq3.next_to(eq2, 3.0*DOWN)
        eq3[1].align_to(eq1[1], LEFT)
        eq3[0].next_to(eq3[1], LEFT)
        eq3b.next_to(eq3[1], RIGHT)
        eq3c.next_to(eq3[3], RIGHT)

        with self.voiceover(text=
                """Next, we dig into the details on how the load is estimated. First, we derive
                   the load estimator out of first principles, detailing the specific choices a
                   P-I controller makes in its implementation. We'll show
                   how these choices amount to an integral action. Later on, we'll discuss other
                   choices for the estimator design, each of them yielding different variations on the
                   standard P-I controller design.
                """):
            self.clear_canvas()
        self.wait(0.5)

        with self.voiceover(text=
                """Again, the starting point is the equation that models the open loop behavior, an integrator
                   driven by the controller's command and burdened by a load.  
                   <bookmark mark="L"/>Rearranging this equation calculates the load as a function of command
                   and system rate of change. 
                   <bookmark mark="H"/>This raw load estimate is filtered to suppress components resulting from
                   differences between the real system behavior and the ideal model assumed by the controller. 
                   <bookmark mark="HH"/>
                   A P-I controller selects this filter to be a simple first-order lowpass one.
                """):
            self.play(Write(eq1))
            self.wait_until_bookmark("L")
            self.play(Transform(eq1[4], eq1b), 
                    eq1[0].animate.next_to(eq1[3], RIGHT), 
                    eq1[1].animate.set_color(RED),
                    eq1[3].animate.set_color(WHITE) )
            self.wait_until_bookmark("H")
            self.play(eq1d.animate.next_to(eq1c[0], 0.6*RIGHT))
            eq1c[1].next_to(eq1d, RIGHT)
            self.play(FadeIn(eq1c))
            self.wait_until_bookmark("HH")
            self.play(Write(eq2a))
        self.wait(0.5)

        cross = Cross(eq1[0], YELLOW)
        with self.voiceover(text=
                """If the time constant of this filter is larger than the time constant of the controller's
                   transient response, which is shaped by its proportional action, 
                   <bookmark mark="S"/>the contribution of the rate of system change will be suppressed by the filter and it can be ignored
                   in the load estimation. Remember though, the price to pay for this simplification is making
                   the load estimator slower than the response time of the closed-loop system.
                """):
            self.play(Write(eq2[3]))
            self.wait_until_bookmark("S")
            self.play(Create(cross))
        self.wait(0.5)

        with self.voiceover(text=
                """What does this mean for the overall control law?
                   <bookmark mark="C"/>The overall control law sums the proportional action, to handle transient behavior,
                   and the load estimate, to handle steady state behavior.
                   <bookmark mark="S"/>Substituting result derived above for the load estimate 
                   <bookmark mark="R"/>yields the complete equation describing the control law of a P-I controller.  
                """):
            self.wait_until_bookmark("C")
            self.play(Write(eq3))
            self.wait_until_bookmark("S")
            self.play(FadeOut(eq3[4]))
            self.play(TransformFromCopy(eq1e, eq3c[0]), TransformFromCopy(eq1c[1], eq3c[1]))
            res = VGroup(eq3[0:4], eq3c)
            self.wait_until_bookmark("R")
            box = SurroundingRectangle(res, color=WHITE, buff=MED_LARGE_BUFF)
            self.play(Create(box))
            box_c = box.copy().set_color(DARK_BLUE)
            self.play(ShowPassingFlash(box_c, run_time=2, time_width=0.5))
        self.wait(1)

        #--------------------------------------------------------------------
        # SCENE 4
        #--------------------------------------------------------------------
        # Update block diagram 
        #
        # Draw Blockdiagram using TikZ
        self.next_section()
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{tikz}")
        template.add_to_preamble(r"\usetikzlibrary{shapes,arrows,positioning,calc}")
        template.add_to_document(
        r"""\tikzset{
                block/.style = {draw, rectangle, minimum height=3em, minimum width=3em},
                gain/.style  = {draw, thick, isosceles triangle, minimum height = 3em, isosceles triangle apex angle=60},                
                tmp/.style  = {coordinate}, 
                sum/.style= {draw, circle, node distance=1cm},
                input/.style = {coordinate},
                output/.style= {coordinate},
                pinstyle/.style = {pin edge={to-,thin,black}}
            }""")

        diagram = MathTex(r"""[auto, node distance=2cm,>=latex]
                \node (sp) {\LARGE{$x_{sp}$}};
                \node [below of=sp, node distance=1.5cm] (pv) {\LARGE{$x$}};
                \node [sum, right of=sp, node distance=1.5cm] (err) {};
                \draw [->] (sp) -- node[pos=0.99]{$+$} (err);
                \draw [->] (pv) -| node[pos=0.99]{$-$} (err);

                \node [gain, right of=err, node distance=1.5cm] (p_action) {\Large{$\frac{1}{\tau}$}};
                \draw [->] (err) -- (p_action);

                \node [sum, right of=p_action, node distance=2.0cm] (mv_aux) {};
                \node [output, right of=mv_aux, node distance=2.5cm] (mv) {};
                \node [coordinate, right of=mv, node distance=0.75cm] (mv_out) {};
                \node [coordinate, below of=mv, node distance=1.5cm] (fb_aux) {};
                \node [coordinate, below of=mv_aux, node distance=1.5cm] (fb_out) {};
                \draw [->] (p_action) -- node[pos=0.99]{$+$} (mv_aux);
	            \draw [->] (fb_out) -- node[left]{\Large{$\hat{u}_{load}$}} node[pos=0.99]{$+$} (mv_aux);
                \draw [->] (mv_aux) -- (mv_out) node[right]{\LARGE{$u_{cmd}$}};                                      
                \node [block, left of=fb_aux, node distance=1.25cm] (fb) {\Large{$\frac{1}{1+s\tau_n}$}};
                \draw node at (mv) {\tiny\textbullet};
	            \draw [->] (mv) |- (fb);
	            \draw [-] (fb) -- (fb_out);
	            \draw node at (fb) {$H(s)$};
            """,
            stroke_width=2, 
            tex_environment="tikzpicture", 
            tex_template=template )

        diagram.scale(0.7)
        diagram.shift(0.5*DOWN)

        labels = index_labels(diagram[0])
        labels.z_index = 1

        p_action = VGroup(diagram[0][0:11], diagram[0][15:17], diagram[0][11:15], diagram[0][18:21])
        p_action.set_color(YELLOW)
        i_action = VGroup(diagram[0][21:23], diagram[0][29:30], diagram[0][23:29])
        i_action.set_color(RED)
        u_cmd = VGroup(diagram[0][17], diagram[0][30:36])
        u_cmd.set_color(BLUE)
        i_h = VGroup(diagram[0][44:47], diagram[0][36:37], diagram[0][47:48])
        i_h_l1 = VGroup(diagram[0][37:44])
        i_h_l2 = VGroup(diagram[0][48:52])
        i_h.set_color(RED)
        i_h_l1.set_color(RED)
        i_h_l2.set_color(RED)

        #self.add(labels)
        with self.voiceover(text=
                """Let's have a look at the corresponding block diagram.
                """):
            self.clear_canvas()
        self.wait(0.5)
        with self.voiceover(text=
                """As discussed before, the major parts of the block diagram
                <bookmark mark="P"/> are the proportional action
                <bookmark mark="I"/>and the load estimate coming together
                <bookmark mark="U"/>to produce the command value.
                <bookmark mark="H"/>A filtered version of the command value is fed back to produce the load estimate.
                A standard P-I controller implements this
                <bookmark mark="LP"/>as a first-order lowpass filter.
                """):
            self.wait_until_bookmark("P")
            self.play(Create(p_action), run_time=1.5)
            self.wait_until_bookmark("I")
            self.play(Create(i_action), run_time=1.5)
            self.wait_until_bookmark("U")
            self.play(Create(u_cmd), run_time=1.5)
            self.wait_until_bookmark("H")
            self.play(Create(i_h), run_time=2.0)
            self.play(Write(i_h_l2))
            self.wait_until_bookmark("LP")
            self.play(FadeOut(i_h_l2), FadeIn(i_h_l1))
        self.wait(0.5)
        with self.voiceover(text=
            """Anyone familiar with a P-I controller will recognize that the blockdiagram does not correspond to a
               classical representation. As its name suggest, a P-I controller sums a component that is 
               proportional to the control error and a component that is proportional to the integral of the control error.
               In what follows, we will show that the blockdiagram on screen is equivalent to the classical representation.
            """):
            self.wait(0.1)
        self.wait(0.5)

        #--------------------------------------------------------------------
        # SCENE 5
        #--------------------------------------------------------------------
        # Explain how this relates to the traditional formulation of a PI controller
        #
        self.next_section()

        with self.voiceover(text=
                """To do so, we return to the equations.
                """):
            self.clear_canvas()
        self.wait(0.5)

        fs = 90
        eq3a = Tex(r'$u_{cmd}$', r'$=$', r'$\frac{x_{sp}-x}{\tau}$', r'$+\frac{u_{cmd}}{1+s\tau_{n}}$', font_size=fs)
        eq3a[0].set_color(BLUE)
        eq3a[1].set_color(BLUE)
        eq3a[2].set_color(YELLOW)
        eq3a[3][0:1].set_color(RED)
        eq3a[3][1:5].set_color(BLUE)
        eq3a[3][5:].set_color(RED)
 
        eq3b = Tex(r'$-\frac{u_{cmd}}{1+s\tau_{n}}$', font_size=fs)
        eq3b[0][0:1].set_color(RED)
        eq3b[0][1:5].set_color(BLUE)
        eq3b[0][5:].set_color(RED)

        eq3c = Tex(r'$\left(1-\frac{1}{1+s\tau_{n}}\right)$', r'$u_{cmd}$', font_size=fs)
        eq3c[0][0].set_color(BLUE)
        eq3c[0][-1].set_color(BLUE)
        eq3c[0][1:-1].set_color(RED)
        eq3c[1].set_color(BLUE)

        eq3d = Tex(r'$\left(\frac{s\tau_{n}}{1+s\tau_{n}}\right)$', r'$u_{cmd}$', font_size=fs)
        eq3d[0][0].set_color(BLUE)
        eq3d[0][-1].set_color(BLUE)
        eq3d[0][1:-1].set_color(RED)
        eq3d[1].set_color(BLUE)

        eq3e = Tex(r'$\left(\frac{s\tau_{n}+1}{s\tau_{n}}\right)$', font_size=fs)
        eq3e[0][0].set_color(BLUE)
        eq3e[0][-1].set_color(BLUE)
        eq3e[0][1:-1].set_color(RED)

        eq3f = Tex(r'$\left(1+\frac{1}{s\tau_{n}}\right)$', font_size=fs)
        eq3f[0][0].set_color(BLUE)
        eq3f[0][-1].set_color(BLUE)
        eq3f[0][1:3].set_color(YELLOW)
        eq3f[0][3:-1].set_color(RED)

        eq3g = Tex(r'$=$', r'$\frac{x_{sp}-x}{\tau}$', r'$+\int\frac{x_{sp}-x}{\tau_{n}\tau}\text{d}t$', font_size=fs)
        eq3g[0].set_color(BLUE)
        eq3g[1].set_color(YELLOW)
        eq3g[2].set_color(RED)

        eq3a.shift(1.0*RIGHT)
        eq3a.shift(1.5*UP)
        eq3b[0].next_to(eq3a[1], LEFT)
        eq3b[0].shift(0.1*DOWN)

        #self.add(index_labels(eq3c[0]))
        with self.voiceover(text=
                """In our formulation so far, a P-I controller adds a 
                <bookmark mark="S0_1"/>proportional term and 
                <bookmark mark="S0_2"/>a filtered version of the command as a load estimate.
                   Let's see how we arrive at the classical representation from here.
                <bookmark mark="S1"/>We start by moving the second right-hand term to the left-hand side.
                <bookmark mark="S2"/>Since both terms contain the command value, they can be grouped together.
                <bookmark mark="S3"/>Next, we add the terms between the brackets,
                <bookmark mark="S4"/>and we bring the resulting coefficient to the right-hand side which is an operation that has it inverted.
                <bookmark mark="S5"/>The inverted coefficient can be expanded in two terms, one equal to unity and one that is inversely 
                                     proportional to the Laplace variable s.
                <bookmark mark="S6"/>Expanding the equation and with 1 over s being the Laplace domain representation of an integral,
                                     we see the command value to equal the sum of 
                <bookmark mark="S6_1"/>a term proportional to the control error and 
                <bookmark mark="S6_2"/>a term integrating the control error. This corresponds to the classical representation of a P-I controller,
                                       which is what we set out to prove. 
                """):
            self.play(Write(eq3a))
            self.wait_until_bookmark("S0_1")
            box = SurroundingRectangle(eq3a[2], color=YELLOW, buff=SMALL_BUFF)
            self.play(ShowPassingFlash(box, run_time=1, time_width=2))
            self.wait_until_bookmark("S0_2")
            box = SurroundingRectangle(eq3a[3], color=RED, buff=SMALL_BUFF)
            self.play(ShowPassingFlash(box, run_time=1, time_width=2))

            self.wait_until_bookmark("S1")
            eq3ab = VGroup(eq3a[0].copy(), eq3b[0], eq3a[1].copy(), eq3a[2].copy())
            eq3ab[0].next_to(eq3ab[1], LEFT)
            eq3ab.shift(2.0*RIGHT)
            eq3ab.shift(2.0*DOWN)
            self.play(TransformFromCopy(eq3a[1], eq3ab[2]))
            self.play(TransformFromCopy(eq3a[2], eq3ab[3]))
            self.play(TransformFromCopy(eq3a[0], eq3ab[0]),
                    TransformFromCopy(eq3a[3], eq3ab[1]))
            
            self.wait_until_bookmark("S2")
            eq3c.next_to(eq3ab[2], LEFT)
            eq3aux = VGroup(eq3ab[0], eq3ab[1])
            self.play(FadeOut(eq3aux), FadeIn(eq3c),run_time=1.5)
            
            self.wait_until_bookmark("S3")
            eq3aux=VGroup(eq3c, eq3ab[2], eq3ab[3])
            eq3d.next_to(eq3aux[1],LEFT)
            self.play(Transform(eq3aux[0], eq3d))
            
            self.wait_until_bookmark("S4")
            self.play(eq3aux.animate.shift(2.0*LEFT))
            eq3e.next_to(eq3aux[1],RIGHT)
            self.play(eq3aux[2].animate.next_to(eq3e))
            self.play(Transform(eq3aux[0][0], eq3e))
            self.play(eq3aux.animate.shift(2.0*LEFT))

            self.wait_until_bookmark("S5")
            eq3f.next_to(eq3aux[1],RIGHT)
            self.play(eq3aux[2].animate.next_to(eq3f))
            #self.play(Transform(eq3aux[0][0], eq3f))
            self.play(FadeOut(eq3aux[0][0]), FadeIn(eq3f))

            self.wait_until_bookmark("S6")
            eq3g[0].align_to(eq3aux[1], UL)
            eq3g[0].shift(2.0*DOWN)
            eq3g[1].next_to(eq3g[0])
            eq3g[2].next_to(eq3g[1])
            self.play(Write(eq3g))
            self.wait_until_bookmark("S6_1")
            box = SurroundingRectangle(eq3g[1], color=YELLOW, buff=SMALL_BUFF)
            self.play(ShowPassingFlash(box, run_time=1, time_width=2))
            self.wait_until_bookmark("S6_2")
            box = SurroundingRectangle(eq3g[2], color=RED, buff=SMALL_BUFF)
            self.play(ShowPassingFlash(box, run_time=1, time_width=2))

        self.wait(0.5)
        with self.voiceover(text=
                """The classical representation certainly has its merits, especially when it comes to understanding how some
                    physical systems naturally implement a P-I controller. We'll see some examples as we study electrical
                    circuits later on. However, from a control design perspective, the initial formulation is more useful
                    as it comes to modifying and expanding the controller and its properties.
                """):
            self.wait(0.1)

        self.wait(3.0)

class PIBlockDiagram(VoiceoverScene):
    def construct(self):
        #self.set_speech_service(GTTSService(lang="en", tld="com"))
        self.set_speech_service(
            AzureService(
                voice="en-US-AlloyTurboMultilingualNeural",
                style="default",  
                global_speed=1.0,
            )
        )

        title = Title("PI Control Explained")
        self.add(title)

        # Draw Blockdiagram using TikZ
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{tikz}")
        template.add_to_preamble(r"\usetikzlibrary{shapes,arrows,positioning,calc}")
        template.add_to_document(
        r"""\tikzset{
                block/.style = {draw, rectangle, minimum height=3em, minimum width=3em},
                gain/.style  = {draw, thick, isosceles triangle, minimum height = 3em, isosceles triangle apex angle=60},                
                tmp/.style  = {coordinate}, 
                sum/.style= {draw, circle, node distance=1cm},
                input/.style = {coordinate},
                output/.style= {coordinate},
                pinstyle/.style = {pin edge={to-,thin,black}}
            }""")

        diagram = MathTex(r"""[auto, node distance=2cm,>=latex]
            \node (sp) {$x_{sp}$};
            \node [sum, right of=sp, node distance=1.5cm] (err) {};
            \draw [->] (sp) -- node[pos=0.99]{$+$} (err);

            \node [below of=sp, node distance=1.5cm] (pv) {$x$};
            \draw [->] (pv) -| node[pos=0.99]{$-$} (err);

            \node [gain, right of=err, node distance=1.5cm] (p_action) {$\frac{1}{\tau}$};
            \draw [->] (err) -- (p_action);

            \node [sum, right of=p_action, node distance=2.0cm] (mv_aux) {};
            \node [input, below of=mv_aux, node distance=1.25cm] (mv_i) {};
            \node [output, right of=mv_aux, node distance=2.0cm] (mv) {};

            \draw [->] (p_action) -- node[pos=0.99]{$+$} (mv_aux);
            \draw [->] (mv_i) node[below]{$\hat{u}_{load}$} -- node[pos=0.99]{$+$} (mv_aux);
            \draw [->] (mv_aux) --  (mv) node[right]{$u_{cmd}$};                                      
                                      
            %\node [block, above of=controller,node distance=1.3cm] (up){$\frac{k_{i\beta}}{s}$};
            %\node [block, below of=controller,node distance=1.3cm] (rate) {$sk_{d\beta}$};
            %\node [block, above = 2cm of sum2](extra){$\frac{1}{\alpha_{\beta2}}$};
            %\node [block, right of=sum2,node distance=2cm] (system){$\frac{a_{\beta 2}}{s+a_{\beta 1}}$};
            %\node [output, right of=system, node distance=2cm] (output) {};
            %\node [tmp, below of=controller] (tmp1){$H(s)$};
            %\draw [->] (sum1) --node[name=z,anchor=north]{$E(s)$} (controller);
            %\draw [->] (controller) -- (sum2);
            %\draw [->] (sum2) -- node{$U(s)$} (system);
            %\draw [->] (system) -- node [name=y] {$Y(s)$}(output);
            %\draw [->] (z) |- (rate);
            %\draw [->] (rate) -| (sum2);
            %\draw [->] (z) |- (up);
            %\draw [->] (up) -| (sum2);
            %\draw [->] (y) |- (tmp1)-| node[pos=0.99] {$-$} (sum1);
            %\draw [->] (extra)--(sum2);
            %\draw [->] ($(0,1.5cm)+(extra)$)node[above]{$d_{\beta 2}$} -- (extra);                          
            """,
            stroke_width=2, 
            tex_environment="tikzpicture", 
            tex_template=template )

        diagram.scale(0.7)
        diagram.shift(DOWN)

        labels = index_labels(diagram[0])
        labels.z_index = 1
        #self.add(labels)

        p_action = VGroup(diagram[0][0:11], diagram[0][15:17], diagram[0][11:15], diagram[0][18:21])
        p_action.set_color(YELLOW)
        i_action = VGroup(diagram[0][23:29], diagram[0][23:29], diagram[0][21:23], diagram[0][29])
        i_action.set_color(RED)
        u_cmd = VGroup(diagram[0][17], diagram[0][30:])
        u_cmd.set_color(BLUE)

        self.wait(1)
        with self.voiceover(text=
                """It is straightforward to draw these equations as a block diagram.
                   <bookmark mark='P'/>There is the proportional action that acts on the control error to get the 
                      system on track.
                   <bookmark mark='I'/>There is the integral action that adds an estimate for the external load.
                   <bookmark mark='U'/>Both are added together to produce the actuator's command value. 
                """
            ):
            self.wait_until_bookmark("P")
            self.play(Create(p_action), run_time=2.5)
            self.wait_until_bookmark("I")
            self.play(Create(i_action), run_time=2.0)
            self.wait_until_bookmark("U")
            self.play(Create(u_cmd), run_time=1.5)

        self.wait(3)

class IAction(Scene):
    def construct(self):
        title = Title("PI Control Explained")
        self.add(title)

        fs = 90
        eq1 = Tex(r'$\frac{\text{d}x}{\text{d}t}$', r'=', r'$u_{cmd}$', r'$-$', r'$u_{load}$', font_size=fs)
        eq1b = Tex(r'$\hat{u}_{load}$', font_size=fs)
        eq1c = Tex(r'$H\big[$', r'$\big]$', font_size=fs)
        eq1d = VGroup(eq1[2], eq1[3], eq1[0])
        eq1e = VGroup(eq1c[0], eq1[2])

        eq2 = Tex(r'$H\left(s\right)$', r'$=$', r'$\frac{1}{1+\tau_{N}}$', r'$,\,\tau_{N}\gg\tau$', font_size=fs)
        eq2a = VGroup(eq2[0:3])

        eq3 = Tex(r'$u_{cmd}$', r'$=$', r'$\frac{x_{sp}-x}{\tau}$', r'$+$', r'$\hat{u}_{load}$', font_size=fs)
        eq3b = VGroup(eq3[2:5])
        eq3c = Tex(r'$H\big[u_{cmd}$', r'$\big]$', font_size=fs)

        eq1[2].set_color(BLUE)
        eq1[3].set_color(RED)
        eq1[4].set_color(RED)
        eq1b[0].set_color(RED)
        eq1c.set_color(RED)

        eq2.set_color(RED)
        eq2[3].set_color(YELLOW)

        eq3[0].set_color(BLUE)
        eq3[1].set_color(BLUE)
        eq3[2].set_color(YELLOW)
        eq3[3].set_color(RED)
        eq3[4].set_color(RED)
        eq3c.set_color(RED)
        eq3c[0][2:6].set_color(BLUE)

        eq1.shift(1.5*UP)
        eq1b.next_to(eq1[1], LEFT)
        eq1c[0].next_to(eq1[1], RIGHT)

        eq2.next_to(eq1, 1.75*DOWN)
        eq2[1].align_to(eq1[1], LEFT)
        eq2[0].next_to(eq2[1], LEFT)
        eq2[2].next_to(eq2[1], RIGHT)
        eq2[3].next_to(eq2[2], RIGHT)

        eq3.next_to(eq2, 3.0*DOWN)
        eq3[1].align_to(eq1[1], LEFT)
        eq3[0].next_to(eq3[1], LEFT)
        eq3b.next_to(eq3[1], RIGHT)
        eq3c.next_to(eq3[3], RIGHT)

        self.play(Write(eq1))
        self.wait(1)
        self.play(Transform(eq1[4], eq1b), 
                  eq1[0].animate.next_to(eq1[3], RIGHT), 
                  eq1[1].animate.set_color(RED),
                  eq1[3].animate.set_color(WHITE) )
        self.wait(1)
        
        self.play(eq1d.animate.next_to(eq1c[0], 0.6*RIGHT))
        eq1c[1].next_to(eq1d, RIGHT)
        self.play(FadeIn(eq1c))
        self.wait(0.5)
        self.play(Write(eq2a))
        self.wait(1)

        cross = Cross(eq1[0], YELLOW)
        self.play(Write(eq2[3]))
        self.wait(0.5)
        self.play(Create(cross))
        self.wait(1)

        self.play(Write(eq3))
        self.wait(0.5)
        self.play(FadeOut(eq3[4]))
        self.play(TransformFromCopy(eq1e, eq3c[0]), TransformFromCopy(eq1c[1], eq3c[1]))
        res = VGroup(eq3[0:4], eq3c)
        box = SurroundingRectangle(res, color=WHITE, buff=MED_LARGE_BUFF)
        self.play(Create(box))

        self.wait(3)

class IBlockDiagram(Scene):
    def construct(self):
        title = Title("PI Control Explained")
        self.add(title)

        # Draw Blockdiagram using TikZ
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{tikz}")
        template.add_to_preamble(r"\usetikzlibrary{shapes,arrows,positioning,calc}")
        template.add_to_document(
        r"""\tikzset{
                block/.style = {draw, rectangle, minimum height=3em, minimum width=3em},
                gain/.style  = {draw, thick, isosceles triangle, minimum height = 3em, isosceles triangle apex angle=60},                
                tmp/.style  = {coordinate}, 
                sum/.style= {draw, circle, node distance=1cm},
                input/.style = {coordinate},
                output/.style= {coordinate},
                pinstyle/.style = {pin edge={to-,thin,black}}
            }""")

        diagram = MathTex(r"""[auto, node distance=2cm,>=latex]
                \node (sp) {\LARGE{$x_{sp}$}};
                \node [below of=sp, node distance=1.5cm] (pv) {\LARGE{$x$}};
                \node [sum, right of=sp, node distance=1.5cm] (err) {};
                \draw [->] (sp) -- node[pos=0.99]{$+$} (err);
                \draw [->] (pv) -| node[pos=0.99]{$-$} (err);

                \node [gain, right of=err, node distance=1.5cm] (p_action) {\Large{$\frac{1}{\tau}$}};
                \draw [->] (err) -- (p_action);

                \node [sum, right of=p_action, node distance=2.0cm] (mv_aux) {};
                \node [output, right of=mv_aux, node distance=2.5cm] (mv) {};
                \node [coordinate, right of=mv, node distance=0.75cm] (mv_out) {};
                \node [coordinate, below of=mv, node distance=1.5cm] (fb_aux) {};
                \node [coordinate, below of=mv_aux, node distance=1.5cm] (fb_out) {};
                \draw [->] (p_action) -- node[pos=0.99]{$+$} (mv_aux);
	            \draw [->] (fb_out) -- node[left]{\Large{$\hat{u}_{load}$}} node[pos=0.99]{$+$} (mv_aux);
                \draw [->] (mv_aux) -- (mv_out) node[right]{\LARGE{$u_{cmd}$}};                                      
                \node [block, left of=fb_aux, node distance=1.25cm] (fb) {\Large{$\frac{1}{1+s\tau_n}$}};
                \draw node at (mv) {\tiny\textbullet};
	            \draw [->] (mv) |- (fb);
	            \draw [-] (fb) -- (fb_out);
	            \draw node at (fb) {$H(s)$};
            """,
            stroke_width=2, 
            tex_environment="tikzpicture", 
            tex_template=template )

        diagram.scale(0.7)
        diagram.shift(0.5*DOWN)

        labels = index_labels(diagram[0])
        labels.z_index = 1

        p_action = VGroup(diagram[0][0:11], diagram[0][15:17], diagram[0][11:15], diagram[0][18:21])
        p_action.set_color(YELLOW)
        i_action = VGroup(diagram[0][21:23], diagram[0][29:30], diagram[0][23:29])
        i_action.set_color(RED)
        u_cmd = VGroup(diagram[0][17], diagram[0][30:36])
        u_cmd.set_color(BLUE)
        i_h = VGroup(diagram[0][44:47], diagram[0][36:37], diagram[0][47:48])
        i_h_l1 = VGroup(diagram[0][37:44])
        i_h_l2 = VGroup(diagram[0][48:52])
        i_h.set_color(RED)
        i_h_l1.set_color(RED)
        i_h_l2.set_color(RED)

        #self.add(labels)
        self.play(Create(p_action), run_time=2.0)
        self.wait(0.5)
        self.play(Create(i_action), run_time=1.5)
        self.wait(0.5)
        self.play(Create(u_cmd), run_time=1.5)
        self.wait(0.5)
        self.play(Create(i_h), run_time=2.0)
        self.play(Write(i_h_l2))

        self.wait(2)
        self.play(FadeOut(i_h_l2), FadeIn(i_h_l1))

        self.wait(3)

class IActionExplained(Scene):
    def construct(self):
        title = Title("PI Control Explained")
        self.add(title)

        fs = 90
        eq3a = Tex(r'$u_{cmd}$', r'$=$', r'$\frac{x_{sp}-x}{\tau}$', r'$+\frac{u_{cmd}}{1+s\tau_{N}}$', font_size=fs)
        eq3a[0].set_color(BLUE)
        eq3a[1].set_color(BLUE)
        eq3a[2].set_color(YELLOW)
        eq3a[3][0:1].set_color(RED)
        eq3a[3][1:5].set_color(BLUE)
        eq3a[3][5:].set_color(RED)
 
        eq3b = Tex(r'$-\frac{u_{cmd}}{1+s\tau_{N}}$', font_size=fs)
        eq3b[0][0:1].set_color(RED)
        eq3b[0][1:5].set_color(BLUE)
        eq3b[0][5:].set_color(RED)

        eq3c = Tex(r'$\left(1-\frac{1}{1+s\tau_{N}}\right)$', r'$u_{cmd}$', font_size=fs)
        eq3c[0][0].set_color(BLUE)
        eq3c[0][-1].set_color(BLUE)
        eq3c[0][1:-1].set_color(RED)
        eq3c[1].set_color(BLUE)

        eq3d = Tex(r'$\left(\frac{s\tau_{N}}{1+s\tau_{N}}\right)$', r'$u_{cmd}$', font_size=fs)
        eq3d[0][0].set_color(BLUE)
        eq3d[0][-1].set_color(BLUE)
        eq3d[0][1:-1].set_color(RED)
        eq3d[1].set_color(BLUE)

        eq3e = Tex(r'$\left(\frac{s\tau_{N}+1}{s\tau_{N}}\right)$', font_size=fs)
        eq3e[0][0].set_color(BLUE)
        eq3e[0][-1].set_color(BLUE)
        eq3e[0][1:-1].set_color(RED)

        eq3f = Tex(r'$\left(1+\frac{1}{s\tau_{N}}\right)$', font_size=fs)
        eq3f[0][0].set_color(BLUE)
        eq3f[0][-1].set_color(BLUE)
        eq3f[0][1:3].set_color(YELLOW)
        eq3f[0][3:-1].set_color(RED)

        eq3g = Tex(r'$=$', r'$\frac{x_{sp}-x}{\tau}$', r'$+\int\frac{x_{sp}-x}{\tau_{N}\tau}\text{d}t$', font_size=fs)
        eq3g[0].set_color(BLUE)
        eq3g[1].set_color(YELLOW)
        eq3g[2].set_color(RED)

        eq3a.shift(1.0*RIGHT)
        eq3a.shift(1.5*UP)
        eq3b[0].next_to(eq3a[1], LEFT)
        eq3b[0].shift(0.1*DOWN)

        #self.add(index_labels(eq3c[0]))

        self.play(Write(eq3a))
        box = SurroundingRectangle(eq3a[2], color=YELLOW, buff=SMALL_BUFF)
        self.play(ShowPassingFlash(box, run_time=1, time_width=2))
        box = SurroundingRectangle(eq3a[3], color=RED, buff=SMALL_BUFF)
        self.play(ShowPassingFlash(box, run_time=1, time_width=2))
        self.wait(1.0)

        eq3ab = VGroup(eq3a[0].copy(), eq3b[0], eq3a[1].copy(), eq3a[2].copy())
        eq3ab[0].next_to(eq3ab[1], LEFT)
        eq3ab.shift(2.0*RIGHT)
        eq3ab.shift(2.0*DOWN)
        self.play(TransformFromCopy(eq3a[1], eq3ab[2]))
        self.play(TransformFromCopy(eq3a[2], eq3ab[3]))
        self.play(TransformFromCopy(eq3a[0], eq3ab[0]),
                  TransformFromCopy(eq3a[3], eq3ab[1]))

        self.wait(1.0)        
        eq3c.next_to(eq3ab[2], LEFT)
        eq3aux = VGroup(eq3ab[0], eq3ab[1])
        self.play(FadeOut(eq3aux), FadeIn(eq3c),run_time=1.5)
        self.wait(0.5)
        eq3aux=VGroup(eq3c, eq3ab[2], eq3ab[3])
        eq3d.next_to(eq3aux[1],LEFT)
        self.play(Transform(eq3aux[0], eq3d))
        self.wait(1.0)
        self.play(eq3aux.animate.shift(2.0*LEFT))
        eq3e.next_to(eq3aux[1],RIGHT)
        self.play(eq3aux[2].animate.next_to(eq3e))
        self.play(Transform(eq3aux[0][0], eq3e))
        self.play(eq3aux.animate.shift(2.0*LEFT))
        self.wait(1.0)
        eq3f.next_to(eq3aux[1],RIGHT)
        self.play(eq3aux[2].animate.next_to(eq3f))
        #self.play(Transform(eq3aux[0][0], eq3f))
        self.play(FadeOut(eq3aux[0][0]), FadeIn(eq3f))
        self.wait(1.0)
        eq3g[0].align_to(eq3aux[1], UL)
        eq3g[0].shift(2.0*DOWN)
        eq3g[1].next_to(eq3g[0])
        eq3g[2].next_to(eq3g[1])
        self.play(Write(eq3g))
        self.wait(3.0)

