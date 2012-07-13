import copy

class controller:
	
	def __init__(self, lambda_map):
		self.lambda_map = lambda_map
	
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
						
		self.lambda_map = new_map
		
	def set_movement(self, move):
		self.single_round()
