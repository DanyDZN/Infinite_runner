import pygame
import math
import sprite_animation


pygame.init()


clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Keep Running")

black_color = (0, 0, 0)

JUMP = False

Y_GRAVITY = 1
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT
Y_POSITION = 230
X_POSITION = 100
Y_POSITION_HITBOX = 330
Y_VELOCITY_HITBOX = JUMP_HEIGHT
Y_GRAVITY_HITBOX = 1


background = pygame.image.load("background.png").convert()
background_width = background.get_width()
ground_tile = pygame.image.load("ground_tile.png").convert_alpha()
ground_tile_width = ground_tile.get_width()
sprite_sheet_image = pygame.image.load("Run.png").convert_alpha()
sprite_sheet = sprite_animation.SpriteAnimation(sprite_sheet_image)
jump_sheet_image = pygame.image.load("Jump.png").convert_alpha()
jump_sheet = sprite_animation.SpriteAnimation(jump_sheet_image)


animation_list = []
jump_animation_list = []
animation_steps = 8
jump_animation_steps = 9
last_update = pygame.time.get_ticks()
last_jump_update = pygame.time.get_ticks()
animation_cooldown = 75
frame = 0
jump_frame = 0

for x in range(animation_steps):
    animation_list.append(sprite_sheet.get_image(x, 96, 128, 3, black_color))

for y in range(jump_animation_steps):
    jump_animation_list.append(jump_sheet.get_image(y, 96, 128, 3, black_color))

scroll = 0
ground_scroll = 0
bg_tiles = math.ceil(SCREEN_WIDTH / background_width) + 1
ground_tiles = math.ceil(SCREEN_WIDTH / ground_tile_width) + 1

run = True
while run:

    clock.tick(FPS)
    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_SPACE] and not JUMP:
        JUMP = True
        Y_VELOCITY = JUMP_HEIGHT

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list):
            frame = 0

    if JUMP:
        if current_time - last_jump_update >= animation_cooldown:
            jump_frame += 1
            last_jump_update = current_time
            if jump_frame >= len(jump_animation_list):
                jump_frame = 0

        Y_POSITION -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        Y_POSITION_HITBOX -= Y_VELOCITY_HITBOX
        Y_VELOCITY_HITBOX -= Y_GRAVITY_HITBOX
        if Y_VELOCITY < -JUMP_HEIGHT:
            JUMP = False
            Y_VELOCITY = JUMP_HEIGHT
        if Y_VELOCITY_HITBOX < -JUMP_HEIGHT:
            Y_VELOCITY_HITBOX = JUMP_HEIGHT

    for tile in range(0, bg_tiles):
        screen.blit(background, (tile * background_width + scroll, 0))

    for tile in range(0, ground_tiles):
        screen.blit(ground_tile, (tile * ground_tile_width + ground_scroll, 480))

    player_rect = pygame.Rect(210, Y_POSITION_HITBOX, 110, 180)

    scroll -= 2
    ground_scroll -= 10

    if abs(scroll) > background_width:
        scroll = 0

    if abs(ground_scroll) > ground_tile_width:
        ground_scroll = 0

    if JUMP:
        screen.blit(jump_animation_list[jump_frame], (X_POSITION, Y_POSITION))
    else:
        screen.blit(animation_list[frame], (X_POSITION, Y_POSITION))

    # pygame.draw.rect(screen, black_color, player_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
