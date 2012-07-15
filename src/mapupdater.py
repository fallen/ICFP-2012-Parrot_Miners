import copy
import sys

class world:

	def __init__(self, lambda_map, waterstuff, trampolines):
		self.lambda_map = lambda_map
		self.lambdas = []
		#~ self.logger = debuglogger()
		self.won= False
		self.last_points=0
		self.waterworld=None
		self.killed=False
		self.warning=""
		self.death_cause=None
		self.waterworld=waterworld(self,waterstuff)
		self.trampolines = trampolines
		self.possible_trampolines = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
		self.trampoline_position = {}

		for x in range(len(self.lambda_map)):
			for y in range(len(self.lambda_map[x])):
				# if this is a trampoline target
				if self.lambda_map[x][y].isdigit() and int(self.lambda_map[x][y]) > 0:
					# we search wich trampoline it is the target of
					for trampoline, target in self.trampolines.iteritems():
						if target == int(self.lambda_map[x][y]):
							# We replace target number by the target coordinates
							# Target number is no longer needed
							self.trampolines[trampoline] = (x, y)
				if self.lambda_map[x][y] in self.possible_trampolines:
					self.trampoline_position[self.lambda_map[x][y]] = (x,y)
					
				if self.lambda_map[x][y] == 'R':
					self.robotpos = (x,y)
				if self.lambda_map[x][y] == '\\' or self.lambda_map[x][y] == '@':
					self.lambdas.append('\\')
		self.lambdasmax = len(self.lambdas)
	
	def get_points(self):
		return self.last_points

	def is_rock(self, char):
		return (char == '*') or (char == '@')

	def single_round(self):
		#allocate
		new_map = copy.deepcopy(self.lambda_map)
		#set it to ''
		for y in range(len(new_map[0])):
			for x in range(len(new_map)):
				if self.lambda_map[x][y] == '@':
					horock = True
				else:
					horock = False
				if self.is_rock(self.lambda_map[x][y]):
					#Rock falling straigth
					if self.lambda_map[x][y-1] == ' ':
						new_map[x][y] = ' '
						if horock and self.lambda_map[x][y-2] != ' ':
							new_map[x][y-1] = '\\'
						else:
							new_map[x][y-1] = self.lambda_map[x][y]
						self.am_i_dead((x,y-1))
					#Rock rolling over rock to the right
					if self.is_rock(self.lambda_map[x][y-1]) and self.lambda_map[x+1][y] == ' ' and self.lambda_map[x+1][y-1] == ' ':
						new_map[x][y] = ' '
						if horock and self.lambda_map[x+1][y-2] != ' ':
							new_map[x+1][y-1] = '\\'
						else:
							new_map[x+1][y-1] = self.lambda_map[x][y]
						self.am_i_dead((x+1,y-1))
					#Rock rolling over rock to the left
					if self.is_rock(self.lambda_map[x][y-1]) and (self.lambda_map[x+1][y] != ' ' or self.lambda_map[x+1][y-1] != ' ') and self.lambda_map[x-1][y] == ' ' and self.lambda_map[x-1][y-1] == ' ':
						new_map[x][y] = ' '
						if horock and self.lambda_map[x-1][y-2] != ' ':
							new_map[x-1][y-1] = '\\'
						else:
							new_map[x-1][y-1] = self.lambda_map[x][y]
						self.am_i_dead((x-1,y-1))
					#Rock rolling over lambda to the right
					if self.lambda_map[x][y-1] == '\\' and self.lambda_map[x+1][y] == ' ' and self.lambda_map[x+1][y-1] == ' ':
						new_map[x][y] = ' '
						if horock and self.lambda_map[x+1][y-2] != ' ':
							new_map[x+1][y-1] = '\\'
						else:
							new_map[x+1][y-1] = self.lambda_map[x][y]
						self.am_i_dead((x+1,y-1))
				# No lambdas left, opening lift
				if self.lambda_map[x][y] == 'L' and len(self.lambdas) == 0:
					new_map[x][y] = 'O'
						
		for x in range(len(new_map)):
			for y in range(len(new_map[x])):			
				self.lambda_map[x][y] = new_map[x][y]


	#If i have a rock over my head that's just been moved there, i'm dead :<
	#This must be called each time a rock moves
	def am_i_dead(self,rockpos):
		if self.robotpos[0] == rockpos[0] and self.robotpos[1] == rockpos[1]-1:
			self.death_cause="Robot died by rock at ("+str(rockpos[0])+","+str(rockpos[1])+")"
			self.kill()

	def print_status(self):
		if self.warning != "":
			print self.warning
		if self.killed:
			print self.death_cause
			print >> sys.stderr, 'Dead robot is dead :('
		print self.waterworld


	def kill(self):
		self.killed=True

	def move(self, x,y, xp,yp):
		self.last_points -= 1
		if self.lambda_map[xp][yp] == ' ' or self.lambda_map[xp][yp] == '.' or self.lambda_map[xp][yp] == '\\' or self.lambda_map[xp][yp] == 'o':
			if self.lambda_map[xp][yp] == '\\':
				self.lambdas.remove('\\')
				self.last_points+=25
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			return True
		elif xp == x+1 and self.is_rock(self.lambda_map[xp][yp]) and self.lambda_map[x+2][y] == ' ':
			self.lambda_map[xp+1][yp] = self.lambda_map[xp][yp]
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			return True
		elif xp == x-1 and self.is_rock(self.lambda_map[xp][yp]) and self.lambda_map[x-2][y] == ' ':
			self.lambda_map[xp-1][yp] = self.lambda_map[xp][yp]
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			return True
		elif self.lambda_map[xp][yp] == 'O':
			self.last_points += 50 * self.lambdasmax
			self.won = True
			self.lambda_map[xp][yp] = 'R'
			self.robotpos = (xp,yp)
			self.lambda_map[x][y] = ' '
			return True
		elif self.lambda_map[xp][yp] in self.trampolines:
			(a,b) = self.trampolines[self.lambda_map[xp][yp]]
			del self.trampolines[self.lambda_map[xp][yp]]
			self.robotpos = (a,b)
			# Robot is teleported
			self.lambda_map[a][b] = 'R'
			# Hit trampoline disappears
			self.lambda_map[xp][yp] = ' '
			# Previous robot location is cleared
			self.lambda_map[x][y] = ' '
			# Searching for other trampolines targetting the same target
			# in order to delete them
			for trampoline in self.trampolines.keys():
				if self.trampolines[trampoline] == (a,b):
					(tx, ty) = self.trampoline_position[trampoline]
					self.lambda_map[tx][ty] = ' '
			return True
					
		else :
			return False
	
	def set_movement(self, move):
		self.last_points=0
		moved = False
		if move == "U":
			moved = self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0], self.robotpos[1]+1)
		if move == "D":
			moved = self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0], self.robotpos[1]-1)
		if move == "L":
			moved = self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0]-1, self.robotpos[1])
		if move == "R":
			moved = self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0]+1, self.robotpos[1])
		if move == "A":
			moved = False
		if move == "W":
			moved = True
			pass
		#~ self.logger.write(move)
		updated = self.single_round()
		if self.waterworld != None:
			self.waterworld.tick(self.robotpos[1])
		if (self.killed):
			self.last_points = -1500
			return True
		return moved or updated
			


class waterworld:
	def __init__(self,world,(water,flooding,waterproof)):
		self.waterproof=waterproof # number of steps we can survive underwater
		self.flooding=flooding # number of steps before water++
		self.water=water # altitude under which we're underwater
		self.counter=0
		self.next_flood=0
		self.world=world

	def reset_ticker(self):
		self.counter=0
		self.next_flood=0

#Call each round after map update
	def tick(self,y):
		if self.flooding>0:
			self.next_flood+=1
			if y <= self.water:
				self.world.warning="!UNDERWATER! water "+str(self.water)+" robot_y "+str(y)+" counter "+str(self.counter)
				if self.waterproof <= self.counter:
					self.world.kill()
					self.world.death_cause="Robot drowned : "+str(self.counter)+" steps underwater with "+str(self.waterproof)+" waterproof points"
				self.counter+=1
			else:
				self.counter=0 # We only count consecutive steps
				self.world.warning=""
			if self.next_flood == self.flooding:
				self.water+=1
				self.next_flood=0
		

		
	def __str__(self):
		res="Water "+str(self.water)+"\n"
		res=res+"Flooding "+str(self.flooding)+"\n"
		res=res+"Waterproof "+str(self.waterproof)+"\n"
		res=res+"Next flood "+ str(self.next_flood)+"\n"
		return res
		

class logger:
	
	loggedstr = ""
		
	def write(self, text):
		self.loggedstr = self.loggedstr+text
		#print self.loggedstr
	
class debuglogger(logger):
	f=open("output","w")	

	def __del__(self):
		#~ print "write_to_file"
		self.f.write(self.loggedstr)
		#~ self.f.close()

class normallogger(logger):
	
	def __del__(self):
		print self.loggedstr
