import random
import g2d
from random import choice, randrange, randint
from actor import Actor, Arena, Point
from wall import Wall
from wallDistr import WallDistr
from bomb import Bomb
from door import Door
from ballom import Ballom
from fire import Fire


class Bomberman(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._spriteW, self._spriteH = 16, 16
        self._dx, self._dy = 0, 0
        self._speed = 2
        self._countU, self._countD, self._countL, self._countR = 0, 0, 0, 0
        self._timerDeath=70
        self._death=False
        
    def is_alive(self):
        return not(self._death)


    def move(self, arena: Arena):
        if self._death:
            self.deathAnimation(arena)
        else:
            keys = arena.current_keys()
            
            if "ArrowUp" in keys:
                if self._countU==1:
                    self._spriteW, self._spriteH=48, 16
                if self._countU==2:
                    self._spriteW, self._spriteH=64, 16
                if self._countU==3:
                    self._spriteW, self._spriteH=80, 16  
                    self._countU=0
                self._countU=self._countU+1    
                self._dy -= self._speed
                self._dx = 0
            elif "ArrowDown" in keys:
                if self._countD==1:
                    self._spriteW, self._spriteH=48, 0
                if self._countD==2:
                    self._spriteW, self._spriteH=64, 0
                if self._countD==3:
                    self._spriteW, self._spriteH=80, 0  
                    self._countD=0
                self._countD=self._countD+1
                self._dy += self._speed
                self._dx = 0
            elif "ArrowLeft" in keys:
                if self._countL==1:
                    self._spriteW, self._spriteH=0, 0
                if self._countL==2:
                    self._spriteW, self._spriteH=16, 0
                if self._countL==3:
                    self._spriteW, self._spriteH=32, 0  
                    self._countL=0
                self._countL=self._countL+1
                self._dx -= self._speed
                self._dy = 0
                self.update_sprite("left")
            elif "ArrowRight" in keys:
                if self._countR==1:
                    self._spriteW, self._spriteH=0, 16
                if self._countR==2:
                    self._spriteW, self._spriteH=16, 16
                if self._countR==3:
                    self._spriteW, self._spriteH=32, 16  
                    self._countR=0
                self._countR=self._countR+1
                self._dx += self._speed
                self._dy = 0

            if "Spacebar" in keys:
                if not any(isinstance(a, Bomb) for a in arena.actors()):
                    arena.spawn(Bomb((self._x, self._y)))

            # Controllo collisioni prima di aggiornare la posizione
            if not self.check_collision(self._x + self._dx, self._y + self._dy, arena):
                self._x += self._dx
                self._y += self._dy

            # Reset dx e dy dopo il movimento
            self._dx = 0
            self._dy = 0

            # Check door collision
        if self.check_door_collision(arena):
            print("Camilla De Pandis SMASH")

    def update_sprite(self, direction):
        if direction == "up":
            self._countU = (self._countU + 1) % 4
            self._spriteW, self._spriteH = 48 + 16 * self._countU, 16
        elif direction == "down":
            self._countD = (self._countD + 1) % 4
            self._spriteW, self._spriteH = 48 + 16 * self._countD, 0
        elif direction == "left":
            self._countL = (self._countL + 1) % 4
            self._spriteW, self._spriteH = 0 + 16 * self._countL, 0
        elif direction == "right":
            self._countR = (self._countR + 1) % 4
            self._spriteW, self._spriteH = 0 + 16 * self._countR, 16

    """def move(self, arena: Arena):
        
        if self._death==True:
            self.deathAnimation(arena)

        else:
            keys = arena.current_keys()
            if "ArrowUp" in keys:
                if self._countU==1:
                    self._spriteW, self._spriteH=48, 16
                if self._countU==2:
                    self._spriteW, self._spriteH=64, 16
                if self._countU==3:
                    self._spriteW, self._spriteH=80, 16  
                    self._countU=0
                self._countU=self._countU+1    
                self._dy -= self._speed
                self._dx = 0
                
            elif "ArrowDown" in keys:
                if self._countD==1:
                    self._spriteW, self._spriteH=48, 0
                if self._countD==2:
                    self._spriteW, self._spriteH=64, 0
                if self._countD==3:
                    self._spriteW, self._spriteH=80, 0  
                    self._countD=0
                self._countD=self._countD+1
                self._dy += self._speed
                self._dx = 0
            
            elif "ArrowLeft" in keys :
                if self._countL==1:
                    self._spriteW, self._spriteH=0, 0
                if self._countL==2:
                    self._spriteW, self._spriteH=16, 0
                if self._countL==3:
                    self._spriteW, self._spriteH=32, 0  
                    self._countL=0
                self._countL=self._countL+1
                self._dx -= self._speed
                self._dy = 0
            elif "ArrowRight" in keys:
                if self._countR==1:
                    self._spriteW, self._spriteH=0, 16
                if self._countR==2:
                    self._spriteW, self._spriteH=16, 16
                if self._countR==3:
                    self._spriteW, self._spriteH=32, 16  
                    self._countR=0
                self._countR=self._countR+1
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
                print("Camilla De Pandis SMASH")"""
    
    def check_collision(self, next_x, next_y, arena: Arena) -> bool:
        
        # Controlla le collisioni con tutti i muri (sia normali che distruttibili)
        for actor in arena.actors():
            if isinstance(actor, (Wall, WallDistr)):  
                ax, ay = actor.pos()
                aw, ah = actor.size()

                if (next_x < ax + aw and next_x + self._w > ax and
                    next_y < ay + ah and next_y + self._h > ay):
                    return True  # C'è una collisione
                
            if isinstance(actor, (Ballom)):
                ax, ay = actor.pos()
                aw, ah = actor.size()
                if (next_x < ax + aw and next_x + self._w > ax and
                    next_y < ay + ah and next_y + self._h > ay):
                    self._death=True

            if isinstance(actor, Fire):
                ax, ay = actor.pos()
                aw, ah = actor.size()

                margin = 16  # Margine aggiunto per il fuoco
                # Collisione normale con il fuoco
                if (next_x < ax + aw and next_x + self._w > ax and
                    next_y < ay + ah and next_y + self._h > ay):
                    self._death = True

                # Collisione con la zona estesa attorno al fuoco
                extended_ax = ax - margin
                extended_ay = ay - margin
                extended_aw = aw + 2 * margin
                extended_ah = ah + 2 * margin

                if (next_x < extended_ax + extended_aw and next_x + self._w > extended_ax and
                    next_y < extended_ay + extended_ah and next_y + self._h > extended_ay):
                    self._death = True

        #nessuna collisione 
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

    def deathAnimation(self, arena: Arena):
        if self._timerDeath <=70 and self._timerDeath >=60:
            self._spriteW, self._spriteH = 0, 32
        if self._timerDeath <=59 and self._timerDeath >=50:
            self._spriteW, self._spriteH = 16, 32
        if self._timerDeath <=49 and self._timerDeath >=40:
            self._spriteW, self._spriteH = 32, 32
        if self._timerDeath <=39 and self._timerDeath >=30:
            self._spriteW, self._spriteH = 48, 32
        if self._timerDeath <=29 and self._timerDeath >=20:
            self._spriteW, self._spriteH = 64, 32
        if self._timerDeath <=19 and self._timerDeath >=10:
            self._spriteW, self._spriteH = 80, 32
        if self._timerDeath <=9 and self._timerDeath >0:
            self._spriteW, self._spriteH = 96, 32
        if self._timerDeath == 0:
            arena.kill(self) 
        self._timerDeath -= 1