from utils import square_f, hz_to_omega
from math import pi

class Source:
    phi = 0

    def __init__(self, hz, noise_f, out_f):
        self.omega = hz_to_omega(hz)
        self.noise_f = noise_f
        self.out_f = out_f

    def step(self, t, dt):
        self.phi += (self.omega + self.noise_f(t)) * dt

    def out(self):
        return self.out_f(self.phi)

class NRZ_TX:
    bit_num = 0
    bit_phi = 0
    conseq = 0
    last_bit = 0.5
    next_bit = 0.5

    def __init__(self, hz, noise_f, data):
        self.omega = hz_to_omega(hz)
        self.noise_f = noise_f
        self.data = data

    def determine_next_bit(self):
        data_bit = self.data[self.bit_num] if self.bit_num < len(self.data) else 0
        if data_bit == self.last_bit:
            if self.conseq >= 5:
                # bit stuffing
                self.next_bit = 1 - self.last_bit
                self.conseq = 1
                return
            self.next_bit = data_bit
            self.conseq += 1
            self.bit_num += 1
            return
        self.next_bit = data_bit
        self.conseq = 1
        self.bit_num += 1

    def step(self, t, dt):
        omega = self.omega + self.noise_f(t)
        assert(omega > 0)

        self.bit_phi += omega * dt
        if self.bit_phi > 2 * pi:
            self.bit_phi -= 2 * pi
            self.determine_next_bit()
            self.last_bit = self.next_bit

    def out(self):
        return self.next_bit

class VCO:
    phi = 0

    def __init__(self, hz, slope_hz):
        self.omega = hz_to_omega(hz)
        self.slope = hz_to_omega(slope_hz)

    def step(self, t, dt, v_in):
        self.phi += (self.omega + v_in * self.slope) * dt

    def out(self):
        return square_f(self.phi)

class LowPass:
    avg = None
    def __init__(self, r):
        self.r = r

    def step(self, t, dt, v_in):
        if self.avg is None:
            self.avg = v_in
            return
        self.avg = self.avg + (v_in - self.avg) / dt * self.r

    def out(self):
        return self.avg

class Detector:
    last_v_1 = 0
    last_v_2 = 0
    up = 0
    down = 0

    def step(self, t, dt, v_1, v_2):
        rise_1 = self.last_v_1 < 0.75 and v_1 > 0.75
        rise_2 = self.last_v_2 < 0.75 and v_2 > 0.75

        if rise_1:
            self.up = 1
        if rise_2:
            self.down = 1

        self.last_v_1 = v_1
        self.last_v_2 = v_2

        if self.up and self.down:
            self.up = 0
            self.down = 0

    def out(self):
        if self.up:
            return 1
        if self.down:
            return -1
        return 0
