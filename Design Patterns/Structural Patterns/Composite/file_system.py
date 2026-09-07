from abc import ABC, abstractmethod
from typing import List


class FileSystemComponent(ABC):
    @abstractmethod
    def show(self, indent: str = ""):
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass


class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def show(self, indent: str = ""):
        print(f"{indent}📄 {self.name} ({self.size} KB)")

    def get_size(self) -> int:
        return self.size


class Directory(FileSystemComponent):
    def __init__(self, name: str):
        self.name = name
        self.children: List[FileSystemComponent] = []

    def add(self, component: FileSystemComponent):
        self.children.append(component)

    def remove(self, component: FileSystemComponent):
        self.children.remove(component)

    def show(self, indent: str = ""):
        print(f"{indent}📁 {self.name}/")
        for child in self.children:
            child.show(indent + "    ")

    def get_size(self) -> int:
        total = 0
        for child in self.children:
            total += child.get_size()
        return total


root = Directory("root")
home = Directory("home")
user = Directory("user")
docs = Directory("documents")

file1 = File("resume.pdf", 120)
file2 = File("photo.jpg", 2500)
file3 = File("notes.txt", 15)
file4 = File("config.ini", 5)

docs.add(file1)
docs.add(file2)
user.add(docs)
user.add(file3)
home.add(user)
root.add(home)
root.add(file4)

root.show()
print(f"\nTotal Volume: {root.get_size()} KB")
