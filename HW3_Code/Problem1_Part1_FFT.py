import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack

for l in range(6):

    wave_array = np.array(["zero40k.wav", "one40k.wav", "two40k.wav", "three40k.wav", "four40k.wav", "five40k.wav"])

    # Get audio sample
    sample_rate, data = scipy.io.wavfile.read(wave_array[l])

    # Calculate the time period of each number (This would ideally be 1s)
    # Note: data.shape[0] or len(data) can be used here. All data has the same time_period here.
    time_period = data.shape[0] / sample_rate

    # Break down the audio signal into 4 time slices
    num_slices = 4
    slice_duration = time_period * 0.25
    slice_length = int(slice_duration * sample_rate)

    # Check values
    print(sample_rate)
    print(time_period)
    print(slice_duration)
    print(slice_length)
    print("\n")

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

    # Four subplots, one for each slice
    fig, ax = plt.subplots(4)

    # Accessing the index and value for each item in the fft_array
    for i, fft_i in enumerate(fft_array):
        ax[i].plot(xf, 2.0/N * np.abs(fft_i[:N//2]))

    ax[0].set_title(wave_array[l])
    ax[3].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel('Amplitude')

plt.show()