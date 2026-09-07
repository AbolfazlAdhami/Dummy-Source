from abc import ABC, abstractmethod
import time


class Image(ABC):
    @abstractmethod
    def display(self):
        pass


class RealImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self):
        print(f"در حال بارگذاری تصویر سنگین: {self.filename} ...")
        time.sleep(1)  # شبیه‌سازی بارگذاری سنگین
        print("بارگذاری تمام شد.")

    def display(self):
        print(f"نمایش تصویر: {self.filename}")


class ProxyImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        self._real_image = None          # هنوز ساخته نشده

    def display(self):
        if self._real_image is None:     # Lazy Initialization
            self._real_image = RealImage(self.filename)
        self._real_image.display()


# ---------- استفاده ----------
print("ساخت Proxy (هنوز تصویری بارگذاری نشده):")
image = ProxyImage("photo_4k.jpg")

print("\nاولین بار display فراخوانی می‌شود:")
image.display()          # اینجا بارگذاری انجام می‌شود

print("\nدومین بار display فراخوانی می‌شود:")
image.display()          # دیگر بارگذاری نمی‌شود
