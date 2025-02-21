import time
import win32gui
import win32process
import win32api
import psutil
import datetime as dt
from database import initialize_database, log_session

class Tracker:
    def __init__(self):
        initialize_database()
        self._running = False
        self._current_app = None
        self._start_time = None

    def start_tracking(self):
        self._running = True
        try:
            while self._running:
                active_app = self.get_foreground_app()

                # If the active app has changed, log the time spent on the previous app
                if active_app != self._current_app:
                    if self._current_app and self._start_time:
                        self.log_time()
                    
                    self._start_time = dt.datetime.now()
                    self._current_app = active_app
                    
                time.sleep(1) # Check every second
        except (KeyboardInterrupt, Exception) as e:
            print(e)
            self.stop_tracking()

    def get_foreground_app(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            exe_path = process.exe()

            # Get the name of the executable from the file description
            try: 
                langs = win32api.GetFileVersionInfo(exe_path, '\\VarFileInfo\\Translation')
                key = 'StringFileInfo\\%04x%04x\\FileDescription' %(langs[0][0], langs[0][1])
                name = win32api.GetFileVersionInfo(exe_path, key)
            except Exception as e:
                name = process.name() # Use the process name if the file description is not available
            
            return name
        except Exception as e:
            return None

    def log_time(self):
        end_time = dt.datetime.now()
        duration = (int)((end_time - self._start_time).total_seconds())
        log_session(self._current_app, self._start_time, end_time, duration)


    def stop_tracking(self):
        self._running = False
        if self._current_app and self._start_time:
            self.log_time()
