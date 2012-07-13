import copy

class controller:
	
	def __init__(self, lambda_map):
		self.lambda_map = lambda_map
		self.lambdas = []
		self.logger = debuglogger()
		self.killed=False

		for x in range(len(self.lambda_map)):
			for y in range(len(self.lambda_map[x])):
				if self.lambda_map[x][y] == 'R':
					self.robotpos = (x,y)
				if self.lambda_map[x][y] == '\\':
					self.lambdas.append((x,y))
		
	def single_round(self):
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
						self.am_i_dead((x,y-1))
					#Rock rolling over rock to the right
					if self.lambda_map[x][y-1] == '*' and self.lambda_map[x+1][y] == ' ' and self.lambda_map[x+1][y-1] == ' ':
						new_map[x][y] = ' '
						new_map[x+1][y-1] = '*'
						self.am_i_dead((x+1,y-1))
					#Rock rolling over rock to the left
					if self.lambda_map[x][y-1] == '*' and (self.lambda_map[x+1][y] != ' ' or self.lambda_map[x+1][y-1] != ' ') and self.lambda_map[x-1][y] == ' ' and self.lambda_map[x-1][y-1] == ' ':
						new_map[x][y] = ' '
						new_map[x-1][y-1] = '*'
						self.am_i_dead((x-1,y-1))
					#Rock rolling over lambda to the right
					if self.lambda_map[x][y-1] == '\\' and self.lambda_map[x+1][y] == ' ' and self.lambda_map[x+1][y-1] == ' ':
						new_map[x][y] = ' '
						new_map[x+1][y-1] = '*'
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
			print "Robot died by rock at (",rockpos[0],",",rockpos[1],")"
			self.killed=True
		
	def move(self, x,y, xp,yp):
		if self.lambda_map[xp][yp] == ' ' or self.lambda_map[xp][yp] == '.' or self.lambda_map[xp][yp] == '\\' or self.lambda_map[xp][yp] == 'o':
			if self.lambda_map[xp][yp] == '\\':
				self.lambdas.remove((xp,yp))
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
		else :
			return False
		
	def set_movement(self, move):
		if move == "U":
			self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0], self.robotpos[1]+1)
		if move == "D":
			self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0], self.robotpos[1]-1)
		if move == "L":
			self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0]-1, self.robotpos[1])
		if move == "R":
			self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0]+1, self.robotpos[1])
		if move == "A":
			pass
		if move == "W":
			pass
		self.logger.write(move)
		self.single_round()
		
class debuglogger():
	f=open("output","w")	
	loggedstr = ""
	def __init__(self):
		pass
	
	def write(self, text):
		self.loggedstr = self.loggedstr+text
		print self.loggedstr
		
	def __del__(self):
		print "write_to_file"
		self.f.write(self.loggedstr)
		self.f.close()
		
#~ class normallogger(logger):
	#~ f=open(sys.stdout) 	
