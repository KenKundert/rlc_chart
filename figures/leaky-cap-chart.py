#!/usr/bin/env python3
"""
Create the RCL chart for a leaky capacitor with the following parameters:

    Rs = 2 Ω
    Rp = 500 kΩ
    C = 1 nF
    L = 10 μH
    fmin = 1 Hz
    fmax = 100 MHz
    zmin = 1 Ω
    zmax = 1 MΩ
    filename = "leaky-cap-chart.svg"
"""

from rlc_chart import RLC_Chart
from inform import display, fatal, os_error
from math import log10 as log, pi as π
from quantiphy import Quantity

# Add parameters as local variables
params = Quantity.extract(__doc__)
globals().update(params)
#display(f"Parameters:")
#for k, v in params.items():
#    display(f'   {k} = {v}')

try:
    with RLC_Chart(filename, fmin, fmax, zmin, zmax) as chart:
        mult = 10**((log(fmax) - log(fmin))/400)
        f = fmin
        freq = []
        impedance = []
        resistance = []
        reactance = []

        # Compute impedance of component
        # z = (Rs + 1/(jωC + jωL) ‖ Rp
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
except OSError as e:
    fatal(os_error(e))
