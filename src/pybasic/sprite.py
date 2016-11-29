
import collections
import sdl2, sdl2.ext
import pybasic.window
import pybasic.draw as draw
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
        self.tint = (255, 255, 255)
        self.alpha = 255
        self.depth = depth
    
    def render_copy(self, renderer, x, y, r):
        r.x, r.y = x + self.x, y + self.y
        r.w = int(self.size[0] * self.scale[0])
        r.h = int(self.size[1] * self.scale[1])
        sdl2.SDL_SetTextureColorMod(self.texture, *self.tint)
        #sdl2.SDL_SetTextureAlphaMod(self.texture, self.alpha)
        sdl2.SDL_RenderCopyEx(renderer,
                              self.texture,
                              None,
                              r,
                              self.angle,
                              self.pivot,
                              self.flip)

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
        rend = self.sdlrenderer
        for sp in sprites:
            sp.render_copy(rend, x, y, r)
        sdl2.SDL_RenderPresent(rend)

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

def from_surface(surface, free=True, texture=False):
    if GlRenderer:
        tex = sdl2.SDL_CreateTextureFromSurface(GlRenderer.renderer, surface)
        sprite = TextureSprite(tex)
        if free:
            sdl2.SDL_FreeSurface(surface)
    else:
        sprite = SoftwareSprite(surface, free=free)
    return sprite

def from_texture(tex):
    return TextureSprite(tex)

def rectangle(color, size, position=(0, 0), alpha=False):
    s = draw.surface(size, alpha=alpha)
    with draw.context(s):
        draw.rectangle(color, size, alpha=alpha)
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

