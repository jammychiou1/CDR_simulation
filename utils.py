from math import sin, pi

noise_f = lambda t: 0.3 * sin(t)
square_f = lambda phi: 0 if phi % (2 * pi) < pi else 1

