import tkinter as tk
from workercounterapp import WorkerCounterApp
from workercountergui import WorkerCounterGUI

def main():
    root = tk.Tk()
    root.geometry("100x50")

    worker_counter = WorkerCounterApp(gui=None)  # Create the worker counter app without GUI reference
    gui = WorkerCounterGUI(root, worker_counter)  # Pass the worker counter instance to the GUI

    worker_counter.main()  # Start the worker counter app's main loop

    # Add code to display live video here using OpenCV or another library
    gui.video_capture()

    root.mainloop()

if __name__ == '__main__':
    main()