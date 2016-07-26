
import sdl2.ext
import pybasic.window
import pybasic.sprite
import pybasic.events
import pybasic.fonts

from pybasic.window import *
from pybasic.sprite import *
from pybasic.fonts import *

__all__ = pybasic.window.__all__
__all__ += pybasic.sprite.__all__
__all__ += pybasic.fonts.__all__
__all__ += ['events', 'Color']

Color = sdl2.ext.Color

sdl2.ext.init()

