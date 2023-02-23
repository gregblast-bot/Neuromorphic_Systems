import numpy as np
import matplotlib.pyplot as plt

# Initialize capacitance (pF)
C_mem = np.power(10.0, -12)

# Initialize current (uA)
I_inject = np.power(10.0, -6)

# Initialize pressure interval for which the output will be plotted (N)
pressure = np.linspace(1, 10, 100)

print(pressure)
# Initialize voltages (V)
V_th = 1
V_reset = 0
Vm_last = 0
V_mem = np.zeros(pressure.shape)
V_out = []

# Initialize conductance (Mho)
g_leak = 0

# Initialize count for spike frequency
count = 0
freq = []

for p in pressure:
    # Set to last (either reset or integrate)
    V_mem = Vm_last
    # Compare
    if V_mem > V_th:
        V_out = np.append(V_out, 1)
        # Reset
        Vm_last = V_reset
        count += 1
    if V_mem < V_th:
        V_out = np.append(V_out, 0)
        Vm_temp = Vm_last
        # Integrate
        Vm_last = ((I_inject * p) / C_mem) + Vm_temp
    freq.append(count)

# Plot
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].plot(pressure, freq)
ax[0].set_xlabel('Pressure (N)')
ax[0].set_ylabel('Frequency (Hz)')
ax[0].set_title('Frequency Vs. Pressure')

ax[1].plot(pressure, V_out)
ax[1].set_xlabel('Pressure (N)')
ax[1].set_ylabel('Voltage (V)')
ax[1].set_title('Voltage Vs. Pressure')
plt.show()
