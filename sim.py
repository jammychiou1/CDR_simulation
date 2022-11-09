from matplotlib import pyplot as plt
import numpy as np

from components import *
from utils import *

start = 0
end = 1000
steps = 100000
dt = (end - start) / steps

vco = VCO(0.3, 0.05)
phase_detector = PhaseDetector()
low_pass = LowPass(0.001)
noise_f = sine_wave_f(0.01, 0.1, 0)
nrz = NRZ_TX(0.295, noise_f, [0, 0, 0, 0, 0, 1, 1, 1, 1, 1] * 1000)
edge_detector = EdgeDetector(0.3)
bbd = BangBangPD()

v_n_s = []
v_o_s = []
v_bb_s = []
v_d_s = []
v_f_s = []
v_e_s = []
ts = np.linspace(start, end, steps)

last_v_f = 0

for t in ts:
    nrz.step(t, dt)
    v_n = nrz.out()

    edge_detector.step(t, dt, v_n)
    v_e = edge_detector.out()

    vco.step(t, dt, last_v_f)
    v_o = vco.out()

    phase_detector.step(t, dt, v_e, v_o)
    v_d = phase_detector.out()

    bbd.step(t, dt, v_n, v_o)
    v_bb = bbd.out()

    low_pass.step(t, dt, v_bb)
    v_f = low_pass.out()

    v_n_s.append(v_n)
    v_o_s.append(v_o)
    v_d_s.append(v_d)
    v_f_s.append(v_f)
    v_e_s.append(v_e)
    v_bb_s.append(v_bb)

    last_v_f = v_f

def graph():
    slc = slice(0, 100000)
    fig, axs = plt.subplots(3, sharex=True)
    axs[0].plot(ts[slc], v_n_s[slc], color='r', label='nrz')
    axs[0].plot(ts[slc], v_o_s[slc], color='g', label='output')
    #axs[1].plot(ts[slc], v_e_s[slc], color='black', label='edge')
    axs[1].plot(ts[slc], v_o_s[slc], color='g', label='output')
    axs[2].plot(ts[slc], v_bb_s[slc], color='b', label='detector')
    axs[2].plot(ts[slc], v_f_s[slc], color='y', label='filtered')
    fig.legend()
    plt.show()

graph()
