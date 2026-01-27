from pynput.keyboard import KeyCode
from pynput import mouse, keyboard
from pynput.mouse import Button
import datetime

# Use Session.__dict__ to serialize into json.
# TO DO:
#  - Add session creator/naming menu.
#  - Should use JSON, not SQLite. Dont. overcomplicate things.
#  - It should display existing session names.
#  - Prompt user to name new session.

class Session:
    name: str
    created_at: float
    started_at: float
    ended_at: float
    mouse_timestamps: list
    keyboard_timestamps: list
    
    def __init__(self, name:str):
        self.name: str = name
        self.created_at: str = datetime.datetime.now().timestamp()
        
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
        
    def stop(self):
        self._is_paused = True
        self._mouse_listener.stop()
        self._keyboard_listener.stop()
        self._mouse_listener = None
        self._keyboard_listener = None
        self.concluded = datetime.datetime.now().timestamp()
        print(self.mouse_timestamps)
        
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
        self.mouse_timestamps.append(datetime.datetime.now().timestamp() - self.started_at)
        # print(self.mouse_timestamps)

    def on_keyboard_press(self, key: KeyCode):
        if self._is_paused:
            return
        
        print("Pressed a key.")

        # Record keyboard presses.
        self.keyboard_timestamps.append(datetime.datetime.now().timestamp() - self.started_at)
        