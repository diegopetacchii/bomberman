import random
import g2d
from random import choice, randrange, randint
from actor import Actor, Arena, Point
from wall import Wall
from wallDistr import WallDistr
from bomb import Bomb
from door import Door


countU = 0
countD = 0
countL = 0
countR = 0

class Bomberman(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._spriteW, self._spriteH = 16, 16
        self._dx, self._dy = 0, 0
        self._speed = 2

    def move(self, arena: Arena):
        global countU, countD, countL, countR
         
        keys = arena.current_keys()
        if "ArrowUp" in keys:
            if countU==1:
                self._spriteW, self._spriteH=48, 16
            if countU==2:
                self._spriteW, self._spriteH=64, 16
            if countU==3:
                self._spriteW, self._spriteH=80, 16  
                countU=0
            countU=countU+1    
            self._dy -= self._speed
            self._dx = 0
             
        elif "ArrowDown" in keys:
            if countD==1:
                self._spriteW, self._spriteH=48, 0
            if countD==2:
                self._spriteW, self._spriteH=64, 0
            if countD==3:
                self._spriteW, self._spriteH=80, 0  
                countD=0
            countD=countD+1
            self._dy += self._speed
            self._dx = 0
           
        elif "ArrowLeft" in keys :
            if countL==1:
                self._spriteW, self._spriteH=0, 0
            if countL==2:
                self._spriteW, self._spriteH=16, 0
            if countL==3:
                self._spriteW, self._spriteH=32, 0  
                countL=0
            countL=countL+1
            self._dx -= self._speed
            self._dy = 0
        elif "ArrowRight" in keys:
            if countR==1:
                self._spriteW, self._spriteH=0, 16
            if countR==2:
                self._spriteW, self._spriteH=16, 16
            if countR==3:
                self._spriteW, self._spriteH=32, 16  
                countR=0
            countR=countR+1
            self._dx += self._speed
            self._dy = 0
        if "Spacebar" in keys:
            already_bomb = False
            for a in arena.actors():
                if isinstance(a, Bomb):
                    already_bomb = True
            if already_bomb == False:
                arena.spawn(Bomb((self._x, self._y)))
                
           
        if self.check_collision(self._x + self._dx, self._y + self._dy, arena) == False:
            self._x += self._dx
            self._y += self._dy
        else:
            self._x -= self._dx
            self._y -= self._dy

        self._dx=0
        self._dy=0
       
        if self.check_door_collision(arena):
            print("Camilla De Pandis SMASH")
   
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
       
    def check_door_collision(self, arena: Arena) -> bool:
        for actor in arena.actors():
            if isinstance(actor, Door):
                ax, ay = actor.pos()
                aw, ah = actor.size()
                if (self._x < ax + aw and self._x + self._w > ax and
                        self._y < ay + ah and self._y + self._h > ay):
                    return True
        return False

    def hit(self, arena: Arena):
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return 16, 16

    def sprite(self) -> Point:
        return self._spriteW, self._spriteH

