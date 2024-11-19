import random
from random import choice, randrange, randint
from actor import Actor, Arena, Point
from wall import Wall
from wallDistr import WallDistr

class Ballom(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._speed = 1
        self._dx, self._dy = self._speed, 0
        self._w, self._h = 16, 16
        self._spriteW, self._spriteH = 0, 240
        self._timerAnimation=0
        self._timerBallom=0
        self._countImagBallom=0

    def move(self, arena: Arena):
        
        arena_w, arena_h = arena.size()
        animationSpeed=20

        if self._timerBallom==0 or self._timerBallom==20:
            movimenti=[0, 1, 2, 3]
            random.shuffle(movimenti)
           
            for i in movimenti:
                if i==0:
                    self._dx=-self._speed
                    self._dy=0
                elif i==1:
                    self._dx=self._speed
                    self._dy=0
                elif i==2:
                    self._dy=-self._speed
                    self._dx=0
                elif i==3:
                    self._dy=self._speed
                    self._dx=0

                if self.check_collision( self._x+self._dx, self._y+self._dy, arena)==False:
                    self._x=self._x+self._dx
                    self._y=self._y+self._dy
                   
                    break
                if self._timerBallom==0:
                    self._timerBallom=self._timerBallom+1
                else:
                    self._timerBallom=0
        else:
            if self.check_collision( self._x+self._dx, self._y+self._dy, arena)==False:
                self._x=self._x+self._dx
                self._y=self._y+self._dy
            else:
                self._x=self._x-self._dx
                self._y=self._y-self._dy
            self._timerBallom=self._timerBallom+1
       
        if self._timerAnimation >= animationSpeed:
            sprite_positions = [0, 16, 32]
            self._spriteW, self._spriteH = sprite_positions[self._countImagBallom % len(sprite_positions)], 240
            self._countImagBallom = (self._countImagBallom + 1) % len(sprite_positions)

            self._timerAnimation = 0
        else:
            self._timerAnimation += 1

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
        # Nessuna collisione

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._spriteW, self._spriteH
