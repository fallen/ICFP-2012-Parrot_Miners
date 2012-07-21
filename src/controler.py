import sys, os,  tty, termios
import copy
from mapupdater import world
from threading import Event
import random
import time
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
		if key == "e":
			return "S"

ACTIONS = ["U", "R", "L", "D"]

class explorerstate:
	def __init__(self):
		self.actionsresults = {}
		self.actionspoints = {}
		self.hope = 0
		self.maxhopeaction = "A"
		self.visited = False
		
	def explore(self, world, move, ASV):
		if world.set_movement(move):
			world_hash = world.hash()
			if world_hash not in ASV:
				self.actionsresults[move] = explorerstate()
				self.actionspoints[move] = world.get_points()
				ASV[world_hash] = self.actionsresults[move]
				return True
			else:
				self.actionsresults[move] = ASV[world_hash]
				self.actionspoints[move] = world.get_points()
		
		else:
			self.actionsresults[move] = None
			self.actionspoints[move] = None
		return False

	def __str__(self):
		print hex(id(self))
		#~ for key, value in self.actionsresults.iteritems():
			#~ print key, " : "
			#~ if value != None:
				#~ MapDrawer(value.lambda_map).draw()
		# TODO : print the map
		print "hope : ", self.hope
		print "maxkey : ", self.maxhopeaction
		print "scoring :", self.actionspoints
		print "worlds :", self.actionsresults
		print "visited :", self.visited
		return ""

class botcontroler(controler):
	
	def __init__(self, world):
		controler.__init__(self, copy.deepcopy(world))
		
		#~ if world.hasBeard:
			#~ ACTIONS.append("S")		
		self.ASV = {}
		self.start = self.ASV[self.world.hash()] = explorerstate()
		#~ print self.start
		self.updated = False
		self.solution_trace_len = 0
		self.final_trace = []
		
		self.exp_step_per_sec = 0
		self.start_count = 0
		
	def update(self, current, world=None):
		hopemax = -1500
		if world and world.won:
			current.hope = world.get_points()
			return
		for move in current.actionsresults:
			if current.actionsresults[move] != None:
				hopemove = current.actionspoints[move] + current.actionsresults[move].hope
				if hopemove > hopemax:
					hopemax = hopemove
					current.maxhopeaction = move
		current.hope = hopemax
		
	def explore_step(self):
		#uncomment to mesure perf
		#~ self.exp_step_per_sec +=1
		#~ if self.start_count == 0:
			#~ self.start_count = time.clock()+1
		#~ elif self.start_count < time.clock():
			#~ print self.exp_step_per_sec, " step/s"
			#~ self.start_count = 0
			#~ self.exp_step_per_sec=0
		
		trace = []
		curiosity = 10
		
		self.world.reset()
		current = self.ASV[self.world.hash()]
		trace.append(current)
		#~ print "exploring_step"
		trace_max = self.world.num_cols * self.world.num_rows
		ACTIONS_len = len(ACTIONS)
		while current and not self.world.won and not self.world.killed and len(trace) < trace_max:
			randomize = False
			# check if we can still move
			if len(current.actionsresults) == len(ACTIONS):
				if len([item for item in current.actionsresults if (current.actionsresults[item] not in trace and current.actionsresults[item] != None)]) == 0:
					break
					
			random.seed = time.clock()
								
			if current.maxhopeaction != "A":
				next_move = current.maxhopeaction
				randomize = random.randint(0,100) < curiosity
			else:
				randomize = True
			
			if randomize:
				next_move = ACTIONS[random.randint(0, len(ACTIONS)-1)]		
			
			current.explore(self.world, next_move, self.ASV)

			
			if current.actionsresults[next_move] and current.actionsresults[next_move] not in trace:
				
				#~ os.system("clear")
				#~ print self.world
				#~ print current
				#~ time.sleep(0.1)
				self.world.validate(True)
				current = current.actionsresults[next_move]
				trace.append(current)
			else:
				self.world.validate(False)
			
		self.update(trace.pop(), self.world)
		
		trace.reverse()
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
		if self.solution_trace_len > self.world.num_cols * self.world.num_rows:
			return "A"
		state = self.start
		self.final_trace.append(state)
		if len(self.final_trace) > 3:
			if self.final_trace[len(self.final_trace)-1] == self.final_trace[len(self.final_trace)-3]:
				return "A"
				
		action = state.maxhopeaction
		if action != "A":
			if action not in state.actionsresults:
				return "A"
			self.start = state.actionsresults[action]
		return action
