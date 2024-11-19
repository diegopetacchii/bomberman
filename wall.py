import random
from random import choice, randrange, randint
from actor import Actor, Arena, Point


class Wall(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16  # Dimensione del blocco muro

    def move(self, arena: Arena):
        pass  # Il muro non si muove

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 48, 48

        
    