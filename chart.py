import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

_VARS = {
         'fig_agg': False,
         'pltFig': False
}

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def drawChart(x: list, y: list, window):
    _VARS['pltFig'] = plt.figure()
    plt.plot(x, y, '.k')
    _VARS['fig_agg'] = draw_figure(window['-CANVAS-'].TKCanvas, _VARS['pltFig'])


# Recreate Synthetic data, clear existing figre and redraw plot.
def updateChart(x: list, y: list, window):
    _VARS['fig_agg'].get_tk_widget().forget()
    # plt.cla()
    plt.clf()
    plt.plot(x, y, '.k')
    _VARS['fig_agg'] = draw_figure(window['-CANVAS-'].TKCanvas, _VARS['pltFig'])


