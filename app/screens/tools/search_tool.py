# Search Tool Screen
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

class SearchToolScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=24, spacing=18)
        self.search_input = TextInput(hint_text='Search artists, songs, or contacts...', size_hint_y=None, height=44, multiline=False)
        layout.add_widget(self.search_input)
        self.tabs = TabbedPanel(do_default_tab=False, tab_height=36)
        for name in ['Artists', 'Songs', 'Business Contacts']:
            tab = TabbedPanelItem(text=name)
            tab.content = ScrollView()
            tab.content.add_widget(Label(text=f'No results yet for {name}.', color=(0.7,0.7,1,1)))
            self.tabs.add_widget(tab)
        layout.add_widget(self.tabs)
        self.add_widget(layout)
