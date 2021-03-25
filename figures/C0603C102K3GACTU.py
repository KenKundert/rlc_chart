#!/usr/bin/env python3

from rlc_chart import RLC_Chart
from inform import fatal, os_error
from pathlib import Path
from math import pi as π
import csv

fmin = 100
fmax = 10e9
zmin = 0.01
zmax = 1e6
cmod = 1e-9
lmod = 700e-12
rmod = 20e-3

def model(f):
    return 1/(2j*π*f*cmod) + rmod + 2j*π*f*lmod

frequency = []
z_data = []
r_data = []
z_model = []
r_model = []
try:
    contents = Path('C0603C102K3GACTU_imp_esr.csv').read_text()
    data = csv.DictReader(contents.splitlines(), delimiter=',')
    for row in data:
        f = float(row['Frequency'])
        z = model(f)
        frequency.append(f)
        z_data.append(float(row['Impedance']))
        r_data.append(float(row['ESR']))
        z_model.append(abs(z))
        r_model.append(z.real)

    with RLC_Chart('C0603C102K3GACTU.svg', fmin, fmax, zmin, zmax, axes='FZCL') as chart:

        # add annotations
        svg_text_args = dict(font_size = 24, fill = 'black')

        # capacitance
        chart.add(chart.text(
            "C = 1 nF",
            insert = (chart.to_x(150e3), chart.to_y(1.5e3)),
            **svg_text_args
        ))
        chart.add_line(1e3, 190.23e6, c=1e-9)

        # inductance
        chart.add(chart.text(
            "L = 700 pH",
            insert = (chart.to_x(12e9), chart.to_y(30)),
            text_anchor = 'start',
            **svg_text_args
        ))
        chart.add_line(190.232e6, 10e9, l=700e-12)

        # resistance
        chart.add(chart.text(
            "ESR = 20 mΩ",
            insert = (chart.to_x(100e3), chart.to_y(25e-3)),
            text_anchor = 'start',
            **svg_text_args
        ))
        chart.add_line(100e3, 1e9, r=20e-3)

        # resonant frequency
        chart.add(chart.text(
            "f₀ = 190 MHz",
            insert = (chart.to_x(190.23e6), chart.to_y(40)),
            text_anchor = 'middle',
            **svg_text_args
        ))
        chart.add_line(1e-2, 30, f=190.23e6)

        # Q
        chart.add(chart.text(
            "Q = 42",
            insert = (chart.to_x(10e6), chart.to_y(100e-3)),
            text_anchor = 'start',
            **svg_text_args
        ))
        chart.add_line(10e6, 190.23e6, r=836.66e-3)

        # title
        chart.add(chart.text(
            "C0603C102K3GACTU",
            insert = (chart.WIDTH/2, 36),
            font_size = 24,
            fill = 'black',
            text_anchor = 'middle',
        ))

        # add traces last, so they are on top
        chart.add_trace(frequency, z_data, stroke='red')
        chart.add_trace(frequency, r_data, stroke='blue')
        chart.add_trace(frequency, z_model, stroke='red', stroke_dasharray=(10,5))
        chart.add_trace(frequency, r_model, stroke='blue', stroke_dasharray=(10,5))

except OSError as e:
    fatal(os_error(e))
