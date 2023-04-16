class NeuronModel:
    def __init__(self):
        pass

    def __str__(self):
        return 'This is the neuron model class. Current models include LIF and Izhikevich.'

    '''
    Function for Izhikevich neuron model spiking behavior
    '''
    def run_spike_izhikevich(self, a, b, c, d, dt, v, u, bias, vth):
        dv = 0.04 * v ** 2 + 5 * v + 140 - u + bias  # dv/dt
        du = a * (b * v - u)  # du/dt
        v += dt * dv
        u += dt * du
        # If v = vth(mV), v is reset to c and u is reset to u + d
        if v >= 30:
            v = c
            u = u + d
        return v, u

    '''
    Function for LIF neuron model spiking behavior
    '''
    def run_spike_lif(self, a, b, c, d, dt, v, u, bias):
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

        '''
        Function for LIF neuron model spiking behavior
        '''
        def run_spike_lif(self, a, b, c, d, dt, v, u, bias):
            # Integrate
            V_mem[i] = V_last

            # Compare
            if V_mem[i] >= V_th:
                V_out[i] = 1  # Spiking
            else:
                V_out[i] = 0  # No spike

            if V_out[i] == 1:
                # Reset
                V_last = V_reset
                # Calculate spike frequency
                t_now = i+1
                temp1 = 1/(t_now-t_last)
                temp2 = temp1*10**4
                freq[j][i] = round(temp2)
            else:
                V_last += ((I_inject * dt) / C_mem)

            t_last = t_now