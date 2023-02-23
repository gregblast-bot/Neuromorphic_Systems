import numpy as np
import matplotlib.pyplot as plt

# Initialize number of stages in the ring oscillator
stages = 6

# Initialize normalized amplitude
A = 1

# Initialize normalized frequency (Hz)
f = 1

# Initialize variable for 2pi
two_pi = 2*np.pi

# Initialize horizontal shift (pi/3 radians = 60 degrees)
shift = two_pi/stages

# Initialize time interval for which the output will be plotted
time = np.linspace(0, 1, 100)

# Initialize an empty list to store the outputs of all stages
y = np.zeros((stages, len(time)))

# Calculate the output of each stage
for i in range(stages):
    y[i, :] = A * np.sin(two_pi * f * time + shift*i)

# Initialize an array to store the cross-correlation outputs
corr = np.zeros((stages, len(time)))

# Calculate the cross-correlation outputs between the first stage and every other stage
for i in range(stages):
    corr[i, :] = np.multiply(y[0, :], y[i, :])

# Threshold level for generating events/spikes
threshold = 0.1

# Apply the windowed threshold function
threshold_array = np.zeros((stages, len(time)))
threshold_array[corr > threshold] = 1
threshold_array[corr < threshold] = 0

fig, ax = plt.subplots(1, 6, figsize=(10, 5))

# Apply the windowed threshold function to  the cross-correlation outputs
# Generate the unique code for each phase Plot the cross-correlation event outputs
for i in range(stages):
    print('Unique code for phase', i, "\n", threshold_array[i, :], "\n")
    ax[i].plot(time, threshold_array[i, :])
    ax[i].set_xlabel('Time (s)')

# Plot
ax[0].set_ylabel('Amplitude')
ax[2].set_title('Unique Phase Codes')
plt.show()