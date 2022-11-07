from matplotlib import pyplot as plt
import numpy as np

from components import *
from utils import *

start = 0
end = 1000
steps = 100000
dt = (end - start) / steps
#print(dt)

src = Source(10, noise_f, square_f)
vco = VCO(10, 3)
detector = Detector()
low_pass = LowPass(0.001)

v_i_s = []
v_o_s = []
v_d_s = []
v_f_s = []
ts = np.linspace(start, end, steps)

last_v_f = 0

for t in ts:
    src.step(t, dt)
    vco.step(t, dt, last_v_f)

    v_i = src.out()
    v_o = vco.out()

    detector.step(t, dt, v_i, v_o)
    v_d = detector.out()

    low_pass.step(t, dt, v_d)
    v_f = low_pass.out()

    v_i_s.append(v_i)
    v_o_s.append(v_o)
    v_d_s.append(v_d)
    v_f_s.append(v_f)

    last_v_f = v_f


def graph():
    last = 3000
    ax, subplots = plt.subplots(2)
    subplots[0].plot(ts[-last:], v_i_s[-last:], color='r')
    subplots[0].plot(ts[-last:], v_o_s[-last:], color='g')
    subplots[1].plot(ts[-last:], v_d_s[-last:], color='b')
    subplots[1].plot(ts[-last:], v_f_s[-last:], color='y')
    plt.show()

graph()
