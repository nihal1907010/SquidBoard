import random
import pygame
import time
from alpha_beta_pruning import *
from functions import *

pygame.init()

NO_OF_SQUARES = 7

SQUARE_WIDTH = 80
SQUARE_HEIGHT = 80

BOARD_WIDTH = NO_OF_SQUARES * SQUARE_WIDTH
BOARD_HEIGHT = NO_OF_SQUARES * SQUARE_HEIGHT

# WIDTH = 800
# HEIGHT = 800

screen = pygame.display.set_mode([BOARD_WIDTH, BOARD_HEIGHT])
pygame.display.set_caption("Squid Board")
font = pygame.font.Font("freesansbold.ttf", 20)
timer = pygame.time.Clock()
fps = 10

red_pieces = ['square', 'triangle', 'circle', 'triangle', 'square']
red_guns = ['short_gun', 'long_gun', 'blast_gun', 'long_gun', 'short_gun']
red_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
red_healths = [30, 30, 30, 30, 30]
captured_pieces_red = []

blue_pieces = ['square', 'triangle', 'circle', 'triangle', 'square']
blue_guns = ['short_gun', 'long_gun', 'blast_gun', 'long_gun', 'short_gun']
blue_locations = [(2, 6), (3, 6), (4, 6), (5, 6), (6, 6)]
blue_healths = [30, 30, 30, 30, 30]
captured_pieces_blue = []

block_locations = []

# 0 - red  : no selection
# 1 - red  : piece selected for shoot
# 2 - red  : piece selected for step
# 3 - blue : no selection
# 4 - blue : piece selected for shoot
# 5 - blue : piece selected for step
cur_state = 0
selection = 100
valid_steps = []
valid_shoots = []
health_pickup_exist = 0
health_pickup_location = []

# Stores the index of dead pieces. This is used to disable (visibility off) dead pieces after they die.
dead_red = []
dead_blue = []

# Weapon
short_gun = pygame.image.load("res/weapon/short.png")
short_gun = pygame.transform.scale(short_gun, (18, 18))

long_gun = pygame.image.load("res/weapon/long.png")
long_gun = pygame.transform.scale(long_gun, (18, 18))

blast_gun = pygame.image.load("res/weapon/blast.png")
blast_gun = pygame.transform.scale(blast_gun, (16, 16))

# Pieces
red_circle = pygame.image.load("res/circle_red.png")
red_circle = pygame.transform.scale(red_circle, (55, 55))
red_square = pygame.image.load("res/square_red.png")
red_square = pygame.transform.scale(red_square, (55, 55))
red_triangle = pygame.image.load("res/triangle_red.png")
red_triangle = pygame.transform.scale(red_triangle, (55, 55))

blue_circle = pygame.image.load("res/circle_blue.png")
blue_circle = pygame.transform.scale(blue_circle, (55, 55))
blue_square = pygame.image.load("res/square_blue.png")
blue_square = pygame.transform.scale(blue_square, (55, 55))
blue_triangle = pygame.image.load("res/triangle_blue.png")
blue_triangle = pygame.transform.scale(blue_triangle, (55, 55))

block = pygame.image.load("res/block.png")
block = pygame.transform.scale(block, (55, 55))

health_pickup = pygame.image.load("res/health_pickup.png")
health_pickup = pygame.transform.scale(health_pickup, (55, 55))

red_images = [red_circle, red_square, red_triangle]
blue_images = [blue_circle, blue_square, blue_triangle]
gun_images = [short_gun, long_gun, blast_gun]

piece_list = ['circle', 'square', 'triangle']
gun_list = ['short_gun', 'long_gun', 'blast_gun']

# Sounds
fire_sfx = pygame.mixer.Sound("res/Sounds/fire.mp3")
reload_sfx = pygame.mixer.Sound("res/Sounds/reload.mp3")
piece_place_sfx = pygame.mixer.Sound("res/Sounds/piece_place.mp3")
death_sfx = pygame.mixer.Sound("res/Sounds/death.mp3")

def draw_board():
    for i in range(NO_OF_SQUARES):
        for j in range(NO_OF_SQUARES):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, "light gray", [j * 80, i * 80, 80, 80])

            if i == 0 or j == 0:
                continue
            pygame.draw.line(screen, "black", (0, 80 * i), (BOARD_WIDTH, 80 * i), 2)
            pygame.draw.line(screen, "black", (80 * j, 0), (80 * j, BOARD_HEIGHT), 2)


def draw_piece():
    # Red
    for i in range(len(red_pieces)):
        if i in dead_red:
            continue

        index = piece_list.index(red_pieces[i])
        index_gun = gun_list.index(red_guns[i])
        screen.blit(red_images[index], (red_locations[i][0] * 80 + 12.5, red_locations[i][1] * 80 + 20.5))

        # Guns
        if red_guns[i] == 'blast_gun':
            screen.blit(gun_images[index], (red_locations[i][0] * 80 + 50, red_locations[i][1] * 80 + 5))
        else:
            screen.blit(gun_images[index], (red_locations[i][0] * 80 + 48, red_locations[i][1] * 80 + 8))

        #Health bar
        pygame.draw.rect(screen, "red", [red_locations[i][0] * 80 + 15, red_locations[i][1] * 80 + 12.5, 30, 7])
        pygame.draw.rect(screen, "dark green",
                         [red_locations[i][0] * 80 + 15, red_locations[i][1] * 80 + 12.5, red_healths[i], 7])

        if cur_state < 3:
            if selection == i:
                pygame.draw.rect(screen, 'red', [red_locations[i][0] * 80 + 1, red_locations[i][1] * 80 + 1,
                                                 80, 80], 4)

    # Blue
    for i in range(len(blue_pieces)):
        if i in dead_blue:
            continue

        index = piece_list.index(blue_pieces[i])
        screen.blit(blue_images[index], (blue_locations[i][0] * 80 + 12.5, blue_locations[i][1] * 80 + 20.5))

        # Guns
        if red_guns[i] == 'blast_gun':
            screen.blit(gun_images[index], (blue_locations[i][0] * 80 + 50, blue_locations[i][1] * 80 + 5))
        else:
            screen.blit(gun_images[index], (blue_locations[i][0] * 80 + 48, blue_locations[i][1] * 80 + 8))

        # Health bar
        pygame.draw.rect(screen, "red", [blue_locations[i][0] * 80 + 15, blue_locations[i][1] * 80 + 12.5, 30, 7])
        pygame.draw.rect(screen, "dark green",
                         [blue_locations[i][0] * 80 + 15, blue_locations[i][1] * 80 + 12.5, blue_healths[i], 7])

        if cur_state >= 3:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [blue_locations[i][0] * 80 + 1, blue_locations[i][1] * 80 + 1,
                                                  80, 80], 4)

def spawn_health_pickup(exist):
    if exist == 0:
        exist = 1
        while True:
            a = (random.randint(0, 9), random.randint(2, 7))
            if a not in red_locations and a not in blue_locations:
                health_pickup_location.append(a)
                screen.blit(health_pickup, (a[0] * 80 + 48, a[1] * 80 + 8))
                break


def set_random_block_location():
    a = 5
    for i in range(0, a):
        b = (random.randint(0, 9), random.randint(2, 7))
        if b in block_locations:
            a = + 1
        else:
            block_locations.append(b)

def draw_blocks():
    for i in range(len(block_locations)):
        screen.blit(block, (block_locations[i][0] * 80 + 13, block_locations[i][1] * 80 + 13))

def blast_damage(position, _red_locations, _blue_locations):
    print("Blast")
    #print('position')
    #print(position)
    for i in range(len(red_pieces)):
        a = abs(position[0] - _red_locations[i][0])
        b = abs(position[1] - _red_locations[i][1])

        #print((_red_locations[i][0], _red_locations[i][1]))
        if a + b == 0:
            red_healths[i] -= 29
        elif (a + b) == 1:
            red_healths[i] -= 14
        elif (a + b) == 2:
            if (position[0] + 1, position[1] + 1) == (_red_locations[i][0], _red_locations[i][1]):
                red_healths[i] -= 7
            elif (position[0] + 1, position[1] - 1) == (_red_locations[i][0], _red_locations[i][1]):
                red_healths[i] -= 7
            elif (position[0] - 1, position[1] - 1) == (_red_locations[i][0], _red_locations[i][1]):
                red_healths[i] -= 7
            elif (position[0] - 1, position[1] + 1) == (_red_locations[i][0], _red_locations[i][1]):
                red_healths[i] -= 7

    for i in range(len(blue_pieces)):
        a = abs(position[0] - _blue_locations[i][0])
        b = abs(position[1] - _blue_locations[i][1])
        if (a + b) == 0:
            blue_healths[i] -= 29
        elif (a + b) == 1:
            blue_healths[i] -= 14
        elif (a + b) == 2:
            if (position[0] + 1, position[1] + 1) == (_blue_locations[i][0], _blue_locations[i][1]):
                blue_healths[i] -= 7
            elif (position[0] + 1, position[1] - 1) == (_blue_locations[i][0], _blue_locations[i][1]):
                blue_healths[i] -= 7
            elif (position[0] - 1, position[1] - 1) == (_blue_locations[i][0], _blue_locations[i][1]):
                blue_healths[i] -= 7
            elif (position[0] - 1, position[1] + 1) == (_blue_locations[i][0], _blue_locations[i][1]):
                blue_healths[i] -= 7

def check_healths():
    #print(red_healths)
    #print(blue_healths)

    for i in range(len(red_pieces)):
        if i in dead_red:
            continue
        if red_healths[i] <= 0:
            captured_pieces_red.append(red_pieces[i])
            #red_pieces.pop(i)
            #red_locations.pop(i)
            #red_healths.pop(i)
            print("read dead")
            death_sfx.play()
            dead_red.append(i)

    for i in range(len(blue_pieces)):
        if i in dead_blue:
            continue
        if blue_healths[i] <= 0:
            captured_pieces_blue.append(blue_pieces[i])
            #blue_pieces.pop(i)
            #blue_locations.pop(i)
            #blue_healths.pop(i)
            print("blue dead")
            death_sfx.play()
            dead_blue.append(i)


def draw_valid(moves):
    if cur_state < 3:
        color = "red"
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 80 + 40, moves[i][1] * 80 + 40), 5)


def draw_valid_shoots(moves):
    if cur_state < 3:
        color = "red"
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, "gray", (moves[i][0] * 80 + 40, moves[i][1] * 80 + 40), 5)


# Initialize Pygame
pygame.init()
set_random_block_location()
# Load the background music
pygame.mixer.music.load('res/Sounds/background_music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# game loop
run = True

while run:
    timer.tick(fps)
    screen.fill("dark gray")
    check_healths()
    draw_board()
    draw_piece()
    draw_blocks()
    
    if selection != 100:
        if cur_state == 1:
            draw_valid_shoots(valid_shoots)
        elif cur_state == 2:
            draw_valid(valid_steps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            x_coord = event.pos[0] // 80
            y_coord = event.pos[1] // 80
            clicked_coords = (x_coord, y_coord)
            
            if cur_state == 0: # no selection
                if clicked_coords in red_locations:
                    piece_place_sfx.play()
                    
                    selection = red_locations.index(clicked_coords)
                    
                    type = red_pieces[selection]
                    pos = red_locations[selection]
                    
                    valid_shoots = get_valid_shoots(type, pos)
                        
                    cur_state = 1
                    
            elif cur_state == 1: # red piece selected for shoot 
                if clicked_coords in red_locations:
                    piece_place_sfx.play()
                    
                    selection = red_locations.index(clicked_coords)
                    
                    type = red_pieces[selection]
                    pos = red_locations[selection]
                    
                    valid_shoots = get_valid_shoots(type, pos)
                        
                elif clicked_coords in valid_shoots:
                    fire_sfx.play()
                    
                    valid_shoots = []
                    ###
                    if selection == 2:
                        blast_damage(clicked_coords, red_locations, blue_locations)

                    elif clicked_coords in blue_locations:
                        x = blue_locations.index(clicked_coords)

                        if x not in dead_blue:
                            blue_piece = blue_locations.index(clicked_coords)
                            blue_healths[blue_piece] -= 10
                            # if blue_healths[blue_piece] <= 0:
                            #     captured_pieces_blue.append(blue_pieces[blue_piece])
                            #     blue_pieces.pop(blue_piece)
                            #     blue_locations.pop(blue_piece)

                    spawn_health_pickup(health_pickup_exist)
                    ###
                    type = red_pieces[selection]
                    pos = red_locations[selection]
                    
                    valid_steps = get_valid_steps(type, pos, red_locations, blue_locations, block_locations)
                    cur_state = 2
                    
            elif cur_state == 2: # red piece selected for step
                if clicked_coords in valid_steps:
                    valid_steps = []
                    
                    red_locations[selection] = clicked_coords
                    
                    ###
                    #Clicked on health pickup
                    if health_pickup_location == clicked_coords:
                        red_healths[selection] += 10
                        health_pickup = 0
                        health_pickup_location.pop(0)
                    ###
                    reload_sfx.play()
                    ###
                    start = time.time()
                    output = alpha_beta_pruning(red_locations=red_locations, blue_locations=blue_locations, block_locations=block_locations,
                                             red_healths=red_healths, blue_healths=blue_healths, height=3, alpha=-1e9, beta=1e9)

                    end = time.time()

                    print("The time of execution of above program is :",(end-start) * 10**3, "ms")
                    print(output)

                    position = output[1]
                    step = output[2]
                    shoot = output[3]

                    idx = blue_locations.index(position)

                    blue_locations[idx] = position[0] + step[0], position[1] + step[1]

                    shoot_location = blue_locations[idx][0] + shoot[0], blue_locations[idx][1] + shoot[1]

                    print(shoot_location)
                    if shoot_location in red_locations:

                        y = red_locations.index(shoot_location)

                        if y not in dead_red:
                            red_piece = red_locations.index(shoot_location)
                            red_healths[red_piece] -= 10

                    cur_state = 0

    pygame.display.flip()

pygame.quit()
