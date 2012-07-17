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
	hasher.update(world.lambda_map.__str__().replace(".", " "))
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
		self.hope = -1500
		self.maxhopeaction = "A"
		self.visited = False
		
	def explore(self, move, ASV):
		cworld = copy.deepcopy(self.world)
		if cworld.set_movement(move):
			cworld_hash = hash_the_world(cworld)
			if cworld_hash not in ASV:
				self.actionsresults[move] = explorerstate(cworld)
				self.actionspoints[move] = cworld.get_points()
				ASV[cworld_hash] = self.actionsresults[move]
				return True
			else:
				self.actionsresults[move] = ASV[cworld_hash]
				self.actionspoints[move] = cworld.get_points()
		
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
		return ""

class botcontroler(controler):
	
	def __init__(self, world):
		controler.__init__(self, copy.deepcopy(world))
		
		if world.hasBeard:
			actions.append("S")
			
		self.ASV = {}
		self.start = self.ASV[hash_the_world(world)] = explorerstate(world)
		self.updated = False
		self.solution_trace_len = 0
			
	def update(self, current):
		hopemax = -1500
		for move in current.actionsresults:
			if current.actionsresults[move] != None:
				hopemove = current.actionspoints[move] + current.actionsresults[move].hope
				if hopemove > hopemax:
					hopemax = hopemove
					current.maxhopeaction = move
		current.hope = hopemax
			
	def explore_step(self):
		trace = []
		trace_len = 0
		curiosity = 25
		
		current = self.start
		trace.append(current)
		#~ print "exploring_step"
		trace_max = self.start.world.num_cols * self.start.world.num_rows
		ACTIONS_len = len(ACTIONS)
		while current and not (current.world.killed) and trace_len < trace_max:
			randomize = False
			# check if we can still move
			if len(current.actionsresults) == ACTIONS_len:
				breakable = True
				for i in ACTIONS:
					if current.actionsresults[i] != None and current.actionsresults[i] not in trace:
						breakable = False
						break
				#if not, break the while
				if breakable:
					break
					
			if current.maxhopeaction != "A":
				next_move = current.maxhopeaction
				randomize = random.randint(0,100) < curiosity
			else:
				randomize = True
			
			random.seed = time.clock()
			if randomize:
				next_move = ACTIONS[random.randint(0, len(ACTIONS)-1)]
			#~ print "current :", current
			#~ print "trace : ", trace
			#~ pdb.set_trace()
			current.explore(next_move, self.ASV)
			if current.actionsresults[next_move] and current.actionsresults[next_move] not in trace:
				current = current.actionsresults[next_move]
				trace.append(current)
				# Better to have a variable to record trace length instead of calculating it over and over again
				trace_len += 1
		#pdb.set_trace()
		trace.reverse()
		#~ reverse_start = current
		#~ while reverse_start != self.start:
			#~ self.update(reverse_start)
			#~ reverse_start = reverse_start.parent
		for state in trace:
			self.update(state)
			
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
		#~ if not self.updated:
			#~ print "saving map"
			#~ self.updated = True
			#~ self.update()
			#~ f = open("saved_map","w")
			#~ stdout = sys.stdout
			#~ sys.stdout = f
			#~ print self.start
			#~ print "**********************"
			#~ for value in self.ASV.values(): print value
			#~ sys.stdout = stdout
			
		self.solution_trace_len +=1
		if self.solution_trace_len > self.start.world.num_cols * self.start.world.num_rows:
			return "A"
		state = self.start
		action = state.maxhopeaction
		if action != "A":
			if action not in state.actionsresults:
				return "A"
			self.start = state.actionsresults[action]
		return action
