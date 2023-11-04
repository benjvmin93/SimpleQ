import tkinter as tk
from tkinter import scrolledtext
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Window_Render(FileSystemEventHandler):

    def __init__(self, file_path):
        self.file_path = file_path
        self.root = tk.Tk()
        self.root.title("Logger")
        self.root.iconbitmap(default="")
        self.text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, fg="lightgreen", bg="black",
                                                     insertbackground="green",
                                                     font=("Helvetica", 12))
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget.config(state=tk.DISABLED)
        self.update_text_content()

        self.observer = Observer()
        self.observer.schedule(self, path=".", recursive=False)
        self.observer.start()
        try :
            self.root.mainloop()
        except KeyboardInterrupt:
            print("LogWindow Closed")
        self.observer.stop()
        self.observer.join()

    def on_modified(self, event):
        self.update_text_content()

    def update_text_content(self):
        with open(self.file_path, 'r') as file:
            content = file.read()
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, content)
        self.text_widget.config(state=tk.DISABLED)
