import random
import g2d
from random import choice, randrange, randint
from actor import Actor, Arena, Point
from wall import Wall
from wallDistr import WallDistr
from door import Door

class Fire(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._spriteW, self._spriteH = 32, 96
        self._timerFire=30

    def move(self, arena: Arena):
        self._timerFire=self._timerFire-1

        if self._timerFire<=30 and self._timerFire>=23:
            self.sprkles(self._x, self._y, self._spriteW, self._spriteH, arena)

        if self._timerFire<=22 and self._timerFire>=15:
            self.sprkles(self._x, self._y, self._spriteW+(16*5), self._spriteH, arena)
           
        if self._timerFire<=14 and self._timerFire>=7:
            self.sprkles(self._x, self._y, self._spriteW, self._spriteH+(16*5), arena)

        if self._timerFire<=6 and self._timerFire>=1:
            self.sprkles(self._x, self._y, self._spriteW+(16*5), self._spriteH+(16*5), arena)
        if self._timerFire==0:
            arena.kill(self)
   
    

    def sprkles(self, xpos, ypos, spriteW, spriteH, arena):
            g2d.draw_image("bomberman.png", self.pos(), (spriteW, spriteH), self.size())
            for i in range(2, 3):
                x = xpos + self._w
                if self.destroy_wall(x, self._y, arena):
                    break
                else:
                    g2d.draw_image("bomberman.png", (x, ypos), (spriteW + (self._w * i), spriteH), self.size())

            for i in range(2, 3):
                x = xpos - self._w
                if self.destroy_wall(x, self._y, arena):
                    break
                else:
                    g2d.draw_image("bomberman.png", (x, ypos), (spriteW - (self._w * i), spriteH), self.size())

            for i in range(2, 3):
                y = ypos + self._w
                if self.destroy_wall(self._x, y, arena):
                    break
                else:
                    g2d.draw_image("bomberman.png", (xpos, y), (spriteW, spriteH + (self._w * i)), self.size())

            for i in range(2, 3):
                y = ypos - self._w
                if self.destroy_wall(self._x, y, arena):
                    break
                else:
                    g2d.draw_image("bomberman.png", (xpos, y), (spriteW, spriteH - (self._w * i)), self.size())


    def destroy_wall(self, next_x, next_y, arena: Arena) -> bool:
        for actor in arena.actors():
            if isinstance(actor, WallDistr):
                ax, ay = actor.pos()
                aw, ah = actor.size()
                if (next_x < ax + aw and next_x + self._w > ax and
                    next_y < ay + ah and next_y + self._h > ay):
                    actor._destroyed = True

                    for other_actor in arena.actors():
                        if isinstance(other_actor, Door) and other_actor.pos() == (ax, ay):
                            other_actor.reveal()

                    return True

            if isinstance(actor, Wall):
                ax, ay = actor.pos()
                aw, ah = actor.size()
                if (next_x < ax + aw and next_x + self._w > ax and
                    next_y < ay + ah and next_y + self._h > ay):
                    return True

        return False



    def check_collision(self, next_x, next_y, arena: Arena) -> bool:
        # Controlla le collisioni con tutti i muri (sia normali che distruttibili)
        for actor in arena.actors():
            if isinstance(actor, (Wall, WallDistr)):  # Controlla sia Wall che WallDistr
                ax, ay = actor.pos()
                aw, ah = actor.size()

                # Se la nuova posizione del personaggio collide con un muro, restituisci True
                if (next_x < ax + aw and next_x + self._w > ax and
                    next_y < ay + ah and next_y + self._h > ay):
                    return True  # C'è una collisione
        return False  

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._spriteW, self._spriteH
   
