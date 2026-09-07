import copy


class Shape:
    def __init__(self, color: str):
        self.color = color

    def clone(self):
        return copy.deepcopy(self)


circle1 = Shape("Red")
circle2 = circle1.clone()
print(circle1.color)  # Output: Red
