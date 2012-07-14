import sys, os,  tty, termios
import copy
from mapupdater import world
from threading import Event
import random
import time
from displayer import MapDrawer
import pdb

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
			

class explorerstate:
	def __init__(self, world):
		self.world = world
		self.actionsresults = {}
		self.actionspoints = {}
		self.hope = 0
		self.maxhopeaction = "W"
		
	def explore(self, move):
		cworld = copy.deepcopy(self.world)
		cworld.set_movement(move)
		self.actionsresults[move] = cworld
		self.actionspoints[move] = cworld.get_points()
		
		
		
	
class botcontroler(controler):
	
	def __init__(self, world):
		controler.__init__(self, world)
		self.actions = ["U", "R", "L", "D", "A", "W"]
		self.ASV = {}
		self.ASV[world] = explorerstate(world)
		for action in self.actions:
				self.ASV[world].explore(action)
	
			
	def explore_step(self):
		pdb.set_trace()
		world = self.world
		random.seed = time.clock()
		randmove = self.actions[random.randint(0,len(self.actions))]
		updatable_world = None
		while world in self.ASV:
			if len(self.ASV[world].actionsresults) == 0:
				updatable_world = world
				break
			randmove = self.actions[random.randint(len(self.actions))]
			world = self.ASV[world].actionresults[randmove]
			
		if updatable_world:	
			self.ASV[updatable_world] = explorerstate(updatable_world)
			for action in self.actions:
				self.ASV[updatable_world].explore(action)
			return True
		else:
			return False
			
		
	def update(self):
		#update each cell in reverse
		updated = False
		for value in reversed(self.ASV.values()):
			for move in self.actions:
				hopemove = value.actionspoints[move] + self.ASV[value.actionsresults[move]].hope
				if hopemove > value.hope:
					value.hope = hopemove
					value.maxhopeaction = move
					updated = True

		#and normal order
		for value in enumerate(self.ASV.values()):
			for move in self.actions:
				hopemove = value.actionspoints[move] + self.ASV[value.actionsresults[move]].hope
				if hopemove > value.hope:
					value.hope = hopemove
					value.maxhopeaction = move
					updated = True
					
		return updated
		
	def get_next(self):
		world = self.world
		action = self.ASV[world].maxhopeaction
		self.world = self.ASV[world].actionsresults[action]
		return action
