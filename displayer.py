#!/usr/bin/env python
# -*- indent-tabs-mode: t -*-


class MapDrawer:
	def __init__(self,lambda_map):
		self.height=len(lambda_map)
		self.width=len(lambda_map[0])
		
		#Here, lambda_map is "raw" ie. indexing came from input
		self.lambda_map=lambda_map
		self.reindex()
		#Now, lambda_map is reindexed to make more sense of lambda_map[x][y]

#change indexing in matrix to be able to use lambda_map[x][y]
	def reindex(self):
		
		lambda_indexed=[[ 'X' for i in range(self.width)] for i in range(self.height) ]

		for i in range(self.width):
			for j in range(self.height):
				lambda_indexed[i][j]=self.lambda_map[j][i]
		self.lambda_map=lambda_indexed

	def getmap(self):
		return self.lambda_map

	def draw(self):
		map_str=""
		list_lines=[]
		# ''.join(list_of_chars_or_strings) -> create a big string :)
		x_no=0
		for y in range(self.height):
			for x in range(self.width):
				map_str+=(self.lambda_map[x][self.height - y-1])
			map_str+=('\n')
		print map_str

