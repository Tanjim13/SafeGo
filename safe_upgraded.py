from math import sqrt
import collections
import sys
import matplotlib.pyplot as plt 
A='Mokarrom Bhaban'
B='Mokarrom Road'
C='Doyel Chottor'
D='DMC OGate'
E='Jagannath Hall'
F='TSC'
G='Shahabag'
H='Nilkhet'
I='Katabon'
J='Aziz'
K='Paribag RD2'
L='Eastern cottage'

class Safe:
	# map er shokol data load korlam
	def __init__(self,Dhaka_Nodes,Road_map,Road_Crime):
		self.Dhaka_Nodes=Dhaka_Nodes
		self.Road_map=Road_map
		self.Road_Crime=Road_Crime
		self.visited=set() #kon kon node visit korse
		self.Heuristic_nodes={} #heuristics joma rakhsi
		self.Graph_converting={} #edge gular distance joma rakhsi
		#self.Crime_edges={}
		self.X=[] #graph e plot korar jonno baki data store korsi
		self.Y=[]
		self.soure=None
		self.target=None
		self.ticks=[]
		#print self.Dhaka_Nodes
		#print self.Road_map
	# def get_val(self):
	# 	print self.Dhaka_Nodes
	# 	print self.Road_map
	# 	print self.Road_Crime
	# 	print self.Crime_edges
	# 	print self.Graph_converting
	# 	print self.visited


		#get_distance er kaaj latitude longitude theke distance dibe
	def get_distance(self,source_latitude,source_longitude,destination_latitude,destination_longitude):

			length=(source_latitude-destination_latitude)*(source_latitude-destination_latitude)+(source_longitude-destination_longitude)*(source_longitude-destination_longitude)
			length=sqrt(length)*111
			return length
	def get_crimeRate(self,n):
		return self.Road_Crime[n]

	# paper er ekta equation jeita Alphar value dibe	
	def calculate_alpha(self,source,target):
		alpha=self.get_crimeRate(target)-self.get_crimeRate(source)
		return alpha
	# amar way te targeted destination theke heuristics calculate korsi	
	def calculate_heuristic(self,visited,target,beta,parent=None):
		if parent==None:
			parent=target
			self.Heuristic_nodes[parent]=beta*self.calculate_alpha(parent,target)

		if target not in visited:
			val=(1-beta)*self.get_distance(self.Dhaka_Nodes[parent][0],self.Dhaka_Nodes[parent][1],self.Dhaka_Nodes[target][0],self.Dhaka_Nodes[target][1])
			val=val+beta*self.calculate_alpha(parent,target)
			self.Heuristic_nodes[target]=self.Heuristic_nodes[parent]+val
			self.visited.add(target)
			for neighbour in self.Road_map[target]:
				parent=target
				self.calculate_heuristic(visited,neighbour,beta,parent)

		else:
			val=(1-beta)*self.get_distance(self.Dhaka_Nodes[target][0],self.Dhaka_Nodes[target][1],self.Dhaka_Nodes[parent][0],self.Dhaka_Nodes[parent][1])
			val=val+beta*self.calculate_alpha(parent,target)+self.Heuristic_nodes[parent]
			self.Heuristic_nodes[target]=min(self.Heuristic_nodes[target],val)
			print(self.Heuristic_nodes[target], target,parent)
		#heuristics er value return korbe	
	def heuristic(self,n):
		return self.Heuristic_nodes[n]

		#neighbours distance shoho store kore rakhbe
	def Converting_Graph(self):
		for source in Dhaka_Nodes:
			l=[]
			for destination in self.Road_map[source]:
				length=self.get_distance(self.Dhaka_Nodes[source][0],self.Dhaka_Nodes[source][1],self.Dhaka_Nodes[destination][0],self.Dhaka_Nodes[destination][1])
				l.append((destination,length))

			self.Graph_converting[source]=l	
		return self.Graph_converting	

		#neighbours return korbe weight shoho

	def get_Neighbours(self,v):
		if v in self.Graph_converting:
			return self.Graph_converting[v]
		else:
			return None
	#modified Astar chalaisi		
	def Astar(self,source,target,safety_factor):
		self.calculate_heuristic(self.visited,target,safety_factor)
		self.Converting_Graph()
		self.source=source
		self.target=target

		#open_set e thakbe shei shokol nodes jeigula ami visit korsi but or neighbour inspect baki ase
		#close_set holo tader list jeigula visited abong tader neighbours inspected
		open_set=set([source])
		close_set=set([])
		#g dharon kore source theke current noder distance
		g={}
		#parent muloto adjacency node dharon kore...parent k dharon kore
		parents={}
		g[source]=0
		parents[source]=source

		while len(open_set)>0:
			n=None
			#node with lowest f() found
			for v in open_set:
				if n==None or g[v]+self.heuristic(v)<g[n]+self.heuristic(n):
					n=v

			if n==target or self.Graph_converting[n]==None:
				pass

			#current node er shokol neighbourer jonno 
			else:
				for(m,weight) in self.get_Neighbours(n):
					#current node m jodi open_set r close_set e na thake
					#add korbo open_set e ar parent banabo n node k
					if m not in open_set and m not in close_set:


						open_set.add(m)
						parents[m]=n
						g[m]=g[n]+weight
					# othoba check korbo ei node ta better kina prothome n node then m node visit er jonno
					#ha hoile update korbo shob kisu
					#ar eita close_set e thakle open_set e anbo 	
					else:
						if g[m]>g[n]+weight:
							g[m]=g[n]+weight
							parents[m]=n

							if m in close_set:
								close_set.remove(m)
								open_set.add(m)

			if n==None:
				print("no path")
				return None


				#current node target e pouchai gele path toiri korbo ar graph e dekhano jonno data store korbo
			if n==target:
				path=[]
				crime=0.00
				while parents[n]!=n:
					path.append(n)
					crime+=self.Road_Crime[n]
					n=parents[n]
				path.append(n)
				path.reverse()

				print('Path found:{}'.format(path))
				crime/=len(path)
				self.X.append(crime)
				self.Y.append(target)
				
				print("average crime:",crime)
				return path
			# n er shokol neighbour inspected tai ber kore dibo open_set theke	
			open_set.remove(n)
			close_set.add(n)

	def Show_Graph(self,col):
		for x in xrange(1,len(self.Y)+1):
			self.ticks.append(x)
		plt.yticks(self.ticks,self.Y)
		plt.plot(self.X,self.ticks,'-ok',color=col)
		plt.xlabel('Average of crimes for usered preferenced safety level from '+self.source) 
		plt.ylabel('Targeted places') 
		plt.xlim([0,30])
		
			

					
			
									





					
			



Dhaka_Nodes={
		'Mokarrom Bhaban':(23.728736,90.399194),
		'Mokarrom Road' :(23.727755, 90.399098),
		'Doyel Chottor' :(23.728001,90.400226),
		'DMC OGate' :(23.727336,90.397626),
		'Jagannath Hall': (23.729442,90.395476),
		'TSC':(23.732585,90.395610),
		'Shahabag':(23.738060,90.395631),
		'Nilkhet':(23.732571,90.387089),
		'Katabon':(23.738729,90.390974),
		'Aziz': (23.738711,90.392281),
		'Paribag RD2':(23.742529,90.395665),
		'Eastern cottage':(23.743054,90.392838),
	}
Road_map={
		'Mokarrom Bhaban':['Mokarrom Road'],
		'Mokarrom Road':['Mokarrom Bhaban','Doyel Chottor','DMC OGate'],
		'Doyel Chottor':['Mokarrom Road','TSC'],
		'DMC OGate':['Mokarrom Road','Jagannath Hall'],
		'Jagannath Hall':['DMC OGate','TSC'],
		'TSC':['Jagannath Hall','Doyel Chottor','Nilkhet','Shahabag'],
		'Shahabag':['TSC','Aziz','Paribag RD2'],
		'Nilkhet':['TSC','Katabon'],
		'Katabon':['Nilkhet','Aziz'],
		'Aziz':['Eastern cottage','Shahabag','Katabon'],
		'Paribag RD2':['Eastern cottage','Shahabag'],
		'Eastern cottage':['Aziz','Paribag RD2'],

}
Road_Crime={A:2,
			B:5,
			C:100,
			D:2,
			E:1,
			F:5,
			G:11,
			H:1,
			I:1,
			J:10,
			K:1,
			L:1,
			}
Graph=Safe(Dhaka_Nodes,Road_map,Road_Crime)
#Graph.get_val()
rokkha_level=.9999
Graph.Astar(A,L,rokkha_level)
Graph.Astar(A,K,rokkha_level)
Graph.Astar(A,J,rokkha_level)
Graph.Astar(A,I,rokkha_level)
Graph.Astar(A,H,rokkha_level)
Graph.Astar(A,G,rokkha_level)
Graph.Astar(A,F,rokkha_level)
Graph.Astar(A,E,rokkha_level)
Graph.Show_Graph('green')
Graph=Safe(Dhaka_Nodes,Road_map,Road_Crime)

rokkha_level=.00001
Graph.Astar(A,L,rokkha_level)
Graph.Astar(A,K,rokkha_level)
Graph.Astar(A,J,rokkha_level)
Graph.Astar(A,I,rokkha_level)
Graph.Astar(A,H,rokkha_level)
Graph.Astar(A,G,rokkha_level)
Graph.Astar(A,F,rokkha_level)
Graph.Astar(A,E,rokkha_level)
Graph.Show_Graph('red')
plt.show()




	