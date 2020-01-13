from pyglet.gl import GL_LINES, GL_QUADS
from pyglet.graphics import vertex_list


class Candle:
    def __init__(self, width):
        self.width = width
        self.body = vertex_list(4, 'v2f', 'c3B')
        self.low_high = vertex_list(2, 'v2f', 'c3B')

    def set_ohlc(self, open_, high, low, close):
        if open_ != close:
            if self.body.get_size() != 4:
                self.body.resize(4)
            self.body.vertices[1] = open_
            self.body.vertices[3] = close
            self.body.vertices[5] = self.body.vertices[3]
            self.body.vertices[7] = self.body.vertices[1]
        else:
            if self.body.get_size() != 2:
                self.body.resize(2)
            self.body.vertices[1] = open_
            self.body.vertices[3] = close
        self.low_high.vertices[1] = low
        self.low_high.vertices[3] = high

    def set_position(self, position: int):
        """Set current position and returns next position"""
        if self.body.get_size() == 4:
            self.body.vertices[0] = position
            self.body.vertices[2] = self.body.vertices[0]
            self.body.vertices[4] = position + self.width
            self.body.vertices[6] = self.body.vertices[4]
        elif self.body.get_size() == 2:
            self.body.vertices[0] = position
            self.body.vertices[2] = position + self.width
        self.low_high.vertices[0] = position + self.width // 2
        self.low_high.vertices[2] = position + self.width // 2

    def set_color(self, color):
        self.body.colors = color * self.body.get_size()
        self.low_high.colors = color * self.low_high.get_size()

    def draw(self):
        mode = GL_QUADS
        if self.body.get_size() == 2:
            mode = GL_LINES
        self.body.draw(mode)
        self.low_high.draw(GL_LINES)
