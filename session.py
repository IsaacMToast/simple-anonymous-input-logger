import datetime
import time
from recorder import Recorder

# Use Session.__dict__ to serialize into json.
# TO DO:
#  - Add session creator/naming menu.
#  - Should use JSON, not SQLite. Dont. overcomplicate things.
#  - It should display existing session names.
#  - Prompt user to name new session.

class Session:
    name: str
    created_at: str
    concluded_at: str
    mouse_timestamps: list
    keyboard_timestamps: list
    
    def __init__(self, name:str):
        self.name: str = name
        self.created_at: str = datetime.datetime.now().isoformat()
        self.concluded_at = None
        self.mouse_timestamps = []
        self.keyboard_timestamps = []
        self.recorder = Recorder(self.mouse_timestamps, self.keyboard_timestamps)        

    def stop(self):
        self.recorder.stop()
        self.concluded = datetime.datetime.now().isoformat()
        
    def start(self):
        self.recorder.start()
        
    def end():
        ...
        
    def pause():
        ...