from pynput.keyboard import KeyCode
from pynput import mouse, keyboard
from pynput.mouse import Button
import json, os, datetime, copy

# TODO: Dump data to json file on stop button press.

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
        self.file.truncate(0)
        json.dump(data, self.file, indent=2)
    
    def __iter__(self):
        return iter({
            "name": self.name,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
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
        milliseconds =  int(round(total_seconds - whole_seconds, 2) * 1000)
        x = lambda x : str(x).rjust(2, "0")[:2]
        return f"{x(minutes)}:{x(seconds)}.{x(milliseconds)}"
    
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
        self.file.close()
        
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