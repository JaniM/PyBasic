
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

class TextureSprite(sdl2.ext.TextureSprite):
    def __init__(self, texture, position=(0, 0), scale=(1, 1), angle=0.0, pivot=None, flip=sdl2.SDL_FLIP_NONE, depth=0):
        super().__init__(texture)
        self.position = position
        self.scale = scale
        self.angle = angle
        self.pivot = pivot
        self.flip = flip
        self.depth = depth

class SoftwareSprite(sdl2.ext.SoftwareSprite):
    def __init__(self, surface, position=(0, 0), scale=(1, 1), angle=0.0, pivot=None, flip=sdl2.SDL_FLIP_NONE, depth=0, free=False):
        super().__init__(surface, free)
        self.position = position
        self.scale = scale
        self.angle = angle
        self.pivot = pivot
        self.flip = flip
        self.depth = 0

class TextureRenderer(sdl2.ext.TextureSpriteRenderSystem):
    def __init__(self, target):
        super().__init__(target)

    def render(self, sprites, x=0, y=0):
        r = sdl2.rect.SDL_Rect(0, 0, 0, 0)
        for sp in sprites:
            r.x, r.y = x + sp.x, y + sp.y
            r.w = int(sp.size[0] * sp.scale[0])
            r.h = int(sp.size[1] * sp.scale[1])
            sdl2.SDL_RenderCopyEx(self.sdlrenderer,
                                  sp.texture,
                                  None,
                                  r,
                                  sp.angle,
                                  sp.pivot,
                                  sp.flip)
        sdl2.SDL_RenderPresent(self.sdlrenderer)

def define_renderer(renderer):
    global _factory
    global _renderer
    global GlRenderer
    if renderer == sdl2.ext.TEXTURE:
        rend = GlRenderer = sdl2.ext.Renderer(pybasic.window.get_window())
        _factory = sdl2.ext.SpriteFactory(renderer, renderer=rend)
        _renderer = TextureRenderer(rend)
    else:
        _factory = sdl2.ext.SpriteFactory(renderer)
        _renderer = _factory.create_sprite_render_system(pybasic.window.get_window())

def use_software_renderer():
    define_renderer(sdl2.ext.SOFTWARE)

def use_texture_renderer():
    define_renderer(sdl2.ext.TEXTURE)

def _create_surface(width, height):
    s = sdl2.SDL_CreateRGBSurface(0,width,height,32,0,0,0,0x000000ff);
    return s

def from_surface(surface, free=True):
    if GlRenderer:
        tex = sdl2.SDL_CreateTextureFromSurface(GlRenderer.renderer, surface)
        sprite = TextureSprite(tex)
        if free:
            sdl2.SDL_FreeSurface(surface)
    else:
        sprite = SoftwareSprite(surface, free=free)
    return sprite

def rectangle(color, size, position=(0, 0)):
    color = sdl2.ext.convert_to_color(color)
    s = _create_surface(*size)
    color = sdl2.SDL_MapRGBA(s.contents.format.contents, color.r, color.g, color.b, color.a)
    sdl2.SDL_FillRect(s, None, color)
    rect = from_surface(s, True)
    rect.position = position
    return rect

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

