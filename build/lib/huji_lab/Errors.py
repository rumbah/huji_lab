import numpy as _np
from math import sqrt as _sqrt
from uncertainties import ufloat as _ufloat
from uncertainties.core import Variable as _varu
from sympy import symbols as _symbols
from sympy import diff as _diff


def chi_squared(xdata, ydata, popt, staterror, func):
    """
    Calculates the reduced x^2 of a data set.
    :param xdata: Array of data representing the x axis.
    :param ydata: Array of data representing the y axis.
    :param popt: List of approximated parameters.
    :param staterror: Array of statistical error corresponding to the ydata array.
    :param func: Fitting function in lambda form (Exm. lambda x,a,b: a*x+b).
    :return: The reduced chi-squared value.
    """
    xdata = _np.array(xdata)
    ydata = _np.array(ydata)
    staterror = _np.array(staterror)
    chi_cal = _np.sum(((ydata - func(xdata, *popt)) / staterror) ** 2)
    reduced_chi_squared = chi_cal / (len(xdata) - len(popt))
    if hasattr(reduced_chi_squared , 'nominal_value'):
        return reduced_chi_squared.nominal_value
    else:
        return reduced_chi_squared


def measurements_deviation_calculator(measurements):
    """
    Calculates the statistical error of n identical measurements.
    :param measurements: An array of measurements.
    :return: A ufloat, as <x>+/-dx
    """
    measurements = _np.array(measurements)
    mean_measurements = measurements.mean()
    n = len(measurements)
    sigma = _sqrt(sum((measurements - mean_measurements) ** 2)/(n-1))
    stats_error = sigma / _sqrt(n)
    return _ufloat(mean_measurements, stats_error)


def results_sum_with_deviation(results):
    """
    Sums an array of different experiment results and calculates the total standard deviation.
    :param results: An array of ufloats.
    :return: A ufloat.
    """
    nominator = []
    denominator = []
    for result in results:
        if type(result) is not _varu:
            print("Error, The input array is not of ufloat")
            return
        else:
            nominator.append(result.nominal_value / result.std_dev**2)
            denominator.append(1 / result.std_dev**2)
    return _ufloat(sum(nominator) / sum(denominator), 1 / _sqrt(sum(denominator)))


def partial_derivatives(equation, params):
    """
    Calculates the equation for a deviation composed of different variable deviations.
    :param equation: A string representing the equation of the measured variable (In python syntax).
                    Exmaple: "mr**2 + 2mR**2"
    :param params: A list of the variables in the given equation. Example: ['m', 'r', 'R']
    :return: A string. Render nicely with Lab.Display.print_latex
    """
    symbol_params = _symbols(" ".join(params))
    answers = "$\\sqrt{"
    for par in symbol_params:
        answers += "((" + str(_diff(equation, par)) + ")\Delta " + str(par) + ")^2 +"
    answers = answers[:-1] + "}$"
    answers = answers.replace('**', '^')
    answers = answers.replace('*', '')
    return answers


def n_sigma_test(n1, dn1, n2, dn2):
    """
    Preforms an Nsigma test between two different measurements.
    :param n1: First measurement result.
    :param dn1: First measurement deviation.
    :param n2: second measurement result.
    :param dn2: second measurement deviation.
    :return: Nsigma test result, Should be smaller the 3.
    """
    return abs(n1-n2)/_sqrt(dn1**2+dn2**2)
