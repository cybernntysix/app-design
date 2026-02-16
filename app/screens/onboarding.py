# Onboarding screen for user role, goal, PIN, and theme selection
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
Window.clearcolor = (0.10, 0.08, 0.18, 1)  # Set window background to match dark theme
from app.utils.ui_utils import draw_card_background
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget
import os

# Removed custom font registration. Using default Roboto (Roboto-Regular.ttf) for all widgets.

class OnboardingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_role = None
        self.artist_name = ''
        layout = BoxLayout(orientation='vertical', padding=[0,80,0,0], spacing=36)
        # Centered card
        card = BoxLayout(orientation='vertical', padding=36, spacing=28, size_hint=(None, None), size=(480, 420), pos_hint={'center_x':0.5, 'center_y':0.5})
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            # Card background: Deep Charcoal (Rosé Pine/Tokyo Night inspired)
            Color(35/255, 33/255, 54/255, 0.98)
            self.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[32])
        card.bind(pos=self._update_card_bg, size=self._update_card_bg)
        card.add_widget(Label(text='Who are you?', font_size=32, color=(230/255, 222/255, 244/255, 1), bold=True, size_hint_y=None, height=48))
        roles = ['Producer', 'Artist', 'Manager']
        self.role_buttons = []
        role_box = BoxLayout(orientation='horizontal', spacing=18, size_hint=(1, None), height=56)
        for role in roles:
            btn = ToggleButton(text=role, group='role', size_hint=(1, 1), font_size=20, background_color=(233/255, 193/255, 119/255, 0.18), color=(230/255, 222/255, 244/255, 1), border=(0,0,0,0))
            btn.bind(on_press=self.on_role_select)
            self.role_buttons.append(btn)
            role_box.add_widget(btn)
        card.add_widget(role_box)
        card.add_widget(Label(text='Artist or Stage Name', font_size=18, color=(196/255, 167/255, 231/255, 1), bold=True, size_hint_y=None, height=32))
        self.name_input = TextInput(hint_text='Enter your name...', multiline=False, size_hint=(1, None), height=48, font_size=20, background_color=(41/255, 39/255, 63/255, 1), foreground_color=(230/255, 222/255, 244/255, 1), padding=[16,12,16,12])
        self.name_input.bind(text=self.on_name_input)
        card.add_widget(self.name_input)
        self.continue_btn = Button(text='Continue', size_hint=(1, None), height=54, background_color=(233/255, 146/255, 135/255, 1), color=(35/255, 33/255, 54/255, 1), font_size=20, bold=True, border=(0,0,0,0), background_normal='')
        self.continue_btn.bind(on_release=self.go_to_theme)
        card.add_widget(self.continue_btn)
        layout.add_widget(card)
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.10, 0.08, 0.18, 1)
            self.bg_rect2 = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.add_widget(layout)
        self.size_hint = (1, 1)

    def _update_bg(self, *args):
        self.bg_rect2.pos = self.pos
        self.bg_rect2.size = self.size

    def _update_card_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_role_select(self, instance):
        self.selected_role = instance.text
        self.update_continue_state()
        for btn in self.role_buttons:
            btn.background_color = (0.5, 0, 1, 1) if btn.state == 'down' else (1, 1, 1, 1)

    def on_name_input(self, instance, value):
        self.artist_name = value
        self.update_continue_state()

    def update_continue_state(self):
        self.continue_btn.disabled = not (self.selected_role and self.artist_name.strip())

    def go_to_theme(self, instance):
        self.manager.current = 'onboarding_theme'

    def _on_key_down(self, window, key, scancode, codepoint, modifier):
        if key in (13, 271) and not self.continue_btn.disabled:  # Enter or Numpad Enter
            self.go_to_theme(None)

    def _update_divider(self, instance, value):
        self.divider_rect.pos = instance.pos
        self.divider_rect.size = (instance.size[0], 2)

class OnboardingGoalScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[0,80,0,0], spacing=36)
        # Centered card
        card = BoxLayout(orientation='vertical', padding=36, spacing=28, size_hint=(None, None), size=(480, 420), pos_hint={'center_x':0.5, 'center_y':0.5})
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            # Card background: Deep Charcoal (Rosé Pine/Tokyo Night inspired)
            Color(35/255, 33/255, 54/255, 0.98)
            self.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[32])
        card.bind(pos=self._update_card_bg, size=self._update_card_bg)
        card.add_widget(Label(text='Welcome!', font_size=32, color=(1,1,1,1), bold=True))
        card.add_widget(Label(text='Let’s get to know you', font_size=20, color=(1,1,1,1), bold=True))
        self.role_input = TextInput(hint_text='Artist, Producer, etc.', multiline=False, size_hint=(1, None), height=48, font_size=20, background_color=(41/255, 39/255, 63/255, 1), foreground_color=(230/255, 222/255, 244/255, 1), padding=[16,12,16,12])
        card.add_widget(self.role_input)
        self.name_input = TextInput(hint_text='Enter your name...', multiline=False, size_hint=(1, None), height=48, font_size=20, background_color=(41/255, 39/255, 63/255, 1), foreground_color=(230/255, 222/255, 244/255, 1), padding=[16,12,16,12])
        card.add_widget(self.name_input)
        continue_btn = Button(text='Continue', size_hint=(1, None), height=48, font_size=20, background_color=(233/255, 146/255, 135/255, 1), color=(35/255, 33/255, 54/255, 1), bold=True)
        card.add_widget(continue_btn)
        layout.add_widget(card)
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.10, 0.08, 0.18, 1)
            self.bg_rect2 = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.add_widget(layout)
