import sys, os,  tty, termios
import copy
from mapupdater import world
from threading import Event
import random
import time
from displayer import MapDrawer
import pdb
import hashlib

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
		moved = cworld.set_movement(move)
		if moved:
			self.actionsresults[move] = cworld
			self.actionspoints[move] = cworld.get_points()
		else:
			self.actionsresults[move] = None
			self.actionspoints[move] = None
		return moved
	
	def __str__(self):
		MapDrawer(self.world.lambda_map).draw()
		#~ for key, value in self.actionsresults.iteritems():
			#~ print key, " : "
			#~ if value != None:
				#~ MapDrawer(value.lambda_map).draw()
		print "hope : ", self.hope
		return ""
			
def hash_the_world(world):
	return hashlib.sha1(world.lambda_map.__str__()).digest()

class botcontroler(controler):
	
	def __init__(self, world):
		controler.__init__(self, world)
		self.actions = ["U", "R", "L", "D"]
		self.ASV = {}
		self.ASV[hash_the_world(world)] = explorerstate(world)
		for action in self.actions:
				if self.ASV[hash_the_world(world)].explore(action):
					self.ASV[hash_the_world(self.ASV[hash_the_world(world)].actionsresults[action])] = explorerstate(self.ASV[hash_the_world(world)].actionsresults[action])
	
			
	def explore_step(self):
		world = self.world
		random.seed = time.clock()
		#~ randmove = self.actions[random.randint(0,len(self.actions)-1)]
		updatable_world = None
		while hash_the_world(world) in self.ASV:
			if len(self.ASV[hash_the_world(world)].actionsresults) == 0:
				updatable_world = world
				break
			randmove = self.actions[random.randint(0,len(self.actions)-1)]
			try_world = self.ASV[hash_the_world(world)].actionsresults[randmove]
			while try_world == None:
				randmove = self.actions[random.randint(0,len(self.actions)-1)]
				try_world = self.ASV[hash_the_world(world)].actionsresults[randmove]
			world = try_world
			
		if updatable_world:	
			for action in self.actions:
				if self.ASV[hash_the_world(updatable_world)].explore(action):
					self.ASV[hash_the_world(self.ASV[hash_the_world(updatable_world)].actionsresults[action])] = explorerstate(self.ASV[hash_the_world(updatable_world)].actionsresults[action])
			return True
		else:
			return False
			
		
	def update(self):
		#update each cell in reverse
		updated = False
		for value in reversed(self.ASV.values()):
			hopemax = -1500
			if len(value.actionsresults) > 0:
				for move in value.actionsresults.keys():
					if value.actionsresults[move] != None:
						hopemove = value.actionspoints[move] + self.ASV[hash_the_world(value.actionsresults[move])].hope
						if hopemove > hopemax:
							hopemax = hopemove
							value.maxhopeaction = move
							updated = True
						value.hope = hopemax

		#and normal order
		for value in self.ASV.values():
			hopemax = -1500
			if len(value.actionsresults) > 0:
				for move in value.actionsresults.keys():
					if value.actionsresults[move] != None:
						hopemove = value.actionspoints[move] + self.ASV[hash_the_world(value.actionsresults[move])].hope
						#~ print hopemove, hopemax
						if hopemove > hopemax:
							hopemax = hopemove
							value.maxhopeaction = move
							updated = True
						value.hope = hopemax
		#~ for value in self.ASV.values(): print value
		#~ print len(self.ASV)
		#~ print "*****************************************"
		#~ pdb.set_trace()
		return updated
		
	def get_next(self):
		#for value in self.ASV.values(): print value
		#print len(self.ASV)
		#~ print "*****************************************"
		#~ print self.ASV[hash_the_world(self.world)]
		world = self.world
		action = self.ASV[hash_the_world(world)].maxhopeaction
		if action == "W":
			action = "A"
		else:
			self.world = self.ASV[hash_the_world(world)].actionsresults[action]
		return action
