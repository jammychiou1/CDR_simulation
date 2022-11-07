from utils import square_f, hz_to_omega

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
        rise_1 = v_1 > self.last_v_1
        rise_2 = v_2 > self.last_v_2

        self.last_v_1 = v_1
        self.last_v_2 = v_2

        if rise_1:
            self.up = 1
        if rise_2:
            self.down = 1

        if self.up and self.down:
            self.up = 0
            self.down = 0

    def out(self):
        if self.up:
            return 1
        if self.down: return -1
        return 0
