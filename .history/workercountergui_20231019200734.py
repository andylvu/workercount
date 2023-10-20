import tkinter as tk
from workercounterapp import WorkerCounterApp
import cv2
from PIL import Image, ImageTk

class WorkerCounterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Worker Counter")
        self.worker_counter = WorkerCounterApp()
        self.worker_count_label = tk.Label(root, text = "Workers: 0")
        self.worker_count_label.pack()
        self.update_count()

        self.video_label = tk.Label(root)
        self.video_label.pack()
        self.video_capture()

    def update_count(self):
        count = self.worker_counter.working_count
        self.worker_count_label.config(text = f"Workers: {count}")
        self.root.after(1000, self.update_count) # update the count every 1 second

    def video_capture(self):
        cap = cv2.VideoCapture(0)
        self.show_frame(cap)

    def show_frame(self, cap):
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            self.video_label.img = img
            self.video_label.config(image=img)
            self.root.after(10, self.show_frame, cap)
        else:
            cap.release()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("100x50")
    app = WorkerCounterGUI(root)
    root.mainloop()