import pygame as pg
from pygame.locals import *
from pygame.time import Clock

from config.game import WINDOW_HEIGHT, WINDOW_WIDTH
from view.tetris_view import TetrisView

class GameView:
    def __init__(self):
        self._running = True
        self.size = WINDOW_WIDTH, WINDOW_HEIGHT
        self._display = None
        self.tetris_view = None
    
    def on_init(self):
        pg.init()
        self._display = pg.display.set_mode(self.size, pg.HWSURFACE | pg.DOUBLEBUF)
        self.tetris_view = TetrisView()
        self.tetris_view.init()
    
    def on_event(self, event):
        if event.type == pg.QUIT:
            self._running = False
        self.tetris_view.on_event(event)

    def on_loop(self):
        self.tetris_view.loop()

    def on_render(self):
        self._display.blit(self.tetris_view.draw(), (0, 0))
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
            for event in pg.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

        

        