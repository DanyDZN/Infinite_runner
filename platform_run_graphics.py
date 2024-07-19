import pygame
import math
import sprite_animation
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Keep Running")

black_color = (0, 0, 0)
white_color = (250, 250, 250)

JUMP = False
DOUBLE_JUMP = False
MAX_JUMPS = 2
current_jumps = 0

font = pygame.font.Font("RabbidHighwaySignII.otf", 20)
game_over_font = pygame.font.Font("RabbidHighwaySignII.otf", 70)
restart_font = pygame.font.Font("RabbidHighwaySignII.otf", 40)
quit_font = pygame.font.Font("RabbidHighwaySignII.otf", 20)
score = 0
last_score = 0
high_score = 0

Y_GRAVITY = 1
JUMP_HEIGHT = 20
Y_VELOCITY = 0
Y_POSITION = 550
X_POSITION = 150
Y_POSITION_HITBOX = 580
Y_VELOCITY_HITBOX = 0
Y_GRAVITY_HITBOX = 1

background = pygame.image.load("game_background_back.png").convert_alpha()
background_width = background.get_width()
background_front = pygame.image.load("game_background_front.png").convert_alpha()
background_front_width = background_front.get_width()
ground_tile = pygame.image.load("back_tile.png").convert_alpha()
ground_tile_width = ground_tile.get_width()
front_tile = pygame.image.load("front_tile.png").convert_alpha()
front_tile_width = front_tile.get_width()
sprite_sheet_image = pygame.image.load("Dude_Monster_Run_6.png").convert_alpha()
sprite_sheet = sprite_animation.SpriteAnimation(sprite_sheet_image)
jump_sheet_image = pygame.image.load("Dude_Monster_Jump_8.png").convert_alpha()
jump_sheet = sprite_animation.SpriteAnimation(jump_sheet_image)
obstacle_image = pygame.image.load("Individual_Spike.png").convert_alpha()
obstacle_image_2 = pygame.image.load("4_Conjoined_Spikes.png").convert_alpha()
game_over_screen = pygame.image.load("game_over.png").convert()

obstacle_hitbox_width = 8
obstacle_hitbox_width_2 = 8
obstacle_hitbox_height = 8
obstacle_hitbox_height_2 = 8
obstacle_width = 57
obstacle_width_2 = 200
obstacle_height = 49
obstacle_height_2 = 49
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))
obstacle_image_2 = pygame.transform.scale(obstacle_image_2, (obstacle_width_2, obstacle_height_2))

obstacles = []
obstacles_2 = []
obstacle_hitboxes = []
obstacle_hitboxes_2 = []
animation_list = []
jump_animation_list = []
animation_steps = 6
jump_animation_steps = 8
last_update = pygame.time.get_ticks()
last_jump_update = pygame.time.get_ticks()
animation_cooldown = 75
frame = 0
jump_frame = 0

game_over = False

for x in range(animation_steps):
    animation_list.append(sprite_sheet.get_image(x, 32, 32, 3, black_color))

for y in range(jump_animation_steps):
    jump_animation_list.append(jump_sheet.get_image(y, 32, 32, 3, black_color))

scroll = 0
background_front_scroll = 0
ground_scroll = 0
front_tile_scroll = 0
bg_tiles = math.ceil(SCREEN_WIDTH / background_width) + 1
bg_front_tiles = math.ceil(SCREEN_WIDTH / background_front_width) + 1
ground_tiles = math.ceil(SCREEN_WIDTH / ground_tile_width) + 1
front_tiles = math.ceil(SCREEN_WIDTH / front_tile_width) + 1

run = True
while run:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not JUMP:
                    JUMP = True
                    Y_VELOCITY = JUMP_HEIGHT
                elif not DOUBLE_JUMP and current_jumps < MAX_JUMPS:
                    DOUBLE_JUMP = True
                    Y_VELOCITY = JUMP_HEIGHT
                    current_jumps += 1
            if event.key == pygame.K_TAB and game_over:
                last_score = score
                if score > high_score:
                    high_score = score
                score = 0
                frame = 0
                jump_frame = 0
                Y_GRAVITY = 1
                JUMP_HEIGHT = 20
                Y_VELOCITY = 0
                Y_POSITION = 550
                X_POSITION = 150
                Y_POSITION_HITBOX = 580
                Y_VELOCITY_HITBOX = 0
                Y_GRAVITY_HITBOX = 1
                obstacles.clear()
                obstacles_2.clear()
                game_over = False
            if event.key == pygame.K_q and game_over:
                run = False

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list):
            frame = 0

    if JUMP or DOUBLE_JUMP:
        if current_time - last_jump_update >= animation_cooldown:
            jump_frame += 1
            last_jump_update = current_time
            if jump_frame >= len(jump_animation_list):
                jump_frame = 0

        Y_POSITION -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY

        Y_POSITION_HITBOX = Y_POSITION + 10

        if Y_POSITION >= 550:
            JUMP = False
            DOUBLE_JUMP = False
            current_jumps = 0
            Y_POSITION = 550
            Y_VELOCITY = 0
            Y_POSITION_HITBOX = 580

    for tile in range(0, bg_tiles):
        screen.blit(background, (tile * background_width + scroll, 0))

    for tile in range(0, bg_front_tiles):
        screen.blit(background_front, (tile * background_front_width + background_front_scroll, 0))

    if JUMP:
        screen.blit(jump_animation_list[jump_frame], (X_POSITION, Y_POSITION))
    else:
        screen.blit(animation_list[frame], (X_POSITION, Y_POSITION))

    if not game_over:
        score += 1
        obstacles = [obstacle for obstacle in obstacles if obstacle[0] > -obstacle_width]
        obstacle_hitboxes = []
        for obstacle in obstacles:
            obstacle[0] -= 6
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))
            obstacle_hitbox = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
            obstacle_hitboxes.append(obstacle_hitbox)

        if len(obstacles) < 3:
            obstacle_x = random.randint(1080, 10000)
            obstacle_y = 593

            while any(abs(obstacle_x - obstacle[0]) < obstacle_width for obstacle in obstacles):
                obstacle_x += random.randint(1080, 10000)

            obstacles.append([obstacle_x, obstacle_y])

        obstacles_2 = [obstacle_2 for obstacle_2 in obstacles_2 if obstacle_2[0] > -obstacle_width_2]
        obstacle_hitboxes_2 = []
        for obstacle_2 in obstacles_2:
            obstacle_2[0] -= 6
            screen.blit(obstacle_image_2, (obstacle_2[0], obstacle_2[1]))
            obstacle_hitbox_2 = pygame.Rect(obstacle_2[0], obstacle_2[1], obstacle_width_2, obstacle_height_2)
            obstacle_hitboxes_2.append(obstacle_hitbox_2)

        if len(obstacles_2) < 4:
            obstacle_x_2 = random.randint(2000, 10000)
            obstacle_y_2 = 593

            while any(abs(obstacle_x_2 - obstacle_2[0]) < obstacle_width_2 for obstacle_2 in obstacles_2):
                obstacle_x_2 += random.randint(2000, 10000)

            obstacles_2.append([obstacle_x_2, obstacle_y_2])

    for tile in range(0, ground_tiles):
        screen.blit(ground_tile, (tile * ground_tile_width + ground_scroll, 0))

    for tile in range(0, front_tiles):
        screen.blit(front_tile, (tile * front_tile_width + front_tile_scroll, 5))

    player_rect = pygame.Rect(180, Y_POSITION_HITBOX, 40, 60)

    for obstacle_hitbox in obstacle_hitboxes:
        if obstacle_hitbox_2.colliderect(obstacle_hitbox):
            obstacle_x_2 += random.randint(1000, 4000)

    scroll -= 2
    background_front_scroll -= 4
    ground_scroll -= 6
    front_tile_scroll -= 10

    if abs(scroll) > background_width:
        scroll = 0

    if abs(background_front_scroll) > background_front_width:
        background_front_scroll = 0

    if abs(ground_scroll) > ground_tile_width:
        ground_scroll = 0

    if abs(front_tile_scroll) > front_tile_width:
        front_tile_scroll = 0

    for obstacle_hitbox in obstacle_hitboxes:
        if player_rect.colliderect(obstacle_hitbox):
            game_over = True

    for obstacle_hitbox_2 in obstacle_hitboxes_2:
        if player_rect.colliderect(obstacle_hitbox_2):
            game_over = True

    if game_over:
        screen.blit(game_over_screen, (0, 0))
        display_game_over = game_over_font.render("You lost!", True, white_color)
        screen.blit(display_game_over, (460, 200))
        display_restart = restart_font.render("Press TAB to restart.", True, white_color)
        screen.blit(display_restart, (420, 350))
        display_quit = quit_font.render("Or Press ""Q"" to QUIT.", True, white_color)
        screen.blit(display_quit, (520, 500))

    display_score = font.render("Score: " + str(score), True, white_color)
    screen.blit(display_score, (10, 10))
    display_last_score = font.render("Last score: " + str(last_score), True, white_color)
    screen.blit(display_last_score, (10, 40))
    display_high_score = font.render("High score: " + str(high_score), True, white_color)
    screen.blit(display_high_score, (1100, 680))
    pygame.display.update()

pygame.quit()
