
import collections
import sdl2, sdl2.ext
import pybasic.window
from pybasic.proxy import Proxy

__all__ = ['use_software_renderer', 'use_texture_renderer', 'rectangle', 'render']

GlRenderer = None
_factory = None
_renderer = None
_renderQueue = []

class SpriteProxy(Proxy):
    def __del__(self):
        if hasattr(self, 'surface'):
            sdl2.SDL_FreeSurface(self.surface)
        else:
            sdl2.SDL_DestroyTexture(self.texture)

def define_renderer(renderer):
    global _factory
    global _renderer
    global GlRenderer
    rend = None
    if renderer == sdl2.ext.TEXTURE:
        rend = GlRenderer = sdl2.ext.Renderer(pybasic.window.get_window())
    _factory = sdl2.ext.SpriteFactory(renderer, renderer=rend)
    _renderer = _factory.create_sprite_render_system(pybasic.window.get_window())

def use_software_renderer():
    define_renderer(sdl2.ext.SOFTWARE)

def use_texture_renderer():
    define_renderer(sdl2.ext.TEXTURE)

def rectangle(color, size, position=(0, 0), factory=sdl2.ext.SOFTWARE):
    if isinstance(color, collections.Sequence):
        color = sdl2.ext.Color(*color)
    rect = _factory.from_color(color, size)
    rect.position = position
    return SpriteProxy(rect)

def render(sprite):
    if isinstance(sprite, collections.Sequence):
        for x in sprite:
            render(x)
        return
    try:
        sprite.render()
    except AttributeError:
        _renderQueue.append(sprite)

def render_all_sprites():
    _renderer.render(_renderQueue)
    _renderQueue.clear()

