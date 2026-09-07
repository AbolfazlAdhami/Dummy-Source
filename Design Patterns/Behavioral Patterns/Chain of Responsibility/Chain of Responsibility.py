from abc import ABC, abstractmethod
from typing import Optional


class Handler(ABC):
    """Abstract handler."""

    def __init__(self) -> None:
        self._next: Optional[Handler] = None

    def set_next(self, handler: "Handler") -> "Handler":
        """Set the next handler in the chain and return it (for fluent chaining)."""
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: str) -> Optional[str]:
        """Handle the request or pass it to the next handler."""
        if self._next:
            return self._next.handle(request)
        return None


class MonkeyHandler(Handler):
    def handle(self, request: str) -> Optional[str]:
        if request == "Banana":
            return f"Monkey: I'll eat the {request}"
        return super().handle(request)


class SquirrelHandler(Handler):
    def handle(self, request: str) -> Optional[str]:
        if request == "Nut":
            return f"Squirrel: I'll eat the {request}"
        return super().handle(request)


class DogHandler(Handler):
    def handle(self, request: str) -> Optional[str]:
        if request == "MeatBall":
            return f"Dog: I'll eat the {request}"
        return super().handle(request)


# Client code
def client_code(handler: Handler) -> None:
    for food in ["Nut", "Banana", "Cup of coffee"]:
        print(f"\nClient: Who wants a {food}?")
        result = handler.handle(food)
        if result:
            print(f"  {result}")
        else:
            print(f"  {food} was left untouched.")


if __name__ == "__main__":
    # Build the chain: Monkey → Squirrel → Dog
    monkey = MonkeyHandler()
    squirrel = SquirrelHandler()
    dog = DogHandler()

    monkey.set_next(squirrel).set_next(dog)

    print("Chain: Monkey > Squirrel > Dog")
    client_code(monkey)

    print("\n" + "="*40)
    print("Subchain: Squirrel > Dog")
    client_code(squirrel)
