import random
from random import choice, randrange, randint
from actor import Actor, Arena, Point
from wall import Wall


class WallDistr(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16  # Dimensione del blocco muro
        self._spriteW, self._spriteH=64, 48
        self._timerWall=50
        self._destroyed=False
        

    def move(self, arena: Arena):
        if self._destroyed==True:
            self.animation(arena)
        pass  # Il muro non si muove

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._spriteW, self._spriteH

    def animation(self, a: Arena):
        
        if self._timerWall > 0: 
            self._spriteW, self._spriteH = 144, 48 
        if self._timerWall >= 10: 
            self._spriteW, self._spriteH = 128, 48 
        if self._timerWall >= 20: 
            self._spriteW, self._spriteH = 112, 48 
        if self._timerWall >= 30: 
            self._spriteW, self._spriteH = 96, 48 
        if self._timerWall >= 40: 
            self._spriteW, self._spriteH = 80, 48 
        if self._timerWall == 0 and self in a._actors: 
            a.kill(self) 
        self._timerWall -= 1
