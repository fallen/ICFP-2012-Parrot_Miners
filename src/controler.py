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

class explorerstate:
	def __init__(self, world):
		self.world = world
		self.actionsresults = {}
		self.actionspoints = {}
		self.hope = 0
		self.maxhopeaction = "A"
		self.arrived_with_w = False
		self.visited = False

	def explore(self, move, ASV=None):
		cworld = copy.deepcopy(self.world)
		moved = cworld.set_movement(move)
		if moved:
			if hash_the_world(cworld) not in ASV:
				self.actionsresults[move] = cworld
				self.actionspoints[move] = cworld.get_points()
			else:
				if move not in self.actionsresults or self.actionsresults[move] == None:
					self.actionsresults[move] = ASV[hash_the_world(cworld)].world
					self.actionspoints[move] = cworld.get_points()
				else:
					return False
		else:
			if move not in self.actionsresults:
				self.actionsresults[move] = None
				self.actionspoints[move] = None
		return moved

	def __str__(self):
		print self.world
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
		if self.arrived_with_w:
			print "origin : W"
		return ""

class botcontroler(controler):
	
	def __init__(self, world):
		controler.__init__(self, world)
		
		self.actions = ["U", "R", "L", "D"]
		if world.wadlersbeard.hasBeards():

			self.actions.append("S")
		self.ASV = {}
		self.ASV[hash_the_world(world)] = explorerstate(world)
		self.updated = False
		for action in self.actions:
			if self.ASV[hash_the_world(world)].explore(action, self.ASV):
				self.ASV[hash_the_world(self.ASV[hash_the_world(world)].actionsresults[action])] = explorerstate(self.ASV[hash_the_world(world)].actionsresults[action])
				
		#~ self.update()
	
	def check_robot_near_beard(self,world):
		robotpos=world.robotpos
		lambda_map=world.lambda_map
		shave_useful=False
		for x in [robotpos[0] , robotpos[0] +1, robotpos[0] -1]:
			for y in [robotpos[1],robotpos[1]+1,robotpos[1]-1]:
				if lambda_map[x][y] == 'W':
					shave_useful=True
		return shave_useful and world.wadlersbeard.canShave()
	
	def explore_step(self):
		ret = False
		world = self.world
		updatable_world = None
		
		for value in self.ASV.iterkeys():
			if len(self.ASV[value].actionsresults) == 0:
				updatable_world = self.ASV[value].world
				break

		if updatable_world:
			if "S" in self.actions and not self.check_robot_near_beard(updatable_world):
				self.actions.remove("S")
			for action in self.actions:
				if self.ASV[hash_the_world(updatable_world)].explore(action, self.ASV) :
					if hash_the_world(self.ASV[hash_the_world(updatable_world)].actionsresults[action]) not in self.ASV:
						self.ASV[hash_the_world(self.ASV[hash_the_world(updatable_world)].actionsresults[action])] = explorerstate(self.ASV[hash_the_world(updatable_world)].actionsresults[action])
						#~ if action == "W":
							#~ self.ASV[hash_the_world(self.ASV[hash_the_world(updatable_world)].actionsresults[action])].arrived_with_w = True
			#~ print "************* END ****************************"
			#~ for value in self.ASV.values(): print value
			#print len(self.ASV)
			#~ print "*****************************************"
			return True
		else:
			return False
			
		#~ print "************* END ****************************"
		#~ for value in self.ASV.values(): print value
		#~ print len(self.ASV)
		#~ print "*****************************************"
		#pdb.set_trace()
		return True
		
	def recurse_update(self, world):
		#if hash_the_world(world) in self.ASV.keys():
		if self.time_max - time.clock() < 0:
			raise RuntimeError
		value = self.ASV[hash_the_world(world)]
		#~ else:
			#~ return
		if value.visited:
			return
		value.visited = True
		#initialize to a possible path
		if value.world.killed:
			value.hope = -1500
			value.visited = True
			return
		if len(value.actionsresults) > 0:
			for i in value.actionsresults.iterkeys():
				if value.actionsresults[i] != None:
					if self.ASV[hash_the_world(value.actionsresults[i])].actionsresults != []:
						value.maxhopeaction = value.actionsresults.keys()[0]
			#~ print value.maxhopeaction
			hopemax = -1500
			for move in value.actionsresults.iterkeys():
				if value.actionsresults[move] != None:
						self.recurse_update(value.actionsresults[move])
			#update value
			for move in value.actionsresults.iterkeys():
				if value.actionsresults[move] != None:
					hopemove = value.actionspoints[move] + self.ASV[hash_the_world(value.actionsresults[move])].hope
					if hopemove > hopemax:
						hopemax = hopemove
						value.maxhopeaction = move
			value.hope = hopemax

				#~ if value.actionsresults[move] != None and hash_the_world(value.actionsresults[move]) in self.ASV:
						#~ hopemove = value.actionspoints[move] + self.ASV[hash_the_world(value.actionsresults[move])].hope
					#	print hopemove, hopemax
						#~ if hopemove > hopemax:
							#~ hopemax = hopemove
							#~ value.maxhopeaction = move
							#~ updated = True
				#~ value.hope = hopemax
		#~ for value in self.ASV.values(): print value
		#~ print len(self.ASV)
		#~ print "*****************************************"
		#~ print self.ASV[hash_the_world(self.world)]
		#~ pdb.set_trace()
		
	def update(self):
		#update each cell in reverse
		for value in self.ASV.itervalues():
			value.visited = False
		self.time_max = time.clock() + 9.0
		try :
			while 1:
				self.recurse_update(self.world)
		except RuntimeError:
			print "exit"
			pass
		return True
		
	def get_next(self):
		#for value in self.ASV.values(): print value
		#print len(self.ASV)
		#~ print "*****************************************"
		#~ print self.ASV[hash_the_world(self.world)]
		#~ pdb.set_trace()
		if not self.updated:
			self.updated = True
			self.update()
#			f = open("saved_map","w")
#			stdout = sys.stdout
#			sys.stdout = f
#			print self.ASV[hash_the_world(self.world)]
#			print "**********************"
#			for value in self.ASV.values(): print value
#			sys.stdout = stdout
			
			
		world = self.world
		if not world :
			return "A"
		if hash_the_world(world) not in self.ASV:
			return "A"
		action = self.ASV[hash_the_world(world)].maxhopeaction
		if action != "A":
			if action not in self.ASV[hash_the_world(world)].actionsresults:
				return "A"
			self.world = self.ASV[hash_the_world(world)].actionsresults[action]
		return action
