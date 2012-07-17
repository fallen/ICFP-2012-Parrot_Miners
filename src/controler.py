import sys, os,  tty, termios
import copy
from mapupdater import world
from threading import Event
import random
import time
from displayer import MapDrawer
import pdb
import hashlib

			
def hash_the_world(world):
	hasher = hashlib.sha1()
	hasher.update(world.lambda_map.__str__())
	if (world.hasWater):
		hasher.update(world.waterworld.water.__str__())
	if (world.hasBeard):
		hasher.update(world.wadlersbeard.__str__())
	return hasher.digest()
	
class SimulatorDieEvent:
	stop_that=Event()
	def __init__(self):
		pass

class controler:
	def __init__(self, world):
		self.world = world

class kcontroler(controler):
	def __init__(self, world):
		controler.__init__(self, world)

	def get_next(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		tty.setraw(fd)
		key = sys.stdin.read(1)
		termios.tcsetattr(fd, termios.TCSANOW, old_settings)
	# in raw terminal mode CTRL+C is ASCII code 0x03
	# We exit upon CTRL+C
		if key == ' ':
			os.system("reset")
			SimulatorDieEvent.stop_that.set()
			sys.exit(0)

		if key == "z":
			return "U"
		if key == "s":
			return "D"
		if key == "q":
			return "L"
		if key == "d":
			return "R"
		if key == "a":
			return "A"
		if key == "w":
			return "W"
		if key == "e":
			return "S"

ACTIONS = ["U", "R", "L", "D"]

class explorerstate:
	def __init__(self, world):
		self.world = world
		self.actionsresults = {}
		self.actionspoints = {}
		self.hope = 0
		self.maxhopeaction = "A"
		self.arrived_with_w = False
		self.visited = False
		self.parents = []
		
	def explore(self, move, ASV):
		cworld = copy.deepcopy(self.world)
		if cworld.set_movement(move):
			if hash_the_world(cworld) not in ASV:
				self.actionsresults[move] = explorerstate(cworld)
				self.actionspoints[move] = cworld.get_points()
				ASV[hash_the_world(cworld)] = self.actionsresults[move]
				self.actionsresults[move].parent.append(self)
				return True
			else:
				self.actionsresults[move] = ASV[hash_the_world(cworld)]
				self.actionspoints[move] = cworld.get_points()
				self.actionsresults[move].parents.append(self)
		
		else:
			self.actionsresults[move] = None
			self.actionspoints[move] = None
		return False

	def __str__(self):
		print hex(id(self))
		MapDrawer(self.world.lambda_map,{}).draw()
		#~ for key, value in self.actionsresults.iteritems():
			#~ print key, " : "
			#~ if value != None:
				#~ MapDrawer(value.lambda_map).draw()
		
		print "hope : ", self.hope
		print "maxkey : ", self.maxhopeaction
		print "scoring :", self.actionspoints
		print "worlds :", self.actionsresults
		print "visited :", self.visited
		print "parent :", self.parents
		
		if self.arrived_with_w:
			print "origin : W"
		return ""

class botcontroler(controler):
	
	def __init__(self, world):
		controler.__init__(self, world)
		
		if world.hasBeard:
			actions.append("S")
			
		self.ASV = {}
		self.start = self.ASV[hash_the_world(world)] = explorerstate(world)
		self.updated = False
			
	def update_parents(self, current):
		if len(current.parents) != 0:
			for parent in current.parents:
				hopemax = -1500
				for move in parent.actionsresults:
					if parent.actionsresults[move] != None:
						hopemove = parent.actionspoints[move] + parent.actionsresults[move].hope
						if hopemove > hopemax:
							hopemax = hopemove
							parent.maxhopeaction = move

			
	def explore_step(self):
		current = self.start
		while(1):
			random.seed = time.clock()
			randmove = random.randint(0,len(ACTIONS)+len(current.parents))
			if randmove > len(ACTIONS):
				pdb.set_trace()
				current = current.parents[randmove - len(ACTIONS)]
			current.explore(randmove, self.ASV)
			if current.actionsresults[randmove] != None:
				current = current.actionsresults[randmove]
				self.update_parents(current)
		
		return True
			
		#~ print "************* END ****************************"
		#~ for value in self.ASV.values(): print value
		#~ print len(self.ASV)
		#~ print "*****************************************"
		#pdb.set_trace()
		return True

	def get_next(self):
		#for value in self.ASV.values(): print value
		#print len(self.ASV)
		#~ print "*****************************************"
		#~ print self.ASV[hash_the_world(self.world)]
		#~ pdb.set_trace()
		if not self.updated:
			self.updated = True
			#~ self.update()
			f = open("saved_map","w")
			stdout = sys.stdout
			sys.stdout = f
			print self.start
			print "**********************"
			for value in self.ASV.values(): print value
			sys.stdout = stdout
			
			
		state = self.start
		if not world :
			return "A"
		action = state.maxhopeaction
		if action != "A":
			if action not in state.actionsresults:
				return "A"
			self.start = state.actionsresults[action]
		return action
