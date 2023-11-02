import os
import shutil
from enum import Enum
from datetime import datetime
from contextlib import redirect_stdout
from window_renderer import Window_Render
import threading
from multiprocessing import Process

log_directory = "./bin/"


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


def get_formated_datetime():
    dateTime = datetime.now()
    formated_str_datetime = f"d:{dateTime.day}/{dateTime.month} h:{dateTime.hour}:{dateTime.minute}:{dateTime.second}"
    return formated_str_datetime


class Logger:
    def __init__(self, isWindowed=False, auto_destroy=False):
        # Create the directory if non existant
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        self.auto_destroy=auto_destroy
        self.isWindowed = isWindowed
        self.filename = log_directory + str(datetime.now().timestamp()) + "logs.txt"
        with open(self.filename, 'w') as f:
            f.write("[logs started on :" + get_formated_datetime() + "]\n\n")
        # Currently, this feature is not functionnal and will be the fruit of a future update
        if self.isWindowed == "bugged":
            self.winddowThread = Process(target=self.run_window())
            self.winddowThread.start()

    def log(self, message, level=0):
        self.print('*' * level + "[" + str(list(LogLevel)[level].name) + "][" + get_formated_datetime() + "]: " + message )

    def print(self, text):
        with open(self.filename, 'a+') as f:
            with redirect_stdout(f):
                print(text)

    def run_window(self):
        Window_Render(self.filename)

    def __del__(self):
        # Destroy Logs upon Logger Object destruction, only if enabled
        if self.auto_destroy:
            shutil.rmtree(log_directory)
