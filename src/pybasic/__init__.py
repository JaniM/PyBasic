
import sdl2.ext
import pybasic.window as window
import pybasic.sprite as sprite
import pybasic.events as events
import pybasic.fonts as fonts

from pybasic.window import *
from pybasic.sprite import *
from pybasic.fonts import *

__all__ = window.__all__
__all__ += sprite.__all__
__all__ += fonts.__all__
__all__ += ['events', 'sprite', 'fonts', 'window', 'Color']

Color = sdl2.ext.Color

sdl2.ext.init()

