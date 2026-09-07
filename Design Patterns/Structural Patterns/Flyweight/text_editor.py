class CharacterStyle:
    """Flyweight: سبک مشترک"""

    def __init__(self, font: str, size: int, bold: bool = False):
        self.font = font
        self.size = size
        self.bold = bold

    def render(self, char: str, x: int, y: int):
        style = "بولد" if self.bold else "عادی"
        print(
            f"رندر '{char}' با فونت {self.font} اندازه {self.size} ({style}) در ({x},{y})")


class StyleFactory:
    _styles = {}

    @classmethod
    def get_style(cls, font: str, size: int, bold: bool = False):
        key = (font, size, bold)
        if key not in cls._styles:
            cls._styles[key] = CharacterStyle(font, size, bold)
        return cls._styles[key]
