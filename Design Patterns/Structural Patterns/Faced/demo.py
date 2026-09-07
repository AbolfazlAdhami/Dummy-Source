class Inventory:
    def check_stock(self, product_id: str) -> bool:
        print(f"بررسی موجودی محصول {product_id}...")
        return True

    def reserve(self, product_id: str, quantity: int):
        print(f"رزرو {quantity} عدد از محصول {product_id}")


class Payment:
    def process(self, amount: float, method: str) -> bool:
        print(f"پردازش پرداخت {amount} تومان با روش {method}...")
        return True


class Shipping:
    def schedule(self, address: str):
        print(f"زمان‌بندی ارسال به آدرس: {address}")


class Notification:
    def send_confirmation(self, email: str):
        print(f"ارسال ایمیل تأیید به {email}")


# ---------- Facade ----------
class OrderFacade:
    def __init__(self):
        self.inventory = Inventory()
        self.payment = Payment()
        self.shipping = Shipping()
        self.notification = Notification()

    def place_order(self, product_id: str, quantity: int, amount: float,
                    payment_method: str, address: str, email: str):
        print("\n--- شروع ثبت سفارش ---")

        if not self.inventory.check_stock(product_id):
            print("موجودی کافی نیست!")
            return False

        self.inventory.reserve(product_id, quantity)

        if not self.payment.process(amount, payment_method):
            print("پرداخت ناموفق بود!")
            return False

        self.shipping.schedule(address)
        self.notification.send_confirmation(email)

        print("--- سفارش با موفقیت ثبت شد ---\n")
        return True


# ---------- استفاده ----------
order = OrderFacade()
order.place_order(
    product_id="LAPTOP-123",
    quantity=1,
    amount=45000000,
    payment_method="کارت بانکی",
    address="تهران، خیابان ولیعصر",
    email="user@example.com"
)
