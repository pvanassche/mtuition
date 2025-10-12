import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Define the system of differential equations modeling PI controller
def system(y, t, p):
    """
    System of ODEs:
    dx/dt = (sp-x)/p[0] + u_l
    du_l/dt = (sp_l-x)/(p[0]*p[1])
    dsp_l/dt = (sp-sp_l)/p[0] 
    
    y[0] = x
    y[1] = u_l
    y[2] = sp_l
    
    p[0] = sp
    p[1] = 0: standard integral action, 1: improved integral action
    p[2] = tau_cl
    p[3] = tau_n
    """
    x, u_l, sp_l = y
    sp = p[0]
    dxdt = (sp-x)/p[2] + u_l
    if p[1]==1:
        du_ldt = (sp_l-x)/(p[2]*p[3])
    else:
        du_ldt = (sp-x)/(p[2]*p[3])
    dsp_ldt = (1-sp_l)/p[2]
    return [dxdt, du_ldt, dsp_ldt]

# Initial conditions
x0    = 0.0   # initial value of x
u_l0  = 0.0   # initial value of u
sp_l0 = 0.0  # initial value of xs
y0 = [x0, u_l0, sp_l0]

# Time array
t = np.linspace(0, 10, 1000)

# Solve ODE for standard integral action
p = [1, 0, 0.5,1]
solution = odeint(system, y0, t, args=(p,))
x1 = solution[:, 0]
u1 = solution[:, 1]

# Solve ODE for improved integral action
p = [1,1, 0.5,1]
solution = odeint(system, y0, t, args=(p,))
x2 = solution[:, 0]
u2 = solution[:, 1]


# Create plots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
lwidth = 8
grid_on = True

# Plot x1 vs t
axes[0, 0].plot(t, x1, 'b-', linewidth=lwidth, color=[84/255, 130/255, 53/255])
axes[0, 0].set_xlabel('Time (t)', fontsize=11)
axes[0, 0].set_ylabel('x(t)', fontsize=11)
axes[0, 0].set_title('standard integral: x vs Time', fontsize=12, fontweight='bold')
if grid_on:
    axes[0, 0].grid(True, alpha=0.3)

# Plot u1 vs t
axes[0, 1].plot(t, u1, 'r-', linewidth=lwidth, color=[192/255, 0/255, 0/255])
axes[0, 1].set_xlabel('Time (t)', fontsize=11)
axes[0, 1].set_ylabel('u(t)', fontsize=11)
axes[0, 1].set_title('standard integral: u_l vs Time', fontsize=12, fontweight='bold')
if grid_on:
    axes[0, 1].grid(True, alpha=0.3)

# Plot x2 vs t
axes[1, 0].plot(t, x2, 'b-', linewidth=lwidth, color=[84/255, 130/255, 53/255])
axes[1, 0].set_xlabel('Time (t)', fontsize=11)
axes[1, 0].set_ylabel('x(t)', fontsize=11)
axes[1, 0].set_title('improved integral: x vs Time', fontsize=12, fontweight='bold')
if grid_on:
    axes[1, 0].grid(True, alpha=0.3)

# Plot u2 vs t
axes[1, 1].plot(t, u2, 'r-', linewidth=lwidth, color=[192/255, 0/255, 0/255])
axes[1, 1].set_xlabel('Time (t)', fontsize=11)
axes[1, 1].set_ylabel('u(t)', fontsize=11)
axes[1, 1].set_title('improved integral: u_l vs Time', fontsize=12, fontweight='bold')
if grid_on:
    axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

