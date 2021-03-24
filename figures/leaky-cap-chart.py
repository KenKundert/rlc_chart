#!/usr/bin/env python3

from rlc_chart import RLC_Chart
from math import log10 as log, pi as π

fmin = 1
fmax = 1e8
zmin = 1
zmax = 1e6
with RLC_Chart(
    'leaky-cap-chart.svg', fmin, fmax, zmin, zmax,
    axes='FZCL',
    #fz_grid_color='red',
    #cl_grid_color='blue',
    #decade=2, font_size=24
) as chart:
    mult = 10**((log(fmax) - log(fmin))/400)
    f = fmin
    freq = []
    impedance = []
    resistance = []
    reactance = []
    while(f <= 1.01*fmax):
        z1 = 2 + 1/(2j*π*f*1e-9) + 2j*π*f*10.0e-6
        z2 = 5e5
        z = z1 * z2 / (z1 + z2)
        freq += [f]
        impedance += [abs(z)]
        resistance += [abs(z.real)]
        reactance += [abs(z.imag)]
        f *= mult
    chart.add_trace(freq, impedance)
    #chart.add_trace(freq, resistance, stroke='blue')
    #chart.add_trace(freq, reactance, stroke='red')
