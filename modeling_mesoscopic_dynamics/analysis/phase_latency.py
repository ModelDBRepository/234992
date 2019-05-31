"""
"""
import numpy as np
import matplotlib.pylab as plt
from scipy.ndimage.filters import gaussian_filter
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from graphs.my_graph import set_plot

### GENERATING FAKE SIGNALS

def one_exponential(t, A1=1., t01=100., Ta1=50., Tb1=500.,\
                    smoothing = 10.):
    """
    building a signal that corresponds to 2 events at t01 and t02
    each event is convoluted with a double exponential waveform 
    of amplitude A, first time constant Ta and second time constant Tb

    we smooth the start at the t0's with a gaussian smoothing
    """
    s = np.zeros(len(t)) # 0 by default
    s = np.array([s[i]+A1*(np.exp(-(t[i]-t01)/Tb1)-np.exp(-(t[i]-t01)/Ta1)) if (t[i]>t01) else s[i] for i in range(len(t))])
    s = gaussian_filter(s, int(smoothing/(t[1]-t[0])))
    return s


### PHASE ANALYSIS
from scipy.signal import hilbert

def get_signal_phase(signal):
    ht = hilbert(signal) # hilbert transform -> complex number
    return np.angle(ht) # just takes the angle

def find_positive_phase_crossing(t, phase, criteria=-np.pi/2.+np.pi/6.):
    return np.where((phase[1:]>criteria) & (phase[:-1]<=criteria))

def find_latencies_over_space(t, X, signal,\
                              signal_criteria=0.05,\
                              baseline=0, discard=20,\
                              phase_criteria=-np.pi/2.+np.pi/4.):
    signal2 = np.abs(signal)
    i_discard = int(discard/(t[1]-t[0]))
    t = t[i_discard:]
    signal2 = signal2[i_discard:,:]-baseline
    XX, TT = [], []
    for i in range(signal2.shape[1]):
        if signal2[:,i].max()>=signal_criteria*signal2.max():
            phase = get_signal_phase(signal2[:,i])
            ii = find_positive_phase_crossing(t, phase)
            if len(ii[0])>0:
                XX.append(X[i])
                TT.append(t[ii[0][0]])
    return TT, XX


if __name__=='__main__':
    
    ### MODEL SETUP
    tstop, dt = 3000., 0.1
    t = np.arange(-2000,int(tstop/dt))*dt
    zoom = [0.,800.] # temporal zoom

    T_nrml = 50. # regular time constant integration
    T_fast = 25. # fast network integration time constant

    fig, AX = plt.subplots(2, 2, figsize=(10,10))
    plt.subplots_adjust(hspace=.3, wspace=.3)

    ## NETWORK WITHOUT FASTER INTEGRATION

    A1_A, A2_A, A2_A_obs = 1., 1., 0.55
    s_lin_A = one_exponential(t, A1=1., Ta1=T_nrml)
    s_obs_A = one_exponential(t, A1=.6, Ta1=T_nrml)

    # signal plot
    for i in range(2):
        AX[0,i].plot(t, s_obs_A, 'r-', lw=3, label='signal A')
        AX[0,i].plot(t, s_lin_A, 'b--', lw=2, label='signal B')
        AX[0,i].legend(frameon=False, loc='best', prop={'size':'xx-small'})

        AX[1,i].plot(t, get_signal_phase(s_obs_A), 'r-', lw=3, label='signal A')
        AX[1,i].plot(t, get_signal_phase(s_lin_A), 'b--', lw=2, label='signal B')
        AX[1,i].legend(frameon=False, loc='best', prop={'size':'xx-small'})

        iA = find_positive_phase_crossing(t, get_signal_phase(s_obs_A))
        iB = find_positive_phase_crossing(t, get_signal_phase(s_lin_A))
        AX[1,i].plot([t[iA],t[iA]], [0,get_signal_phase(s_obs_A)[iA]], 'r-', lw=1)
        AX[1,i].plot([t[iB],t[iB]], [0,get_signal_phase(s_lin_A)[iB]], 'b--', lw=1)
        AX[0,i].plot([t[iA],t[iA]], [0,s_obs_A[iA]], 'r-', lw=1)
        AX[0,i].plot([t[iB],t[iB]], [0,s_lin_A[iB]], 'b--', lw=1)

    AX[0,0].set_title('zoom')
    AX[0,0].set_xlim(zoom)
    AX[0,1].set_title('full signal')

    set_plot(AX[0,1], xlabel='time (ms)', ylabel='VSD signal')
    set_plot(AX[1,1], xlabel='time (ms)', ylabel='phase $\phi(t)$ (Rd)',\
             yticks=[-np.pi/2., 0, np.pi/2.],\
             yticks_labels=['$-\pi$/2','0','$\pi$/2'])
    set_plot(AX[0,0], xlabel='time (ms)', ylabel='VSD signal', xlim=zoom)
    set_plot(AX[1,0], xlabel='time (ms)', ylabel='phase $\phi(t)$ (Rd)',xlim=zoom,\
             yticks=[-np.pi/2., 0, np.pi/2.],\
             yticks_labels=['$-\pi$/2','0','$\pi$/2'])

    plt.show()
