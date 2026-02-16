# Song detail and data entry screen
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class SongDetailScreen(Screen):
    """
    SongDetailScreen lets users view and edit detailed info for each song, including:
    - Streams and revenue per platform
    - Royalty splits (publishing, mechanical, other)
    - Actionable insights (e.g., "Register this song for more royalties")
    - Export data for accounting/tax purposes
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=24)
        # Back button
        back_btn = Button(text='< Back', size_hint=(None, None), size=(100, 40), background_color=(0.5,0,1,1), color=(1,1,1,1))
        back_btn.bind(on_release=self.go_back)
        layout.add_widget(back_btn)
        # Song title and summary
        layout.add_widget(Label(text='Song: Dreams', font_size=26, color=(0.5,0,1,1), size_hint_y=None, height=40))
        layout.add_widget(Label(text='Top performing track. Registered on all major platforms.', font_size=16, color=(0.7,0.7,1,1), size_hint_y=None, height=28))
        # Streams and revenue per platform
        layout.add_widget(Label(text='Streams & Revenue', font_size=20, color=(0,1,1,1), size_hint_y=None, height=32))
        streams = [('YouTube', 70000, 210), ('Spotify', 60000, 180), ('SoundCloud', 20000, 40)]
        for platform, count, revenue in streams:
            layout.add_widget(Label(text=f'{platform}: {count:,} streams | ${revenue}', font_size=16, color=(1,1,1,1), size_hint_y=None, height=26))
        # Royalty splits (publishing, mechanical, other)
        layout.add_widget(Label(text='Royalty Splits', font_size=20, color=(0,1,1,1), size_hint_y=None, height=32))
        splits = [('Publishing', 'Alice (50%)', 'Bob (50%)'), ('Mechanical', 'Alice (30%)', 'Bob (70%)'), ('Other', 'Charity (100%)', '')]
        for split in splits:
            type = split[0]
            recipients = ', '.join(split[1:])
            layout.add_widget(Label(text=f'{type}: {recipients}', font_size=16, color=(1,1,1,1), size_hint_y=None, height=26))
        # Actionable insights
        layout.add_widget(Label(text='Actionable Insights', font_size=20, color=(0,1,1,1), size_hint_y=None, height=32))
        insights = ['Register this song for more royalties', 'Consider a remix for increased streams', 'Reach out to influencers for promotion']
        for insight in insights:
            layout.add_widget(Label(text=f'- {insight}', font_size=16, color=(1,1,1,1), size_hint_y=None, height=26))
        # Export data button
        export_btn = Button(text='Export Data', size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5}, background_color=(0.5,0,1,1), color=(1,1,1,1))
        layout.add_widget(export_btn)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'dashboard'