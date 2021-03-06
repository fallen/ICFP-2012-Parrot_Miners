import copy
import sys
import pdb

import hashlib

class world:
	def __init__(self, lambda_map,robotpos=None,lambdas=None, trampstuff=None, waterstuff=None, beardstuff=None):
			for x in range(1, len(lambda_map) - 1):
				for y in range(1,len(lambda_map[x]) - 1):
					point = lambda_map[x][y]
					if point == '.':
						removable = True
						for z in range(y,len(lambda_map[x]) - 1):
							if lambda_map[x][z] == '#':
								break
							if lambda_map[x][z] == '*' or lambda_map[x+1][z] == '*' or lambda_map[x-1][z] in ['*', '\\']:
								removable = False

						if removable:
							lambda_map[x][y] = ' '
		
			self.lambda_map = lambda_map
			self.new_map = copy.deepcopy(self.lambda_map)
			self.original_map = copy.deepcopy(self.lambda_map)
			#~ self.logger = debuglogger()
			self.won= False
			self.last_points=0
			#~ self.waterworld=None
			self.killed=False
			self.warning=""
			self.death_cause=None
			self.lambdamax = 0
			for x in range(len(self.lambda_map)):
				for y in range(len(self.lambda_map[0])):
					if self.lambda_map[x][y] == "\\":
						self.lambdamax+=1
					if self.lambda_map[x][y] == "R":
						self.robotpos = (x,y)
			self.lambdas = self.lambdamax
			self.previous_robotpos = self.original_robotpos = self.robotpos
			self.num_cols = len(self.lambda_map)
			self.num_rows = len(self.lambda_map[0])
			self.cols = range(self.num_cols)
			self.rows = range(self.num_rows)
			self.lambda_pickedup = False
			
			#~ self.hasBeard = self.wadlersbeard.hasBeards()
			#~ self.hasWater = (waterstuff[0] == 0) and (waterstuff[1] == 0)
			#~ self.hasTrampolines = len(trampstuff[0]) != 0

	
	def hash(self):
		hasher = hashlib.sha1()
		hasher.update(self.lambda_map.__str__())
		#~ if (world.hasWater):
			#~ hasher.update(world.waterworld.water.__str__())
		#~ if (world.hasBeard):
			#~ hasher.update(world.wadlersbeard.__str__())
		return hasher.digest()
		
	def reset(self):
		self.lambda_map = copy.deepcopy(self.original_map)
		self.won= False
		self.last_points=0
		self.killed=False
		self.warning=""
		self.death_cause=None
		self.robotpos = self.original_robotpos
		self.lambdas = self.lambdamax
		
	def __str__(self):
			map_str=""
			height=len(self.lambda_map[0])
			width=len(self.lambda_map)
			for y in range(height):
				for x in range(width):
					map_str+=(self.lambda_map[x][height - y-1])
				map_str += "\n"
			if self.warning != "":
				map_str+=self.warning
			if self.killed:
				map_str+=self.death_cause + "\n"
				print >> sys.stderr, 'Dead robot is dead :('
			#~ print self.waterworld
			#~ print self.wadlersbeard
			return map_str
			
	def get_points(self):
		return self.last_points

	def is_rock(self, char):
		return (char == '*') or (char == '@')

	def single_round(self):
		ret = False
		#set it to ''
		#~ self.wadlersbeard.startUpdate()
		new_map = copy.deepcopy(self.lambda_map)
		for y in self.rows:
			for x in self.cols:
				#~ if self.lambda_map[x][y] == '@':
					#~ horock = True
				#~ else:
				horock = False
				
				if self.is_rock(self.lambda_map[x][y]):
					#Rock falling straigth
					if self.lambda_map[x][y-1] == ' ':
						new_map[x][y] = ' '
						if horock and self.lambda_map[x][y-2] != ' ':
							new_map[x][y-1] = '\\'
						else:
							new_map[x][y-1] = self.lambda_map[x][y]
						ret = True
						self.am_i_dead((x,y-1))
					#Rock rolling over rock to the right
					if self.is_rock(self.lambda_map[x][y-1]) and self.lambda_map[x+1][y] == ' ' and self.lambda_map[x+1][y-1] == ' ':
						new_map[x][y] = ' '
						if horock and self.lambda_map[x+1][y-2] != ' ':
							new_map[x+1][y-1] = '\\'
						else:
							new_map[x+1][y-1] = self.lambda_map[x][y]
						ret = True
						self.am_i_dead((x+1,y-1))
					#Rock rolling over rock to the left
					if self.is_rock(self.lambda_map[x][y-1]) and (self.lambda_map[x+1][y] != ' ' or self.lambda_map[x+1][y-1] != ' ') and self.lambda_map[x-1][y] == ' ' and self.lambda_map[x-1][y-1] == ' ':
						new_map[x][y] = ' '
						if horock and self.lambda_map[x-1][y-2] != ' ':
							new_map[x-1][y-1] = '\\'
						else:
							new_map[x-1][y-1] = self.lambda_map[x][y]
						ret = True
						self.am_i_dead((x-1,y-1))
					#Rock rolling over lambda to the right
					if self.lambda_map[x][y-1] == '\\' and self.lambda_map[x+1][y] == ' ' and self.lambda_map[x+1][y-1] == ' ':
						new_map[x][y] = ' '
						if horock and self.lambda_map[x+1][y-2] != ' ':
							new_map[x+1][y-1] = '\\'
						else:
							new_map[x+1][y-1] = self.lambda_map[x][y]
						ret = True
						self.am_i_dead((x+1,y-1))
				# No lambdas left, opening lift
				if self.lambda_map[x][y] == 'L' and self.lambdas == 0:
					ret = True
					new_map[x][y] = 'O'
				# Growing beards if necessary
				#~ if self.lambda_map[x][y] == 'W':
					#~ self.wadlersbeard.tick(self.lambda_map,new_map)
				#~ # If robot wannashave, lets shavetheworld
				#~ if self.lambda_map[x][y] == 'R' and self.wadlersbeard.wannaShave():
					#~ self.wadlersbeard.shavetheworld(x,y,self.lambda_map,new_map)
		for i in self.cols:
			self.lambda_map.pop()
		for x in self.cols:
			self.lambda_map.append(new_map[x])
		return ret
		
	def validate(self, valid):
		if not valid:
			self.lambda_map = self.lambda_saved
			self.robotpos = self.previous_robotpos
			self.won = False
			self.killed = False
		self.lambda_pickedup = False
	


	#If i have a rock over my head that's just been moved there, i'm dead :<
	#This must be called each time a rock moves
	def am_i_dead(self,rockpos):
		if self.robotpos[0] == rockpos[0] and self.robotpos[1] == rockpos[1]-1:
			self.death_cause="Robot died by rock at ("+str(rockpos[0])+","+str(rockpos[1])+")"
			self.kill()

	def kill(self):
		self.killed=True

	def move(self, x,y, xp,yp):
		self.previous_robotpos = self.robotpos
				
		if self.lambda_map[xp][yp] == ' ' or self.lambda_map[xp][yp] == '.' or self.lambda_map[xp][yp] == '\\' or self.lambda_map[xp][yp] == '!':
			if self.lambda_map[xp][yp] == '\\': # Pick up lambda
				self.lambda_pickedup = True
				self.lambdas-=1
				self.last_points+=25
			#~ if self.lambda_map[xp][yp] == '!': # Pick up razor
				#~ self.wadlersbeard.pickupRazor()
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			return True
		# Pushing rock to the right
		elif xp == x+1 and self.is_rock(self.lambda_map[xp][yp]) and self.lambda_map[x+2][y] == ' ':
			self.lambda_map[xp+1][yp] = self.lambda_map[xp][yp]
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			return True
		# Pushing rock to the left
		elif xp == x-1 and self.is_rock(self.lambda_map[xp][yp]) and self.lambda_map[x-2][y] == ' ':
			self.lambda_map[xp-1][yp] = self.lambda_map[xp][yp]
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			return True
		# Going into open lift
		elif self.lambda_map[xp][yp] == 'O':
			self.last_points += 50 * self.lambdamax
			self.won = True
			self.lambda_map[xp][yp] = 'R'
			self.robotpos = (xp,yp)
			self.lambda_map[x][y] = ' '
			return True
			
		# TRAMPOLINE, TRAMPOLINE !!!
		#~ elif self.lambda_map[xp][yp] in self.trampolines:
			#~ (a,b) = self.trampolines[self.new_map[xp][yp]]
			#~ del self.trampolines[self.lambda_map[xp][yp]]
			#~ self.robotpos = (a,b)
			#~ # Robot is teleported
			#~ self.lambda_map[a][b] = 'R'
			#~ # Hit trampoline disappears
			#~ self.lambda_map[xp][yp] = ' '
			#~ # Previous robot location is cleared
			#~ self.lambda_map[x][y] = ' '
			#~ # Searching for other trampolines targetting the same target
			#~ # in order to delete them
			#~ for trampoline in self.trampolines.iterkeys():
				#~ if self.trampolines[trampoline] == (a,b):
					#~ (tx, ty) = self.trampoline_position[trampoline]
					#~ self.lambda_map[tx][ty] = ' '
			#~ return True
					
		else :
			return False

	def set_movement(self, move):
		self.lambda_saved = copy.deepcopy(self.lambda_map)
		self.won = False
		self.last_points=-1
		moved = False
		self.shave=False # This is read if single_round to apply shave
		if move == "S" and self.wadlersbeard.razors == 0:
			return False
			
		if move == "U":
			if self.robotpos[1] + 1 > len(self.lambda_map)-1:
				return False
			moved = self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0], self.robotpos[1]+1)
		if move == "D":
			if self.robotpos[1] - 1 < 0:
				return False
			moved = self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0], self.robotpos[1]-1)
		if move == "L":
			if self.robotpos[0] - 1 < 0:
				return False
			moved = self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0]-1, self.robotpos[1])
		if move == "R":
			if self.robotpos[0] + 1 > len(self.lambda_map)-1:
				return False
			moved = self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0]+1, self.robotpos[1])
		
		if not moved and move in ["U", "D", "L", "R"]:
			return False
		
		#~ if move == "S":
			#~ self.wadlersbeard.setFlagShave()
			#~ moved = True
		if move == "A":
			self.last_points += 25 * (self.lambdamax - self.lambdas)
			moved = True
		#~ if move == "W":
			#~ moved = False
			#~ pass
		#~ self.logger.write(move)
		updated = self.single_round()
		#~ if self.waterworld != None:
			#~ self.waterworld.tick(self.robotpos[1])
		if (self.killed):
			self.last_points -= 1500
			return True
		#~ if move == "W" and updated:
			#~ pdb.set_trace()
		#~ if move=="W" and self.robotpos[0]+1 < len(self.lambda_map) and self.robotpos[0]-1 > 0 and self.robotpos[1]-1 > 0 and self.robotpos[1]+1 < len(self.lambda_map[0]) and self.lambda_map[self.robotpos[0]+1][self.robotpos[1]] not in ["."," "] and self.lambda_map[self.robotpos[0]-1][self.robotpos[1]] not in ["."," "] and self.lambda_map[self.robotpos[0]][self.robotpos[1]+1] not in ["."," "] and self.lambda_map[self.robotpos[0]][self.robotpos[1]-1] not in ["."," "]:
			#~ moved = True
		return moved

		def __deepcopy__(self, memo):
			print "deepcopy_called"
			exit(0)
			#~ newworld = world(copy.deepcopy(self.lambda_map, memo))
			#~ newworld.cols = self.cols
			#~ newworld.rows = self.rows
			#~ newworld.num_cols = self.num_cols
			#~ newworld.num_rows = self.num_rows
#~ 
			#~ if self.hasWater:
				#~ newworld.waterworld = copy.deepcopy(self.waterworld, memo)
				#~ newworld.hasWater = True
			#~ else:
				#~ newworld.hasWater = False
#~ 
			#~ if self.hasBeards:
				#~ newworld.wadlersbeard = copy.deepcopy(self.wadlersbeard, memo)
				#~ newworld.hasBeards = True
			#~ else:
				#~ newworld.hasBeards = False
#~ 
			#~ if self.hasTrampolines:
				#~ newworld.trampolines = copy.deepcopy(self.trampolines, memo)
				#~ newworld.trampoline_position = copy.deepcopy(self.trampoline_position, memo)
				#~ newworld.hasTrampolines = True
			#~ else:
				#~ newworld.hasTrampolines = False
#~ 
			#~ newworld.robotpos = self.robotpos
			#~ newworld.lambdasmax = self.lambdasmax
			#~ newworld.lambdas = copy.deepcopy(self.lambdas, memo)
			#~ newworld.killed = self.killed
			#~ return newworld
			


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
		

class wadlersbeard:
	def __init__(self,(razors,growth,beards)):
		self.razors=razors # Initial razors value
		self.growth_rate=growth # Number of steps before beards expansion
		self.beards=beards # list of 2-tuples of beards coordinates
		self.counter=self.growth_rate-1
		self.robotwannashave=False # Flag to check Shave action
		self.startupdate=True # This flag is set to True before map update. We can then detect first call to tick and update counter only once per update (instead of once per beard !!)

	def __str__(self):
		res="Razors "+str(self.razors)+"\n"
		res=res+"Growth counter "+str(self.counter)+"\n"
		res=res+"Beards coordinates "+str(self.beards)
		return res

	def startUpdate(self):
		self.startupdate=True

	def setFlagShave(self,value=True):
		self.robotwannashave=value

	def hasBeards(self):
		return len(self.beards) != 0

	def wannaShave(self):
		return self.robotwannashave


	# Add one razor
	def pickupRazor(self):
		self.razors+=1

	def shaveIfPossible(self,lambda_map,newmap,x,y):
		if lambda_map[x][y] == 'W' :
			newmap[x][y] = ' '

	# Use one razor and apply on map. This manages shave action
	def shavetheworld(self,x,y,lambda_map,newmap):
		if self.razors > 0 :
			self.razors-=1
			self.setFlagShave(False)
			for i in [ x, x+1 , x-1] :
				for j in [ y, y+1, y-1 ] :
					#9 cases checked even if only 8 are useful
					self.shaveIfPossible(lambda_map,newmap,i,j)
		else:
			pass
			#raise Exception("Can't shave without razors ! Should've used more canShave() !")


	# Have we enough razors to shave ?
	def canShave(self):
		return self.razors==0

	def expandBeardIfPossible(self,lambda_map,newmap, x,y):
		if lambda_map[x][y] == ' ':
			newmap[x][y] = 'W'
			return (x,y)
		else:
			return None

	#This will modify world to set new beards if necessary. It manages environement beard growth
	def tick(self,lambda_map,newmap):
		if self.counter == 0:
			self.counter=self.growth_rate-1
			newbeards=[]
			for (bx, by) in self.beards:
				# for each beard, expand if possible. 9 cases checked even if only 8 are useful
				#print "Try expand beard "+str(bx)+" "+str(by)
				for x in [ bx+1, bx, bx-1 ] :
					for y in [ by ,by+1,by-1 ]:
						res=self.expandBeardIfPossible(lambda_map,newmap,x,y)
						if res != None :
							newbeards.append(res)
			self.beards.extend(newbeards)
		else:
			if self.startupdate:
				self.counter-=1
				self.startupdate=False


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
