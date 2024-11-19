import random
import g2d
from random import choice, randrange, randint
from actor import Actor, Arena, Point
from wall import Wall
from wallDistr import WallDistr

class Door(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._spriteW, self._spriteH = 176, 48
        self._hidden = True

    def move(self, arena: Arena):
        pass

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._spriteW, self._spriteH

    def is_hidden(self) -> bool:
        return self._hidden

    def reveal(self):
        self._hidden = False 
