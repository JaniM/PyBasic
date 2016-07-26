
import time
import sdl2
import sdl2.ext

TICK = 100000
QUIT = sdl2.SDL_QUIT

callbacks = {}

def register(type, cb):
    if type not in callbacks:
        callbacks[type] = []
    callbacks[type].append(cb)

def get():
    return sdl2.ext.get_events()

def loop(target_fps=60, fps_update=250):
    last_time = sdl2.timer.SDL_GetTicks()
    s_ticks = s_ms = 0
    ticks_per_sec = 0
    while True:
        t = sdl2.timer.SDL_GetTicks()
        delta = (t - last_time) / 1000
        s_ms += t - last_time
        last_time = t
        if s_ms >= fps_update:
            s_ms -= s_ms if s_ms > fps_update*2 else fps_update
            ticks_per_sec = int(s_ticks * (1000/fps_update)) 
            s_ticks = 0
        s_ticks += 1
        for evt in get():
            if evt.type in callbacks:
                for cb in callbacks[evt.type]:
                    cb(delta, evt)
            if evt.type == QUIT:
                return
        for cb in callbacks[TICK]:
            cb(delta, ticks_per_sec)
        sleeptime = (1./target_fps - delta)*1000
        sleeptime = int(sleeptime)
        if sleeptime > 0:
            #print(int((1./target_fps - delta)*1000))
            sdl2.SDL_Delay(sleeptime)
