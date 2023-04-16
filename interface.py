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

# if arduino.isOpen() == True:
#     arduinoData = arduino.readline().decode("ASCII")
#
# arduino.reset_input_buffer()

q = RingBuffer(100)  # Instantiate ring buffer, pass in capacity
arr = np.zeros(100)  # Initialize an int array of zeros for a given size


# arduino = serial.Serial('COM3', '9600')

# Get sensor data from Arduino in a separate flow of execution
def get_data():
    # While the program persists, we get data
    while True:
        # rawdata = int(arduino.readline()) # Read in the serial data
        rawdata = random.randint(1, 50)
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

    # Initialize variables
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

    # Initialize time and time step
    dt = 0.1
    time = np.arange(0, 10, dt)

    # Set input current to a pseudorandom even integer from 0 to 20 inclusive
    # I = random.randrange(0, 21, 2)
    I = 0.5 * 20 * (signal.square(2 * np.pi * time) + 1)

    # Initialize arrays
    v_array = np.zeros((4, time.shape[0]))
    u_array = np.zeros((4, time.shape[0]))

    # Create dictionary of variables for the modes of operation
    modes = {
        'a': [a, a, a, a_fs],
        'b': [b, b, b, b],
        'c': [c_rs, c_ib, c_ch, c],
        'd': [d_rs, d_ib, d_ch, d]
    }

    nm = NeuronModel()

    # Loop through dictionary
    # for i in range(4):
    #     # Set v and u
    #     v = modes['a'][i]
    #     u = modes['b'][i] * v
    #     for t in range(len(time)):
    #         v, u = nm.run_spike_izhikevich(a=modes['a'][i], b=modes['b'][i], c=modes['c'][i], d=modes['d'][i],
    #                                        dt=dt, v=v, u=u, bias=arr[t])
    #         v_array[i][t] = v
    #         u_array[i][t] = u

    # initializing a figure in
    # which the graph will be plotted
    fig = plt.figure()

    # marking the x-axis and y-axis
    axis = plt.axes(xlim=(0, 4),
                    ylim=(-2, 2))

    # initializing a line variable
    line, = axis.plot([], [], lw=3)

    # data which the line will
    # contain (x, y)
    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        x = np.linspace(0, 10, 1000)
        v = modes['a'][0]
        u = modes['b'][0] * v
        # plots a sine graph
        v, u = nm.run_spike_izhikevich(a=modes['a'][0], b=modes['b'][0], c=modes['c'][0], d=modes['d'][0],
                                       dt=dt, v=v, u=u, bias=arr[i])
        line.set_data(i, v)

        return line,


    anim = FuncAnimation(fig, animate, init_func=init, frames=100, interval=20, blit=True)

    plt.show()

    # titles = ['Regular Spiking', 'Intrinsically Bursting', 'Chattering', 'Fast Spiking']
    # plt.title(f'{titles[0]} for Membrane Potential (v)')
    # plt.xlabel('Time (ms)')
    # plt.ylabel('Voltage (mV)')
    # plt.plot(time, v_array[0])
    # plt.show()

    '''
    Function for plotting the Izhikevich neuron model spiking behavior
    '''
    # titles = ['Regular Spiking', 'Intrinsically Bursting', 'Chattering', 'Fast Spiking']
    # Plot membrane potential (v) and recovery variable (u) for all modes
    # for i in range(4):
    #     plt.title(f'{titles[i]} for Membrane Potential (v)')
    #     plt.xlabel('Time (ms)')
    #     plt.ylabel('Voltage (mV)')
    #     plt.plot(time, v_array[i])
    #     plt.show()
    #     plt.title(f'{titles[i]} for Recovery Varaible (u)')
    #     plt.xlabel('Time (ms)')
    #     plt.ylabel('Voltage (mV)')
    #     plt.plot(time, u_array[i])
    #     plt.show()
