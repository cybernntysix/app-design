# Bottom navigation bar for main tools
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.image import Image as CoreImage
import os

class NavItem(BoxLayout):
    def __init__(self, icon, label, screen, screen_manager, **kwargs):
        super().__init__(orientation='vertical', spacing=2, padding=[0,6,0,0], size_hint=(1,1), **kwargs)
        icon_path = icon
        icon_widget = None
        if os.path.exists(icon_path):
            try:
                # Try to load the image
                icon_widget = Image(source=icon_path, size_hint=(1, 0.65), allow_stretch=True, keep_ratio=True)
            except Exception:
                icon_widget = None
        if not icon_widget:
            # Fallback: colored box with initial
            fallback = BoxLayout(size_hint=(1,0.65), padding=0)
            with fallback.canvas:
                Color(0.2,0.2,0.4,1)
                rect = Rectangle(pos=fallback.pos, size=fallback.size)
            def update_rect(instance, value):
                rect.pos = fallback.pos
                rect.size = fallback.size
            fallback.bind(pos=update_rect, size=update_rect)
            fallback.add_widget(Label(text=label[0], color=(1,1,1,1), font_size=22, bold=True))
            icon_widget = fallback
        self.text_label = Label(text=label, size_hint=(1, 0.35), color=(0.7,0.7,1,1), font_size=13, halign='center', valign='middle')
        self.text_label.bind(size=self.text_label.setter('text_size'))
        self.add_widget(icon_widget)
        self.add_widget(self.text_label)
        self.screen = screen
        self.sm = screen_manager
        self.bind(on_touch_down=self.on_touch_down)
    def on_touch_down(self, touch, *args):
        if self.collide_point(*touch.pos) and not any(child.collide_point(*touch.pos) for child in self.children):
            self.sm.current = self.screen
            return True
        return super().on_touch_down(touch)

class BottomNavBar(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=64, spacing=0, padding=[0,0,0,0], **kwargs)
        with self.canvas.before:
            # Set background to match app dark theme
            Color(0.10, 0.08, 0.18, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            # Subtle top border
            # Color(0.2, 0.2, 0.4, 0.18)
            # self.top_border = Rectangle(pos=(self.x, self.top-2), size=(self.width, 2))
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.sm = screen_manager
        self.buttons = [
            ('assets/icons/dashboard.png', 'Dashboard', 'dashboard'),
            ('assets/icons/search.png', 'Search', 'search_tool'),
            ('assets/icons/chat.png', 'Chat', 'chatbot'),
            ('assets/icons/email.png', 'Outreach', 'outreach_writer'),
            ('assets/icons/notepad.png', 'Notepad', 'notepad'),
        ]
        for icon, label, screen in self.buttons:
            nav_item = NavItem(icon, label, screen, self.sm)
            self.add_widget(nav_item)
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        # self.top_border.pos = (self.x, self.top-2)
        # self.top_border.size = (self.width, 2)
