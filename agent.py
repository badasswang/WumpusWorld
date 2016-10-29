import updatewumpus
import FOPC

'''
while agent is alive:
    while gold is none:
       get current percepts
       bind current percepts for current cell
       check current percepts for anomaly:
         gold
          if gold: pick up gold and set gold to true
         wumpus nearby?
         pit nearby?
         if both wumpus and pit nearby:
          there is only one safe cell near us besides the one we came from
       get list of nearby cells
       if wumpus nearby:
         flag nearby cells as dangerous
       if pit nearby:
         flag nearby cells as maybe_pit
       for each nearby cell in nearby cells that is not somewhere we went:
         check if there is a safe cell
          go to safe cell
         else:
          if a cell is both dangerous and maybe_pit:
              we check if we got nasty smell already in its nearby cells >= 2
              if not:
                 it may not be wumpus
              we check if we got breeze already in its nearbby cells >= 2
              if not:
                 it may not be pit
              if neither wumpus nor pit, we can go there
                 go to maybe safe cell
          no safe cell?
              we're stuck
    while gold is picked up:
       get list of safe cells
       connect cells
       exit
'''

world_map = {}

def all_adja(a_cell):
    cell_col = int(a_cell[-2])
    cell_row = int(a_cell[-1])
    adja_list = ["Cell " + str(cell_col+1) + str(cell_row),
            "Cell " + str(cell_col-1) + str(cell_row),
            "Cell " + str(cell_col) + str(cell_row+1),
            "Cell " + str(cell_col) + str(cell_row-1)]
    return adja_list

def cell2cell(_from, _to):
    print "from ", _from, " to ",_to
    if int(_from[-2]) > int(_to[-2]) & int(_from[-1]) == int(_to[-1]):
       direction = 'Left'
    elif int(_from[-2]) == int(_to[-2]) & int(_from[-1]) < int(_to[-1]):
       direction = 'Up'
    elif int(_from[-2]) == int(_to[-2]) & int(_from[-1]) > int(_to[-1]):
       direction = 'Down'
    else:
       direction = 'Right'
    this_cell = updatewumpus.take_action(this_world, direction)
    this_cell = updatewumpus.take_action(this_world, "Step")

def is_not_wumpus(a_cell):
    conclusion = False
    for cell in all_adja(a_cell):
        if cell in world_map:
            percepts = world_map.get(cell)
            if percepts[0] == 'clean':
                conclusion = True
                break
    return conclusion

def is_not_pit(a_cell):
    conclusion = False
    for cell in all_adja(a_cell):
        if cell in world_map:
            percepts = world_map.get(cell)
            if percepts[1] == 'calm':
                conclustion = True
                break
    return conclusion

def is_safe(a_cell):
    return True if is_not_wumpus(a_cell) and is_not_pit(a_cell) else False

def store_info(a_cell):
    location = a_cell[5]
    if location not in world_map:
        world_map[location] = (a_cell[:4])

def pickup_gold(a_cell):
    if a_cell[2] == 'glitter':
        a_cell = updatewumpus.take_action(this_world, "PickUp")
        gold = 1
        print "We picked up gold in ", a_cell[5]
    else:
        print "There is no gold in ", a_cell[5]

def agent_dead(a_cell):
    if a_cell[7] == 'dead':
        agent = 0
        print "Agent is dead, game ends!"

def get_neighbors():
    return updatewumpus.look_ahead(this_world)

def move():
    this_cell = updatewumpus.take_action(this_world, "Up") 
    agent_dead(this_cell)
    while agent:
        pickup_gold(this_cell)
        while not gold:
            print "No gold yet, agent alive!\n"
            store_info(this_cell)
            nearby_cells = get_neighbors()
            print "Nearby cells are ", nearby_cells
            safe_cells = []
            if this_cell[0] == 'clean' and this_cell[1] == 'calm':
                safe_cells = nearby_cells
            else:
                for cell in nearby_cells:
                    if is_safe(cell):
                        safe_cells.append(cell)
            print "Safe cells are ", safe_cells
            if len(safe_cells) == 0:
                return
            possible_cells = []
            for cell in safe_cells:
                if cell in nearby_cells:
                    possible_cells.append(cell)
            possible_cells.append(this_cell[5])
            while possible_cells:
                print "Possible cells are ", possible_cells
                for cell in possible_cells:
                    cell2cell(this_cell[5], cell)
                    move()

this_world = updatewumpus.intialize_world()
agent = 1
gold = 0
move()
