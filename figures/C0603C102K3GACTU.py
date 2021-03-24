#!/usr/bin/env python3

from rlc_chart import RLC_Chart
from inform import fatal, os_error
from pathlib import Path
import csv

fmin = 100
fmax = 10e9
zmin = 0.01
zmax = 1e6

frequency = []
impedance = []
ESR = []
try:
    contents = Path('C0603C102K3GACTU_imp_esr.csv').read_text()
    data = csv.DictReader(contents.splitlines(), delimiter=',')
    for row in data:
        frequency.append(float(row['Frequency']))
        impedance.append(float(row['Impedance']))
        ESR.append(float(row['ESR']))

    with RLC_Chart('C0603C102K3GACTU.svg', fmin, fmax, zmin, zmax, axes='FZCL') as chart:
        chart.add_trace(frequency, impedance, stroke='red')
        chart.add_trace(frequency, ESR, stroke='blue')

        chart.add(chart.text(
            "1 nF",
            insert = (chart.to_x(150_000), chart.to_y(1_500)),
            font_size = 24,
            fill = 'black'
        ))
        chart.add(chart.text(
            "700 pH",
            insert = (chart.to_x(2_000_000_000), chart.to_y(10)),
            font_size = 24,
            fill = 'black',
            text_anchor = 'end',
        ))
        chart.add(chart.text(
            "20 mΩ",
            insert = (chart.to_x(175_000_000), chart.to_y(0.012)),
            font_size = 24,
            fill = 'black',
            text_anchor = 'middle',
        ))
        chart.add(chart.text(
            "C0603C102K3GACTU",
            insert = (chart.WIDTH/2, 36),
            font_size = 24,
            fill = 'black',
            text_anchor = 'middle',
        ))
except OSError as e:
    fatal(os_error(e))
