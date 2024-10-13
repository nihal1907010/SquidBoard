import multiprocessing as mp

def own_health_low(x):
    if x < 0 or x > 40:
        return 0
    elif x < 30:
        return 1
    elif x >= 30:
        return 1 - (x - 30) / (40 - 30)

def own_health_medium(x):
    if x < 20 or x > 70:
        return 0
    elif x <= 40:
        return 0 + (x - 20) / (40 - 20)
    elif x > 40 and x < 60:
        return 1
    elif x >= 60:
        return 1 - (x - 60) / (80 - 60)

def own_health_high(x):
    if x < 60 or x > 100:
        return 0
    elif x <= 70:
        return 0 + (x - 60) / (70 - 60)
    elif x > 70:
        return 1

def opp_health_low(x):
    if x < 0 or x > 40:
        return 0
    elif x < 25:
        return 1
    elif x >= 25:
        return 1 - (x - 25) / (40 - 25)

def opp_health_medium(x):
    if x < 25 or x > 75:
        return 0
    elif x <= 40:
        return 0 + (x - 25) / (40 - 25)
    elif x > 40 and x < 60:
        return 1
    elif x >= 60:
        return 1 - (x - 60) / (75 - 60)

def opp_health_high(x):
    if x < 60 or x > 100:
        return 0
    elif x <= 75:
        return 0 + (x - 60) / (75 - 60)
    elif x > 75:
        return 1

def adv_low(x):
    if x < 0 or x > 80:
        return 0
    elif x < 30:
        return 1
    elif x >= 30:
        return 1 - (x - 30) / (80 - 30)

def adv_medium(x):
    if x < 40 or x > 60:
        return 0
    elif x < 50:
        return 1
    elif x >= 50:
        return 1 - (x - 50) / (60 - 50)

def adv_high(x):
    if x < 50 or x > 100:
        return 0
    elif x <= 70:
        return 0 + (x - 50) / (70 - 50)
    elif x > 70:
        return 1

def evaluate_rules(own_health, opp_health):
    high1 = min(own_health_high(own_health), opp_health_low(opp_health))
    low1 = max(own_health_low(own_health), opp_health_high(opp_health))
    medium1 = min(own_health_high(own_health), opp_health_high(opp_health))
    medium2 = min(own_health_low(own_health), opp_health_low(opp_health))
    medium3 = min(own_health_medium(own_health), opp_health_medium(opp_health))
    high2 = max(own_health_high(own_health), opp_health_low(opp_health))
    low2 = min(own_health_medium(own_health), opp_health_high(opp_health))
    medium4 = max(own_health_medium(own_health), opp_health_low(opp_health))
    low3 = min(own_health_low(own_health), opp_health_medium(opp_health))
    low4 = max(own_health_medium(own_health), opp_health_high(opp_health))

    return {"low": max(low1, low2, low3, low4),
            "medium": max(medium1, medium2, medium3, medium4),
            "high": max(high1, high2)}

def defuzzify(own_health, opp_health):
    outputs = evaluate_rules(own_health=own_health, opp_health=opp_health)

    numerator = 0
    denominator = 0

    for i in range(100 + 1):
        low = min(outputs["low"], adv_low(i))
        medium = min(outputs["medium"], adv_medium(i))
        high = min(outputs["high"], adv_high(i))

        height = max(low, medium, high)

        numerator += height * i
        denominator += height

    return numerator / denominator

def update_location_health(height, blue_healths, blue_locations, red_healths, red_locations, piece_type, position, step, shoot):
    new_position = position[0] + step[0], position[1] + step[1]

    if height % 2 == 1:
        own_health = blue_healths
        own_locations = blue_locations
        opponent_health = red_healths
        opponent_locations = red_locations
    else:
        own_health = red_healths
        own_locations = red_locations
        opponent_health = blue_healths
        opponent_locations = blue_locations

    idx = own_locations.index(position)
    own_locations[idx] = new_position

    if piece_type == 'circle':
        shooting_location = new_position[0] + shoot[0], new_position[1] + shoot[1]
        if shooting_location in opponent_locations:
            index = opponent_locations.index(shooting_location)
            opponent_health[index] -= 10
    elif piece_type == 'square':
        shooting_location = new_position[0] + shoot[0], new_position[1] + shoot[1]
        if shooting_location in opponent_locations:
            index = opponent_locations.index(shooting_location)
            opponent_health[index] -= 10
    elif piece_type == 'triangle':
        shooting_location = new_position[0] + shoot[0], new_position[1] + shoot[1]
        if shooting_location in opponent_locations:
            index = opponent_locations.index(shooting_location)
            opponent_health[index] -= 10

def fuzzy_logic(position, step, shoot, height, blue_healths, red_healths, blue_locations, red_locations, piece_type):
    update_location_health(height=height, blue_healths=blue_healths, red_healths=red_healths,
                                                      red_locations=red_locations, blue_locations=blue_locations,
                                                      piece_type=piece_type, position=position, step=step, shoot=shoot)
    
    if height % 2 == 1:
        own_health = blue_healths
        opponent_health = red_healths
    else:
        own_health = red_healths
        opponent_health = blue_healths

    own_health_100 = 0
    opponent_health_100 = 0

    for h in own_health:
        own_health_100 += h

    own_health_100 = own_health_100 * 100.0 / 150

    for h in opponent_health:
        opponent_health_100 += h

    opponent_health_100 = opponent_health_100 * 100.0 / 150

    result = defuzzify(own_health=own_health_100, opp_health=opponent_health_100)

    return result