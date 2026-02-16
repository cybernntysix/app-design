# Outreach Writer Screen
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class OutreachWriterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=24, spacing=12)
        self.editor = TextInput(hint_text='Draft your outreach message here...', size_hint=(1, 1))
        btn_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=44, spacing=8)
        btn_row.add_widget(Button(text='Copy'))
        btn_row.add_widget(Button(text='Save to Notepad'))
        layout.add_widget(self.editor)
        layout.add_widget(btn_row)
        self.add_widget(layout)
