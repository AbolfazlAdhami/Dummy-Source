class DataService:
    def get_data(self, key: str) -> str:
        print(f"دریافت داده از منبع اصلی برای کلید: {key}")
        return f"داده-{key}"


class CachingProxy:
    def __init__(self, service: DataService):
        self._service = service
        self._cache = {}

    def get_data(self, key: str) -> str:
        if key not in self._cache:
            self._cache[key] = self._service.get_data(key)
        else:
            print(f"برگرداندن از کش برای کلید: {key}")
        return self._cache[key]


# استفاده
service = CachingProxy(DataService())
print(service.get_data("user_42"))
print(service.get_data("user_42"))   # از کش می‌آید
