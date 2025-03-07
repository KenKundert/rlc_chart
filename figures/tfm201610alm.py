#!/usr/bin/env python3
# Convert S-parameters of inductor, measured as a two port, to impedance

from inform import fatal, os_error
from rlc_chart import RLC_Chart
from cmath import rect, pi as π
from pathlib import Path

y11 = []
y12 = []
y21 = []
y22 = []
Zind = []
freq = []
z0 = 50

try:
    data = Path('tfm201610alm_r47mtaa.s2p').read_text()
    lines = data.splitlines()
    for line in lines:
        line = line.strip()
        if line[0] in '!#':
            continue
        f, s11m, s11p, s12m, s12p, s21m, s21p, s22m, s22p = line.split()
        s11 = rect(float(s11m), π*float(s11p)/180)
        s12 = rect(float(s12m), π*float(s12p)/180)
        s21 = rect(float(s21m), π*float(s21p)/180)
        s22 = rect(float(s22m), π*float(s22p)/180)
        Δ = (1 + s11)*(1 + s22) - s12*s21
        y11 = ((1 - s11)*(1 + s22) + s12*s21) / Δ / z0
        y12 = -2*s12 / Δ / z0
        y21 = -2*s21 / Δ / z0
        y22 = ((1 + s11)*(1 - s22) + s12*s21) / Δ / z0
        f = float(f)
        if f:
            freq.append(f)
            Zind.append(abs(1/y12))

    with RLC_Chart('tfm201610alm.svg', 100e3, 1e9, 0.1, 1000) as chart:
        chart.add_trace(freq, Zind)

except OSError as e:
    fatal(os_error(e))
