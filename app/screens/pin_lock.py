# PIN lock screen for app security
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class PinLockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Remove all logic that tries to auto-switch screens
        # This screen is now a placeholder and will not be used
