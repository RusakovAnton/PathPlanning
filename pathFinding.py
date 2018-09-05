from __future__ import print_function
import numpy as np         #array library
import sys
import math

INF = 10000000


class Vertex:
	def __init__(self, x, y, k):
		#print(k)
		self.key = k
		self.key_orig = k
		self.x = x
		self.y = y
		self.dist = INF
		self.index = -1

class PriorityQueue:
	def __init__(self, n):
		self.size = int(math.sqrt(n))
		self.count = 0
		self.heap = []

	def insert(self, v):
		i = self.count
		self.heap.append(v)
		while (i > 0 and self.heap[(i - 1) / 4].dist > v.dist):
			self.heap[(i - 1) / 4], self.heap[i] = self.heap[i], self.heap[(i - 1) / 4]
			self.heap[i].index = i
			i = (i - 1) / 4
		self.count += 1
		self.heap[i].index = i

	def min(self):
		v = self.heap[0]
		self.count -= 1
		self.heap[0] = self.heap[self.count]
		i = 0

		while(4 * i + 1 < self.count):
			left1 = 4 * i + 1
			left2 = 4 * i + 2
			right1 = 4 * i + 3
			right2 = 4 * i + 4
			j = left1
			if (left2 < self.count and self.heap[left2].dist < self.heap[j].dist):
				j = left2
			if (right1 < self.count and self.heap[right1].dist < self.heap[j].dist):
				j = right1
			if (right2 < self.count and self.heap[right2].dist < self.heap[j].dist):
				j = right2
			if (self.heap[i].dist <= self.heap[j].dist):
				break
			self.heap[j], self.heap[i] = self.heap[i], self.heap[j]
			self.heap[i].index = i
			self.heap[j].index = j
			i = j

		return v

	def changeKey(self, v):
		i = v.index
		v.key = v.dist
		
		while (i > 0 and self.heap[(i - 1) / 4].dist > v.dist):
			self.heap[(i - 1) / 4], self.heap[i] = self.heap[i], self.heap[(i - 1) / 4]
			self.heap[i].index = i
			i = (i - 1) / 4
		v.index = i
		
	def Relax(self, u, v):
		changed = False
		if (u.dist + v.key < v.dist):
			changed = True
			v.dist = u.dist + v.key
		return changed

	def search_length_path(self, mapArray):
		while(self.count > 0):
			minVertex = self.min()
			minVertex.index = -1
			x = minVertex.x
			y = minVertex.y

			if (x + 1 < self.size and mapArray[x + 1][y].index != -1 and self.Relax(minVertex, mapArray[x + 1][y])):
				self.changeKey(mapArray[x + 1][y])
			if (y + 1 < self.size and mapArray[x][y + 1].index != -1 and self.Relax(minVertex, mapArray[x][y + 1])):
				self.changeKey(mapArray[x][y + 1])
			if (x > 0 and mapArray[x - 1][y].index != -1 and self.Relax(minVertex, mapArray[x - 1][y])):
				self.changeKey(mapArray[x - 1][y])
			if (y > 0 and mapArray[x][y - 1].index != -1 and self.Relax(minVertex, mapArray[x][y - 1])):
				self.changeKey(mapArray[x][y - 1])
		return mapArray

	def search_path(self,modified,original):
		pass

#def djikstra():

def main():

	f=open('in.txt','r')

	orig_stdout = sys.stdout
	f_out=open('outt.txt','w')
	sys.stdout = f_out

	whole_file = f.read().split('\n')

	N = int(whole_file[0])
	#print(N * N)
	prQueue = PriorityQueue(N * N)

	mapArray = [[]]

	for i in range(N):
		row = whole_file[i + 1].split()
		for j in range(len(row)):
			k = int(row[j])
			v = Vertex(i,j,k)
			mapArray[i].append(v)
			prQueue.insert(mapArray[i][j])
		mapArray.append([])
	mapArray = mapArray[0:-1]

	mapArray[0][0].dist = mapArray[0][0].key;
	print(prQueue.search_length_path(mapArray)[prQueue.size - 1][prQueue.size - 1].dist)
	
	for i in range(N):
		print([row[i].dist for row in mapArray], sep =' ')
	print("---------------")

	for i in range(N):
		print([row[i].key_orig for row in mapArray], sep =' ')

	sys.stdout = orig_stdout
	f_out.close()

main()
	