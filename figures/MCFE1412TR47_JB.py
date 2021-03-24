#!/usr/bin/env python3

from psf_utils import PSF
from inform import Error, os_error, fatal
from rlc_chart import RLC_Chart

try:
    psf = PSF('MCFE1412TR47_JB.ac')
    sweep = psf.get_sweep()
    z_ckt = psf.get_signal('1')
    z_mod = psf.get_signal('2')

    with RLC_Chart('MCFE1412TR47_JB.svg', 100, 1e9, 0.01, 1000) as chart:
        chart.add_trace(sweep.abscissa, abs(z_ckt.ordinate), stroke='red')
        chart.add_trace(sweep.abscissa, abs(z_mod.ordinate), stroke='blue')

    with RLC_Chart('MCFE1412TR47_JB.rxz.svg', 100, 1e9, 0.01, 1000) as chart:
        chart.add_trace(sweep.abscissa, abs(z_ckt.ordinate.real), stroke='green')
        chart.add_trace(sweep.abscissa, abs(z_ckt.ordinate.imag), stroke='orange')
        chart.add_trace(sweep.abscissa, abs(z_mod.ordinate.real), stroke='blue')
        chart.add_trace(sweep.abscissa, abs(z_mod.ordinate.imag), stroke='red')
        chart.add(chart.text(
            " ← poor loss modeling",
            insert = (
                chart.to_x(sweep.abscissa[-1]),
                chart.to_y(abs(z_mod.ordinate.real[-1]))
            ),
            **chart.text_props
        ))
        chart.add(chart.text(
            "MCFE1412TR47_JB",
            insert = (chart.WIDTH/2, 24),
            font_size = 24,
            fill = 'black',
            text_anchor = 'middle',
        ))

except Error as e:
    e.terminate()
except OSError as e:
    fatal(os_error(e))

