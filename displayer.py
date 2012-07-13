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

		lambda_indexed=[[ 'X' for i in range(self.height)] for i in range(self.width) ]

		line_no=0
		char_no=0
		for line in self.lambda_map:
			for char in line:
				lambda_indexed[line_no][char_no]=char
				char_no+=1
			line_no+=1
			char_no=0
		lambda_indexed.reverse()
		self.lambda_map=lambda_indexed

	def getmap(self):
		return self.lambda_map

	def draw(self):
		map_str=""
		list_lines=[]
		# ''.join(list_of_chars_or_strings) -> create a big string :)
		x_no=0
		for x in range(self.width):
			for y in range(self.height):
				map_str+=(self.lambda_map[x][y])
			map_str+=('\n')
		print map_str

