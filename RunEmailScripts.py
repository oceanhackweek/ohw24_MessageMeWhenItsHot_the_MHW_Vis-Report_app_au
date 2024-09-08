import threading
import time
import subprocess


# Function to run the two scripts
def run_scripts():
    while True:
        # Run CheckJson.py
        subprocess.run(["python", "CheckJson.py"])
        # Run CheckRecord.py
        subprocess.run(["python", "CheckRecord.py"])
        # Wait for 5 minutes before running again
        time.sleep(600)


# Start the background task
script_thread = threading.Thread(target=run_scripts, daemon=True)
script_thread.start()
