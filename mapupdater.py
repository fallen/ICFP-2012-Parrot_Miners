import copy

class controller:
	
	def __init__(self, lambda_map):
		self.lambda_map = lambda_map
		self.lambdas = []
		for x in range(len(self.lambda_map)):
			for y in range(len(self.lambda_map[x])):
				if self.lambda_map[x][y] == 'R':
					self.robotpos = (x,y)
				if self.lambda_map[x][y] == '\\':
					self.lambdas.append((x,y))
					
		print self.robotpos
		print self.lambdas
				 
	def single_round(self):
		#allocate
		new_map = copy.deepcopy(self.lambda_map)
		#set it to ''
		for x in range(len(new_map)):
			for y in range(len(new_map[x])):
				if self.lambda_map[x][y] == '*':
					if self.lambda_map[x][y-1] == ' ':
						new_map[x][y] = ' '
						new_map[x][y-1] = '*'
					if self.lambda_map[x][y-1] == '*' and self.lambda_map[x+1][y] == ' ' and self.lambda_map[x+1][y-1] == ' ':
						new_map[x][y] = ' '
						new_map[x+1][y-1] = '*'
					if self.lambda_map[x][y-1] == '*' and (self.lambda_map[x+1][y] != ' ' or self.lambda_map[x+1][y-1] != ' ') and self.lambda_map[x-1][y] == ' ' and self.lambda_map[x-1][y-1] == ' ':
						new_map[x][y] = ' '
						new_map[x-1][y-1] = ' '
					if self.lambda_map[x][y-1] == '\\' and self.lambda_map[x+1][y] == ' ' and self.lambda_map[x+1][y-1] == ' ':
						new_map[x][y] = ' '
						new_map[x+1][y-1] = '*'
				
				if self.lambda_map[x][y] == 'L' and len(self.lambdas) == 0:
					self.lambda_map[x][y] == 'o'
						
		for x in range(len(new_map)):
			for y in range(len(new_map[x])):			
				self.lambda_map[x][y] = new_map[x][y]
		
	def move(self, x,y, xp,yp):
		if self.lambda_map[xp][yp] == ' ' or self.lambda_map[xp][yp] == '.' or self.lambda_map[xp][yp] == '\\' or self.lambda_map[xp][yp] == 'o':
			if self.lambda_map[xp][yp] == '\\':
				print "eat a lambda"
				self.lambdas.remove((xp,yp))
			print "go normally"
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			return True
		elif xp == x+1 and self.lambda_map[xp][yp] == '*' and self.lambda_map[x+2][y] == ' ':
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[xp+1][yp] = '*'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			print "push a boulder"
			return True
		elif xp == x-1 and self.lambda_map[xp][yp] == '*' and self.lambda_map[x-2][y] == ' ':
			self.lambda_map[xp][yp] = 'R'
			self.lambda_map[xp-1][yp] = '*'
			self.lambda_map[x][y] = ' '
			self.robotpos = (xp,yp)
			print "push a boulder"
			return True
		else :
			return False
		
	def set_movement(self, move):
		if move == "U":
			print "up"
			print self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0], self.robotpos[1]+1)
		if move == "D":
			print "down"
			print self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0], self.robotpos[1]-1)
		if move == "L":
			print "left"
			print self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0]-1, self.robotpos[1])
		if move == "R":
			print "right"
			print self.move(self.robotpos[0], self.robotpos[1], self.robotpos[0]+1, self.robotpos[1])
		if move == "A":
			print "abort"
			pass
		if move == "W":
			print "wait"
			pass
		self.single_round()
		print self.robotpos
