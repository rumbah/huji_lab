import matplotlib.pyplot as _plt
from IPython.display import Image as _Image
from IPython.display import display as _display
from IPython.display import Markdown as _Markdown
from IPython.display import Latex

"""
# A dangerous override function, currently unimplemented.
from uncertainties.core import Variable as _varu


def is_ufloat(num):
    if type(num) is _varu:
        if num.std_dev / abs(num.nominal_value) > 0.02:
            print_color_bold(num, 'red')
        else:
            print_color_bold(num, 'green')
    else:
        print_color_bold(num, 'none')


def print_color_bold(string, color):
    if color != 'none':
        num = str(string)
        text_line = _Markdown("<span style=\"color: " + color + "\">**" + num + "**</span>")  # type: tuple
        _display(text_line)
    else:
        _display(string)
        
global print
print = is_ufloat
"""


def print_color_bold(string, color='black'):
    text_line = _Markdown("<span style=\"color: " + color + "\">**" + string + "**</span>")  # type: tuple
    _display(text_line)


def _print_latex_old(text_to_print):
    """
    DEPRECATED, Please don't use
    Nicely prints LaTeX syntax, inline with python output.
    :param text_to_print:
    :return: None.
    """
    fig, ax = _plt.subplots(figsize=(1, 1))
    _plt.rc('text', usetex=True)
    _plt.tight_layout()
    _plt.axis('off')
    ax.grid(False)
    _plt.figtext(0, 0, text_to_print, fontsize=40, bbox=dict(facecolor='white', linewidth=0))


def print_latex(text_to_print):
    Latex(text_to_print)


def print_wolfram(wolf_query):
    """
    Nicely prints a wolframAlpha query as a series of photos.
    :param wolf_query: A wolfram_query() object.
    :return: None.
    """
    for result in wolf_query['pod']:
        outer = result['subpod']
        if type(outer) is dict:
            disp = _Image(url=outer['img']['@src'])  # type: tuple
            _display(disp)
        else:
            for i in range(len(outer)):
                disp = _Image(url=outer[i]['img']['@src'])  # type: tuple
                _display(disp)
