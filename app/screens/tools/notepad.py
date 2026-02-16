# Notepad Screen
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.text import LabelBase
import os

# Removed custom font registration. Using default Roboto (Roboto-Regular.ttf) for all widgets.

class NotepadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.10, 0.08, 0.18, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.notes = []
        self.layout = BoxLayout(orientation='vertical', padding=24, spacing=16)
        # Card background for notes area
        notes_card = BoxLayout(orientation='vertical', padding=18, spacing=10, size_hint=(1, 1))
        with notes_card.canvas.before:
            Color(0.16, 0.14, 0.22, 0.98)
            notes_card.bg = RoundedRectangle(radius=[24], pos=notes_card.pos, size=notes_card.size)
        notes_card.bind(pos=lambda inst, val: setattr(notes_card.bg, 'pos', val), size=lambda inst, val: setattr(notes_card.bg, 'size', val))
        self.notes_area = ScrollView(size_hint=(1, 1))
        self.notes_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=(0,8))
        self.notes_list.bind(minimum_height=self.notes_list.setter('height'))
        self.notes_area.add_widget(self.notes_list)
        notes_card.add_widget(self.notes_area)
        self.layout.add_widget(notes_card)
        # Add Note button with accent style
        self.add_btn = Button(text='Add Note', size_hint_y=None, height=48, font_name='Roboto-Bold', font_size=18, background_color=(0.22,0.5,1,1), color=(1,1,1,1), bold=True)
        self.add_btn.bind(on_release=self.add_note)
        self.layout.add_widget(self.add_btn)
        self.default_msg = Label(text='No notes yet. Tap "Add Note" to create one!', color=(0.7,0.7,1,1), font_size=16, font_name='Roboto-Bold', size_hint_y=None, height=32)
        self.add_widget(self.layout)
        self.refresh_notes()

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def refresh_notes(self):
        self.notes_list.clear_widgets()
        if not self.notes:
            if self.default_msg.parent is None:
                self.layout.add_widget(self.default_msg)
        else:
            if self.default_msg.parent:
                self.layout.remove_widget(self.default_msg)
            for idx, note in enumerate(self.notes):
                note_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=44, spacing=10)
                # Card for each note
                note_card = BoxLayout(orientation='horizontal', size_hint=(1,1), padding=[14,6,14,6])
                with note_card.canvas.before:
                    Color(0.18, 0.16, 0.28, 0.98)
                    note_card.bg = RoundedRectangle(radius=[14], pos=note_card.pos, size=note_card.size)
                note_card.bind(pos=lambda inst, val: setattr(note_card.bg, 'pos', val), size=lambda inst, val: setattr(note_card.bg, 'size', val))
                note_lbl = Label(text=note, color=(1,1,1,1), font_size=16, font_name='Roboto-Bold', size_hint_x=0.7, halign='left', valign='middle')
                note_lbl.bind(size=note_lbl.setter('text_size'))
                edit_btn = Button(text='Edit', size_hint_x=0.15, size_hint_y=None, height=32, font_name='Roboto-Bold', font_size=15, background_color=(0.22,0.5,1,1), color=(1,1,1,1))
                delete_btn = Button(text='Delete', size_hint_x=0.15, size_hint_y=None, height=32, font_name='Roboto-Bold', font_size=15, background_color=(0.8,0.2,0.2,1), color=(1,1,1,1))
                edit_btn.bind(on_release=lambda inst, i=idx: self.edit_note(i))
                delete_btn.bind(on_release=lambda inst, i=idx: self.delete_note(i))
                note_card.add_widget(note_lbl)
                note_card.add_widget(edit_btn)
                note_card.add_widget(delete_btn)
                note_row.add_widget(note_card)
                self.notes_list.add_widget(note_row)
        self.notes_list.height = max(44 * len(self.notes), 44)

    def add_note(self, instance):
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        popup_layout = BoxLayout(orientation='vertical', padding=12, spacing=8)
        note_input = TextInput(hint_text='Enter your note...', multiline=True, size_hint_y=None, height=80)
        save_btn = Button(text='Save', size_hint_y=None, height=40)
        popup_layout.add_widget(note_input)
        popup_layout.add_widget(save_btn)
        popup = Popup(title='Add Note', content=popup_layout, size_hint=(None, None), size=(340, 200))
        save_btn.bind(on_release=lambda inst: self.save_new_note(note_input.text, popup))
        popup.open()

    def save_new_note(self, text, popup):
        if text.strip():
            self.notes.append(text.strip())
            self.refresh_notes()
        popup.dismiss()

    def edit_note(self, idx):
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        popup_layout = BoxLayout(orientation='vertical', padding=12, spacing=8)
        note_input = TextInput(text=self.notes[idx], multiline=True, size_hint_y=None, height=80)
        save_btn = Button(text='Save', size_hint_y=None, height=40)
        popup_layout.add_widget(note_input)
        popup_layout.add_widget(save_btn)
        popup = Popup(title='Edit Note', content=popup_layout, size_hint=(None, None), size=(340, 200))
        save_btn.bind(on_release=lambda inst: self.save_edited_note(idx, note_input.text, popup))
        popup.open()

    def save_edited_note(self, idx, text, popup):
        if text.strip():
            self.notes[idx] = text.strip()
            self.refresh_notes()
        popup.dismiss()

    def delete_note(self, idx):
        del self.notes[idx]
        self.refresh_notes()
