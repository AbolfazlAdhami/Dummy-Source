from abc import ABC, abstractmethod

# ---------- Component ----------


class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


# ---------- ConcreteComponent ----------
class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 2.0

    def description(self) -> str:
        return "قهوه ساده"


# ---------- Decorator پایه ----------
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()


# ---------- Concrete Decorators ----------
class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.5

    def description(self) -> str:
        return self._coffee.description() + " + شیر"


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.2

    def description(self) -> str:
        return self._coffee.description() + " + شکر"


class WhipDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.7

    def description(self) -> str:
        return self._coffee.description() + " + خامه"


# ---------- استفاده ----------
coffee = SimpleCoffee()
print(f"{coffee.description()} → {coffee.cost()} تومان")

coffee = MilkDecorator(coffee)
print(f"{coffee.description()} → {coffee.cost()} تومان")

coffee = SugarDecorator(coffee)
print(f"{coffee.description()} → {coffee.cost()} تومان")

coffee = WhipDecorator(coffee)
print(f"{coffee.description()} → {coffee.cost()} تومان")
