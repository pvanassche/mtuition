# Various way to implement a PI Control

The standard PI controller consists of a proportional action and an integral action. The purpose of the proportional action is to bring the process on the setpoint trajectory, i.e. to eliminate any deviations from the setpoint trajectory. 
The purpose of the integral action is to keep the process on the setpoint trajectory, i.e. to zero any steady-state errors.

The standard implementation of a PI controller has some quirks. This folder contains implementations in Python of various improvements.
* **pi_control_integral.py**: eleiminate integral action-induced overshoot by computing the error that is integrated relative to the ideal closed-loop response rather than the setpoint itself. 
