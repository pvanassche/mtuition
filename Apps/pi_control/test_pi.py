"""
PI Control Simulator - Interactive Web Application

A NiceGUI/Numpy/Scipy application for simulating and visualizing coupled the 
behaviour of a PI controller subject to a setpoint change and a load step.

Copyright (c) 2025 Piet Vanassche. All rights reserved.

DISCLAIMER:
This software is provided "as is", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement. In no event shall the
authors or copyright holders be liable for any claim, damages or other
liability, whether in an action of contract, tort or otherwise, arising from,
out of or in connection with the software or the use or other dealings in the
software.

This simulator is intended for educational and research purposes only. Users
should validate all results independently before using them for any critical
applications.
"""

import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from nicegui import app, ui

class DynamicalSystem:
    """
    A callable class representing the dynamical system:
    c_p * dx/dt = (sp - x) / t_cl + u - ul
    dr/dt = (s - r) / t_cl
    du/dt = (sp - x) / (t_cl * t_n)
       OR
    du/dt = (r - x) / (t_cl * t_n)
    """
    
    def __init__(self, x0=0.0,u0=0.0,r0=0.0, c_p=1.0, t_cl=0.5,t_n=1.5, sp=None,ul=None, use_ref=False, adapt_t=False, u_lim=None):
        self.y0 = [x0, u0, r0]
        self.c_p = c_p
        self.t_cl = t_cl
        self.t_n = t_n
        self.sp = sp if sp is not None else lambda t: 1.0
        self.ul = ul if ul is not None else lambda t: 0.0
        self.use_ref = use_ref
        self.adapt_t = adapt_t
        self.u_lim = u_lim if u_lim is not None else [-1.0, 1.0]
        self.solution = None
        
    def __call__(self, t, y):
        x, u_raw, r = y
        sp_t = self.sp(t)
        ul_t = self.ul(t)

        t_cl = self.t_cl
        t_n = self.t_n
        t_lim = t_cl/20

        u = np.clip(u_raw, self.u_lim[0], self.u_lim[1])

        if self.adapt_t:
            t_cl_min = (sp_t-x)/(self.u_lim[1] - u + 1e-8)
            aux = (sp_t-x)/(u - self.u_lim[0] + 1e-8)
            if t_cl_min < 0: t_cl_min = aux
            if t_cl < t_cl_min: t_cl = t_cl_min
            t_n = (self.t_n/self.t_cl) * t_cl

        dxdt = (np.clip((sp_t - x) / t_cl + u, self.u_lim[0], self.u_lim[1]) - ul_t) / self.c_p
        if self.use_ref:
            dudt = (r - x) / (t_cl * t_n)
        else:
            dudt = (sp_t - x) / (t_cl * t_n)
        if (dudt < 0) and (u_raw <= self.u_lim[0]):
            dudt = (self.u_lim[0] - u_raw) / t_lim
        if (dudt > 0) and (u_raw >= self.u_lim[1]):
            dudt = (self.u_lim[1] - u_raw) / t_lim

        drdt = (sp_t - r) / t_cl

        return [dxdt, dudt, drdt]
    
    def solve(self, t_span=(0, 20), t_eval=None, method='LSODA'):
        if t_eval is None:
            t_eval = np.linspace(t_span[0], t_span[1], 1000)
        self.solution = solve_ivp(self, t_span, self.y0, 
                                  t_eval=t_eval, method=method)
        return self.solution
    
    def get_results(self):
        if self.solution is None:
            raise ValueError("System not solved yet. Call solve() first.")
        t = self.solution.t
        x = self.solution.y[0]
        u = self.solution.y[1]
        r = self.solution.y[2]
        return t, x, u, r


def create_plots(c_p_val, t_cl_val, t_n_val, use_ref_val, adapt_t_val, u_lim_val):
    """Create and return plotly figure"""
    # Define setpoint function
    def setpoint_step(t):
        return 1.0 if t >= 2.0 else 0.0
    
    def load_step(t):
        return 0.5 if t >= 10.0 else 0.0

    # Create and solve system
    system = DynamicalSystem(
        x0=0.0, 
        u0=0.0,
        r0=0.0,
        c_p=c_p_val,
        t_cl=t_cl_val, 
        t_n=t_n_val,
        sp=setpoint_step,
        ul=load_step,
        use_ref=use_ref_val,
        adapt_t=adapt_t_val,
        u_lim=u_lim_val
    )
    system.solve(t_span=(0, 20))
    t, x, u, r = system.get_results()
    
    # Get setpoint values
    sp_vals = np.array([system.sp(ti) for ti in t])
    ul_vals = np.array([system.ul(ti) for ti in t])
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
            f'<b>Process Variable</b>',
            f'<b>Load Estimate</b>'
        ),
        vertical_spacing=0.2
    )
    
    # Add x(t) trace
    fig.add_trace(
        go.Scatter(
            x=t, y=x,
            name='x(t)',
            line=dict(color='#3b82f6', width=3),
            mode='lines',
            hovertemplate='<b>x(t)</b><br>Time: %{x:.2f}<br>Value: %{y:.4f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add setpoint trace
    fig.add_trace(
        go.Scatter(
            x=t, y=sp_vals,
            name='setpoint',
            line=dict(color='#64748b', width=2, dash='dash'),
            mode='lines',
            hovertemplate='<b>sp(t)</b><br>Time: %{x:.2f}<br>Value: %{y:.4f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add u(t) trace
    fig.add_trace(
        go.Scatter(
            x=t, y=u,
            name='u(t)',
            line=dict(color='#ef4444', width=3),
            mode='lines',
            showlegend=True,
            hovertemplate='<b>u(t)</b><br>Time: %{x:.2f}<br>Value: %{y:.4f}<extra></extra>'
        ),
        row=2, col=1
    )

    # Add load trace
    fig.add_trace(
        go.Scatter(
            x=t, y=ul_vals,
            name='load',
            line=dict(color='#64748b', width=2, dash='dash'),
            mode='lines',
            hovertemplate='<b>sp(t)</b><br>Time: %{x:.2f}<br>Value: %{y:.4f}<extra></extra>'
        ),
        row=2, col=1
    )

    # Update axes labels
    fig.update_xaxes(title_text="<b>Time (s)</b>", row=1, col=1, gridcolor='#e5e7eb')
    fig.update_yaxes(title_text="<b>x(t)</b>", row=1, col=1, gridcolor='#e5e7eb')
    fig.update_xaxes(title_text="<b>Time (s)</b>", row=2, col=1, gridcolor='#e5e7eb')
    fig.update_yaxes(title_text="<b>u(t)</b>", row=2, col=1, gridcolor='#e5e7eb')
    
    # Update layout
    fig.update_layout(
        height=575,
        showlegend=True,
        hovermode='x unified',
        template='plotly_white',
        font=dict(family='Inter, sans-serif', size=13),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#e5e7eb',
            borderwidth=1
        ),
        margin=dict(t=60, b=40, l=60, r=40)
    )
    
    return fig


# Create NiceGUI app with custom styling
@ui.page('/')
def main_page():
    # Add custom CSS
    ui.add_head_html('''
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            
            .main-container {
                max-width: 90%;
                width: 90%;
                margin: 2rem auto;
                padding: 0 1rem;
            }
            
            .glass-card {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 8px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.18);
            }
            
            .header-badge {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 10px;
                font-size: 0.9rem;
                font-weight: 600;
                display: inline-block;
                margin-left: 0.5rem;
            }
                     
            .mtuition-1 {
                background: rgba(25, 25, 25, 0.95);
                color: white;
                padding: 0.1rem 0.5rem;
                border-radius: 10px;
                font-size: 1.1rem;
                font-weight: 800;
                display: inline-block;
                margin-left: 0.5rem;
            }
            .mtuition-2 {
                color: black;
                padding: 0.1rem 0.075rem;
                font-size: 1.0rem;
                font-weight: 600;
                display: inline-block;
                margin-left: 0.0rem;
            }
        </style>
    ''')
    
    with ui.column().classes('main-container gap-3'):
        # Header
        with ui.card().classes('glass-card w-full p-6'):
            with ui.row().classes('items-center gap-3 w-full'):
                ui.icon('analytics', size='2.5rem').classes('text-purple-600')
                with ui.column().classes('gap-1 flex-grow'):
                    ui.label('PI Control — Simulation').classes('text-3xl font-bold text-gray-800')
                ui.html('<span class="mtuition-1">m</span><span class="mtuition-2">tuition</span>')
        
        with ui.row().classes('w-full gap-3').style('align-items: stretch'):
            # Control Panel
            with ui.card().classes('glass-card p-6 gap-1').style('flex: 0 0 300px'):
                with ui.row().classes('items-center gap-2 mb-2'):
                    ui.icon('tune', size='1.5rem').classes('text-purple-600')
                    ui.label('Settings').classes('text-xl font-semibold text-gray-800')
                
                ui.separator().classes('mb-2')
                
                # c_p parameter
                with ui.column().classes('gap-1 mb-1'):
                    with ui.row().classes('items-center justify-between w-full'):
                        with ui.element().tooltip("System inertia with a value of 1.0 matching the controller's estimate."):
                            ui.markdown('System Inertia C<sub>p</sub>').classes('text-sm font-semibold text-gray-700')
                        c_p_badge = ui.badge('1.00', color='blue').classes('text-sm')
                    
                    c_p_slider = ui.slider(min=0.5, max=1.5, step=0.1, value=1.0) \
                        .props('color=blue').classes('w-full')
                    
                    with ui.row().classes('gap-2 w-full'):
                        ui.label('0.5').classes('text-xs text-gray-500')
                        ui.space()
                        ui.label('1.5').classes('text-xs text-gray-500')

                # t_cl parameter
                with ui.column().classes('gap-1 mb-1'):
                    with ui.row().classes('items-center justify-between w-full'):
                        with ui.element().tooltip("Target closed loop time constant [s]."):
                            ui.markdown('Closed Loop T<sub>cl</sub>').classes('text-sm font-semibold text-gray-700')
                        t_cl_badge = ui.badge('0.50', color='purple').classes('text-sm')
                    
                    t_cl_slider = ui.slider(min=0.1, max=5.0, step=0.1, value=0.5) \
                        .props('color=purple').classes('w-full')
                    
                    with ui.row().classes('gap-2 w-full'):
                        ui.label('0.1').classes('text-xs text-gray-500')
                        ui.space()
                        ui.label('5.0').classes('text-xs text-gray-500')
                
                # t_n parameter
                with ui.column().classes('gap-1 mb-1'):
                    with ui.row().classes('items-center justify-between w-full'):
                        with ui.element().tooltip("Load estimation time constant [s]."):
                            ui.markdown('Integral action T<sub>n</sub>').classes('text-sm font-semibold text-gray-700')
                        t_n_badge = ui.badge('1.50', color='purple').classes('text-sm')
                    
                    t_n_slider = ui.slider(min=0.1, max=5.0, step=0.1, value=1.5) \
                        .props('color=purple').classes('w-full')
                    
                    with ui.row().classes('gap-2 w-full'):
                        ui.label('0.1').classes('text-xs text-gray-500')
                        ui.space()
                        ui.label('5.0').classes('text-xs text-gray-500')
                
                # use_ref switch
                with ui.column().classes('gap-1 mb-1'):
                    with ui.row().classes('items-center justify-normal w-full'):
                        ui.label('Improved Integral').classes('text-sm font-semibold text-gray-700').tooltip("When active, the integrated error is computed relative to the ideal closed-loop trajectory.")
                        use_ref_switch = ui.switch(value=False).props('color=purple')
                    ui.label('Reference trajectory for integral error').classes('text-xs text-gray-500')
                
                # adapt_t switch
                with ui.column().classes('gap-1 mb-1'):
                    with ui.row().classes('items-center justify-normal w-full'):
                        ui.label('Gain Scheduling').classes('text-sm font-semibold text-gray-700').tooltip("When active, clipping of the controller output is handled through adaptive gain scheduling.")
                        adapt_t_switch = ui.switch(value=False).props('color=purple')
                    ui.label('Limit handling via adaptive time constants').classes('text-xs text-gray-500')
                
                # u_lim inputs
                with ui.column().classes('gap-1 mb-1'):
                    ui.label('Control Limits u_lim').classes('text-sm font-semibold text-gray-700').tooltip("Minimum and maximum allowable values for the controller output.")
                    with ui.row().classes('gap-2 w-full items-center'):
                        u_min_input = ui.number(label='u_min', value=-1.0, step=0.1, min=-5.0, max=0.0, format='%.2f') \
                            .classes('flex-1').props('outlined dense')
                        u_max_input = ui.number(label='u_max', value=1.0, step=0.1, min=0.0, max=5.0, format='%.2f') \
                            .classes('flex-1').props('outlined dense')
                    ui.label('Set minimum and maximum control values').classes('text-xs text-gray-500')
                
                ui.separator().classes('my-2')
                
                # Info card
                #with ui.card().classes('bg-purple-50 border-purple-200 p-4'):
                #    with ui.row().classes('items-start gap-2'):
                #        ui.icon('info', size='1.2rem').classes('text-purple-600')
                #        with ui.column().classes('gap-1'):
                #            ui.label('System Info').classes('text-sm font-semibold text-purple-900')
                #            ui.label('• Initial conditions: x₀ = 0, u₀ = 0').classes('text-xs text-purple-800')
                #            ui.label('• Setpoint: Step at t = 2s').classes('text-xs text-purple-800')
                #            ui.label('• Time range: 0 to 20s').classes('text-xs text-purple-800')
                
                #ui.space()
                
                # Update button
                update_button = ui.button('Run Simulation', icon='play_arrow', on_click=lambda: update_plots()) \
                    .props('color=purple size=md').classes('w-full mt-2')
            
            # Plot Area
            with ui.card().classes('glass-card p-6').style('flex: 1'):
                with ui.row().classes('items-center gap-2 mb-4'):
                    ui.icon('show_chart', size='1.5rem').classes('text-purple-600')
                    ui.label('Simulation Results').classes('text-xl font-semibold text-gray-800')
                
                plot = ui.plotly(create_plots(1.0,0.5, 1.5, False, False, [-1.0, 1.0])).classes('w-full')
        
        def update_plots():
            """Update plots with current parameter values"""
            u_lim_val = [u_min_input.value, u_max_input.value]
            fig = create_plots(c_p_slider.value, t_cl_slider.value, t_n_slider.value, use_ref_switch.value, 
                             adapt_t_switch.value, u_lim_val)
            plot.update_figure(fig)
            c_p_badge.set_text(f'{c_p_slider.value:.2f}')
            t_cl_badge.set_text(f'{t_cl_slider.value:.2f}')
            t_n_badge.set_text(f'{t_n_slider.value:.2f}')
            ui.notify('Simulation updated successfully!', type='positive', 
                     position='top', icon='check_circle')
        
        # Update badges when sliders change
        c_p_slider.on_value_change(lambda e: c_p_badge.set_text(f'{e.value:.2f}'))
        t_cl_slider.on_value_change(lambda e: t_cl_badge.set_text(f'{e.value:.2f}'))
        t_n_slider.on_value_change(lambda e: t_n_badge.set_text(f'{e.value:.2f}'))

app.native.window_args['resizable'] = True
app.native.start_args['debug'] = False
app.native.settings['ALLOW_DOWNLOADS'] = True
app.native

# Run the app
#ui.run(title='PI Simulator', port=8080, favicon='📊')
ui.run(title='PI Simulator', window_size=(1300, 950), native=True, reload=False)

