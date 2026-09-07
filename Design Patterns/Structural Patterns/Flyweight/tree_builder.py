from abc import ABC, abstractmethod
from typing import Dict


# ---------- Flyweight ----------
class TreeType:
    """Intrinsic State: مشترک بین درختان هم‌نوع"""

    def __init__(self, name: str, color: str, texture: str):
        self.name = name
        self.color = color
        self.texture = texture

    def draw(self, x: int, y: int):
        print(f"رسم درخت {self.name} با رنگ {self.color} در موقعیت ({x}, {y})")


# ---------- Flyweight Factory ----------
class TreeFactory:
    _tree_types: Dict[str, TreeType] = {}

    @classmethod
    def get_tree_type(cls, name: str, color: str, texture: str) -> TreeType:
        key = f"{name}_{color}_{texture}"
        if key not in cls._tree_types:
            print(f"ایجاد نوع درخت جدید: {key}")
            cls._tree_types[key] = TreeType(name, color, texture)
        return cls._tree_types[key]

    @classmethod
    def get_total_types(cls) -> int:
        return len(cls._tree_types)


# ---------- Context (حاوی Extrinsic State) ----------
class Tree:
    def __init__(self, x: int, y: int, tree_type: TreeType):
        self.x = x          # Extrinsic
        self.y = y          # Extrinsic
        self.type = tree_type  # Intrinsic (اشتراکی)

    def draw(self):
        self.type.draw(self.x, self.y)


# ---------- Client ----------
class Forest:
    def __init__(self):
        self.trees = []

    def plant_tree(self, x: int, y: int, name: str, color: str, texture: str):
        tree_type = TreeFactory.get_tree_type(name, color, texture)
        tree = Tree(x, y, tree_type)
        self.trees.append(tree)

    def draw(self):
        for tree in self.trees:
            tree.draw()


# ---------- استفاده ----------
forest = Forest()

# کاشت تعداد زیادی درخت با انواع محدود
for i in range(5):
    forest.plant_tree(i * 10, i * 20, "کاج", "سبز", "بافت-کاج")
    forest.plant_tree(i * 15, i * 25, "بلوط", "قهوه‌ای", "بافت-بلوط")
    forest.plant_tree(i * 12, i * 18, "کاج", "سبز", "بافت-کاج")  # نوع تکراری

print(f"\nتعداد کل درختان: {len(forest.trees)}")
print(f"تعداد انواع درخت (Flyweight): {TreeFactory.get_total_types()}")
print("\nرسم جنگل:")
forest.draw()
