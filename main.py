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


AX, AY= 463, 366
AX2, AY2= 463, 336
delta_pos=30
timer=200
count_frame=0
fps=30

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
            if isinstance(actor, (Wall, Bomberman, Ballom)):
                ax, ay = actor.pos()
                if (x < ax + block_size and x + block_size > ax and
                        y < ay + block_size and y + block_size > ay):
                    collision = True
                    break

        if not collision:
            arena.spawn(WallDistr((x, y)))
            added_walls += 1


def spawn_door(arena):
    for actor in arena.actors():
        if isinstance(actor, WallDistr):
            wx, wy = actor.pos()
            arena.spawn(Door((wx, wy)))
            print(f"Porta creata alla posizione: {(wx, wy)}") 
            break
 

def tick(arena:Arena):
    global AX2, AY2, delta_pos, timer, count_frame, fps
    arena_width, arena_height = arena.size()
    

    g2d.set_color((60, 123, 1))
    g2d.draw_rect((0, 0), (arena_width, arena_height))

    g2d.set_color((105, 105, 105))
    g2d.draw_rect((0, 0), (arena_width, delta_pos))

    count_frame=count_frame+1
    if count_frame==fps:
        count_frame=0
        timer=timer-1
    g2d.set_color((255, 105, 105))
    g2d.draw_text(f"Time: {timer}", (50, 15), 15)
    if timer==195:
        game_over(arena)
        return
        

    for a in arena.actors():
        if isinstance(a, Wall):
            g2d.draw_image("bomberman.png", a.pos(), a.sprite(), a.size())
        elif isinstance(a, WallDistr):
            g2d.draw_image("bomberman.png", a.pos(), a.sprite(), a.size())
        elif isinstance(a, Bomberman):
            g2d.draw_image("bomberman.png", a.pos(), a.sprite(), a.size())
        elif isinstance(a, Ballom):
            g2d.draw_image("bomberman.png", a.pos(), a.sprite(), a.size())
        elif isinstance(a, Bomb):
            g2d.draw_image("bomberman.png", a.pos(), a.sprite(), a.size())
        elif isinstance(a, Door):
            if not a.is_hidden():  # Disegna la porta solo se non è nascosta
                g2d.draw_image("bomberman.png", a.pos(), a.sprite(), a.size())

    for a in arena.actors():
        if isinstance(a, (Ballom, Bomberman, Bomb, Fire, WallDistr)):
            a.move(arena)

    arena.tick(g2d.current_keys())


def game_over(arena:Arena):
    arena_width, arena_height = arena.size()
    g2d.draw_text("GAME OVER", (arena_width//2-50, arena_height//2), 30)
    main()
    


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

    walls_distr(arena, 80)
    
    spawn_door(arena)

def home_screen():
    global g2d, AX, AY
    arena = Arena((AX, AY))
    g2d.init_canvas((AX, AY))
    
    ciclo = True
    while ciclo:
        # Disegna la schermata iniziale
        print("ciao")
        g2d.clear_canvas()
        g2d.draw_text("Press Enter to Start", (AX // 2 - 100, AY // 2), 24)  # Centra il testo
        g2d.update_canvas()

        time.sleep(1) 

        # Controlla i tasti premuti
        keys = g2d.current_keys()
        if "Enter" in keys:
            print("Enter premuto")
            arena.spawn(Ballom((16, 128)))
            arena.spawn(Bomberman((16, 288)))
            add_walls(arena)
            g2d.main_loop(tick)
            ciclo = False  # Esce dal ciclo

             


def main():
    home_screen()

if __name__ == "__main__":
    main()