class NeuronModel:
    def __init__(self):
        pass

    def __str__(self):
        return 'This is the neuron model class. Current models include LIF and Izhikevich.'

    '''
    Function for Izhikevich neuron model spiking behavior
    '''
    def run_spike_izhikevich(self, a, b, c, d, dt, v, u, bias):
        dv = 0.04 * v ** 2 + 5 * v + 140 - u + bias  # dv/dt
        du = a * (b * v - u)  # du/dt
        v += dt * dv
        u += dt * du
        # If v = 30mV, v is reset to c and u is reset to u + d
        if v >= 30:
            v = c
            u = u + d
        return v, u

    '''
    Function for LIF neuron model spiking behavior
    '''
    def run_spike_lif(self, a, b, c, d, dt, v, u, bias):
        dv = 0.04 * v ** 2 + 5 * v + 140 - u + bias  # dv/dt
        du = a * (b * v - u)  # du/dt
        v += dt * dv
        u += dt * du
        # If v = 30mV, v is reset to c and u is reset to u + d
        if v >= 30:
            v = c
            u = u + d
        return v, u