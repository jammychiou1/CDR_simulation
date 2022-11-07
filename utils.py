from math import sin, pi

def hz_to_omega(hz):
    return hz * 2 * pi

noise_f = lambda t: 0.03 * sin(t)
square_f = lambda phi: 0 if phi % (2 * pi) < pi else 1
