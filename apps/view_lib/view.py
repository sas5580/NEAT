import pygame as pg
from pygame.locals import *
from pygame.time import Clock


class GameView:
    def __init__(self, controller, ai_controller=None, ai_state=None):
        self._running = True
        self._display = None
        self.controller = controller

        self.ai_controller = ai_controller
        self.ai_state = ai_state

    def on_init(self):
        pg.init()
        self._display = pg.display.set_mode(self.controller.window_size(), pg.HWSURFACE | pg.DOUBLEBUF)
        self.controller.init()

    def on_event(self, event):
        if event.type == pg.QUIT:
            self._running = False
        self.controller.on_event(event)

    def on_loop(self):
        self.controller.loop()

    def on_render(self):
        self._display.blit(self.controller.draw(), (0, 0))
        pg.display.update()

    def on_cleanup(self):
        pg.quit()

    def run(self):
        try:
            self.on_init()
        except Exception as ex:
            print(ex)
            self._running = False

        while self._running:
            if self.ai_controller is None:
                for event in pg.event.get():
                    self.on_event(event)
            else:
                self.ai_controller(self.ai_state)

            self.on_loop()
            self.on_render()
        self.on_cleanup()
