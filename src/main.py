
import os
os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..\\dll")

import random
from pybasic import *

def update_all(ents, delta):
    for x in ents:
        x.update(delta)

class Rect:
    def __init__(self, x1, x2, speed, y, w, h, color):
        self.x = (x1 + x2) / 2
        self.x1, self.x2 = x1, x2
        self.speed = speed
        self.rect = rectangle(color, (w, h), (x1, y))
    
    def update(self, delta):
        self.x += self.speed * delta
        if self.x > self.x2:
            self.x = self.x2
            self.speed *= -1
        elif self.x < self.x1:
            self.x = self.x1
            self.speed *= -1
        self.rect.x = int(self.x)
    
    def render(self):
        render(self.rect)

create_window("Test", (400, 300))
use_texture_renderer()
add_font('res/Roboto-Regular.ttf', 'Roboto')

rects = []
for i in range(5):
    color = [random.randint(0, 255) for _ in range(3)]
    rects.append(Rect(150 - i*10, 150 + i*10, i*20, 70 + i*30, 100, 20, color))

def update(delta, fps):
    update_all(rects, delta)
    render(rects)
    render(text("FPS: {}".format(fps), position=(10, 10)))
    refresh_window()

events.register(events.TICK, update)
events.loop(1000)

