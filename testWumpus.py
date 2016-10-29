import updatewumpus

name = updatewumpus.intialize_world()
bindings = {}

print updatewumpus.take_action(name, "Up")
here = updatewumpus.take_action(name, "Step")
if here[0] == 'nasty':
	for cell in updatewumpus.look_ahead(name):
		statement = ('wumpus', cell)
		pattern = ('wumpus', '?x') 
		binding = FOPC.match(statement,pattern,bindings)
		




updatewumpus.take_action(name, "Exit")
