# Chatbot/Copilot Screen
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Rectangle
import os

class ChatbotScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.10, 0.08, 0.18, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        layout = BoxLayout(orientation='vertical', padding=24, spacing=16)
        # Card background for chat area
        chat_card = BoxLayout(orientation='vertical', padding=18, spacing=10, size_hint=(1, 1))
        with chat_card.canvas.before:
            Color(0.16, 0.14, 0.22, 0.98)
            chat_card.bg = RoundedRectangle(radius=[24], pos=chat_card.pos, size=chat_card.size)
        chat_card.bind(pos=lambda inst, val: setattr(chat_card.bg, 'pos', val), size=lambda inst, val: setattr(chat_card.bg, 'size', val))
        self.chat_area = ScrollView(size_hint=(1, 1))
        self.chat_log = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=(0,8))
        self.chat_log.bind(minimum_height=self.chat_log.setter('height'))
        self.chat_area.add_widget(self.chat_log)
        chat_card.add_widget(self.chat_area)
        layout.add_widget(chat_card)
        # Input row with card background
        input_card = BoxLayout(orientation='horizontal', size_hint_y=None, height=54, spacing=10, padding=[16,8,16,8])
        with input_card.canvas.before:
            Color(0.18, 0.16, 0.28, 1)
            input_card.bg = RoundedRectangle(radius=[18], pos=input_card.pos, size=input_card.size)
        input_card.bind(pos=lambda inst, val: setattr(input_card.bg, 'pos', val), size=lambda inst, val: setattr(input_card.bg, 'size', val))
        self.input_box = TextInput(hint_text='Ask a business question or draft outreach...', multiline=False, font_name='Roboto-Bold', font_size=17, background_color=(0,0,0,0), foreground_color=(1,1,1,1), padding=[12,10,12,10], cursor_color=(0.5,0.8,1,1))
        # Modern send icon (fallback to text if icon missing)
        icon_path = os.path.join('assets', 'icons', 'send.png')
        if os.path.exists(icon_path):
            self.send_btn = Button(size_hint_x=None, width=54, background_normal=icon_path, background_down=icon_path, background_color=(0,0,0,0))
        else:
            self.send_btn = Button(text='Send', size_hint_x=None, width=80, background_color=(0.22,0.5,1,1), color=(1,1,1,1), font_name='Roboto', font_size=16)
        input_card.add_widget(self.input_box)
        input_card.add_widget(self.send_btn)
        layout.add_widget(input_card)
        self.add_widget(layout)
        self.send_btn.bind(on_release=self.on_send)
        self.input_box.bind(on_text_validate=self.on_send)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_send(self, instance):
        msg = self.input_box.text.strip()
        if msg:
            self.add_message(msg, sender='user')
            # Demo bot response
            self.add_message("[b]Bot:[/b] This is a demo response. (Your message was: '{}')".format(msg), sender='bot')
            self.input_box.text = ''

    def add_message(self, text, sender='user'):
        # Modern message bubble style
        from kivy.uix.boxlayout import BoxLayout
        bubble = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, padding=[0,0,0,0], spacing=0)
        if sender == 'user':
            bg_color = (0.22, 0.5, 1, 0.95)
            align = 'right'
            txt_color = (1,1,1,1)
        else:
            bg_color = (0.18, 0.16, 0.28, 0.98)
            align = 'left'
            txt_color = (0.7,1,1,1)
        msg_card = BoxLayout(size_hint_x=0.85, size_hint_y=None, height=36, padding=[14,6,14,6])
        with msg_card.canvas.before:
            Color(*bg_color)
            msg_card.bg = RoundedRectangle(radius=[16], pos=msg_card.pos, size=msg_card.size)
        msg_card.bind(pos=lambda inst, val: setattr(msg_card.bg, 'pos', val), size=lambda inst, val: setattr(msg_card.bg, 'size', val))
        lbl = Label(text=text, color=txt_color, font_size=16, font_name='Roboto-Bold', size_hint_y=None, height=24, halign=align, valign='middle', markup=(sender=='bot'))
        lbl.bind(size=lbl.setter('text_size'))
        msg_card.add_widget(lbl)
        if sender == 'user':
            bubble.add_widget(BoxLayout())
            bubble.add_widget(msg_card)
        else:
            bubble.add_widget(msg_card)
            bubble.add_widget(BoxLayout())
        self.chat_log.add_widget(bubble)
