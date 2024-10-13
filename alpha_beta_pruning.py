import random
from fuzzy_inference import *
from genetic_algorithm import *

red_pieces = ['circle', 'square', 'triangle', 'square', 'circle']
blue_pieces = ['circle', 'square', 'triangle', 'square', 'circle']

def empty_position(position, red_locations, blue_locations, block_locations):
        return position[0] >= 0 and position[0] < 7 and \
                position[1] >= 0 and position[1] < 7 and \
                position not in red_locations and \
                position not in blue_locations and \
                position not in block_locations

def generate_steps_dxdy_circle(position, red_locations, blue_locations, block_locations):
    steps_dxdy = []
    new_position = position[0] + 0, position[1] + 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((+0, +1))

        # new_position = position[0] + 0, position[1] + 2
        # if empty_position(new_position, red_locations, blue_locations, block_locations):
        #     steps_dxdy.append((+0, +2))

    new_position = position[0] + 0, position[1] - 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((+0, -1))

        # new_position = position[0] + 0, position[1] - 2
        # if empty_position(new_position, red_locations, blue_locations, block_locations):
        #     steps_dxdy.append((+0, -2))

    new_position = position[0] + 1, position[1] + 0
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((+1, +0))

        # new_position = position[0] + 2, position[1] + 0
        # if empty_position(new_position, red_locations, blue_locations, block_locations):
        #     steps_dxdy.append((+2, +0))

    new_position = position[0] - 1, position[1] + 0
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((-1, +0))

        # new_position = position[0] - 2, position[1] + 0
        # if empty_position(new_position, red_locations, blue_locations, block_locations):
        #     steps_dxdy.append((-2, +0))

    return steps_dxdy

def generate_steps_dxdy_square(position, red_locations, blue_locations, block_locations):
    steps_dxdy = []
    new_position = position[0] + 1, position[1] + 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((+1, +1))

        # new_position = position[0] + 2, position[1] + 2
        # if empty_position(new_position, red_locations, blue_locations, block_locations):
        #     steps_dxdy.append((+2, +2))

    new_position = position[0] - 1, position[1] - 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((-1, -1))

        # new_position = position[0] - 2, position[1] - 2
        # if empty_position(new_position, red_locations, blue_locations, block_locations):
        #     steps_dxdy.append((-2, -2))

    new_position = position[0] - 1, position[1] + 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((-1, +1))

        # new_position = position[0] - 2, position[1] + 2
        # if empty_position(new_position, red_locations, blue_locations, block_locations):
        #     steps_dxdy.append((-2, +2))

    new_position = position[0] + 1, position[1] - 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((+1, -1))

        # new_position = position[0] + 2, position[1] - 2
        # if empty_position(new_position, red_locations, blue_locations, block_locations):
        #     steps_dxdy.append((+2, -2))

    return steps_dxdy

def generate_steps_dxdy_triangle(position, red_locations, blue_locations, block_locations):
    steps_dxdy = []
    new_position = position[0] - 1, position[1] + 0
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((-1, +0))

    new_position = position[0] - 1, position[1] + 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((-1, +1))

    new_position = position[0] + 0, position[1] + 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((+0, +1))

    new_position = position[0] + 1, position[1] + 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((+1, +1))

    new_position = position[0] + 1, position[1] + 0
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((+1, +0))

    new_position = position[0] + 1, position[1] - 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((+1, -1))

    new_position = position[0] + 0, position[1] - 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((+0, -1))

    new_position = position[0] - 1, position[1] - 1
    if empty_position(new_position, red_locations, blue_locations, block_locations):
        steps_dxdy.append((-1, -1))

    return steps_dxdy

def generate_steps_dxdy(position, piece_type, red_locations, blue_locations, block_locations):

    if piece_type == 'circle':
        return generate_steps_dxdy_circle(position, red_locations, blue_locations, block_locations)

    elif piece_type == 'square':
        return generate_steps_dxdy_square(position, red_locations, blue_locations, block_locations)

    elif piece_type == 'triangle':
        return generate_steps_dxdy_triangle(position, red_locations, blue_locations, block_locations)
    
def generate_shoots_dxdy(piece_type):
    if piece_type == 'circle':
        return [(0, -2), (0, -1), (0, +1), (0, +2), (-2, 0), (-1, 0), (+1, 0), (+2, 0)]
    elif piece_type == 'square':
        return [(-2, -2), (-1, -1), (+1, +1), (+2, +2), (-2, -2), (-1, -1), (+1, +1), (+2, +2)]
    elif piece_type == 'triangle':
        return [(0, -2), (0, +2), (-2, 0), (+2, 0)]

def alpha_beta_pruning(red_locations, blue_locations, block_locations, red_healths, blue_healths, height, alpha, beta):
    if height == 0:
        own_health = 0
        opponent_health = 0

        for h in blue_healths:
            own_health += h
        
        for h in red_healths:
            opponent_health += h

        own_health *= 100 / 150
        opponent_health *= 100 / 150

        fuzzy = random.randint(0, 10)

        if fuzzy == 0:
            score = own_health - opponent_health
        else:
            score = defuzzify(own_health=own_health, opp_health=opponent_health) 
            score = (score - 50) * 2000 / 100
        
        return score, (0, 0), (0, 0), (0, 0)

    if height % 2 == 1:
        size = len(blue_locations)
        optimal_score = -1e6
    else:
        size = len(red_locations)
        optimal_score = +1e6

    optimal_output = optimal_score, (0, 0), (0, 0), (0, 0)

    for idx in range(size):
        if height % 2 == 1:
            position = blue_locations[idx]
            piece_type = blue_pieces[idx]
            if blue_healths[idx] <= 0:
                continue
        else:
            position = red_locations[idx]
            piece_type = red_pieces[idx]
            if red_healths[idx] <= 0:
                continue


        steps_dxdy = generate_steps_dxdy(position=position, piece_type=piece_type, red_locations=red_locations,
                                         blue_locations=blue_locations, block_locations=block_locations)
        shoots_dxdy = generate_shoots_dxdy(piece_type)

        genetic = random.randint(0, 10)

        if genetic == 0:
            steps_dxdy, shoots_dxdy = genetic_algorithm(position=position, steps_dxdy=steps_dxdy, shoots_dxdy=shoots_dxdy,
                                            piece_type=piece_type, height=height, red_locations=red_locations,
                                            blue_locations=blue_locations,
                                            red_healths=red_healths, blue_healths=blue_healths)

        # print(steps_dxdy)
        # print(shoots_dxdy)

        for step_dxdy in steps_dxdy:
            for shoot_dxdy in shoots_dxdy:

                temp_red_locations = red_locations.copy()
                temp_blue_locations = blue_locations.copy()
                temp_red_healths = red_healths.copy()
                temp_blue_healths = blue_healths.copy()

                update_location_health(height=height, blue_healths=temp_blue_healths, red_healths=temp_red_healths, 
                                        red_locations=temp_red_locations, blue_locations=temp_blue_locations,
                                        piece_type=piece_type, position=position, step=step_dxdy, shoot=shoot_dxdy)
                

                output = alpha_beta_pruning(red_locations=temp_red_locations, blue_locations=temp_blue_locations, 
                                                     red_healths=temp_red_healths, blue_healths=temp_blue_healths, block_locations=block_locations, height=height - 1, alpha=alpha, beta=beta)
                
                score = output[0]

                if height % 2 == 1:
                    if score > optimal_score:
                        optimal_score = score
                        optimal_output = optimal_score, position, step_dxdy, shoot_dxdy
                    alpha = max(alpha, score)
                else:
                    if score < optimal_score:
                        optimal_score = score
                        optimal_output = optimal_score, position, step_dxdy, shoot_dxdy
                    beta = min(beta, score)

                if alpha >= beta:
                    break

    return optimal_output
