import updatewumpus

'''knowledge base: a dict of cell:percepts as key:value'''
world_map = {}
'''path: a dict of cell:last cell as key:value'''
agent_path = {}

''' find all cells possibly adjacent to a_cell'''
def all_adja(a_cell):
    # a_cell column
    cell_col = int(a_cell[-2])
    # a_cell row
    cell_row = int(a_cell[-1])
    # increment row by -1, 1 and increment column by -1, 1
    adja_list = ["Cell " + str(cell_col+1) + str(cell_row),
            "Cell " + str(cell_col-1) + str(cell_row),
            "Cell " + str(cell_col) + str(cell_row+1),
            "Cell " + str(cell_col) + str(cell_row-1)]
    return adja_list

'''move from _from cell to _to cell'''
def cell2cell(_from, _to):
    # print "from ", _from, " to ",_to
    from_row = int(_from[-1])
    to_row = int(_to[-1])
    from_column = int(_from[-2])
    to_column = int(_to[-2])
    # get direction based on row and column
    if from_row == to_row:
        if from_column < to_column:
            direction = 'Right'
        elif from_column > to_column:
            direction = 'Left'
        else:
            print "Move not possible"
    elif from_column == to_column:
        if from_row < to_row:
            direction = 'Up'
        elif from_row > to_row:
            direction = 'Down'
        else:
            print "Move not possible"
    else:
       print "Move not possible"
    # Step in direction
    updatewumpus.take_action(this_world, direction)
    updatewumpus.take_action(this_world, "Step")

'''returns True if a_cell is not a wumpus cell, otherwise False'''
def is_not_wumpus(a_cell):
    conclusion = False
    # in all cells around a_cell, if we have been to a neighboring cell and it did not have a stench, a_cell cannot be a wumpus cell 
    for cell in all_adja(a_cell):
        # if cell is beyond the border of the board, it won't be in world_map
        if cell in world_map:
            percepts = world_map.get(cell)
            if percepts[0] == 'clean':
                conclusion = True
                break
    return conclusion

'''returns True if a_cell is not a pit cell, otherwise False'''
def is_not_pit(a_cell):
    conclusion = False
    # in all cells around a_cell, if we have been to a neighboring cell and it did not have a breeze, a_cell cannot be a pit cell 
    for cell in all_adja(a_cell):
        # if cell is beyond the border of the board, it won't be in world_map
        if cell in world_map:
            percepts = world_map.get(cell)
            if percepts[1] == 'calm':
                conclusion = True
                break
    return conclusion

'''returns True is a_cell is safe (not a wumpus or pit cell), otherwise False'''
def is_safe(a_cell):
    return True if is_not_wumpus(a_cell) and is_not_pit(a_cell) else False

'''fills world_map with cell location and its percepts''' 
def store_info(a_cell):
    location = a_cell[5]
    if location not in world_map:
        world_map[location] = (a_cell[:4])

'''pick up gold and return True, if no gold, return False'''
def pickup_gold(a_cell):
    if a_cell[2] == 'glitter':
        a_cell = updatewumpus.take_action(this_world, "PickUp")
        # print "We picked up gold in ", a_cell[5]
        return True
    else:
        # print "There is no gold in ", a_cell[5]
        return False

'''returns True if agent is dead, else False'''
def agent_dead(a_cell):
    if a_cell[7] == 'dead':
        print "Agent is dead, game ends!"
        return True
    else:
        return False

'''return a list of neighbors from current cell'''
def get_neighbors():
    return updatewumpus.look_ahead(this_world)

'''main loop to traverse through the wumpus world'''
def move():
    # get initial percepts
    this_cell = updatewumpus.take_action(this_world, "Up")
    # loop breaks when either agent is dead or we have gold
    while not agent_dead(this_cell) and not pickup_gold(this_cell):
        # print "No gold yet, agent alive!\n"
        # store this_cell's percepts to world_map
        store_info(this_cell)
        # get list of cells agent can go to
        nearby_cells = get_neighbors()
        # print "Nearby cells are ", nearby_cells
        safe_cells = []
        # if this_cell is clean and calm, all nearby cells are safe
        if this_cell[0] == 'clean' and this_cell[1] == 'calm':
            safe_cells = nearby_cells
        else:
            # checks if any nearby cells are safe and add to safe list
            for cell in nearby_cells:
                if is_safe(cell):
                    safe_cells.append(cell)
        # all the cells agent has been to
        visited = [k for k,v in agent_path.iteritems()]
        possible_cells = []
        # only want to go to cells agent has not been to
        for cell in safe_cells:
            if cell not in visited:
                possible_cells.append(cell)
        # we have exhausted options for current cell, move back one cell
        if len(possible_cells) == 0:
            cell2cell(this_cell[5], agent_path.get(this_cell[5]))
            # update this_cell to get current percepts
            this_cell = updatewumpus.take_action(this_world, "Up")
        # we have possible cells, go to any one
        else:
            # print "Possible cells are ", possible_cells
            cell = possible_cells.pop()
            # add current cell and the next cell to agent path
            agent_path[cell] = this_cell[5]
            cell2cell(this_cell[5], cell)
            # update this_cell to get current percepts
            this_cell = updatewumpus.take_action(this_world, "Up")
    # agent is currently at a cell with gold if agent is alive
    if not agent_dead(this_cell):
        pickup_gold(this_cell)
        # going back to exit via agent path
        while this_cell[5] != "Cell 11":
            cell2cell(this_cell[5], agent_path.get(this_cell[5]))
            # update this_cell to get current percepts
            this_cell = updatewumpus.take_action(this_world, "Up")
        # Exit at cell 11
        updatewumpus.take_action(this_world, "Exit")

this_world = updatewumpus.intialize_world()
move()
