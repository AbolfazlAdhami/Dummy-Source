from abc import ABC, abstractmethod


class BankAccount(ABC):
    @abstractmethod
    def deposit(self, amount: float):
        pass

    @abstractmethod
    def withdraw(self, amount: float):
        pass

    @abstractmethod
    def get_balance(self) -> float:
        pass


class RealBankAccount(BankAccount):
    def __init__(self, balance: float = 0):
        self._balance = balance

    def deposit(self, amount: float):
        self._balance += amount
        print(f"واریز {amount} تومان انجام شد.")

    def withdraw(self, amount: float):
        if amount <= self._balance:
            self._balance -= amount
            print(f"برداشت {amount} تومان انجام شد.")
        else:
            print("موجودی کافی نیست!")

    def get_balance(self) -> float:
        return self._balance


class ProtectionProxy(BankAccount):
    def __init__(self, account: RealBankAccount, user_role: str):
        self._account = account
        self._user_role = user_role

    def deposit(self, amount: float):
        if self._user_role in ["admin", "user"]:
            self._account.deposit(amount)
        else:
            print("دسترسیdenied: شما اجازه واریز ندارید.")

    def withdraw(self, amount: float):
        if self._user_role == "admin":
            self._account.withdraw(amount)
        else:
            print("دسترسیdenied: فقط ادمین می‌تواند برداشت کند.")

    def get_balance(self) -> float:
        if self._user_role in ["admin", "user"]:
            return self._account.get_balance()
        else:
            print("دسترسیdenied")
            return 0


# ---------- استفاده ----------
real_account = RealBankAccount(1000)

admin_proxy = ProtectionProxy(real_account, "admin")
user_proxy = ProtectionProxy(real_account, "user")
guest_proxy = ProtectionProxy(real_account, "guest")

print("--- ادمین ---")
admin_proxy.withdraw(200)
print(f"موجودی: {admin_proxy.get_balance()}")

print("\n--- کاربر عادی ---")
user_proxy.deposit(100)
user_proxy.withdraw(50)          # رد می‌شود

print("\n--- مهمان ---")
guest_proxy.get_balance()        # رد می‌شود
