import random
from random import choice, randrange, randint
from actor import Actor, Arena, Point
from wall import Wall
from wallDistr import WallDistr
from fire import Fire

class Ballom(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._speed = 1
        self._dx, self._dy = self._speed, 0
        self._w, self._h = 16, 16
        self._spriteW, self._spriteH = 0, 240
        self._timerAnimation=0
        self._countDirection=0
        self._death=False
        self._timerDeath=50

    def move(self, arena: Arena):
        
        if self._death==True:
            self.deathAnimation(arena)

        else:
            if self._countDirection < random.randint(10, 50):
                if self.check_collision(self._x + self._dx, self._y + self._dy, arena)==False:
                    self._x += self._dx
                    self._y += self._dy

                    self._timerAnimation += 1

                    # Cambia immagine in base al timer
                    if 0 <= self._timerAnimation < 20:
                        self._spriteW, self._spriteH = 0, 240
                    elif 20 <= self._timerAnimation < 40:
                        self._spriteW, self._spriteH = 16, 240
                    elif 40 <= self._timerAnimation < 60:
                        self._spriteW, self._spriteH = 32, 240
                    elif 60 <= self._timerAnimation < 80:
                        self._spriteW, self._spriteH = 48, 240
                    elif 80 <= self._timerAnimation < 100:
                        self._spriteW, self._spriteH = 64, 240
                    elif 100 <= self._timerAnimation < 120:
                        self._spriteW, self._spriteH = 80, 240

                    # Resetta il timer quando raggiunge il limite massimo
                    if self._timerAnimation >= 120:
                        self._timerAnimation = 0
                        
                self._countDirection = self._countDirection + 1
            
            else:
                self._countDirection=0
                directions=self.possible_directions(arena)
                random.shuffle(directions)
                self._dx, self._dy = directions[0]

        

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


    def deathAnimation(self, arena: Arena):
        if self._timerDeath <=50 and self._timerDeath >=40:
            self._spriteW, self._spriteH = 96, 240
        if self._timerDeath <=39 and self._timerDeath >=30:
            self._spriteW, self._spriteH = 112, 240
        if self._timerDeath <=29 and self._timerDeath >=20:
            self._spriteW, self._spriteH = 128, 240
        if self._timerDeath <=19 and self._timerDeath >=10:
            self._spriteW, self._spriteH = 144, 240
        if self._timerDeath <=9 and self._timerDeath >=0:
            self._spriteW, self._spriteH = 160, 240
        if self._timerDeath == 0:
            arena.kill(self) 
        self._timerDeath -= 1

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

        return False  
        # Nessuna collisione

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._spriteW, self._spriteH
