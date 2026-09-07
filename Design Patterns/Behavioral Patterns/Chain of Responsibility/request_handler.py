from abc import ABC, abstractmethod
from typing import Optional


class Handler(ABC):
    """کلاس پایه برای پردازش‌کننده‌ها"""

    def __init__(self):
        self._next_handler: Optional[Handler] = None

    def set_next(self, handler: "Handler") -> "Handler":
        self._next_handler = handler
        # بازگرداندن handler برای امکان چینش زنجیره‌ای (Chaining)
        return handler

    @abstractmethod
    def handle(self, request: dict) -> Optional[str]:
        if self._next_handler:
            return self._next_handler.handle(request)
        return None

# ۱. پردازش‌کننده احراز هویت


class AuthenticationHandler(Handler):
    def handle(self, request: dict) -> Optional[str]:
        if not request.get("is_authenticated"):
            return "خطا: کاربر احراز هویت نشده است."
        print("[Auth] کاربر تایید شد.")
        return super().handle(request)

# ۲. پردازش‌کننده بررسی دسترسی (Role)


class AuthorizationHandler(Handler):
    def handle(self, request: dict) -> Optional[str]:
        if request.get("role") != "admin":
            return "خطا: سطح دسترسی کافی نیست."
        print("[AuthZ] دسترسی ادمین تایید شد.")
        return super().handle(request)

# ۳. پردازش‌کننده محدودیت تعداد درخواست (Rate Limit)


class RateLimitHandler(Handler):
    def handle(self, request: dict) -> Optional[str]:
        if request.get("request_count", 0) > 100:
            return "خطا: تعداد درخواست‌ها بیش از حد مجاز است."
        print("[RateLimit] تعداد درخواست مجاز است.")
        return super().handle(request)


# --- کد کلاینت ---
# ساخت زنجیره: Auth -> Role -> RateLimit
auth = AuthenticationHandler()
role = AuthorizationHandler()
rate_limit = RateLimitHandler()

auth.set_next(role).set_next(rate_limit)

# تست ۱: درخواست معتبر
req_valid = {"is_authenticated": True, "role": "admin", "request_count": 10}
result = auth.handle(req_valid)
print("نتیجه:", result or "درخواست با موفقیت پردازش شد.\n")

# تست ۲: درخواست بدون دسترسی ادمین
req_invalid = {"is_authenticated": True, "role": "user", "request_count": 10}
result = auth.handle(req_invalid)
print("نتیجه:", result)
