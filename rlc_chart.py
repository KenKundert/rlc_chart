# RLC Chart by Ken Kundert
# encoding: utf8

# Description {{{1
"""
*RLC Chart* is a Python library that creates SVG impedance charts with
capacitance and inductance overlays.
"""
__version__ = '0.1.0'
__released__ = '2021-03-25'


# License {{{1
# Copyright (C) 2018-21 Kenneth S. Kundert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].


# Imports {{{1
from svgwrite import Drawing
from pathlib import Path
from math import ceil, floor, log10 as log, pi as π
from quantiphy import Quantity

Quantity.set_prefs(
    map_sf = Quantity.map_sf_to_sci_notation,
    spacer = Quantity.narrow_non_breaking_space,
    output_sf = 'YZEPTGMkmunpfazy',
)

# RLC_Chart class {{{1
class RLC_Chart(Drawing):

    # settings {{{2
    TRACE_WIDTH = 0.025
    TRACE_COLOR = 'black'
    MAJOR_LINE_WIDTH = 0.01
    MINOR_LINE_WIDTH = 0.005
    OUTLINE_LINE_WIDTH = 0.015
    OUTLINE_LINE_COLOR = 'black'
    FZ_GRID_COLOR = 'grey'
    CL_GRID_COLOR = 'grey'
    BACKGROUND = 'white'
    AXES = 'FZCL'
    MINOR_DIVS = '123456789'
    DECADE = 1
    LEFT_MARGIN = 1
    RIGHT_MARGIN = 1
    TOP_MARGIN = 1
    BOTTOM_MARGIN = 1
    FONT_FAMILY = 'sans-serif'
    FONT_SIZE = 12
    TEXT_COLOR = 'black'
    TEXT_OFFSET = 0.15
    PIXELS_PER_UNIT = 96   # 96 pixels per inch

    # constructor {{{2
    def __init__(self, filename, fmin, fmax, zmin, zmax, **kwargs):
        # process arguments {{{3
        self.filename = Path(filename)
        assert fmin < fmax, "fmin must be less that fmax."
        assert 0 < fmin, "fmin must be greater than zero."
        assert zmin < zmax, "zmin must be less that zmax."
        assert 0 < zmin, "zmin must be greater than zero."
        svg_args = {}
        for k, v in kwargs.items():
            if hasattr(self, k.upper()):
                setattr(self, k.upper(), v)
            else:
                svg_args[k] = v
        text_props = dict(
            font_family = self.FONT_FAMILY,
            font_size = self.FONT_SIZE,
            fill = self.TEXT_COLOR,
        )
        self.text_props = text_props

        def to_pixels(d):
            return d * self.PIXELS_PER_UNIT
        self.to_pixels = to_pixels

        # find bounds {{{3
        x0 = floor(log(fmin))
        x1 = ceil(log(fmax))
        y0 = floor(log(zmin))
        y1 = ceil(log(zmax))
        fmin = self.fmin = 10**x0
        fmax = self.fmax = 10**x1
        zmin = self.zmin = 10**y0
        zmax = self.zmax = 10**y1
        grid_width = self.DECADE * (x1 - x0)
        grid_height = self.DECADE * (y1 - y0)
        canvas_width = grid_width + self.LEFT_MARGIN + self.RIGHT_MARGIN
        canvas_height = grid_height + self.TOP_MARGIN + self.BOTTOM_MARGIN
        self.HEIGHT = to_pixels(canvas_height)
        self.WIDTH = to_pixels(canvas_width)

        # create canvas
        super().__init__(
            filename,
            size = (to_pixels(canvas_width), to_pixels(canvas_height)),
            **svg_args
        )

        # coordinate transformations {{{3
        # coordinate transformations for base units (Hz, Ω)
        def x(f):
            x = log(f)
            X = self.LEFT_MARGIN + grid_width*(x-x0)/(x1-x0)
            return to_pixels(X)

        def y(z):
            y = log(z)
            Y = canvas_height - self.BOTTOM_MARGIN - grid_height*(y-y0)/(y1-y0)
            return to_pixels(Y)

        # coordinate transformations for log units (log(Hz), log(Ω))
        def X(x):
            X = self.LEFT_MARGIN + grid_width*(x-x0)/(x1-x0)
            return to_pixels(X)

        def Y(y):
            Y = canvas_height - (grid_height*(y-y0)/(y1-y0) + self.BOTTOM_MARGIN)
            return to_pixels(Y)

        self.to_x = x
        self.to_y = y

        # Draw traditional FZ log-log grid {{{3
        minor_divs = [log(int(d)) for d in self.MINOR_DIVS.lstrip('1')]

        # draw background
        attrs = dict(stroke_linecap='round', fill='none', stroke=self.FZ_GRID_COLOR)
        grid = self.g(id='grid')
        self.add(grid)
        background = self.polygon([
                (X(x0), Y(y0)),
                (X(x0), Y(y1)),
                (X(x1), Y(y1)),
                (X(x1), Y(y0)),
            ],
            fill = self.BACKGROUND,
            stroke='none'
        )
        grid.add(background)

        # create clipping region
        clipper = self.clipPath(id='plotting-region')
        self.defs.add(clipper)
        clipper.add(background)


        # minor FZ divisions {{{4
        if 'Z' in self.AXES:
            attrs['stroke_width'] = to_pixels(self.MINOR_LINE_WIDTH)
            for major in range(y0, y1):
                for minor in minor_divs:
                    v = major + minor
                    grid.add(
                        self.line(start=(X(x0), Y(v)), end=(X(x1), Y(v)), **attrs)
                    )
        if 'F' in self.AXES:
            for major in range(x0, x1):
                for minor in minor_divs:
                    v = major + minor
                    grid.add(
                        self.line(start=(X(v), Y(y0)), end=(X(v), Y(y1)), **attrs)
                    )

        # major FZ divisions and labels {{{4
        if 'Z' in self.AXES or 'z' in self.AXES:
            attrs['stroke_width'] = to_pixels(self.MAJOR_LINE_WIDTH)
            for v in range(y0, y1+1):
                grid.add(self.line(start=(X(x0), Y(v)), end=(X(x1), Y(v)), **attrs))
                z = 10**v
                grid.add(self.text(
                    Quantity(z, 'Ω').render(),
                    insert = (X(x0) - to_pixels(self.TEXT_OFFSET), Y(v) + 0.35*self.FONT_SIZE),
                    text_anchor = 'end',
                    **text_props
                ))
                # grid.add(self.text(
                #     Quantity(1/z, 'Ʊ').render(),
                #     insert = (X(x1) + to_pixels(self.TEXT_OFFSET), Y(v) + 0.35*self.FONT_SIZE),
                #     text_anchor = 'start',
                #     **text_props
                # ))
        if 'F' in self.AXES or 'f' in self.AXES:
            for v in range(x0, x1+1):
                grid.add(self.line(start=(X(v), Y(y0)), end=(X(v), Y(y1)), **attrs))
                f = 10**v
                grid.add(self.text(
                    Quantity(f, 'Hz').render(),
                    insert = (X(v), Y(y0) + to_pixels(self.TEXT_OFFSET) + self.FONT_SIZE),
                    text_anchor = 'middle',
                    **text_props
                ))

        # draw CL log-log grids {{{3
        attrs['stroke'] = self.CL_GRID_COLOR
        if 'stroke_width' in attrs:
            del attrs['stroke_width']

        # draw capacitance grid {{{4
        def c_start(C):
            # find lower right end point of capacitance gridline
            fstart = 1/(2*π*zmin*C)
            if fstart <= fmax:
                return (X(log(fstart)), Y(y0))
            z = 1/(2*π*fmax*C)
            if z <= zmax:
                return (X(x1), Y(log(z)))

        def c_stop(C):
            # find upper left end point of capacitance gridline
            fstop = 1/(2*π*zmax*C)
            if fstop >= fmin:
                return (X(log(fstop)), Y(y1))
            z = 1/(2*π*fmin*C)
            if z >= zmin:
                return (X(x0), Y(log(z)))

        # minor C divs {{{5
        if 'C' in self.AXES:
            attrs['stroke_width'] = to_pixels(self.MINOR_LINE_WIDTH)
            for v in range(x0, x1+y1-y0+1):
                for d in self.MINOR_DIVS:
                    scale = int(d)/zmin
                    C = scale*10**-(v+1)
                    start = c_start(C)
                    stop = c_stop(C)
                    if start and stop:
                        grid.add(self.line(start=start, end=stop, **attrs))

        # major C divs and labels {{{5
        if 'C' in self.AXES or 'c' in self.AXES:
            attrs['stroke_width'] = to_pixels(self.MAJOR_LINE_WIDTH)
            for v in range(x0, x1+y1-y0):
                C = (10**-(v+1))/zmin
                start = c_start(C)
                stop = c_stop(C)
                if start and stop:
                    grid.add(self.line(start=start, end=stop, **attrs))
                    x = stop[0] - self.FONT_SIZE
                    y = stop[1] - 0.5*self.FONT_SIZE
                    grid.add(self.text(
                        Quantity(C, 'F').render(),
                        insert = (x, y),
                        text_anchor = 'end',
                        transform = f'rotate(45, {x}, {y})',
                        **text_props
                    ))

        # draw inductance grid {{{4
        def l_start(L):
            # find lower right end point of inductance gridline
            fstart = zmin/(2*π*L)
            if fstart >= fmin:
                return (X(log(fstart)), Y(y0))
            z = 2*π*fmin*L
            if z <= zmax:
                return (X(x0), Y(log(z)))

        def l_stop(L):
            # find upper left end point of inductance gridline
            fstop = zmax/(2*π*L)
            if fstop <= fmax:
                return (X(log(fstop)), Y(y1))
            z = 2*π*fmax*L
            if z >= zmin:
                return (X(x1), Y(log(z)))

        # minor L divs {{{5
        if 'L' in self.AXES:
            attrs['stroke_width'] = to_pixels(self.MINOR_LINE_WIDTH)
            for v in range(x0-(y1-y0), x1+1):
                for d in self.MINOR_DIVS:
                    scale = int(d)
                    L = zmin*scale*10**-(v+1)
                    start = l_start(L)
                    stop = l_stop(L)
                    if start and stop:
                        grid.add(self.line(start=start, end=stop, **attrs))

        # major L divs and labels {{{5
        if 'L' in self.AXES or 'l' in self.AXES:
            attrs['stroke_width'] = to_pixels(self.MAJOR_LINE_WIDTH)
            for v in range(x0-(y1-y0), x1):
                L = zmin*10**-(v+1)
                start = l_start(L)
                stop = l_stop(L)
                if start and stop:
                    grid.add(self.line(start=start, end=stop, **attrs))
                    x = stop[0] + self.FONT_SIZE
                    y = stop[1] - 0.5*self.FONT_SIZE
                    grid.add(self.text(
                        Quantity(L, 'H').render(),
                        insert = (x, y),
                        text_anchor = 'start',
                        transform = f'rotate(-45, {x}, {y})',
                        **text_props
                    ))

        # outline {{{3
        attrs.update(dict(
            stroke_width = to_pixels(self.OUTLINE_LINE_WIDTH),
            stroke = self.OUTLINE_LINE_COLOR
        ))
        grid.add(self.line(start=(X(x0), Y(y0)), end=(X(x1), Y(y0)), **attrs))
        grid.add(self.line(start=(X(x0), Y(y1)), end=(X(x1), Y(y1)), **attrs))
        grid.add(self.line(start=(X(x0), Y(y0)), end=(X(x0), Y(y1)), **attrs))
        grid.add(self.line(start=(X(x1), Y(y0)), end=(X(x1), Y(y1)), **attrs))

        self.traces = self.g(id='traces')
        self.add(self.traces)

    # add_trace() {{{2
    def add_trace(self, frequencies, impedances, name=None, **svg_args):

        kwargs = dict(
            stroke = self.TRACE_COLOR,
            stroke_width = self.to_pixels(self.TRACE_WIDTH),
            stroke_linecap = 'round',
            fill = 'none',
        )
        kwargs.update(svg_args)

        self.traces.add(
            self.polyline(
                [
                    (self.to_x(f), self.to_y(z))
                    for f, z in zip(frequencies, impedances)
                ],
                clip_path = 'url(#plotting-region)',
                **kwargs
            )
        )

    # add_line() {{{2
    def add_line(self, start, end, *, r=None, l=None, c=None, f=None, **svg_args):

        kwargs = dict(
            stroke = self.OUTLINE_LINE_COLOR,
            stroke_width = self.to_pixels(self.OUTLINE_LINE_WIDTH),
            stroke_linecap = 'round',
            fill = 'none',
        )
        kwargs.update(svg_args)

        if r is not None:
            f_start, f_end = start, end
            z_start = z_end = r
        elif l is not None:
            f_start, f_end = start, end
            z_start = 2*π*start*l
            z_end = 2*π*end*l
        elif c is not None:
            f_start, f_end = start, end
            z_start = 1/(2*π*start*c)
            z_end = 1/(2*π*end*c)
        elif f is not None:
            z_start = start
            z_end = end
            f_start = f_end = f
        else:
            raise AssertionError('must specify either r, l, c, or f.')

        self.traces.add(
            self.line(
                start = (self.to_x(f_start), self.to_y(z_start)),
                end = (self.to_x(f_end), self.to_y(z_end)),
                **kwargs
            )
        )

    # close() {{{2
    def close(self):
       self.save(pretty=True)

    # context manager {{{2
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
