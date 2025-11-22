import logging
import logging.handlers
import json
import os


class JsonFormatter(logging.Formatter):
    def format(self, record):
        msg = {
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record)
        }
        if record.exc_info:
            msg["exc"] = self.formatException(record.exc_info)
        return json.dumps(msg)


def configure_logging():
    root = logging.getLogger()
    if root.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root.setLevel(logging.INFO)
    root.addHandler(handler)

    # optional rotating file
    log_file = os.getenv("LOG_FILE", "")
    if log_file:
        fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=3)
        fh.setFormatter(JsonFormatter())
        root.addHandler(fh)
