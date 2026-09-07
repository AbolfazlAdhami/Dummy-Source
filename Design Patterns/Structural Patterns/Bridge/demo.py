from abc import ABC, abstractmethod

# ---------- Implementation ----------


class Renderer(ABC):
    @abstractmethod
    def render_circle(self, radius: float):
        pass

    @abstractmethod
    def render_square(self, side: float):
        pass


class VectorRenderer(Renderer):
    def render_circle(self, radius: float):
        print(f"Drawing a circle of radius {radius} with vectors")

    def render_square(self, side: float):
        print(f"Drawing a square of side {side} with vectors")


class RasterRenderer(Renderer):
    def render_circle(self, radius: float):
        print(f"Drawing pixels for a circle of radius {radius}")

    def render_square(self, side: float):
        print(f"Drawing pixels for a square of side {side}")


# ---------- Abstraction ----------
class Shape(ABC):
    def __init__(self, renderer: Renderer):
        self.renderer = renderer          # Bridge: composition

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def resize(self, factor: float):
        pass


class Circle(Shape):
    def __init__(self, renderer: Renderer, radius: float):
        super().__init__(renderer)
        self.radius = radius

    def draw(self):
        self.renderer.render_circle(self.radius)

    def resize(self, factor: float):
        self.radius *= factor


class Square(Shape):
    def __init__(self, renderer: Renderer, side: float):
        super().__init__(renderer)
        self.side = side

    def draw(self):
        self.renderer.render_square(self.side)

    def resize(self, factor: float):
        self.side *= factor


# ---------- استفاده ----------
vector = VectorRenderer()
raster = RasterRenderer()

circle = Circle(vector, 5)
circle.draw()          # Drawing a circle of radius 5 with vectors

circle2 = Circle(raster, 5)
circle2.draw()         # Drawing pixels for a circle of radius 5

square = Square(vector, 4)
square.draw()
square.resize(2)
square.draw()
