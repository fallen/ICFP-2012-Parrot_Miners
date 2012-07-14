import sys, os,  tty, termios
import copy
from mapupdater import world
from threading import Event

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
			

class explorer:
	def __init__(self, world):
		self.world = copy.deepcopy(world)
		self.actionspoints = {}
		
	def explore(self, move):
		cworld = self.world
		cworld.set_movement(move)
	
class botcontroler(controler):
	
	def __init__(self, world):
		controler.__init__(self, world)
		#~ ASF is Action State Value
		self.actions = ["U", "R", "L", "D"]
		self.ASV = {}
		for action in self.actions:
			self.ASV[(action, world.lambda_map)] = 0
	
	def explore_step(self, move, world):
		cworld = copy.deepcopy(world)
		cworld.set_movement(move)
		self.ASV[(move, world.lambda_map)] += cworld.get_points()
		
	def get_next(self):
		#~ exp = explorer(
		maxikey = key = "W"
		maxi = -1500
		for index, value in enumerate(self.actions):
			self.actionspoints[value] = self.explore(value)
			if maxi < self.actionspoints[value]:
				maxi = self.actionspoints[value]
				maxikey = value
		
		return maxikey
