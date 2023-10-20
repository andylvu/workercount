import tkinter as tk
from workercounterapp import WorkerCounterApp
from workercountergui import WorkerCounterGUI
import threading  # To run the WorkerCounterApp and GUI concurrently

def main():
    # Create the main Tkinter window for the GUI
    root = tk.Tk()
    root.geometry("100x50")

    # Create instances of WorkerCounterApp and WorkerCounterGUI
    worker_counter = WorkerCounterApp()
    gui = WorkerCounterGUI(root, worker_counter)

    # Create a thread to run the WorkerCounterApp
    worker_app_thread = threading.Thread(target=worker_counter.main)
    worker_app_thread.start()

    # Start the GUI main loop to display the worker count
    root.mainloop()

if __name__ == '__main__':
    main()
