class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = "Connected to DB"  # type: ignore
        return cls._instance


db1 = Database()
db2 = Database()
print(db1 is db2)  # True
