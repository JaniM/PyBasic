
import sdl2
import sdl2.ext
import pybasic.sprite as sp

__all__ = ['add_font', 'text']

_manager = None

def add_font(font, alias=None):
    global _manager
    if _manager is None:
        _manager = sdl2.ext.FontManager(font, alias)
    else:
        _manager.add(font, alias)

def text(text, alias=None, size=None, width=None, color=None, bg_color=None, position=(0, 0)):
    surface = _manager.render(text, alias, size, width, color, bg_color)
    sprite = sp._factory.from_surface(surface)
    if sp.GlRenderer:
        sdl2.SDL_FreeSurface(surface)
    sprite.position = position
    return sp.SpriteProxy(sprite)
