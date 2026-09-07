from abc import ABC, abstractmethod
from typing import List


class Employee(ABC):
    @abstractmethod
    def show_details(self, indent: str = ""):
        pass

    @abstractmethod
    def get_salary(self) -> float:
        pass


class Developer(Employee):
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    def show_details(self, indent: str = ""):
        print(f"{indent}👨‍💻 {self.name} - ${self.salary}")

    def get_salary(self) -> float:
        return self.salary


class Manager(Employee):
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary
        self.subordinates: List[Employee] = []

    def add(self, employee: Employee):
        self.subordinates.append(employee)

    def show_details(self, indent: str = ""):
        print(f"{indent}👔 {self.name} (Manager) - ${self.salary}")
        for emp in self.subordinates:
            emp.show_details(indent + "    ")

    def get_salary(self) -> float:
        total = self.salary
        for emp in self.subordinates:
            total += emp.get_salary()
        return total


dev1 = Developer("علی", 80000)
dev2 = Developer("سارا", 85000)
dev3 = Developer("رضا", 78000)

manager1 = Manager("مینا", 120000)
manager1.add(dev1)
manager1.add(dev2)

ceo = Manager("آقای محمدی", 200000)
ceo.add(manager1)
ceo.add(dev3)

ceo.show_details()
print(f"\nجمع کل حقوق: ${ceo.get_salary()}")
