import random
from random import choice, randrange, randint
from actor import Actor, Arena, Point
from wall import Wall
from fire import Fire


class Bomb(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._spriteW, self._spriteH = 0, 48
        self._timerBomb=100
        self._timer2=20


    def move(self, arena: Arena):
        self._timerBomb=self._timerBomb-1
        if self._timerBomb==80:
            self._spriteW, self._spriteH=16, 48
        if self._timerBomb==60:
            self._spriteW, self._spriteH=32, 48
        if self._timerBomb==40:
            self._spriteW, self._spriteH=16, 48
        if self._timerBomb==20:
            self._spriteW, self._spriteH=0, 48
        if self._timerBomb==0:
            arena.kill(self)
            arena.spawn(Fire((self._x, self._y)))

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._spriteW, self._spriteH
   
