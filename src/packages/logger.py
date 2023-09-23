from datetime import datetime
import json
from enum import Enum

log_file = "logs.json"

class LogLevels(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

def get_logs():
    final_logs = []
    logs = {}
    with open(log_file, "r") as f:
        logs = f.read()
    logs = json.loads(logs)
    for log in logs:
        final_logs.append(log)
    return final_logs

def get_formated_datetime():
    dateTime = datetime.now()
    formated_str_datetime = f"{dateTime.year}-{dateTime.month}-{dateTime.day} {dateTime.hour}:{dateTime.minute}:{dateTime.second}"
    return formated_str_datetime



class Logger:
    def __init__(self, filename):
        self.filename = filename

    def write_log(self, log):
        all_logs = None
        with open(self.filename, "r") as f:
            all_logs = f.read()
        all_logs = json.loads(all_logs)
        all_logs.append(log)
        with open(self.filename, "w") as f:
           json.dump(all_logs, f)

    def log(self, message, level):
        log = {}
        log["time"] = get_formated_datetime()

        if level == LogLevels.DEBUG:
            log["level"] = "DEBUG"
        if level == LogLevels.INFO:
            log["level"] = "INFO"
        if level == LogLevels.WARNING:
            log["level"] = "WARNING"
        if level == LogLevels.ERROR:
            log["level"] = "ERROR"
        if level == LogLevels.CRITICAL:
            log["level"] = "CRITICAL"
        log["message"] = message

        self.write_log(log)
        

logger = Logger(log_file)