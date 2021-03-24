#!/usr/bin/env python3

from svg_schematic import (
    Schematic, Capacitor, Ground, Inductor, Resistor, Pin, Source, Wire
)
from inform import Error, error, os_error

try:
    with Schematic(
        filename = 'leaky-cap.svg',
        background = 'none',
        line_width = 1.5,
    ):
        p1 = Pin(kind='in')
        c = Capacitor(p=p1.C, xoff=50, value='C', orient='v')
        l = Inductor(p=c.n, yoff=-12.5, value='L', orient='v')
        r = Resistor(p=l.n, yoff=-12.5, value='Rs', orient='v')
        p2 = Pin(C=r.n, xoff=-50, kind='in')
        Wire([p1.C, c.p], '-|')
        Wire([p2.C, r.n], '-|')
        rp = Resistor(C=l.C, xoff=100, value='Rp', orient='v')
        Wire([p1.C, rp.p], '-|')
        Wire([p2.C, rp.n], '-|')
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))

