import tkinter as tk
from workercounterapp import WorkerCounterApp
from workercountergui import WorkerCounterGUI
import threading
import sys  # Import sys module

def main():
    # Create the main Tkinter window for the GUI
    root = tk.Tk()
    root.geometry("200x50")

    # Create instances of WorkerCounterApp and WorkerCounterGUI
    worker_counter = WorkerCounterApp()
    gui = WorkerCounterGUI(root)

    # Create a thread to run the WorkerCounterApp
    worker_app_thread = threading.Thread(target=worker_counter.run_worker_counter_app)
    worker_app_thread.start()

    # Start the GUI main loop to display the worker count
    try:
        root.mainloop()
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt by cleaning up
        worker_counter.cleanup()  # Add a cleanup method in WorkerCounterApp
        root.destroy()
        sys.exit(0)

if __name__ == '__main__':
    main()
