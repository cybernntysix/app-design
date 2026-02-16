# Main entry point for the Kivy app
from kivy.app import App
import kivy.resources as resources
resources.resource_add_path('app/assets')
from kivy.uix.screenmanager import ScreenManager
from app.screens.onboarding import OnboardingScreen
from app.screens.onboarding_theme import OnboardingThemeScreen
from app.screens.dashboard import DashboardScreen
from app.screens.song_detail import SongDetailScreen
from app.screens.pin_lock import PinLockScreen
from app.screens.tools.search_tool import SearchToolScreen
from app.screens.tools.chatbot import ChatbotScreen
from app.screens.tools.outreach_writer import OutreachWriterScreen
from app.screens.tools.notepad import NotepadScreen
from app.utils.bottom_nav import BottomNavBar

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PinLockScreen(name='pin_lock'))
        sm.add_widget(OnboardingScreen(name='onboarding'))
        sm.add_widget(OnboardingThemeScreen(name='onboarding_theme'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(SongDetailScreen(name='song_detail'))
        sm.add_widget(SearchToolScreen(name='search_tool'))
        sm.add_widget(ChatbotScreen(name='chatbot'))
        sm.add_widget(OutreachWriterScreen(name='outreach_writer'))
        sm.add_widget(NotepadScreen(name='notepad'))
        sm.current = 'onboarding'  # Start at onboarding, skipping PIN
        # Root layout with ScreenManager and BottomNavBar
        from kivy.uix.boxlayout import BoxLayout
        root = BoxLayout(orientation='vertical')
        root.add_widget(sm)
        root.add_widget(BottomNavBar(sm))
        return root

if __name__ == '__main__':
    MainApp().run()
