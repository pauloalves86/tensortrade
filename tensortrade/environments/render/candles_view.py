import numpy as np
from pyglet.gl import GL_LINE_LOOP, glScalef, glTranslatef
from pyglet.graphics import vertex_list

from tensortrade.environments.render.candle import Candle

RED = (128, 0, 0)
GREEN = (0, 128, 0)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class CandlesView:
    def __init__(self, width: int, height: int, n_candles: int,
                 up_color=GREEN, down_color=RED):
        self.width = width - 50
        self.height = height
        half_candle_width = self.width / (n_candles * 3 - 1)
        candle_width = half_candle_width * 2
        self.candles = [Candle(candle_width) for _ in range(n_candles)]
        self.up_color = up_color
        self.down_color = down_color
        self.low_high = _LowHigh(n_candles)
        self.positions = [pos * half_candle_width * 3
                          for pos in range(n_candles)]
        self.margin = vertex_list(
            4,
            ('v2i', (1, 0, 1, height - 1, width - 1, height - 1, width - 1, 0)),
            ('c3B', (0, 0, 0) * 4)
        )

    def update(self, open_, high, low, close):
        candle = self.candles.pop(0)
        candle.set_color(self.up_color if open_ <= close else self.down_color)
        candle.set_ohlc(open_, high, low, close)
        self.candles.append(candle)
        self.low_high.update(low, high)
        for candle, pos in zip(self.candles, self.positions):
            candle.set_position(pos)

    def draw(self):
        self.margin.draw(GL_LINE_LOOP)
        scale = self.height / max(1, self.low_high.amplitude)
        glTranslatef(0, -self.low_high.lowest * scale, 0)
        glScalef(1, scale, 1)
        for candle in self.candles:
            candle.draw()


class _LowHigh:
    def __init__(self, max_count: int):
        self.max_count = max_count
        self.low = [np.inf] * max_count
        self.high = [-np.inf] * max_count

    def update(self, low: float, high: float):
        self.low.pop(0)
        self.low.append(low)
        self.high.pop(0)
        self.high.append(high)

    @property
    def lowest(self):
        return min(self.low)

    @property
    def highest(self):
        return max(self.high)

    @property
    def amplitude(self):
        return self.highest - self.lowest
