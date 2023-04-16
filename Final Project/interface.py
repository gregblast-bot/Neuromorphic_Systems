import serial
import threading
import time
import logging
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import signal
from RingBuffer import RingBuffer
from NeuronModel import NeuronModel

# try:
#     arduino = serial.Serial("COM3", baudrate=9600, write_timeout=1, timeout=1)
# except:
#     print('Please check the port')

# arduino.reset_input_buffer()

q = RingBuffer(1000)  # Instantiate ring buffer, pass in capacity
arr = np.zeros(1000)  # Initialize an int array of zeros for a given size

try:
    arduino = serial.Serial("COM3", baudrate=9600)
except:
    print('Please check the port')


# Get sensor data from Arduino in a separate flow of execution
def get_data():
    # While the program persists, we get data
    while True:
        rawdata = int(arduino.readline())/10 # Read in the serial data and divide by power of 10 for data usability
        # rawdata = random.randint(1, 50)
        # If the ring buffer is not full, fill. Otherwise, empty all.
        if not q.full():
            q.enqueue(rawdata)
        else:
            for i in range(q.capacity):
                arr[i] = q.dequeue()


# The main flow of execution handles the neuron model while the program persists
if __name__ == "__main__":
    thread_x = threading.Thread(target=get_data, daemon=True)
    thread_x.start()

    # Initialize all local variables for LIF and Izhikevich neuron models
    a = 0.02  # Describes the timescale of the recovery variable u
    b = 0.2  # Describes the sensitivity of u to the sub-threshold fluctuations of the membrane potential v
    c = -65  # Describes the after-spike reset value of the membrane potential v caused by the caused by the fast high-threshold K+ conductances
    d = 2  # Describes after-spike reset of u caused by slow high-threshold Na+ and K+ conductances

    # Excitatory
    c_rs = -65  # Deep voltage reset for regular spiking
    d_rs = 8  # Large after-jump spike of u for regular spiking

    c_ib = -55  # High voltage reset for intrinsically bursting
    d_ib = 4  # Large after-jump spike of u for intrinsically bursting

    c_ch = -50  # Very high voltage reset for chattering
    d_ch = 2  # Moderate after-jump spike of u for chattering

    # Inhibitory
    a_fs = 0.1  # Fast recovery for fast spiking

    # Initialize time-step and time
    dt = 0.1
    time = np.arange(0, 100, dt)

    # Initialize arrays
    v_array = np.zeros(time.shape[0])
    u_array = np.zeros(time.shape[0])

    # Create dictionary of variables for the modes of operation
    modes = {
        'a': [a, a, a, a_fs],
        'b': [b, b, b, b],
        'c': [c_rs, c_ib, c_ch, c],
        'd': [d_rs, d_ib, d_ch, d]
    }

    # Instantiate neuron model
    nm = NeuronModel()
    vth = 80  # Define threshold voltage

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1)

    # Initialize two line objects (one in each axes)
    line1, = ax1.plot([], [], lw=3)
    line2, = ax2.plot([], [], lw=3, color='r')
    line = [line1, line2]

    # Initialize both axes, mark the x-axis and y-axis ranges and specify grid
    for ax in [ax1, ax2]:
        ax.set_ylim(-80, 50)
        ax.set_xlim(0, 100)
        ax.grid()

    # Data which the line will contain (x, y)
    def init():
        line[0].set_data([], [])
        line[1].set_data([], [])
        return line

    # Animate our neuron model output
    def animate(i):
        v = modes['a'][0]
        u = modes['b'][0] * v
        for t in range(len(time)):
            v, u = nm.run_spike_izhikevich(a=modes['a'][0], b=modes['b'][0], c=modes['c'][0], d=modes['d'][0],
                                           dt=dt, v=v, u=u, bias=arr[t], vth=vth)
            v_array[t] = v
            u_array[t] = u

        # update the data of both line objects
        line[0].set_data(time, v_array)
        line[1].set_data(time, u_array)

        return line


    '''
    Function for plotting the Izhikevich neuron model spiking behavior
    '''
    # Plot membrane potential (v) and recovery variable (u) for specified mode
    anim = FuncAnimation(fig, animate, init_func=init, frames=100, interval=20, blit=True)
    titles = ['Regular Spiking', 'Intrinsically Bursting', 'Chattering', 'Fast Spiking']
    plt.suptitle(f'{titles[0]} for Membrane Potential (v) and Recovery Variable (u)')
    plt.xlabel('Time (ms)')
    plt.ylabel('Pressure (N)')
    ax.yaxis.set_label_coords(-0.1, 1.1)
    plt.show()
