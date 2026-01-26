from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import KeyCode
import datetime

class Recorder:
    def __init__(self, mouse_timestamps: list[str], keyboard_timestamps: list[str]):
        self.active: bool = False
        self.mouse_timestamps = mouse_timestamps
        self.keyboard_timestamps = keyboard_timestamps
        
    def on_mouse_click(self, x: int, y: int, button: Button, pressed: bool):
        # Discard release events.
        if pressed == False:
            return
        
        print("Clicked the mouse.")
        
        # Record mouse clicks.
        self.mouse_timestamps.append(datetime.datetime.now().isoformat())
        # print(self.mouse_timestamps)

    def on_keyboard_press(self, key: KeyCode):
        print("Pressed a key.")

        # Record keyboard presses.
        self.keyboard_timestamps.append(datetime.datetime.now().isoformat())

    def start(self):
        self._mouse_listener = mouse.Listener(
            on_click=self.on_mouse_click
        )
        self._keyboard_listener = keyboard.Listener(
            on_press=self.on_keyboard_press
        )
        self._mouse_listener.start()
        self._keyboard_listener.start()

    def stop(self):
        self._mouse_listener.stop()
        self._keyboard_listener.stop()