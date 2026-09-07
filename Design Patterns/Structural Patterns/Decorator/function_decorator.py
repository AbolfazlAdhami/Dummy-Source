import time
from functools import wraps


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"زمان اجرای {func.__name__}: {end - start:.4f} ثانیه")
        return result
    return wrapper


def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"فراخوانی {func.__name__} با آرگومان‌های {args}")
        result = func(*args, **kwargs)
        print(f"نتیجه: {result}")
        return result
    return wrapper


@timing_decorator
@log_decorator
def calculate_sum(n):
    return sum(range(n))


calculate_sum(1000000)
