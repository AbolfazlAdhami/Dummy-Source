# client.py
import socket
import json
from abc import ABC, abstractmethod


class CalculatorInterface(ABC):
    """Subject - رابط مشترک"""
    @abstractmethod
    def add(self, a: float, b: float) -> float:
        pass

    @abstractmethod
    def multiply(self, a: float, b: float) -> float:
        pass

    @abstractmethod
    def divide(self, a: float, b: float) -> float:
        pass


class RemoteCalculatorProxy(CalculatorInterface):
    """Remote Proxy - نماینده شیء روی سرور"""

    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port

    def _remote_call(self, method: str, *args, **kwargs):
        """ارسال درخواست از طریق شبکه و دریافت پاسخ"""
        request = {
            "method": method,
            "args": args,
            "kwargs": kwargs
        }

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.sendall(json.dumps(request).encode('utf-8'))

            data = sock.recv(4096).decode('utf-8')
            response = json.loads(data)

            if response["status"] == "error":
                raise Exception(response["message"])
            return response["result"]

    def add(self, a: float, b: float) -> float:
        print(f"[Proxy] ارسال درخواست add({a}, {b}) به سرور...")
        return self._remote_call("add", a, b)

    def multiply(self, a: float, b: float) -> float:
        print(f"[Proxy] ارسال درخواست multiply({a}, {b}) به سرور...")
        return self._remote_call("multiply", a, b)

    def divide(self, a: float, b: float) -> float:
        print(f"[Proxy] ارسال درخواست divide({a}, {b}) به سرور...")
        return self._remote_call("divide", a, b)


# ---------- استفاده ----------
if __name__ == "__main__":
    calc = RemoteCalculatorProxy()

    print("نتیجه جمع:", calc.add(10, 5))
    print("نتیجه ضرب:", calc.multiply(4, 7))
    print("نتیجه تقسیم:", calc.divide(20, 4))

    try:
        print(calc.divide(10, 0))
    except Exception as e:
        print("خطا:", e)
