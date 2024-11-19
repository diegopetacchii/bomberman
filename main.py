import random
from random import choice, randrange, randint
from actor import Actor, Arena, Point
from wall import Wall
from ballom import Ballom
from wallDistr import WallDistr
from bomb import Bomb
from fire import Fire
from door import Door
from bomberman import Bomberman


def walls_distr(arena, num_walls):
    arena_w, arena_h = arena.size()
    block_size = 16
    added_walls = 0

    while added_walls < num_walls:
        x = random.randrange(block_size, arena_w - block_size, block_size)
        y = random.randrange(block_size, arena_h - block_size, block_size)

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
            arena.spawn(Door((wx, wy + 16)))
            break
 

def tick():
    arena_width, arena_height = arena.size()

    g2d.set_color((60, 123, 1))
    g2d.draw_rect((0, 0), (arena_width, arena_height))

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
            g2d.draw_image("bomberman.png", a.pos(), a.sprite(), a.size())

    for a in arena.actors():
        if isinstance(a, (Ballom, Bomberman, Bomb, Fire)):
            a.move(arena)

    arena.tick(g2d.current_keys())

def add_walls(arena):
        arena_w, arena_h = arena.size()
        block_size = 16  # Dimensione del muro

        # Aggiungi muri ai bordi superiori e inferiori
        for x in range(0, arena_w, block_size):
            arena.spawn(Wall((x, 0)))
            arena.spawn(Wall((x, arena_h - block_size)))

        # Aggiungi muri ai bordi laterali
        for y in range(0, arena_h, block_size):
            arena.spawn(Wall((0, y)))
            arena.spawn(Wall((arena_w - block_size, y)))

        # muri in mezzo
        for x in range(block_size * 2, arena_w - block_size, block_size * 2):
            for y in range(block_size * 2, arena_h - block_size, block_size * 2):
                if (x // block_size) % 2 == 0 or (y // block_size) % 2 == 0:
                    arena.spawn(Wall((x, y)))

        walls_distr(arena, 80)
    
        spawn_door(arena)

def main():
    global g2d, arena
    import g2d

    arena = Arena((464, 336))
    arena.spawn(Ballom((16, 16)))
    arena.spawn(Bomberman((16, 160)))

    add_walls(arena)  # Aggiungi i muri ai bordi e nelle altre posizioni

    g2d.init_canvas(arena.size())
    g2d.main_loop(tick)  # Avvia il ciclo principale e assicurati che il canvas si aggiorni

   
if __name__ == "__main__":
    main()