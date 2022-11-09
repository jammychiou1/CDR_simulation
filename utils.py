from math import pi, sin

def hz_to_omega(hz):
    return hz * 2 * pi

square_f = lambda phi: 0 if phi % (2 * pi) < pi else 1
def sine_wave_f(A, Hz, phi):
    return lambda t: A * sin(hz_to_omega(Hz) * t + phi)
