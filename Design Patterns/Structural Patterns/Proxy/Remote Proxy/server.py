# server.py
import socket
import json
import threading


class Calculator:
    """Real Subject - شیء واقعی روی سرور"""

    def add(self, a: float, b: float) -> float:
        print(f"[Server] محاسبه {a} + {b}")
        return a + b

    def multiply(self, a: float, b: float) -> float:
        print(f"[Server] محاسبه {a} * {b}")
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("تقسیم بر صفر مجاز نیست")
        print(f"[Server] محاسبه {a} / {b}")
        return a / b


def handle_client(conn, addr, calculator):
    print(f"[Server] اتصال جدید از {addr}")
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            request = json.loads(data)
            method = request.get("method")
            args = request.get("args", [])
            kwargs = request.get("kwargs", {})

            try:
                result = getattr(calculator, method)(*args, **kwargs)
                response = {"status": "success", "result": result}
            except Exception as e:
                response = {"status": "error", "message": str(e)}

            conn.sendall(json.dumps(response).encode('utf-8'))
    finally:
        conn.close()
        print(f"[Server] اتصال {addr} بسته شد")


def start_server(host='localhost', port=9999):
    calculator = Calculator()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"[Server] در حال گوش دادن روی {host}:{port} ...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=handle_client, args=(conn, addr, calculator))
        thread.start()


if __name__ == "__main__":
    start_server()
