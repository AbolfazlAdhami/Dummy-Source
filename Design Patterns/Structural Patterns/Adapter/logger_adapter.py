import logging

# Adaptee


class OldLogger:
    def log_message(self, level, message):
        print(f"[{level.upper()}] {message}")

# Adapter


class LoggingAdapter(logging.Handler):
    def __init__(self, old_logger: OldLogger):
        super().__init__()
        self.old_logger = old_logger

    def emit(self, record):
        level = record.levelname
        message = self.format(record)
        self.old_logger.log_message(level, message)


old = OldLogger()
adapter = LoggingAdapter(old)
logger = logging.getLogger("my_app")
logger.addHandler(adapter)
logger.setLevel(logging.INFO)

logger.info("This is Test Message!")
logger.error("Error!")
logger.critical("Access Permission!")
