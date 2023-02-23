import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack

mic = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 40000
CHUNK = int(RATE/20)
stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)
fig, ax = plt.subplots(figsize=(14, 6))
x = np.arange(0, 2 * CHUNK, 2)
ax.set_ylim(-5000, 5000)
ax.set_xlim(0, CHUNK)  # make sure our x axis matched our chunk size
line, = ax.plot(x, np.random.rand(CHUNK))

# Initialize array to store frames
frames = []
# Loop for roughly one second
duration = 1

# Store data in chunks for the set time
for i in range(0, int(RATE / CHUNK)*duration):
    data = stream.read(CHUNK)
    frames.append(data)
    data = np.frombuffer(data, np.int16)
    # line.set_ydata(data)
    # fig.canvas.draw()
    # fig.canvas.flush_events()
    # plt.pause(0.01)

# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
mic.terminate()

# Concatenate into a single bytes object to be used
data = np.frombuffer(b''.join(frames), np.int16)

# Save recording to .wav file
scipy.io.wavfile.write("name.wav", RATE, data)