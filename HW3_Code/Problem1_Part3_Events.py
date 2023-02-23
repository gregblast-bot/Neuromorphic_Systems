import numpy as np
import scipy.fftpack
from scipy import signal

for l in range(6):

    wave_array = np.array(["zero40k.wav", "one40k.wav", "two40k.wav", "three40k.wav", "four40k.wav", "five40k.wav"])

    # Get audio sample
    sample_rate, data = scipy.io.wavfile.read(wave_array[l])

    # Calculate the time period of each number (This would ideally be 1s)
    # Note: data.shape[0] or len(data) can be used here
    time_period = data.shape[0] / sample_rate

    # Break down the audio signal into 4 time slices
    num_slices = 4
    slice_duration = time_period * 0.25
    slice_length = int(slice_duration * sample_rate)

    # Check values
    # print(sample_rate)
    # print(time_period)
    # print(slice_duration)
    # print(slice_length)

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
    # [750, 1150, 2250, 3000, 3750, 4500, 5250, 6000] // Given for 40K
    # [535, 1130, 1725, 2320, 2915, 3510, 4105, 4700] // Made for 10K
    # [1175, 2350, 3525, 4700] // Test
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
    events = np.zeros(shape=(8, 4))
    for i in range(energies_array.shape[0]):
        # Set the threshold to half of the maximum power level recorded
        threshold = np.max(energies_array[i]) / 2
        # print(threshold)
        for j in range(4):
            if energies_array[i] > threshold:
                events[i][j] = 1

    print(wave_array[l])
    print(events)
    print("\n")