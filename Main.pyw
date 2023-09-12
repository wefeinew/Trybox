import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from random import randrange, seed, randint
import random
import sys
import pymunk.pygame_util
seed_value = random.randint(1, 666)
random.seed(seed_value)
pymunk.pygame_util.positive_y_is_up = False
objects = []
bombs = []
APP_NAME = "TryBox."

# PyGame parameters
RES = WIDTH, HEIGHT = 900, 700
FPS = 60
p_key_pressed = False
pg.init()
pg.display.set_caption("TryBox")
icon = pg.image.load("images/logo/logo.jpg")
pg.display.set_icon(icon)
surface = pg.display.set_mode(RES, pg.RESIZABLE)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

space = pymunk.Space()
space.gravity = 0, 1000

def create_walls():
    wall_width = 26
    segment_shape_left = pymunk.Segment(space.static_body, (wall_width // 2, HEIGHT), (wall_width // 2, 0), wall_width)
    segment_shape_right = pymunk.Segment(space.static_body, (WIDTH - wall_width // 2, HEIGHT), (WIDTH - wall_width // 2, 0), wall_width)

    space.add(segment_shape_left, segment_shape_right)

    segment_shape_left.elasticity = 0.8
    segment_shape_left.friction = 1.0
    segment_shape_left.color = [128, 128, 128, 255]

    segment_shape_right.elasticity = 0.8
    segment_shape_right.friction = 1.0
    segment_shape_right.color = [128, 128, 128, 255]  # Серый цвет

    
    return segment_shape_left, segment_shape_right

segment_shape_left, segment_shape_right = create_walls()
def exit():
        pg.quit()  # Закрыть Pygame
        sys.exit()  # Завершить программу
    
def create_platform():
    segment_shape = pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 26)
    space.add(segment_shape)
    segment_shape.elasticity = 0.8
    segment_shape.friction = 1.0
    segment_shape.color = [128, 128, 128, 255]
    return segment_shape

segment_shape = create_platform()

def create_house(space, pos):
    house_width = 200
    house_height = 200

    # Создаем основу дома (прямоугольник)
    base_size = (house_width, 20)
    base_mass = 10
    base_moment = pymunk.moment_for_box(base_mass, base_size)
    base_body = pymunk.Body(base_mass, base_moment)
    base_body.position = pos[0], pos[1] + house_height // 2 - 10  # Позиция основы в центре дома
    base_shape = pymunk.Poly.create_box(base_body, base_size)
    base_shape.elasticity = 0.4
    base_shape.friction = 1.0
    space.add(base_body, base_shape)

    # Создаем крышу (треугольник)
    roof_height = 50
    roof_width = 220
    roof_mass = 5
    roof_moment = pymunk.moment_for_poly(roof_mass, [(0, -roof_height / 2), (roof_width / 2, roof_height / 2), (-roof_width / 2, roof_height / 2)])
    roof_body = pymunk.Body(roof_mass, roof_moment)
    roof_body.position = pos[0], pos[1] + house_height // 2 - 10 + roof_height // 2
    roof_shape = pymunk.Poly(roof_body, [(0, -roof_height / 2), (roof_width / 2, roof_height / 2), (-roof_width / 2, roof_height / 2)])
    roof_shape.elasticity = 0.4
    roof_shape.friction = 1.0
    space.add(roof_body, roof_shape)

    # Создаем дверь (прямоугольник)
    door_width = 60
    door_height = 120
    door_mass = 2
    door_moment = pymunk.moment_for_box(door_mass, (door_width, door_height))
    door_body = pymunk.Body(door_mass, door_moment)
    door_body.position = pos[0] - house_width // 4, pos[1] - door_height // 2
    door_shape = pymunk.Poly.create_box(door_body, (door_width, door_height))
    door_shape.elasticity = 0.4
    door_shape.friction = 1.0
    space.add(door_body, door_shape)

    # Создаем окно (прямоугольник)
    window_width = 40
    window_height = 40
    window_mass = 1
    window_moment = pymunk.moment_for_box(window_mass, (window_width, window_height))
    window_body = pymunk.Body(window_mass, window_moment)
    window_body.position = pos[0] + house_width // 4, pos[1] + house_height // 4
    window_shape = pymunk.Poly.create_box(window_body, (window_width, window_height))
    window_shape.elasticity = 0.4
    window_shape.friction = 1.0
    space.add(window_body, window_shape)
    objects.append((window_body, window_shape, door_body, door_shape, roof_body, roof_shape, base_body, base_shape))

# Где-то в вашем коде перед началом цикла игры вызовите функцию для создания дома
create_house(space, (WIDTH // 2, HEIGHT // 2))


def create_triangle(space, pos, size):
    triangle_mass = 2
    triangle_moment = pymunk.moment_for_poly(triangle_mass, [(0, -size / 2), (size / 2, size / 2), (-size / 2, size / 2)])
    triangle_body = pymunk.Body(triangle_mass, triangle_moment)
    triangle_body.position = pos
    triangle_shape = pymunk.Poly(triangle_body, [(0, -size / 2), (size / 2, size / 2), (-size / 2, size / 2)])
    triangle_shape.elasticity = 0.4
    triangle_shape.friction = 1.0
    triangle_shape.color = [randrange(256) for _ in range(4)]
    
    space.add(triangle_body, triangle_shape)
    objects.append((triangle_body, triangle_shape))


def create_square(space, pos, square_size):
    square_mass = 2
    square_moment = pymunk.moment_for_box(square_mass, square_size)
    square_body = pymunk.Body(square_mass, square_moment)
    square_body.position = pos
    square_shape = pymunk.Poly.create_box(square_body, square_size)
    square_shape.elasticity = 0.4
    square_shape.friction = 1.0

    if randint(1, 1000000) == 1:
        # Генерируем список цветов для создания градиента
        gradient_colors = [(255, 0, 0, 255), (255, 165, 0, 255), (255, 255, 0, 255),
                           (0, 128, 0, 255), (0, 0, 255, 255), (75, 0, 130, 255),
                           (148, 0, 211, 255)]

        # Генерируем случайные индексы для начального и конечного цветов градиента
        start_color_index = randrange(len(gradient_colors))
        end_color_index = (start_color_index + randrange(1, len(gradient_colors))) % len(gradient_colors)

        # Создаем градиентный цвет для радужного блока
        start_color = gradient_colors[start_color_index]
        end_color = gradient_colors[end_color_index]
        color = [int((start + end) / 2) for start, end in zip(start_color, end_color)]
        square_shape.color = color
        square_mass = 2000
    else:
        square_shape.color = [randrange(256) for _ in range(4)]

    space.add(square_body, square_shape)
    objects.append((square_body, square_shape))

def create_rectangle(space, pos, size):
    rectangle_mass = 2
    rectangle_moment = pymunk.moment_for_box(rectangle_mass, size)
    rectangle_body = pymunk.Body(rectangle_mass, rectangle_moment)
    rectangle_body.position = pos
    rectangle_shape = pymunk.Poly.create_box(rectangle_body, size)
    rectangle_shape.elasticity = 0.4
    rectangle_shape.friction = 1.0

    if randint(1, 1000000) == 1:
        gradient_colors = [(255, 0, 0, 255), (255, 165, 0, 255), (255, 255, 0, 255),
                           (0, 128, 0, 255), (0, 0, 255, 255), (75, 0, 130, 255),
                           (148, 0, 211, 255)]

        start_color_index = randrange(len(gradient_colors))
        end_color_index = (start_color_index + randrange(1, len(gradient_colors))) % len(gradient_colors)

        start_color = gradient_colors[start_color_index]
        end_color = gradient_colors[end_color_index]
        color = [int((start + end) / 2) for start, end in zip(start_color, end_color)]
        rectangle_shape.color = color
        rectangle_mass = 2000
    else:
        rectangle_shape.color = [randrange(256) for _ in range(4)]

    space.add(rectangle_body, rectangle_shape)
    objects.append((rectangle_body, rectangle_shape))
    

def create_circle(space, pos, circle_radius):
    circle_mass = 1
    circle_moment = pymunk.moment_for_circle(circle_mass, 0, circle_radius)
    circle_body = pymunk.Body(circle_mass, circle_moment)
    circle_body.position = pos
    circle_shape = pymunk.Circle(circle_body, circle_radius)
    circle_shape.elasticity = 0.4
    circle_shape.friction = 1.0

    if randint(1, 1000000) == 1:
        # Генерируем список цветов для создания градиента
        gradient_colors = [(255, 0, 0, 255), (255, 165, 0, 255), (255, 255, 0, 255),
                           (0, 128, 0, 255), (0, 0, 255, 255), (75, 0, 130, 255),
                           (148, 0, 211, 255)]

        # Генерируем случайные индексы для начального и конечного цветов градиента
        start_color_index = randrange(len(gradient_colors))
        end_color_index = (start_color_index + randrange(1, len(gradient_colors))) % len(gradient_colors)

        # Создаем градиентный цвет для радужного блока
        start_color = gradient_colors[start_color_index]
        end_color = gradient_colors[end_color_index]
        color = [int((start + end) / 2) for start, end in zip(start_color, end_color)]
        circle_shape.color = color
        circle_mass = 1000
    else:
        circle_shape.color = [randrange(256) for _ in range(4)]

    space.add(circle_body, circle_shape)
    objects.append((circle_body, circle_shape))  # Исправьте на circles, если это опечатка


def create_bomb(space, pos):
    bomb_mass = 1
    bomb_radius = 30
    bomb_moment = pymunk.moment_for_circle(bomb_mass, 0, bomb_radius)
    bomb_body = pymunk.Body(bomb_mass, bomb_moment)
    bomb_body.position = pos
    bomb_shape = pymunk.Circle(bomb_body, bomb_radius)
    bomb_shape.elasticity = 0.4
    bomb_shape.friction = 1.0
    bomb_shape.color = [0, 0, 0, 0]
    space.add(bomb_body, bomb_shape)
    bombs.append((bomb_body, bomb_shape))    

notification = None
notification_timer = 0
fps_font = pg.font.Font(None, 36)
fps_text = ''
fps_color = pg.Color('white')

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            surface = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
            space.remove(segment_shape)
            space.remove(segment_shape_left, segment_shape_right)
            segment_shape_left, segment_shape_right = create_walls()
            segment_shape = create_platform()
  
                
        elif event.type == pg.KEYDOWN and event.key == pg.K_DELETE:
            for body, shape in objects:
                space.remove(body, shape)
            notification = "Objects deleted successfully"
            objects = []
            notification_timer = FPS * 5
        elif event.type == pg.KEYDOWN and event.key == pg.K_q:
            segment_shape.body.position = (WIDTH // 2, HEIGHT)
            segment_shape.body.velocity = (0, 0)
                
        elif event.type == pg.KEYDOWN and event.key == pg.K_0:
            notification = "Version: 1.6 Beta relese"
            notification_timer = FPS * 5

        elif event.type == pg.KEYDOWN and event.key == pg.K_p:
            if not p_key_pressed:
                p_key_pressed = True
            else:
                p_key_pressed = False

        elif event.type == pg.KEYDOWN and event.key == pg.K_t:
            mouse_pos = pg.mouse.get_pos()
            create_triangle(space, mouse_pos, 60)  # Размер треугольника (60 пикселей)
                
        elif event.type == pg.KEYDOWN and event.key == pg.K_r:
            mouse_pos = pg.mouse.get_pos()
            create_rectangle(space, mouse_pos, (100, 60))  # Прямоугольник (100x60 пикселей)

        elif event.type == pg.KEYDOWN and event.key == pg.K_x:
            mouse_pos = pg.mouse.get_pos()
            create_rectangle(space, mouse_pos, (60, 100))  # Прямоугольник (100x60 пикселей)
      
    if seed_value == 666:
        surface.fill(pg.Color('red'))
        APP_NAME = ":) :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) "
        pg.display.set_caption("HAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAH")
    else:
        surface.fill(pg.Color('black'))

    font = pg.font.Font(None, 36)
    text_surface = font.render(APP_NAME, True, pg.Color('white'))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 30))
    surface.blit(text_surface, text_rect)

    if pg.mouse.get_pressed()[0]:
        mouse_pos = pg.mouse.get_pos()
        new_square_size = (60, 60)
        create_square(space, mouse_pos, new_square_size)

    if len(pg.mouse.get_pressed()) >= 3 and pg.mouse.get_pressed()[2]:
        mouse_pos = pg.mouse.get_pos()
        new_circle_radius = 30  # Пример радиуса для нового круга
        create_circle(space, mouse_pos, new_circle_radius)

    if pg.key.get_pressed()[pg.K_e]:
        mouse_pos = pg.mouse.get_pos()
        create_bomb(space, mouse_pos)
# Размер треугольника (60 пикселей)
     

    if pg.key.get_pressed()[pg.K_ESCAPE]:
         exit()
        
    # Логика взрыва бомбы
    for bomb_body, bomb_shape in bombs:
        if pg.time.get_ticks() > 1000:
            bomb_explosion_radius = 150
            for body, shape in objects:
                explosion_vector = body.position - bomb_body.position
                distance = explosion_vector.length
                if distance > 0 and distance < bomb_explosion_radius:  # Добавлено условие distance > 0
                    explosion_force = (explosion_vector / distance) * 50000 / (distance + 1)
                    body.apply_impulse_at_local_point(explosion_force)
        space.remove(bomb_body, bomb_shape)
        bombs.remove((bomb_body, bomb_shape))   

    if p_key_pressed:
        for body, shape in objects:
            body.apply_force_at_local_point((-1000, 0), (0, 0))
            notification = "Blowing off objects"
            notification_timer = FPS * 0.1

    space.step(1 / FPS)
    
    if notification:
        font = pg.font.Font(None, 24)
        notification_surface = font.render(notification, True, pg.Color('green'))
        notification_rect = notification_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        surface.blit(notification_surface, notification_rect)
        
        notification_timer -= 1
        if notification_timer <= 0:
            notification = None
     
    
    space.debug_draw(draw_options)
    fps = int(clock.get_fps())
    fps_text = f"FPS: {fps}"

    # Determine text color based on FPS value
    if fps >= 30:
        fps_color = pg.Color('green')
    elif fps >= 20:
        fps_color = pg.Color('yellow')
    else:
        fps_color = pg.Color('red') 

    # Draw FPS text
    fps_surface = fps_font.render(fps_text, True, fps_color)
    fps_rect = fps_surface.get_rect(topleft=(10, 10))
    surface.blit(fps_surface, fps_rect)
    
    seed_text = f"Random Number: {seed_value}"
    seed_surface = font.render(seed_text, True, pg.Color('white'))
    seed_rect = seed_surface.get_rect(bottomleft=(10, HEIGHT - 10))
    surface.blit(seed_surface, seed_rect)
    pg.display.flip()
    clock.tick(FPS)
