from pynput.keyboard import KeyCode
from pynput import mouse, keyboard
from pynput.mouse import Button
import json, os, datetime, copy

# TODO: 
#  - Remove temp file replacement thing for file dumping. 
#  - Can only use the same file to read/write.

class Session:
    name: str
    created_at: float
    started_at: float
    ended_at: float
    mouse_timestamps: list
    keyboard_timestamps: list
    
    def __init__(self, name:str):
        self.name: str = name
        self.created_at: float = datetime.datetime.now().timestamp()
        
        # Begin/end times.
        self.started_at = None
        self.ended_at = None
        
        # Pausing logic variables.
        self._is_paused = True
        self._paused_at = 0
        self._resumed_at = 0
        self._duration_paused = 0
        
        # Keystroke lists.
        self.mouse_timestamps = []
        self.keyboard_timestamps = []
        
        # Event listeners.
        self._mouse_listener = None
        self._keyboard_listener = None
        
        # File stream.
        self.file = open(self.get_data_filepath(), "r+")
        self.data_snapshot = json.load(self.file)
        
    def dump_data(self):
        data = copy.deepcopy(self.data_snapshot)
        data["sessions"].append(dict(self))
        with open(self.get_data_filepath(), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())

    
    def __iter__(self):
        return iter({
            "name": self.name,
            "created_at": datetime.datetime.fromtimestamp(self.created_at).isoformat(),
            "started_at": datetime.datetime.fromtimestamp(self.started_at).isoformat(),
            "ended_at": None if not self.ended_at else datetime.datetime.fromtimestamp(self.ended_at).isoformat(),
            "mouse_timestamps": self.mouse_timestamps,
            "keyboard_timestamps": self.keyboard_timestamps
        }.items())
    
    def get_data_filepath(self):
        PATH = "./data.json"
        if not os.path.isfile(PATH):
            with open(PATH, "w") as f:
                placeholder = {
                    "sessions": []
                }
                json.dump(placeholder, f, indent=2)
        return PATH
    
    def seconds_to_duration(self, total_seconds: float):
        whole_seconds = int(total_seconds)
        minutes = int(whole_seconds // 60)
        seconds = int(whole_seconds % 60)
        milliseconds =  int((total_seconds - whole_seconds) * 1000)
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}".replace(" ", "0")
    
    def get_duration_timestamp(self):
        return self.seconds_to_duration(self.elapsed)    
        
    def stop(self):
        self._is_paused = True
        self._mouse_listener.stop()
        self._keyboard_listener.stop()
        self._mouse_listener = None
        self._keyboard_listener = None
        self.ended_at = datetime.datetime.now().timestamp()
        self.dump_data()
        
    def start(self):
        self._is_paused = False
        self._mouse_listener = mouse.Listener(
            on_click=self.on_mouse_click
        )
        self._keyboard_listener = keyboard.Listener(
            on_press=self.on_keyboard_press
        )
        self._mouse_listener.start()
        self._keyboard_listener.start()
        self.started_at = datetime.datetime.now().timestamp()
        
    def pause(self):
        self._is_paused = True
        self._paused_at = datetime.datetime.now().timestamp()
        
    def resume(self):
        self._is_paused = False
        self._resumed_at = datetime.datetime.now().timestamp()
        self._duration_paused += self._resumed_at - self._paused_at
        
    @property
    def elapsed(self):
        end = self.ended_at or datetime.datetime.now().timestamp()
        return end - self.started_at - self._duration_paused
    
    def on_mouse_click(self, x: int, y: int, button: Button, pressed: bool):
        if pressed == False:
            return
        elif self._is_paused:
            return
        
        print("Clicked the mouse.")
        
        # Record mouse clicks.
        self.mouse_timestamps.append(self.get_duration_timestamp())
        self.dump_data()

    def on_keyboard_press(self, key: KeyCode):
        if self._is_paused:
            return
        
        print("Pressed a key.")

        # Record keyboard presses.
        self.keyboard_timestamps.append(self.get_duration_timestamp())
        self.dump_data()