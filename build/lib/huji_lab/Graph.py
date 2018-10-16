import pandas as _pd
import matplotlib.pyplot as _plt
import numpy as _np
import seaborn as _sns
from scipy.optimize import curve_fit as _curve_fit
from uncertainties import ufloat as _ufloat
import mplcursors as _mplcursors
from IPython import display as _dynamicdis
import time as _time
from huji_lab.Generators import expand_linspace as _expand_linspace
from huji_lab.Errors import chi_squared as _chi_squared


def graph_it(x, y, graph_type=None, x_error=0, y_error=0,
             title="", x_title="", y_title="", size=(20, 10),
             sig_digi=3, coeff_x=0.8, coeff_y=0.8,
             error_fill_bet=True, plot_residuals=True, show_chi=True, coeff_text=(''),
             resid_x_error=0, resid_y_error=0, y_scale="", x_scale="",
             extra_code_main='', extra_code_residuals=''):
    """
    Plot and Customize two 1D arrays.
    :param x: Horizontal axis data.
    :param y: Vertical axis data.
    :param graph_type: Formula of fit. Example: lambda x,a,b: a*x+b.
    :param x_error: X Error bar size.
    :param y_error: Y Error bar size.
    :param title: Graphs title.
    :param x_title: X axis title.
    :param y_title: Y axis title.
    :param size: Graphs size.
    :param sig_digi: Significant digits length.
    :param coeff_x: X position of the legend.
    :param coeff_y: Y position of the legend.
    :param error_fill_bet: Draws an aura of error freedom around the graph. Default is Off.
    :param plot_residuals: Plots the residuals as another graph under the Data graph.
    :param show_chi: Show reduced chi-squared result.
    :param coeff_text: Tuple of units for graphs legend.
    :param resid_x_error: X residuals error bar size.
    :param resid_y_error: Y residuals error bar size.
    :param y_scale: gets a an array of two iterables, one for for actual rescaling and one for lables,
                    most commonly use with generatePiAxis().
    :param x_scale: gets a an array of two iterables, one for for actual rescaling and one for lables,
                    most commonly use with generatePiAxis().
    :param extra_code_main: Runs extra script after the main graph plot.
    :param extra_code_residuals: uns extra script after the residuals graph plot.
    :return: A list of guessed parameters given in graph_type.
    """
    _plt.rc('text', usetex=False)
    fig, ax = _plt.subplots(figsize=size)
    tick_fine = 0

    x = _np.array(x)
    y = _np.array(y)

    if graph_type is not None:
        popt, pcov = _curve_fit(graph_type, x, y, maxfev=100000)
        sigma_ab = _np.sqrt(_np.diagonal(pcov))  # type: _np.ndarray
        x_model = _expand_linspace(x.min(), x.max(), len(x) * 3)
        _plt.plot(x_model, graph_type(x_model, *popt), 'black')
        _plt.errorbar(x, y, xerr=x_error, yerr=y_error, fmt='o', color='r', visible=False, alpha=0.6)
        if show_chi == True:
            if y_error == 0:
                print("No stat. error data provided, skipping chi squared calculation")
            else:
                chi = _chi_squared(x, y, popt, y_error, graph_type)
                title += "\n$\\chi^2 = %s$" %str(chi)
        if error_fill_bet:
            bound_upper = graph_type(x_model, *(popt + sigma_ab))
            bound_lower = graph_type(x_model, *(popt - sigma_ab))
            # plotting the confidence intervals
            _plt.fill_between(x_model, bound_lower, bound_upper, color='midnightblue', alpha=0.15)
        if coeff_text != ():
            coeff_text = list(coeff_text)
            coeff_text += [''] * (len(popt) - len(coeff_text))
            text_res = ""
            for i, param in enumerate(popt):
                text_res += ((graph_type.__code__.co_varnames[i + 1]) +
                             str((" = {:." + str(sig_digi) + "u}").format(_ufloat(popt[i], sigma_ab[i])) +
                                 coeff_text[i] + "\n"))
            _plt.figtext(coeff_x, coeff_y, text_res, size=20, family='DejaVu Sans')
        tick_fine = 1

    _plt.scatter(x, y, facecolor='red', edgecolor='black', s=70, alpha=1)
    ax.set_title(title)
    ax.set_ylabel(y_title)
    ax.set_xlabel(x_title)

    if x_scale != "":
        ax.set_xticks(x_scale[0])
        ax.set_xticklabels(x_scale[1])
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(25)
    if y_scale != "":
        ax.set_yticks(y_scale[0])
        ax.set_yticklabels(y_scale[1])
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(25)

    if tick_fine == 1:
        ax.set_xlim(x_model.min(), x_model.max())
    else:
        ax.set_xlim(_expand_linspace(x.min(), x.max(),len(x) * 3).min(),_expand_linspace(x.min(), x.max(),len(x) * 3).max())

    exec(extra_code_main)

    if plot_residuals and graph_type is not None:
        residuals = y - graph_type(x, *popt)
        fig, ax = _plt.subplots(figsize=(20, 5))
        _sns.residplot(x, residuals, color='r', scatter_kws={'s': 100})
        ax.errorbar(x, residuals, xerr=resid_x_error, yerr=residuals * resid_y_error, fmt='none')
        ax.set_xlim(x_model.min(), x_model.max())
        ax.set_ylim(residuals.min() - _np.abs(residuals.min()*0.5), residuals.max() + _np.abs(residuals.max()*0.5))
        ax.set_title("Residuals Plot of " + title)
        ax.set_ylabel(y_title)
        ax.set_xlabel(x_title)
    _mplcursors.cursor(hover=True)

    exec(extra_code_residuals)
    if tick_fine == 1:
        return [(_ufloat(popt[i], sigma_ab[i])) for i in range(len(popt))]
    else:
        return


def dynamic_draw(path, refresh_time=1, sheet='Sheet1'):
    """
    Dynamically plots a 2D array, read from an XLS or XLSX file (Save the file == Refresh the graph).
    :param path: Full path to the csv file.
    :param refresh_time: Seconds between graph redraw
    :param sheet:   Defaults to Sheet1, change accordingly.
    :return: None.
    """
    fig, ax = _plt.subplots(figsize=(20, 10))
    while True:
        try:
            tempdf = _pd.read_excel(path, sheet_name=sheet)
            _sns.regplot(x=tempdf.iloc[:, 0], y=tempdf.iloc[:, 1], fit_reg=False, ax=ax, scatter_kws={"s": 100})
            _dynamicdis.display(_plt.gcf())
            _dynamicdis.clear_output(wait=True)
            _time.sleep(refresh_time)
        except KeyboardInterrupt:
            break
