import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack
from scipy import signal
import time

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

# Loop for roughly one second
duration = 1

while True:
    # Initialize array to store frames
    frames = []

    print("SPEAK\n\n")

    # Store data in chunks for the set time
    for i in range(0, int(RATE / CHUNK)*duration):
        data = stream.read(CHUNK)
        frames.append(data)
        data = np.frombuffer(data, np.int16)
        # line.set_ydata(data)
        # fig.canvas.draw()
        # fig.canvas.flush_events()
        # plt.pause(0.01)

    # Concatenate into a single bytes object to be used
    data = np.frombuffer(b''.join(frames), np.int16)

    # Calculate the time period of each number (This would ideally be 1s)
    # Note: data.shape[0] or len(data) can be used here
    time_period = len(data) / RATE

    # Break down the audio signal into 4 time slices
    num_slices = 4
    slice_duration = time_period * 0.25
    slice_length = int(slice_duration * RATE)

    # Slice the audio into 4 parts
    slices = np.array_split(data, 4)

    # FFT
    # Number of sample points per slice (10000)
    # According to Nyquist-Shannon sampling theorem, the maximum frequency that can be represented at this rate is 5KHz
    N = slice_length
    # Sample spacing (0.0001)
    T = 1.0 / slice_length
    # Set x to time ([0, 1] seconds with 10000 samples)
    x = np.linspace(0.0, N*T, N)

    # Initialize list and loop to perform FFT on each slice, accessing only the values in slices
    fft_array = []
    for slice_i in slices:
        fft = scipy.fftpack.fft(slice_i)
        fft_array.append(fft)

    # Set xf to Hertz ([0, 5000] Hz with 5000 samples)
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

    # Define center frequencies and bandwidth of the BPF
    center_frequencies = [535, 1130, 1725, 2320, 2915, 3510, 4105, 4700]
    # [750, 1150, 2250, 3000, 3750, 4500, 5250, 6000]
    # [535, 1130, 1725, 2320, 2915, 3510, 4105, 4700]
    # [1175, 2350, 3525, 4700]
    bandwidth = 500

    # Compute the BPF transfer function for each center frequency
    bpfs = []
    for center_frequency in center_frequencies:
        # We have two critical frequencies for a BPF
        lower_frequency = center_frequency - bandwidth/2
        upper_frequency = center_frequency + bandwidth/2
        # Use butter method to design and implement 2nd order BPFs
        bpf = signal.butter(2, [lower_frequency, upper_frequency], btype='bandpass', fs=slice_length)
        bpfs.append(bpf)

    # Apply the BPF to each of the FFT outputs
    bpf_outputs = []
    for bpf in bpfs:
        for fft in fft_array:
            # Compute only magnitude not phase, or we get warning...
            # ComplexWarning: Casting complex values to real discards the imaginary part
            bpf_output = signal.lfilter(bpf[0], bpf[1], fft)
        bpf_outputs.append(bpf_output)

    # Compute the energy/power level in each frequency band
    energies = []
    for bpf_output in bpf_outputs:
        energy = np.sum(bpf_output)
        energies.append(energy)

    # Use numpy array and set the shape of the event matrix (8x4)
    energies_array = np.array(energies)
    events = np.zeros(shape=(8))
    for i in range(energies_array.shape[0]):
        # Set the threshold to half of the maximum power level recorded
        threshold = np.max(energies_array[i]) / 2
        if energies_array[i] > threshold:
            events[i] = 1
        # for j in range(4):
        #     if energies_array[i] > threshold:
        #         events[i][j] = 1

    # zero_event = np.array([[0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [0., 0., 0., 0.],
    #                        [0., 0., 0., 0.]])
    # 
    # one_event = np.array([[1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [0., 0., 0., 0.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [0., 0., 0., 0.]])
    # 
    # two_event = np.array([[0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.]])
    # 
    # three_event = np.array([[0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [0., 0., 0., 0.]])
    # 
    # four_event = np.array([[0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.]])
    # 
    # five_event = np.array([[1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [1., 1., 1., 1.],
    #                        [0., 0., 0., 0.],
    #                        [0., 0., 0., 0.],
    #                        [0., 0., 0., 0.]])

    zero_event = np.array([0., 0., 0., 1., 1., 1., 0., 0.])

    one_event = np.array([1., 1., 0., 1., 1., 0., 0., 0.])

    two_event = np.array([0., 0., 0., 1., 1., 1., 1., 1.])

    three_event = np.array([0., 0., 0., 0., 0., 1., 1., 0.])

    four_event = np.array([0., 0., 1., 1., 0., 0., 1., 1.])

    five_event = np.array([1., 1., 1., 1., 1., 0., 0., 0.])

    zero_comparison = zero_event == events
    one_comparison = one_event == events
    two_comparison = two_event == events
    three_comparison = three_event == events
    four_comparison = four_event == events
    five_comparison = five_event == events

    print(events)

    if zero_comparison.all() == True:
        print("ZERO\n\n\n")
    elif one_comparison.all() == True:
        print("ONE\n\n\n")
    elif two_comparison.all() == True:
        print("TWO\n\n\n")
    elif three_comparison.all() == True:
        print("THREE\n\n\n")
    elif four_comparison.all() == True:
        print("FOUR\n\n\n")
    elif five_comparison.all() == True:
        print("FIVE\n\n\n")
    else:
        print("UNDEFINED\n\n\n")

    time.sleep(3)