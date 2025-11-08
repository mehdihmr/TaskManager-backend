import logging
import os
from datetime import date, timedelta, datetime
import re


class Logger:
    logger = None

    @classmethod
    def setup_logger(cls):
        """Set up the logger.

        This method configures a logger with both console and file handlers,
        allowing for logging to both the console and a log file.
        """

        if cls.logger is None:
            cls.__delete_old_logs()
            cls.logger = logging.getLogger("Candy-Machine")

            cls.logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)

            today_date = date.today()
            log_file_name = f"candy_machine_logs_{today_date}.log"
            file_path = os.path.join(os.path.dirname(__file__), log_file_name)
            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            if not cls.logger.hasHandlers():
                cls.logger.addHandler(console_handler)
                cls.logger.addHandler(file_handler)

    @staticmethod
    def log_error(message):
        Logger.setup_logger()
        Logger.logger.error(message)

    @staticmethod
    def log_warning(message):
        Logger.setup_logger()
        Logger.logger.warning(message)

    @staticmethod
    def log_info(message):
        Logger.setup_logger()
        Logger.logger.info(message)

    @staticmethod
    def log_debug(message):
        Logger.setup_logger()
        Logger.logger.debug(message)

    @staticmethod
    def log_critical(message):
        Logger.setup_logger()
        Logger.logger.critical(message)

    @staticmethod
    def __delete_old_logs():
        date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})")
        logs_path = "src/utilities/Logger"
        threshold = datetime.now() - timedelta(days=30)

        for filename in os.listdir(logs_path):
            if not filename.endswith(".log"):
                continue

            match = date_pattern.search(filename)
            if not match:
                continue

            date_str = match.group(1)
            try:
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
            except Exception:
                continue

            if file_date <= threshold:
                file_path = os.path.join(logs_path, filename)
                os.remove(file_path)
