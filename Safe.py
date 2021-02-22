from math import sqrt
import collections
import sys

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
Dhaka={
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
def get_distance(srclat,srclong,deslat,deslong):
	length=((srclat-deslat)*(srclat-deslat))+((srclong-deslong)*(srclong-deslong))
	dist_len=sqrt(length)*111
	dist_len=round(dist_len,3)*1000
	return dist_len


Graph_converting={}
a=0




Road_Crime={A:2,
			B:1.5,
			C:10000,
			D:11.34,
			E:10,
			F:100000,
			G:100000,
			H:5.13,
			I:3.12,
			J:1.5,
			K:1,
			L:0,
			}
def get_crimeRate(n):
	return Road_Crime[n]

#print Graph_converting
#print get_crimeRate(A)
def calculate_Alpha(source, target):
	alpha=get_crimeRate(target)-get_crimeRate(source)
	return round(alpha,3)
# print calculate_Alpha(A,L)	


Crime_edges={}
for src in Dhaka:

	l=[]
	c=[]
	for dest in Road_map[src]:
			destlength=get_distance(Dhaka[src][0],Dhaka[src][1],Dhaka[dest][0],Dhaka[dest][1])
			l.append((dest,destlength))
			c.append((dest,calculate_Alpha(src,dest)))		
	Graph_converting[src]=l
	Crime_edges[src]=c

#print Graph_converting
print('\n')
#print Graph_converting
#print Crime_edges
Heuristic_nodes={}
# def calculate_heuristic(source,target,beta):
# 	dest=target
# 	src= source
# 	visited= set()
# 	queue = collections.deque([dest])
# 	visited.add(target)

# 	while queue:
# 		vertex=queue.popleft()
# 		Heuristic_nodes[vertex]=
# 		print(str(vertex)+" ")
# 		for neigbour in Road_map[vertex]:
# 			if neigbour not in visited:
# 				visited.add(neigbour)
# 				queue.append(neigbour)
visited=set()


	
def calculate_heuristic(visited,target,beta,parent=None):
	if parent==None:
		parent=target
		Heuristic_nodes[parent]=beta*calculate_Alpha(target,parent)

	if target not in visited:
		val=(1-beta)*get_distance(Dhaka[target][0],Dhaka[target][1],Dhaka[parent][0],Dhaka[parent][1])
		val=val+beta*calculate_Alpha(parent,target)
		Heuristic_nodes[target]=Heuristic_nodes[parent]+val
		#print (target,parent)

		visited.add(target)
		for neigbour in Road_map[target]:

			parent=target
			calculate_heuristic(visited,neigbour,beta,parent)


	else:
		val=(1-beta)*get_distance(Dhaka[target][0],Dhaka[target][1],Dhaka[parent][0],Dhaka[parent][1])
		val=val+beta*calculate_Alpha(parent,target)+Heuristic_nodes[parent]
		Heuristic_nodes[target]=min(Heuristic_nodes[target],val)
						

	



	
			




def heuristic(n):
    
    return Heuristic_nodes[n]



#define fuction to return neighbor and its distance
#from the passed node
def get_Neighbours(v):
	if v in Graph_converting:
		return Graph_converting[v]
	else:
		return None
#print get_Neighbours(L)			
def Astar(source,target,safety_factor):
		calculate_heuristic(visited,target,safety_factor)
		#print Heuristic_nodes
		open_set=set([source])
		#print open_set
		#print source
		close_set=set([])
	#store distance from starting node
		g={}
	#store previous location
		parents={}
	# source node is has no parents node,

		g[source]=0
		#print g

	# it is its own root
		parents[source]=source

		while len(open_set)>0:
			n=None
		#node with lowest f() found
			for v in open_set:
				#print v
				if n==None or g[v]+heuristic(v)<g[n]+heuristic(n):
					n=v
			if n==target or Graph_converting[n]==None:
				pass
			else:
				for (m,weight) in get_Neighbours(n):
					#m first ar last set e nai, first set a add korlam
					#m er parent update korlam
					if m not in open_set and m not in close_set:
						open_set.add(m)
						parents[m]=n
						g[m]=g[n]+weight

					else: 
						if g[m]>g[n]+weight:
							#update g[m]
							g[m]=g[n]+weight
							#change parent m to n
							parents[m]=n

							if m in close_set:
								close_set.remove(m)
								open_set.add(m)
			if n== None:
				print("No path")
				return None
			if n==target:
				path=[]
				while parents[n]!=n:
					path.append(n)
					n=parents[n]
				path.append(source)	
				path.reverse()
				print('Path found:{}'.format(path))
				return path	

			
			#print ("op : ", open_set)	
			open_set.remove(n)
			#print ("op rm : ", open_set)

			close_set.add(n)
			#print open_set
		print("Path doesnt exist")
		return None


Astar(L,A,.001)

				

		