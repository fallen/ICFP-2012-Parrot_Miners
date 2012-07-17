#!/usr/bin/env python
# -*- indent-tabs-mode: t -*-

class MapDrawer:
	
	possible_trampolines = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
	def __init__(self,lambda_map,trampolines):
		#Map from input uses first index for lines, we want it for columns
		self.height=len(lambda_map)
		self.width=len(lambda_map[0])
		#Here, lambda_map is "raw" ie. indexing came from input
		self.lambda_map=lambda_map
		self.beards=[]
		self.trampolines=trampolines
		self.trampoline_position = {}
		self.lambdas=[]

	def gettrampostuff(self):
		return (self.trampolines , self.trampoline_position)
	
	def getrobotpos(self):
		return self.robotpos
	
	def getlambda(self):
		return self.lambdas

#change indexing in matrix to be able to use lambda_map[x][y]
	def reindex(self):
		lambda_indexed=[[ 'X' for i in range(self.height)] for i in range(self.width) ]
		for i in range(self.width):
			for j in range(self.height):
				lambda_indexed[i][j]=self.lambda_map[j][i]
				 # Filling beards list coordinates.
				if lambda_indexed[i][j] == "W" :
					t=(i,j)
					self.beards.append(t)
				if lambda_indexed[i][j].isdigit():
					for trampoline, target in self.trampolines.iteritems():
						if target == int(lambda_indexed[i][j]):
							self.trampolines[trampoline] = (i, j)
				if lambda_indexed[i][j] in MapDrawer.possible_trampolines:
					self.trampoline_position[lambda_indexed[i][j]] = (i,j)
				if lambda_indexed[i][j] == 'R':
					self.robotpos = (i,j)
				if lambda_indexed[i][j] == '\\' or lambda_indexed[i][j] == '@':
					self.lambdas.append('\\')
		self.lambda_map=lambda_indexed

	def getbeards(self):
		return self.beards

	def getmap(self):
		return self.lambda_map

	def draw(self):
		self.map_str=""
		self.list_lines=[]
		self.height=len(self.lambda_map[0])
		self.width=len(self.lambda_map)
		for y in range(self.height):
			for x in range(self.width):
				self.map_str+=(self.lambda_map[x][self.height - y-1])
			self.map_str+=('\n')
		print self.map_str

