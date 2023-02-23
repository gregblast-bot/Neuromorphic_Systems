import numpy as np
import matplotlib.pyplot as plt

# Initialize capacitance (pF)
C_mem = np.power(10.0, -12)

# Initialize current (uA)
I_inject = np.power(10.0, -6)

# Initialize time interval for which the output will be plotted
time = np.linspace(0, 1, 10)

# Initialize voltages (V)
V_th = 1
V_reset = 0
Vm_last = 0
V_mem = np.zeros(time.shape)
V_out = []

# Initialize conductance (Mho)
g_leak = 0

for t in time:
    # Set to last (either reset or integrate)
    V_mem = Vm_last
    # Compare
    if V_mem > V_th:
        V_out = np.append(V_out, 1)
        # Reset
        Vm_last = V_reset
    if V_mem < V_th:
        V_out = np.append(V_out, 0)
        Vm_temp = Vm_last
        # Integrate
        Vm_last = ((I_inject * t) / C_mem) + Vm_temp

# Plot
plt.plot(time, V_out)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Vmem as a Function of Time')
plt.show()

