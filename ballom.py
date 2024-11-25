import random
from random import choice, randrange, randint
from actor import Actor, Arena, Point
from wall import Wall
from wallDistr import WallDistr
from fire import Fire

class Ballom(Actor):
    def __init__(self, pos, sprite):
        self._x, self._y = pos
        self._speed = 1
        self._dx, self._dy = self._speed, 0
        self._w, self._h = 16, 16
        self._spriteW, self._spriteH = sprite
        self._timerAnimation=0
        self._countDirection=0
        self._death=False
        self._timerDeath=65
        self._timerPoint=30
        self._point=0
        self._addPoint=True
        

    #metodo move
    def move(self, arena: Arena):
        
        #controllo se il ballom e ancora in vita
        if self._death==True:
            if self._point == 0:  # Imposta i punti
                self._point = 100
                self._addPoint = False
            self.deathAnimation(arena)

        #movimento del ballom
        else:
            if self._countDirection < random.randint(10, 50):
                if self.check_collision(self._x + self._dx, self._y + self._dy, arena)==False:
                    self._x += self._dx
                    self._y += self._dy

                    self._timerAnimation += 1

                    if 0 <= self._timerAnimation < 20:
                        self._spriteW, self._spriteH = (0), self._spriteH
                    elif 20 <= self._timerAnimation < 40:
                        self._spriteW, self._spriteH = (self._w), self._spriteH
                    elif 40 <= self._timerAnimation < 60:
                        self._spriteW, self._spriteH = (self._w * 2), self._spriteH
                    elif 60 <= self._timerAnimation < 80:
                        self._spriteW, self._spriteH = (self._w * 3), self._spriteH
                    elif 80 <= self._timerAnimation < 100:
                        self._spriteW, self._spriteH = (self._w * 4), self._spriteH
                    elif 100 <= self._timerAnimation < 120:
                        self._spriteW, self._spriteH = (self._w * 5), self._spriteH
                    
                    
                    #reset timer
                    if self._timerAnimation >= 120:
                        self._timerAnimation = 0
                        
                self._countDirection = self._countDirection + 1
            
            #incremento della posizione del ballom
            else:
                self._countDirection=0
                directions=self.possible_directions(arena)
                random.shuffle(directions)
                self._dx, self._dy = directions[0]

        
    #medoto per definire le possibili direzioni in cui puo andare il ballom
    def possible_directions(self, arena: Arena):
        self._speed=1
        self._dx=self._speed
        self._dy=self._speed


        directions=[]
        if self.check_collision(self._x + self._dx, self._y, arena)==False:
            directions.append((self._dx, 0))
        if self.check_collision(self._x, self._y + self._dy, arena)==False:
            directions.append((0, self._dy))
        if self.check_collision(self._x - self._dx, self._y, arena)==False:
            directions.append((-self._dx, 0))
        if self.check_collision(self._x, self._y - self._dy, arena)==False:
            directions.append((0, -self._dy))
        
        return directions

    #animazione della morte del ballom
    def deathAnimation(self, arena: Arena):
        if self._timerDeath <=65 and self._timerDeath >=40:
            self._spriteW, self._spriteH = 96, 240
        if self._timerDeath <=39 and self._timerDeath >=30:
            self._spriteW, self._spriteH = 112, 240
        if self._timerDeath <=29 and self._timerDeath >=20:
            self._spriteW, self._spriteH = 128, 240
        if self._timerDeath <=19 and self._timerDeath >=10:
            self._spriteW, self._spriteH = 144, 240
        if self._timerDeath <=9 and self._timerDeath >=0:
            self._spriteW, self._spriteH = 160, 240
        if self._timerDeath <= 0:
            self._spriteW=112
            self._spriteH=336
            self._w=16
            self._h=8
            
            if self._timerPoint==0:
                arena.kill(self)
            else:
                self._timerPoint -=1 
        
        self._timerDeath -= 1

    #controllo collisioni di ballom
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
            
            if isinstance(actor, Fire):
                ax, ay = actor.pos()
                aw, ah = actor.size()

                margin = 10   
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

        return False  # Nessuna collisione

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._spriteW, self._spriteH

    def point(self) -> int:
        return self._point
    
    def addPoint(self) -> bool:
        return self._addPoint
    
    def set_add_point(self):
        self._addPoint = True
