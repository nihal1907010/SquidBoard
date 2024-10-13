import random
from fuzzy_inference import *

def calculate_fitness(position, piece_type, height, red_locations, blue_locations, red_healths, blue_healths, moves):
    fitness_values = []
    total_fitness = 0
    for stepx, stepy, shootx, shooty in moves:

        temp_red_locations = red_locations.copy()
        temp_blue_locations = blue_locations.copy()
        temp_red_healths = red_healths.copy()
        temp_blue_healths = blue_healths.copy()

        fitness_value = fuzzy_logic(position=position, step=(stepx, stepy), shoot=(shootx, shooty),
                                    height=height, red_healths=temp_red_healths, red_locations=temp_red_locations,
                                    blue_healths=temp_blue_healths, blue_locations=temp_blue_locations,
                                    piece_type=piece_type)

        total_fitness += fitness_value
        fitness_values.append(fitness_value)
    return fitness_values, total_fitness

def genetic_algorithm(position, steps_dxdy, shoots_dxdy, piece_type, height, red_locations, blue_locations, red_healths, blue_healths):
    # Population Initialization
    moves = []
    for stepx, stepy in steps_dxdy:
        for shootx, shooty in shoots_dxdy:
            moves.append((stepx, stepy, shootx, shooty))

    total_moves = len(moves)

    if total_moves % 2 == 1:
        moves.pop(random.randint(0, total_moves))
        total_moves -= 1

    fitness_values, total_fitness = \
        calculate_fitness(position=position, piece_type=piece_type, height=height,
        red_locations=red_locations, blue_locations=blue_locations,
        red_healths=red_healths, blue_healths=blue_healths, moves=moves)

    actual_counts = [0] * total_moves
    temp_count = 0

    for idx in range(total_moves):
        probability = fitness_values[idx] / total_fitness
        expected_count = total_moves * probability
        actual_counts[idx] = round(expected_count)
        temp_count += actual_counts[idx]

    while temp_count < total_moves:
        for idx in range(total_moves):
            if temp_count < total_moves:
                actual_counts[idx] += 1
                temp_count += 1

    while temp_count > total_moves:
        for idx in range(total_moves):
            if actual_counts[idx] > 0 and temp_count > total_moves:
                actual_counts[idx] -= 1
                temp_count -= 1

    # Crossover
    mating_pool = []
    for idx in range(total_moves):
        for _ in range(actual_counts[idx]):
            mating_pool.append(moves[idx])

    new_moves = []

    for idx in range(0, total_moves, 2):
        move1, move2 = mating_pool[idx], mating_pool[idx + 1]

        stepx1, stepy1, shootx1, shooty1 = move1
        stepx2, stepy2, shootx2, shooty2 = move2

        move12 = stepx1, stepy1, shootx2, shooty2
        move21 = stepx2, stepy2, shootx1, shooty1

        new_moves.append(move12)
        new_moves.append(move21)

    fitness_values, total_fitness = calculate_fitness(position=position, piece_type=piece_type, height=height,
        red_locations=red_locations, blue_locations=blue_locations,
        red_healths=red_healths, blue_healths=blue_healths, moves=new_moves)

    max_fitness = 0
    for fitness in fitness_values:
        max_fitness = max(max_fitness, fitness)

    threshold = max_fitness * 0.9

    temp_steps_dxdy = []
    temp_shoots_dxdy = []

    for idx in range(total_moves):
        if fitness_values[idx] >= threshold:
            temp_steps_dxdy.append((new_moves[idx][0], new_moves[idx][1]))
            temp_shoots_dxdy.append((new_moves[idx][2], new_moves[idx][3]))
    
    return temp_steps_dxdy[:2], temp_shoots_dxdy[:2]