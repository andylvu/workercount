import tkinter as tk
from workercounterapp import WorkerCounterApp
from workercountergui import WorkerCounterGUI
import threading

def main():
    # Create the main Tkinter window for the GUI
    root = tk.Tk()
    root.geometry("100x50")

    # Create instances of WorkerCounterApp and WorkerCounterGUI
    worker_counter = WorkerCounterApp()
    gui = WorkerCounterGUI(root)

    # Link the WorkerCounterApp instance to the GUI
    gui.set_worker_counter(worker_counter)

    # Create a thread to run the WorkerCounterApp
    worker_app_thread = threading.Thread(target=worker_counter.main)
    worker_app_thread.start()

    # Start the GUI main loop to display the worker count
    root.mainloop()

if __name__ == '__main__':
    main()
