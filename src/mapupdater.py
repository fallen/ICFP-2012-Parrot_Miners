import copy
import sys
import pdb

class world:
	
	def __init__(self, lambda_map, waterstuff):
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
		
		for x in range(len(self.lambda_map)):
			for y in range(len(self.lambda_map[x])):
				if self.lambda_map[x][y] == 'R':
					self.robotpos = (x,y)
				if self.lambda_map[x][y] == '\\':
					self.lambdas.append((x,y))
		self.lambdasmax = len(self.lambdas)
	
	def get_points(self):
		return self.last_points
		
	def single_round(self):
		ret = False
		#allocate
		new_map = copy.deepcopy(self.lambda_map)
		#set it to ''
		for y in range(len(new_map[0])):
			for x in range(len(new_map)):
				if self.lambda_map[x][y] == '*':
                    #Rock falling straigth
					if self.lambda_map[x][y-1] == ' ':
						new_map[x][y] = ' '
						new_map[x][y-1] = '*'
						ret = True
						self.am_i_dead((x,y-1))
					#Rock rolling over rock to the right
					if self.lambda_map[x][y-1] == '*' and self.lambda_map[x+1][y] == ' ' and self.lambda_map[x+1][y-1] == ' ':
						new_map[x][y] = ' '
						new_map[x+1][y-1] = '*'
						ret = True
						self.am_i_dead((x+1,y-1))
					#Rock rolling over rock to the left
					if self.lambda_map[x][y-1] == '*' and (self.lambda_map[x+1][y] != ' ' or self.lambda_map[x+1][y-1] != ' ') and self.lambda_map[x-1][y] == ' ' and self.lambda_map[x-1][y-1] == ' ':
						new_map[x][y] = ' '
						new_map[x-1][y-1] = '*'
						ret = True
						self.am_i_dead((x-1,y-1))
					#Rock rolling over lambda to the right
					if self.lambda_map[x][y-1] == '\\' and self.lambda_map[x+1][y] == ' ' and self.lambda_map[x+1][y-1] == ' ':
						new_map[x][y] = ' '
						new_map[x+1][y-1] = '*'
						ret = True
						self.am_i_dead((x+1,y-1))
				# No lambdas left, opening lift
				if self.lambda_map[x][y] == 'L' and len(self.lambdas) == 0:
					ret = True
					new_map[x][y] = 'O'
						
		for x in range(len(new_map)):
			for y in range(len(new_map[x])):			
				self.lambda_map[x][y] = new_map[x][y]
		
		return ret


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
		if self.lambda_map[xp][yp] == ' ' or self.lambda_map[xp][yp] == '.' or self.lambda_map[xp][yp] == '\\' or self.lambda_map[xp][yp] == 'o':
			if self.lambda_map[xp][yp] == '\\':
				self.lambdas.remove((xp,yp))
				self.last_points+=25
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			return True
		elif xp == x+1 and self.lambda_map[xp][yp] == '*' and self.lambda_map[x+2][y] == ' ':
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[xp+1][yp] = '*'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			return True
		elif xp == x-1 and self.lambda_map[xp][yp] == '*' and self.lambda_map[x-2][y] == ' ':
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[xp-1][yp] = '*'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			return True
		elif self.lambda_map[xp][yp] == 'O':
			self.last_points += 50 * self.lambdasmax
			self.won = True
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[x][y] = ' '
			return True
		else :
			return False
	
	def set_movement(self, move):
		self.last_points=-1
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
			self.last_points += 25 * (self.lambdasmax - len(self.lambdas))
			moved = True
		if move == "W":
			moved = False
			pass
		#~ self.logger.write(move)
		updated = self.single_round()
		if self.waterworld != None:
			self.waterworld.tick(self.robotpos[1])
		if (self.killed):
			return True
		#~ if move == "W" and updated:
			#~ pdb.set_trace()
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
