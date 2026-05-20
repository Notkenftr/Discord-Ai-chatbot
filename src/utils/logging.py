import os
import datetime


class Logging:
    def __init__(self):
        self.log_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
        )

        os.makedirs(self.log_path, exist_ok=True)

        date = datetime.datetime.now().strftime("%Y-%m-%d")

        counter = 1

        while True:
            filename = f"{date}_{counter}.log"
            filepath = os.path.join(self.log_path, filename)

            if not os.path.exists(filepath):
                self.log_file = filepath
                break

            counter += 1

    def _write(self, level: str, message: str):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        log_text = f"[{current_time}] [{level.upper()}] {message}\n"

        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(log_text)

        print(log_text, end="")

    def info(self, message: str):
        self._write("INFO", message)

    def warning(self, message: str):
        self._write("WARNING", message)

    def error(self, message: str):
        self._write("ERROR", message)

    def debug(self, message: str):
        self._write("DEBUG", message)

    def critical(self, message: str):
        self._write("CRITICAL", message)