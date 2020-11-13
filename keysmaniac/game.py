from pyglet import gl
from pyglet.window import Window
from pyglet.app import run

from .display import Grid
from .log import logging
from .scenes import TitleScene, PlayScene


class Game:
    def __init__(self):
        # gl.glEnable(gl.GL_TEXTURE_2D)
        # gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.window = Window(width=640, height=360, resizable=True)
        # self.window.config.alpha_size = 8
        gl.glEnable(gl.GL_BLEND)
        self.window.set_caption('KeysManiac (development build)')
        Grid.set_factor_from_resolution(*self.window.get_size())
        self.window.push_handlers(self)
        self.scene = None
        # self.load_scene(TitleScene)
        # self.load_scene(PlayScene)

    def load_scene(self, scene_class):
        """Changes the current scene, takes a Class as parameter, not an Object"""
        context = None
        if self.scene:
            context = self.scene.context
            self.scene.unload()
        new_scene = scene_class(game=self, context=context)
        new_scene.load()
        self.scene = new_scene

    def run(self):
        run()

    def on_draw(self):
        if not self.scene:
            logging.warning('No scene has been loaded')
            return
        self.window.clear()
        self.scene.draw()

    def on_resize(self, width, height):
        Grid.set_factor_from_resolution(width, height)
        if not self.scene:
            return
        self.scene.resize()

    def on_activate(self):
        self.on_draw()

    def on_key_press(self, symbol, modifiers):
        if not self.scene:
            return
        self.scene.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if not self.scene:
            return
        self.scene.on_key_release(symbol, modifiers)
