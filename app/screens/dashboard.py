# Dashboard screen for displaying metrics and navigation
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy_garden.graph import Graph, MeshLinePlot
import random
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.texture import Texture
from app.utils.ui_utils import draw_card_background, get_platform_icon, draw_glow_border
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
# Removed invalid Tooltip import
# from kivy.core.text import LabelBase
# LabelBase.register(name="RobotoBold", fn_bold="assets/fonts/Roboto-Bold.ttf")

class DashboardScreen(Screen):
    """
    DashboardScreen gives artists a real-time, enterprise-level view of their brand and business metrics.
    - Layout: All content in a single vertical ScrollView for natural scrolling.
    - Each section: Card-style, with short description, metric, and expandable area for charts/details.
    - Visually balanced, modern, and responsive.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.10, 0.08, 0.18, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            # Remove any white dash artifact by ensuring full coverage and no stray rectangles
        self.bind(pos=self._update_bg, size=self._update_bg)
        # Main vertical ScrollView for all dashboard content
        self.scrollview = ScrollView(size_hint=(1, 1), bar_width=8, scroll_type=['bars', 'content'], do_scroll_x=False, do_scroll_y=True)
        self.content_layout = GridLayout(cols=1, spacing=32, padding=[40, 30, 40, 30], size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        self.scrollview.add_widget(self.content_layout)
        self.add_widget(self.scrollview)
        # Chart section (as before)
        self.platforms = ['YouTube', 'Spotify', 'SoundCloud']
        self.song_data = {
            'YouTube': [('Dreams', 70000, 210), ('Legacy', 30000, 90), ('Violet Skies', 20000, 60)],
            'Spotify': [('Dreams', 60000, 180), ('Legacy', 25000, 75), ('Violet Skies', 10000, 30)],
            'SoundCloud': [('Dreams', 20000, 40), ('Legacy', 15000, 30), ('Violet Skies', 5000, 10)]
        }
        self.selected_platform = self.platforms[0]
        self.chart_box = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, None), height=260)
        self.platform_spinner = Spinner(
            text=self.selected_platform,
            values=self.platforms,
            size_hint=(1, None),
            height=40,
            background_color=(0.5,0,1,1),
            color=(1,1,1,1),
            font_size=18
        )
        self.platform_spinner.bind(text=self.on_platform_select)
        self.chart_box.add_widget(self.platform_spinner)
        self.graph = Graph(xlabel='Songs', ylabel='Royalties ($)', x_ticks_minor=1, x_ticks_major=1, y_ticks_major=50,
                           y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                           xmin=0, xmax=3, ymin=0, ymax=250, background_color=(0.15,0.12,0.25,1), border_color=(0.5,0,1,1),
                           size_hint=(1, None), height=200)
        self.plot = MeshLinePlot(color=[0, 1, 1, 1])
        self.graph.add_plot(self.plot)
        self.chart_box.add_widget(self.graph)
        # Demo gradient texture for cards
        self.card_gradient = self._create_gradient_texture()

    def _create_gradient_texture(self):
        # Simple vertical gradient (cyan to purple)
        tex = Texture.create(size=(1, 64), colorfmt='rgba')
        buf = b''
        for i in range(64):
            r = int(80 + 120 * (i/63))
            g = int(200 - 120 * (i/63))
            b = int(255)
            a = 255
            buf += bytes([r, g, b, a])
        tex.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        tex.wrap = 'repeat'
        tex.uvsize = (1, -1)
        return tex

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self):
        self.content_layout.clear_widgets()
        self.content_layout.height = 0
        artist_name = self.manager.get_screen('onboarding').artist_name
        # Export and Connect buttons row
        btn_row = BoxLayout(orientation='horizontal', spacing=18, size_hint=(1, None), height=48)
        export_btn = Button(text='Export Data', size_hint=(None, None), size=(160, 44), background_color=(0,1,1,0.8), color=(0.1,0.1,0.2,1), font_size=16, bold=True)
        export_btn.bind(on_release=self._on_export)
        connect_btn = Button(text='Connect Platform', size_hint=(None, None), size=(180, 44), background_color=(0.5,0,1,0.5), color=(1,1,1,0.7), font_size=16, bold=True, disabled=True)
        connect_btn.bind(on_release=self._show_connect_popup)
        btn_row.add_widget(export_btn)
        btn_row.add_widget(connect_btn)
        self.content_layout.add_widget(btn_row)
        # Search bar for songs
        search_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=44, padding=[0,0,0,0])
        self.song_search = TextInput(hint_text='Search songs...', size_hint=(1, None), height=44, multiline=False)
        self.song_search.bind(text=self.on_song_search)
        search_row.add_widget(self.song_search)
        self.content_layout.add_widget(search_row)
        # Metrics in GridLayout
        metrics_grid = GridLayout(cols=2, spacing=18, size_hint=(1, None), height=260)
        metrics = [
            {"title": "Total Revenue", "desc": "Estimated total royalties from all platforms.", "accent": (0,1,1,1), "details": [("Publishing", "$700"), ("Mechanical", "$400"), ("Other", "$150")], "icon": None},
            {"title": "Top-Earning Songs", "desc": "Your highest earning tracks this year.", "accent": (0.5,0,1,1), "details": [("Dreams", "$500"), ("Legacy", "$300"), ("Violet Skies", "$200")], "icon": None},
            {"title": "Top Platforms", "desc": "Where your music earns the most.", "accent": (1,0,1,1), "details": [("YouTube", "$600"), ("Spotify", "$400"), ("SoundCloud", "$250")], "icon": None},
            {"title": "Opportunities", "desc": "Register 'Violet Skies' and 'Street Spirit' for more royalties.", "accent": (0.7,0.2,1,1), "details": None, "icon": None}
        ]
        for m in metrics:
            card = self._metric_card(title=m["title"], value=self._get_metric_value(m["title"]), desc=m["desc"], accent=m["accent"], details=m["details"], icon=m["icon"])
            # Make Top-Earning Songs card clickable
            if m["title"] == "Top-Earning Songs":
                card.bind(on_touch_down=self._on_song_card_touch)
            # Add info/help icon with popup
            help_icon = Button(text='?', size_hint=(None, None), size=(24,24), background_color=(0,0,0,0.2), color=(0,1,1,1), font_size=16)
            help_icon.bind(on_release=lambda inst, desc=m["desc"]: self._show_info_popup(desc))
            card.add_widget(help_icon)
            metrics_grid.add_widget(card)
        self.content_layout.add_widget(metrics_grid)
        # Chart section
        self.content_layout.add_widget(self.chart_box)
        self.update_chart()
        # Artist summary card
        summary_card = BoxLayout(orientation='vertical', padding=18, spacing=8, size_hint=(1, None), height=120)
        summary_card.add_widget(Label(text=f"[b]{artist_name}[/b]", font_size=18, markup=True, color=(1,1,1,1), size_hint_y=None, height=32, halign='left', valign='top'))
        summary_card.add_widget(Label(text="Rising star, visionary sound.", font_size=14, color=(0.7,0.7,1,1), size_hint_y=None, height=22, halign='left', valign='top'))
        summary_card.add_widget(Label(text="[b]Awards:[/b] Platinum x2, Gold x1", font_size=13, markup=True, color=(0.5,0,1,1), size_hint_y=None, height=20, halign='left', valign='middle'))
        self.content_layout.add_widget(summary_card)
        # News Feed
        self.content_layout.add_widget(Label(text="[b]Music News Feed[/b]", font_size=18, markup=True, color=(0,1,1,1), size_hint_y=None, height=30, halign='left', valign='middle'))
        news = [
            ("Genius", "Top 10 Lyrics of the Week"),
            ("Lyrical Lemonade", "New Visuals: Rising Artists to Watch"),
            ("Rolling Stone", "Indie Artists Breaking Out in 2025"),
            ("Billboard", "Streaming Trends: Hip Hop & Beyond")
        ]
        for source, headline in news:
            self.content_layout.add_widget(Label(text=f"{source}: {headline}", font_size=14, color=(1,1,1,1), size_hint_y=None, height=24, halign='left', valign='middle'))
        # Set layout height to fit all widgets
        self.content_layout.height = self.content_layout.minimum_height

    def _get_metric_value(self, title):
        if title == "Total Revenue":
            # Calculate from all platforms
            total = 0
            for platform in self.song_data.values():
                for song in platform:
                    total += song[2]
            return f"${total:,}"
        if title == "Top-Earning Songs":
            return "Dreams ($500)"
        if title == "Top Platforms":
            return "YouTube ($600)"
        if title == "Opportunities":
            return "Register 2 songs"
        return "-"

    def on_platform_select(self, spinner, value):
        self.selected_platform = value
        self.update_chart()

    def on_song_search(self, instance, value):
        # Filter song cards and chart by search
        pass

    def _show_export_popup(self, instance):
        content = FloatLayout()
        msg = Label(text='[b]Export Demo[/b]\nYour data is private and never leaves your device.\n(Export to CSV/JSON coming soon!)', markup=True, color=(0,1,1,1), size_hint=(1, None), height=120, pos_hint={'center_x':0.5, 'center_y':0.6})
        content.add_widget(msg)
        close_btn = Button(text='Close', size_hint=(None, None), size=(120, 40), pos_hint={'center_x':0.5, 'y':0.05})
        popup = Popup(title='Export Data', content=content, size_hint=(None, None), size=(380, 220), auto_dismiss=False)
        close_btn.bind(on_release=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()

    def _show_connect_popup(self, instance):
        content = FloatLayout()
        msg = Label(text='[b]Connect Platform[/b]\nAPI integration coming soon!\nYour credentials will always be private.', markup=True, color=(1,0.5,1,1), size_hint=(1, None), height=100, pos_hint={'center_x':0.5, 'center_y':0.6})
        content.add_widget(msg)
        close_btn = Button(text='Close', size_hint=(None, None), size=(120, 40), pos_hint={'center_x':0.5, 'y':0.05})
        popup = Popup(title='Connect Platform', content=content, size_hint=(None, None), size=(380, 200), auto_dismiss=False)
        close_btn.bind(on_release=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()

    def _show_info_popup(self, desc):
        popup = Popup(title='Info', content=Label(text=desc, color=(0,1,1,1), font_size=16), size_hint=(None, None), size=(340, 160))
        popup.open()

    def update_chart(self):
        data = sorted(self.song_data[self.selected_platform], key=lambda x: x[1], reverse=True)
        royalties = [d[2] for d in data]
        self.plot.points = [(i+1, royalties[i]) for i in range(len(royalties))]
        self.graph.xmax = len(royalties) + 1
        self.graph.xmin = 0
        self.graph.ymax = max(royalties) + 50
        self.graph.ymin = 0
        self.graph.xlabel = 'Songs (descending streams)'
        self.graph.ylabel = 'Royalties ($)'

    def _metric_card(self, title, value, desc, accent, details=None, icon=None):
        card = BoxLayout(orientation='vertical', padding=18, spacing=10, size_hint=(1, None), height=120)
        draw_card_background(card, color=(0.15, 0.12, 0.25, 0.95), radius=22, gradient=self.card_gradient, shadow=True)
        title_row = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=32)
        if icon:
            title_row.add_widget(get_platform_icon(icon))
        title_lbl = Label(text=title, font_size=20, color=accent, size_hint_y=None, height=32)
        title_row.add_widget(title_lbl)
        card.add_widget(title_row)
        value_lbl = Label(text=value, font_size=28, color=(1,1,1,1), size_hint_y=None, height=38)
        desc_lbl = Label(text=desc, font_size=14, color=(0.7,0.7,1,1), size_hint_y=None, height=22)
        card.add_widget(value_lbl)
        card.add_widget(desc_lbl)
        if details:
            for d in details:
                detail_row = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=22)
                if d[0] in ['YouTube', 'Spotify', 'SoundCloud', 'Apple']:
                    detail_row.add_widget(get_platform_icon(d[0]))
                detail_row.add_widget(Label(text=f"{d[0]}: {d[1]}", font_size=15, color=(0.8,0.8,1,1)))
                card.add_widget(detail_row)
        return card

    def _update_card_bg(self, instance, *args):
        for instr in instance.canvas.before.children:
            if isinstance(instr, Rectangle):
                instr.pos = instance.pos
                instr.size = instance.size

    def _on_export(self, instance):
        # Warn if no songs
        has_songs = any(self.song_data[platform] for platform in self.song_data)
        if not has_songs:
            popup = Popup(title='Export Error', content=Label(text='No songs to export!', color=(1,0,0,1), font_size=16), size_hint=(None, None), size=(340, 160))
            popup.open()
        else:
            self._show_export_popup(instance)

    def _on_song_card_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # Open song detail screen (demo: just switch to song_detail)
            self.manager.current = 'song_detail'
            return True
        return False
