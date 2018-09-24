import pandas as _pd
import numpy as _np
from analytic_wfm import peakdetect as _peakdetect
import scipy.optimize as _opt
import wolframalpha as _wolframalpha


def fit_sin(tt, yy):
    """
    Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq",
    "period" and "fitfunc"
    :param tt: x parameter, a 1D array.
    :param yy: y parameter, a 1D array.
    :return: A dictionary containing a sin fit of the data.
    """
    tt = _np.array(tt)
    yy = _np.array(yy)
    ff = _np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    fyy = abs(_np.fft.fft(yy))
    guess_freq = abs(ff[_np.argmax(fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = _np.std(yy) * 2.**0.5
    guess_offset = _np.mean(yy)
    guess = _np.array([guess_amp, 2.*_np.pi*guess_freq, 0., guess_offset])  # type: float

    def sinfunc(time, amp, angular_freq, phase, const):
        return amp * _np.sin(angular_freq*time + phase) + const

    popt, pcov = _opt.curve_fit(sinfunc, tt, yy, p0=guess)
    a, w, p, c = popt
    f = w/(2.*_np.pi)
    return {"amp": a, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f,
            "fitfunc": lambda t: a * _np.sin(w*t + p) + c, "maxcov": _np.max(pcov), "rawres": (guess, popt, pcov)}


def detect_maxima(x, y, sensitivity=100):
    """
    Takes two 1D arrays (x,y) and returns a dataframe of MAXIMAS. Optional controls the lookahead parameter
    :param x: A 1D array.
    :param y: A 1D array.
    :param sensitivity: Int representing the lookahead for maximas detection.
    :return: A pandas dataframe containing local Maximas.
    """
    peaks = _peakdetect(_np.array(y), _np.array(x), lookahead=sensitivity)[0]
    return _pd.DataFrame.from_records(peaks, columns=['Column1', 'Column2'])


def detect_minima(x, y, sensitivity=100):
    """
    Takes two 1D arrays (x,y) and returns a dataframe of MINIMAS. Optional controls the lookahead parameter
    :param x: A 1D array.
    :param y: A 1D array.
    :param sensitivity: Int representing the lookahead for minimas detection.
    :return: A pandas dataframe containing local Minimas.
    """
    peaks = _peakdetect(y, x, lookahead=sensitivity)[1]
    return _pd.DataFrame.from_records(peaks, columns=['Column1', 'Column2'])


def freq_over_time_calculator(time_list):
    """
    Takes a list of times of recurring event, and returns approximated frequency.
    When dealing with Sin() events, use fit_sin for better results.
    :param time_list: A list of Ints representing times of recurring events.
    :return: A numpy array of approximated frequencies.
    """
    over_time = []
    for pair in range(len(time_list)-1):
        over_time.append(float(1/_np.abs(time_list[pair + 1] - time_list[pair])))
    return _np.array(over_time)


def wolfram_query(c_query):
    """
    Send a query to wolfram. Use Lab.Display.print_wolfram() for a nicely printed output.
    :param c_query: A string containing a wolframAlpha query.
    :return: A dictionary containing the wolframAlpha result.
    """
    app_id = "RVW9Y2-4XPJG9LX55"
    client = _wolframalpha.Client(app_id)
    return client.query(c_query)
