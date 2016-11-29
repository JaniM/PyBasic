
import sdl2
import sdl2.ext

__all__ = []

DRAW_CONTEXT = None

class DrawContext:
    def __init__(self, surface):
        self.old_surface = None
        self.surface = surface
    
    def __enter__(self):
        global DRAW_CONTEXT
        self.old_surface = DRAW_CONTEXT
        DRAW_CONTEXT = self.surface
    
    def __exit__(self, *args):
        global DRAW_CONTEXT
        DRAW_CONTEXT = self.old_surface
        self.old_surface = None

def context(surface=None):
    if surface is None:
        return DrawContext(DRAW_CONTEXT)
    return DrawContext(surface)

def surface(size, alpha=False):
    if alpha:
        masks = (0xff000000,0x00ff0000,0x0000ff00,0x000000ff)
    else:
        masks = (0,0,0,0)
    s = sdl2.SDL_CreateRGBSurface(0,size[0],size[1],32,*masks);
    return s

def rectangle(color, size, position=(0, 0), alpha=False):
    color = sdl2.ext.convert_to_color(color)
    s = DRAW_CONTEXT
    if alpha:
        color = sdl2.SDL_MapRGBA(s.contents.format.contents, color.r, color.g, color.b, color.a)
    else:
        color = sdl2.SDL_MapRGB(s.contents.format.contents, color.r, color.g, color.b)
    if size is None:
        sdl2.SDL_FillRect(s, None, color)
    else:
        r = sdl2.SDL_Rect(*position, *size)
        sdl2.SDL_FillRect(s, r, color)
