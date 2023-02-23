import numpy as np
import matplotlib.pyplot as plt

# Initialize vacuum permittivity (F/m)
e0 = 8.854*np.power(10.0, -12)

# Initialize relative permittivity
e_rel = 10

# Initialize absolute permittivity (F/m)
e_abs = e0*e_rel

# Initialize Area (mm^2)
A = 1.13

# Initialize distance (mm)
d0 = 1

# Initialize constant (mm/N)
k = 0.01

# Initialize pressure interval for which the output will be plotted (N)
pressure = np.linspace(1, 10, 100)

# Initialize capacitance to empty list
C_mem = []

# Loop through pressure interval and apply given equations
for p in pressure:
    d = d0 - k*p
    C_mem = np.append(C_mem, (e_abs*A)/d)

# Plot
plt.plot(pressure, C_mem)
plt.xlabel('Pressure (N)')
plt.ylabel('Capacitance (F)')
plt.title('Cmem as a Function of Pressure')
plt.show()