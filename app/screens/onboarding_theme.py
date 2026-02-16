# Onboarding theme and final setup screen
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

class OnboardingThemeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=28)
        layout.add_widget(Label(text='Theme: Futuristic Violet (Dark Mode)', font_size=22, color=(0.5,0,1,1)))
        # Add more theme or onboarding options here if needed
        self.continue_btn = Button(text='Continue', size_hint=(1, 0.2), background_color=(0.5,0,1,1), color=(1,1,1,1), font_size=18)
        self.continue_btn.bind(on_release=self.go_to_dashboard)
        layout.add_widget(self.continue_btn)
        self.add_widget(layout)
        Window.bind(on_key_down=self._on_key_down)

    def go_to_dashboard(self, instance):
        self.manager.current = 'dashboard'

    def _on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 13:  # Enter
            if not self.continue_btn.disabled:
                self.go_to_dashboard(self.continue_btn)
