from typing import Tuple

import pyglet
from pyglet.gl import *

from tensortrade.environments.render.candles_view import CandlesView

MARGIN = 5


def new_label(text, xpos, ypos, anchor_x='center'):
    label = pyglet.text.Label(f'{text}', font_name='Courier',
                              font_size=10, color=(0, 0, 0, 255),
                              x=xpos, y=ypos,
                              anchor_x=anchor_x, anchor_y='center')
    return label


class PygletTradingChart:
    # pylint: disable=attribute-defined-outside-init
    """An OHLCV trading visualization using
    pyglet made to render gym environments."""

    def __init__(self, n_candles: int, width: int = 960, height: int = 540):
        self.window = pyglet.window.Window(width, height)
        self.chart = CandlesView(width, height, n_candles)
        self.chart_viewport = (
            MARGIN,
            MARGIN,
            int(self.window.width - MARGIN * 2),
            int(self.window.height * .75 - MARGIN * 2)
        )

    def render(self, ohlc: Tuple[float, float, float, float],
               volume: float, net_worth: float):
        self.chart.update(*ohlc)

        glClearColor(1, 1, 1, 1)
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()
        self._draw_chart()
        self.window.flip()

    def _draw_chart(self):
        glViewport(*self.chart_viewport)
        glPushMatrix()
        self.chart.draw()
        glPopMatrix()
