
import sdl2, sdl2.ext
import pybasic.sprite as sp
import pybasic.draw as draw

__all__ = ['create_window', 'refresh_window', 'get_window']

_window = None

def create_window(title, size, position=None, flags=None):
    global _window
    _window = sdl2.ext.Window(title, size, position, flags)
    _window.show()
    
def refresh_window(clear=True, cls_color=(0, 0, 0)):
    if clear:
        if sp.GlRenderer:
            sp.GlRenderer.clear(cls_color)
        else:
            sdl2.ext.fill(sp._renderer.surface, cls_color)
    sp.render_all_sprites()
    _window.refresh()

def get_window():
    return _window