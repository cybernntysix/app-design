# Icon and color utilities for a modern, vibrant dashboard
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

def get_platform_icon(platform):
    icons = {
        'YouTube': 'assets/icons/youtube.png',
        'Spotify': 'assets/icons/spotify.png',
        'SoundCloud': 'assets/icons/soundcloud.png',
        'Apple': 'assets/icons/apple.png',
        'Billboard': 'assets/icons/billboard.png',
        'Genius': 'assets/icons/genius.png',
        'Lyrical Lemonade': 'assets/icons/lyrical_lemonade.png',
        'Rolling Stone': 'assets/icons/rollingstone.png',
    }
    path = icons.get(platform, None)
    if path:
        return Image(source=path, size_hint=(None, None), size=(24, 24))
    return Widget(size_hint=(None, None), size=(24, 24))

def draw_card_background(widget, color, radius=18, gradient=None, shadow=True):
    # Remove previous canvas instructions if any
    widget.canvas.before.clear()
    with widget.canvas.before:
        if shadow:
            Color(0, 0, 0, 0.18)
            shadow_rect = RoundedRectangle(pos=(widget.x-6, widget.y-6), size=(widget.width+12, widget.height+12), radius=[radius+4])
        if gradient:
            from kivy.graphics import Rectangle
            Color(1,1,1,1)
            Rectangle(texture=gradient, pos=widget.pos, size=widget.size)
        else:
            Color(*color)
            bg = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[radius])
    def update_bg(instance, value):
        if shadow:
            shadow_rect.pos = (widget.x-6, widget.y-6)
            shadow_rect.size = (widget.width+12, widget.height+12)
        if gradient:
            # Gradient rectangle
            pass
        else:
            bg.pos = widget.pos
            bg.size = widget.size
    widget.bind(pos=update_bg, size=update_bg)

def draw_glow_border(widget, color=(0,1,1,0.5), width=3, radius=18):
    from kivy.graphics import Color, Line
    with widget.canvas.after:
        Color(*color)
        border = Line(rectangle=(widget.x, widget.y, widget.width, widget.height), width=width, rounded_rectangle=[radius])
    def update_border(instance, value):
        border.rectangle = (widget.x, widget.y, widget.width, widget.height)
    widget.bind(pos=update_border, size=update_border)
