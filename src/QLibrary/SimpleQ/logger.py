from datetime import datetime
import json

DEBUG = 1
INFO = 2
WARNING = 3
ERROR = 4
CRITICAL = 5

log_file = "logs.json"

def get_logs():
    final_logs = []
    logs = {}
    with open(log_file, "r") as f:
        logs = json.loads(f.read())
    for log in logs:
        final_logs.append(json.loads(log))
    return final_logs

def get_formated_datetime():
    dateTime = datetime.now()
    formated_str_datetime = f"{dateTime.year}-{dateTime.month}-{dateTime.day} {dateTime.hour}:{dateTime.minute}:{dateTime.second}"
    return formated_str_datetime

class Logger:
    def __init__(self, filename):
        self.filename = filename

    def log(self, message, level):
        log = {}
        log["time"] = get_formated_datetime()

        if level == DEBUG:
            log["level"] = "DEBUG"
        if level == INFO:
            log["level"] = "INFO"
        if level == WARNING:
            log["level"] = "WARNING"
        if level == ERROR:
            log["level"] = "ERROR"
        if level == CRITICAL:
            log["level"] = "CRITICAL"

        log["message"] = message

        json_log = json.dumps(log, indent=4)
        all_logs = None
        with open(self.filename, "r") as f:
            all_logs = f.read()
            all_logs = json.loads(all_logs)

        all_logs.append(json_log)
        with open(self.filename, "w") as f:
           json.dump(all_logs, f)

logger = Logger(log_file)