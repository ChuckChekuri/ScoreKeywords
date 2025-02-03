import csv
import time
import psutil
import win32gui
import win32process
from datetime import datetime
import os
import ctypes

def get_active_window_title():
    window = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(window)
    process = psutil.Process(pid)
    return process.name(), win32gui.GetWindowText(window)

def get_idle_time():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
    
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))
    millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0

def main():
    output_dir = r"C:\temp"
    os.makedirs(output_dir, exist_ok=True)
    csv_file = os.path.join(output_dir, f"app_usage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Application", "Window Title", "Duration (seconds)"])

    last_app, last_title = "", ""
    start_time = time.time()
    last_active_time = time.time()

    while True:
        try:
            current_app, current_title = get_active_window_title()
            current_time = time.time()
            idle_time = get_idle_time()

            if idle_time > 60:  # Consider system idle after 60 seconds of inactivity
                last_active_time = current_time - idle_time

            if current_app != last_app or current_title != last_title:
                if last_app:
                    duration = last_active_time - start_time
                    with open(csv_file, 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S'),
                            last_app,
                            last_title,
                            round(duration, 2)
                        ])

                last_app, last_title = current_app, current_title
                start_time = last_active_time = current_time

            time.sleep(1)

        except KeyboardInterrupt:
            print("Tracking stopped.")
            break

if __name__ == "__main__":
    main()
