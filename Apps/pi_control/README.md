# PI Control Simulator

An interactive application for simulating and visualizing the behaviour of a PI controller with real-time parameter adjustment.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)

## Overview

This application provides an intuitive interface for simulating a PI controller. Built with NiceGUI and Plotly, it offers real-time visualization and interactive parameter control for exploring system behavior.

## System Equations

The simulator solves the following equations:

```
(1)  c_p * dx/dt = u_ctrl - ul
(2)  u_ctrl = (sp - x) / t_cl + u 
(3)  du/dt = (r - x) / (t_cl × t_n)
(4a) r = sp
      OR
(4b) dr/dt = (sp - r) / t_cl
```

Where:
- `x(t)` is the process variable to be controlled
- `u_ctrl(t)` is the command produced by the PI controller
- `u(t)` is the load as estimated by the integral action of the PI controller
- `sp(t)` is a setpoint function (step input by default)
- `ul(t)` is the actual load (step input by default)
- `c_p` is the actual system inertia. The PI controller assues c_p=1.
- `t_cl` is the closed-loop time constant in seconds
- `t_n` is the integration time constant in seconds

## Features

### Interactive Controls
- **Plant model**: Plant is an integrator with adjustable slider for `c_p`.
- **Time Constants**: Adjustable sliders for `t_cl` and `t_n`.
- **Improved Integral**: Toggle switch to use the ideal closed-loop reference trajectory for computing the integral error.
- **Gain Scheduling**: Toggle switch for handling limiting of `u_ctrl` via gain scheduling, i.e. by adjusting `t_cl` and `t_n`.
- **Control Limits**: Input fields for minimum and maximum allowable control values for `u_ctrl` 

### Visualization
- Real-time plotting using Plotly with interactive features:
  - Zoom, pan, and hover capabilities.
  - Separate plots for process variable `x(t)` and load estimate `u(t)`.
  - Setpoint and load overlay for tracking performance.

### Modern UI/UX
Interface design created using NiceGUI which in turn builds on Vue, Quasar and Tailwind. NiceGUI enables the app to be 
coded in Python with deployment as a stand-alone application or as a web application. For more info, go to [https://nicegui.io](https://nicegui.io).

## Installation

### Prerequisites
- Python 3.11 or higher

### Dependencies

```bash
pip install pywebview numpy scipy plotly nicegui
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

### requirements.txt
```
nicegui>=1.4.0
numpy>=1.24.0
scipy>=1.10.0
plotly>=5.14.0
```

## Usage

### Running the Application

```bash
python test_pi.py
```

The application will start a local web server and a stand-alone GUI. When starting the app as a web app, open your browser and navigate to:

```
http://localhost:8080
```

### Using the Interface

1. **Adjust Parameters**: Use the sliders to modify `c_p`, `t_cl` and `t_n`
2. **Configure Options**: Toggle switches to adjust computation of integral action and clipping of the controller output.
3. **Set Control Limits**: Enter desired `u_min` and `u_max` values
4. **Run Simulation**: Click the "Run Simulation" button to update the plots
5. **Interact with Plots**: Hover over the plots to see exact values, zoom in/out, or pan

### Default Configuration

- Initial conditions: `x₀ = 0`, `u₀ = 0`, `r₀ = 0`
- System inertia: `c_p = 1.0` (perfect match with controller's assumption)
- Time constants: `t_cl = 0.5`, `t_n = 1.5`
- Setpoint: Step function (0 → 1 at t = 2s)
- Load: Step function (0 → 0.5 at t = 10s)
- Time range: 0 to 20 seconds
- Control limits: `u_lim = [-1.0, 1.0]`

## Code Structure

### DynamicalSystem Class

A callable class that encapsulates the PI controller. This makes it easy to manage parameters, setpoints and load.

```python
class DynamicalSystem:
    def __init__(self, x0=0.0,u0=0.0,r0=0.0, c_p=1.0, t_cl=0.5,t_n=1.5,
        sp=None,ul=None, use_ref=False, adapt_t=False, u_lim=None):
        
    def __call__(self, t, y):
        # ODE evaluation (compatible with scipy.solve_ivp)
        
    def solve(self, t_span=(0, 10), t_eval=None, method='LSODA'):
        # Solve the system using scipy.integrate.solve_ivp
        
    def get_results(self):
        # Extract time series data
```

## Customization

### Modifying the Setpoint Function

Edit the `setpoint_step` and `load_step` function in `create_plots()`:

```python
def setpoint_step(t):
    return 1.0 if t >= 2.0 else 0.0

def load_step(t):
    return 0.5 if t >= 10.0 else 0.0
    
# Alternative examples:
# Ramp: return min(t / 5.0, 1.0)
# Sine: return 1.0 + 0.5 * np.sin(2 * np.pi * t / 10.0)
```

### Adjusting Time Range

Modify the time span in the `solve()` call:

```python
system.solve(t_span=(0, 20))  # Default: 0 to 20 seconds
```

## Browser Compatibility

Tested and optimized for:
- Chrome/Edge (recommended)
- Firefox
- Safari

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [NiceGUI](https://nicegui.io/) - Python UI framework
- Visualization powered by [Plotly](https://plotly.com/python/)
- Numerical integration using [SciPy](https://scipy.org/)

---

**Note**: This simulator is intended for educational and research purposes. Always validate results with analytical solutions when possible.
