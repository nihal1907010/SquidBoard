def valid(pos, dx, dy):
    x = pos[0] + dx
    y = pos[1] + dy
    return x >= 0 and x < 7 and y >= 0 and y < 7

def empty(pos, dx, dy, red, blue, block):
    new_pos = (pos[0] + dx, pos[1] + dy)
    return valid(pos, dx, dy) \
            and new_pos not in red \
            and new_pos not in blue \
            and new_pos not in block

def get_shoot_square(pos):
    locs = []
    dxdy = []
    if valid(pos, +1, 0):
        locs.append((pos[0] + 1, pos[1] + 0))
        dxdy.append((+1, 0))
        if valid(pos, +2, 0):
            locs.append((pos[0] + 2, pos[1] + 0))
            dxdy.append((+2, 0))
    if valid(pos, 0, +1):
        locs.append((pos[0] + 0, pos[1] + 1))
        dxdy.append((0, +1))
        if valid(pos, 0, +2):
            locs.append((pos[0] + 0, pos[1] + 2))
            dxdy.append((0, +2))
    if valid(pos, -1, 0):
        locs.append((pos[0] - 1, pos[1] + 0))  
        dxdy.append((-1, 0))      
        if valid(pos, -2, 0):
            locs.append((pos[0] - 2, pos[1] + 0))
            dxdy.append((-2, 0))
    if valid(pos, 0, -1):
        locs.append((pos[0] + 0, pos[1] - 1))  
        dxdy.append((0, -1))  
        if valid(pos, 0, -2):
            locs.append((pos[0] + 0, pos[1] - 2))
            dxdy.append((0, -2))  
    return locs
        
def get_shoot_triangle(pos):
    locs = []
    dxdy = []
    if valid(pos, +1, +1):
        locs.append((pos[0] + 1, pos[1] + 1))
        dxdy.append((+1, +1))  
        if valid(pos, +2, +2):
            locs.append((pos[0] + 2, pos[1] + 2))
            dxdy.append((+2, +2))  
    if valid(pos, -1, +1):
        locs.append((pos[0] - 1, pos[1] + 1))
        dxdy.append((-1, +1))  
        if valid(pos, -2, +2):
            locs.append((pos[0] - 2, pos[1] + 2))
            dxdy.append((-2, +2))  
    if valid(pos, -1, -1):
        locs.append((pos[0] - 1, pos[1] - 1))
        dxdy.append((-1, -1))  
        if valid(pos, -2, -2):
            locs.append((pos[0] - 2, pos[1] - 2))
            dxdy.append((-2, -2))  
    if valid(pos, +1, -1):
        locs.append((pos[0] + 1, pos[1] - 1))
        dxdy.append((+1, -1))  
        if valid(pos, +2, -2):
            locs.append((pos[0] + 2, pos[1] - 2))
            dxdy.append((+2, -2))  
    return locs
        
def get_shoot_circle(pos):
    locs = []
    dxdy = []
    if valid(pos, +2, 0):
        locs.append((pos[0] + 2, pos[1] + 0))
        dxdy.append((+2, 0))  
    if valid(pos, 0, +2):
        locs.append((pos[0] + 0, pos[1] + 2))
        dxdy.append((0, +2))  
    if valid(pos, -2, 0):
        locs.append((pos[0] - 2, pos[1] + 0))     
        dxdy.append((-2, 0))   
    if valid(pos, 0, -2):
        locs.append((pos[0] + 0, pos[1] - 2))   
        dxdy.append((0, -2))  
    return locs
    
def get_step_square(pos, red, blue, block):
    locs = []
    dxdy = []
    if empty(pos, +1, 0, red, blue, block):
        locs.append((pos[0] + 1, pos[1] + 0))
        dxdy.append((+1, 0))  
    if empty(pos, 0, +1, red, blue, block):
        locs.append((pos[0] + 0, pos[1] + 1))
        dxdy.append((0, +1))  
    if empty(pos, -1, 0, red, blue, block):
        locs.append((pos[0] - 1, pos[1] + 0))
        dxdy.append((-1, 0))  
    if empty(pos, 0, -1, red, blue, block):
        locs.append((pos[0] + 0, pos[1] - 1))
        dxdy.append((0, -1))  
    return locs

def get_step_triangle(pos, red, blue, block):
    locs = []
    dxdy = []
    if empty(pos, +1, +1, red, blue, block):
        locs.append((pos[0] + 1, pos[1] + 1))
        dxdy.append((+1, +1))
    if empty(pos, -1, +1, red, blue, block):
        locs.append((pos[0] - 1, pos[1] + 1))
        dxdy.append((-1, +1))
    if empty(pos, -1, -1, red, blue, block):
        locs.append((pos[0] - 1, pos[1] - 1))
        dxdy.append((-1, -1))
    if empty(pos, +1, -1, red, blue, block):
        locs.append((pos[0] + 1, pos[1] - 1))
        dxdy.append((+1, -1))
    return locs

def get_step_circle(pos, red, blue, block):
    locs = []
    dxdy = []
    if empty(pos, +1, 0, red, blue, block):
        locs.append((pos[0] + 1, pos[1] + 0))
        dxdy.append((+1, 0))
    if empty(pos, +1, +1, red, blue, block):
        locs.append((pos[0] + 1, pos[1] + 1))
        dxdy.append((+1, +1))
    if empty(pos, 0, +1, red, blue, block):
        locs.append((pos[0] + 0, pos[1] + 1))
        dxdy.append((0, +1))
    if empty(pos, -1, +1, red, blue, block):
        locs.append((pos[0] - 1, pos[1] + 1))
        dxdy.append((-1, +1))
    if empty(pos, -1, 0, red, blue, block):
        locs.append((pos[0] - 1, pos[1] + 0))
        dxdy.append((-1, 0))
    if empty(pos, -1, -1, red, blue, block):
        locs.append((pos[0] - 1, pos[1] - 1))
        dxdy.append((-1, -1))
    if empty(pos, 0, -1, red, blue, block):
        locs.append((pos[0] + 0, pos[1] - 1))
        dxdy.append((0, -1))
    if empty(pos, +1, -1, red, blue, block):
        locs.append((pos[0] + 1, pos[1] - 1))
        dxdy.append((+1, -1))
    return locs

def get_valid_shoots(type, pos):
    if type == 'square':
        valid_shoots = get_shoot_square(pos)
    elif type == 'triangle':
        valid_shoots = get_shoot_triangle(pos)
    elif type == 'circle':
        valid_shoots = get_shoot_circle(pos)
    return valid_shoots

def get_valid_steps(type, pos, red, blue, block):
    if type == 'square':
        valid_steps = get_step_square(pos, red, blue, block)
    elif type == 'triangle':
        valid_steps = get_step_triangle(pos, red, blue, block)
    elif type == 'circle':
        valid_steps = get_step_circle(pos, red, blue, block)
    return valid_steps