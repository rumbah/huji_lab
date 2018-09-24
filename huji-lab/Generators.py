import numpy as _np
from math import pi as _pi
from fractions import Fraction as _Fraction


def generate_pi_axis(start=0, end=2 * _pi, jumps=5):
    """
    Generates an evenly spaced scale, in Pi multiplicities.
    :param start: A number to start the scale.
    :param end: A number to end the scale.
    :param jumps: Number of slices of the scale.
    :return: A tuple made of two lists, one for actual numbers and one for nicely formatted LaTeX scale.
    """

    jump_size = (end - start) / (jumps - 1)
    y_ticks = []
    y_ticks_labels = []
    for y_tick in range(0, jumps):
        cur_tick = start + jump_size * y_tick
        y_ticks.append(cur_tick)
        cur_tick = _Fraction(cur_tick / _pi).limit_denominator(max_denominator=10)
        if cur_tick.numerator == 0:
            y_ticks_labels.append("0")
        elif cur_tick.denominator == 1:
            y_ticks_labels.append("$%s\\pi$" % (str(cur_tick.numerator)))
        elif cur_tick.numerator < 0:
            y_ticks_labels.append("$-\\frac{%s}{%s}\\pi$" % (str(-cur_tick.numerator), str(cur_tick.denominator)))
        else:
            y_ticks_labels.append("$\\frac{%s}{%s}\\pi$" % (str(cur_tick.numerator), str(cur_tick.denominator)))
    return y_ticks, y_ticks_labels


def expand_linspace(lin_min, lin_max, chunks):
    """
    Uniformly expands a numpy linspace by 10%.
    :param lin_min: A number to start the scale.
    :param lin_max: A number to end the scale.
    :param chunks: Number of slices of the scale.
    :return: Expanded numpy linspace.
    """
    return _np.linspace(lin_min - _np.abs(lin_min * 0.1), lin_max + _np.abs(lin_max * 0.1), chunks)
