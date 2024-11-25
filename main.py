import random, time
import g2d
from random import choice, randrange, randint
from actor import Actor, Arena, Point
from wall import Wall
from ballom import Ballom
from wallDistr import WallDistr
from bomb import Bomb
from fire import Fire
from door import Door
from bomberman import Bomberman
from ballomBlue import BallomBlue

#variabili gloali
AX, AY= 463, 366
AX2, AY2= 464, 336
delta_pos=30
timer=200
count_frame=0
fps=30
left =3
point=0

#funzione per la creazione dei muri distruttibili
def walls_distr(arena, num_walls):
    global AX2, AY2, delta_pos
    arena_w, arena_h = AX2, AY2
    block_size = 16
    added_walls = 0
    

    while added_walls < num_walls:
        x = random.randrange(block_size, arena_w - block_size, block_size)
        y = random.randrange(block_size, arena_h - block_size, block_size)+delta_pos

        collision = False
        for actor in arena.actors():
            if isinstance(actor, (Wall, Bomberman, Ballom, BallomBlue)):
                ax, ay = actor.pos()
                if (x < ax + block_size and x + block_size > ax and
                        y < ay + block_size and y + block_size > ay):
                    collision = True
                    break

        if not collision:
            arena.spawn(WallDistr((x, y)))
            added_walls += 1

#funzione per la creazione della porta
def spawn_door(arena):
    for actor in arena.actors():
        if isinstance(actor, WallDistr):
            wx, wy = actor.pos()
            print(f"porta: {wx, wy}"  )
            arena.spawn(Door((wx, wy)))
            break
 
def tick():
    global AX2, AY2, delta_pos, timer, count_frame, fps, point
    arena_width, arena_height = arena.size()

    # Disegna lo sfondo e spazio per i parametri 
    g2d.set_color((60, 123, 1))
    g2d.draw_rect((0, 0), (arena_width, arena_height))

    g2d.set_color((105, 105, 105))
    g2d.draw_rect((0, 0), (arena_width, delta_pos))

    #aggiornamento timer
    count_frame += 1
    if count_frame == fps:
        count_frame = 0
        timer -= 1

    # Disegna i parametri
    g2d.set_color((255, 255, 255))
    g2d.draw_text(f"Time: {timer}", (50, 15), 15)
    g2d.draw_text(f"Points: {point}", (200, 15), 15)
    g2d.draw_text(f"Left: {left}", (400, 15), 15)

    # Controllo se il timer è scaduto
    if timer <= 0:
        game_over(arena)


    for b in arena.actors():
        if isinstance(b, Bomberman):
            bomberman = b
            break
    else:
        bomberman = None

    # Disegno tutti gli oggetti del gioco
    for a in arena.actors():
        if isinstance(a, (Wall, WallDistr)):
            g2d.draw_image("bomberman.png", a.pos(), a.sprite(), a.size())

    for a in arena.actors():
        if isinstance(a, Door):
            if not a.is_hidden():
                g2d.draw_image("bomberman.png", a.pos(), a.sprite(), a.size())

    for a in arena.actors():
        if isinstance(a, (Ballom, Bomberman, Bomb, Fire, WallDistr, BallomBlue)):
            g2d.draw_image("bomberman.png", a.pos(), a.sprite(), a.size())

    for a in arena.actors():
        if isinstance(a, Ballom):
            if a._death and not a.addPoint():  # Verifica se il Ballom è morto e i punti non sono stati aggiunti
                point += a.point()  # Incrementa i punti
                a.set_add_point() 
    
    for a in arena.actors():
        if isinstance(a, BallomBlue):
            if a._death and not a.addPoint():  # Verifica se il Ballom è morto e i punti non sono stati aggiunti
                point += a.point()  # Incrementa i punti
                a.set_add_point() 
                               
    # Controllo se il bomberman è morto
    if bomberman and not bomberman.is_alive():
        bomberman.deathAnimation(arena)

        if bomberman._timerDeath <= 0:
            game_over(arena)
        return

    if bomberman and bomberman.is_alive():
        for a in arena.actors():
            if isinstance(a, (Ballom, Bomberman, Bomb, Fire, WallDistr, BallomBlue)):
                a.move(arena)
            if isinstance(a, Bomberman):
                if a.victory() == True:
                    victory()

    arena.tick(g2d.current_keys())

#funzione per la vittoria
def victory():
    arena_width, arena_height = arena.size()
    g2d.set_color((0, 0, 0))
    g2d.draw_rect((0, 0), (arena_width, arena_height))
    g2d.set_color((0, 255, 0))
    g2d.draw_text("VICTORY", (arena_width // 2, arena_height // 2), 50)
    g2d.update_canvas()
    time.sleep(3)
    reset()

#funzione per il game over
def game_over(arena: Arena):
    global left
    left -= 1
    if left > 0:
        reset()  # Resetta il gioco se ci sono vite rimanenti
    else:
        # Mostra la schermata di Game Over
        left = 3
        arena_width, arena_height = arena.size()
        g2d.set_color((0, 0, 0))
        g2d.draw_rect((0, 0), (arena_width, arena_height))
        g2d.set_color((255, 0, 0))
        g2d.draw_text("GAME OVER", (arena_width // 2, arena_height // 2), 50)
        g2d.update_canvas()
        time.sleep(3)
        main()

#ressetta parametri del gioco
def reset(): 
    global timer, point, count_frame 
    timer = 200
    point = 0 
    count_frame = 0 
    main()

#funzione per aggiunta dei muri
def add_walls(arena):
    global AX2, AY2, delta_pos
    arena_w, arena_h = AX2, AY2
    block_size = 16  # Dimensione del muro
    

    # Aggiungi muri ai bordi superiori e inferiori
    for x in range(0, arena_w, block_size):
        arena.spawn(Wall((x, delta_pos)))
        arena.spawn(Wall((x, delta_pos+arena_h - block_size)))

    # Aggiungi muri ai bordi laterali
    for y in range(0, arena_h, block_size):
        arena.spawn(Wall((0, y+delta_pos)))
        arena.spawn(Wall((arena_w - block_size, y+delta_pos)))

    # muri in mezzo
    for x in range(block_size * 2, arena_w - block_size, block_size * 2):
        for y in range(block_size * 2, arena_h - block_size, block_size * 2):
            if (x // block_size) % 2 == 0 or (y // block_size) % 2 == 0:
                arena.spawn(Wall((x, y+delta_pos)))

    #aggiunta muri distruttibili
    walls_distr(arena, 80)
    
    spawn_door(arena)

def start():
    global g2d, arena, AX, AY, left
    import g2d

    #definizione dell arena
    arena = Arena((AX, AY))
    g2d.init_canvas(arena.size(), 2)

    #immagine iniziale del gioco
    if left ==3:
        g2d.draw_image("homescreen.jpeg", (0,0),(AX, AY))
        g2d.update_canvas()
        time.sleep(3)

    #immagine per il livello 1
    g2d.draw_image("stage1.jpeg", (0,0),(AX, AY))
    g2d.update_canvas()
    time.sleep(3)

    #spown dei personaggi 
    arena.spawn(Bomberman((16, 160)))
    arena.spawn(Ballom((16, 64), (0, 240))) 
    arena.spawn(Ballom((80, 320), (0, 240))) 
    arena.spawn(BallomBlue((272, 128), (0, 256)))

    #agiunta muri
    add_walls(arena) 

    
    g2d.main_loop(tick)  # Avvia il ciclo principale e assicurati che il canvas si aggiorni



def main():
    start() #funzione di avvio
   
if __name__ == "__main__":
    main()