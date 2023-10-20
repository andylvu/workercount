import tkinter as tk
from workercounterapp import WorkerCounterApp
import sys

class WorkerCounterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Worker Counter")
        self.worker_counter = WorkerCounterApp()
        self.worker_count_label = tk.Label(root, text = "Workers: 0")
        self.worker_count_label.pack()
        self.update_count()

    def update_count(self):
        try:
            count = self.worker_counter.working_count
            self.worker_count_label.config(text = f"Workers: {count}")
            self.root.after(1000, self.update_count) # update the count every 1 second

        except KeyboardInterrupt:
            self.root.destroy()
            sys.exit(0)
