import networkx as nx
import plotly.plotly as py
from plotly.graph_objs import *
from plotly.offline import plot
import math

def load_graph(edge_filename):
	"""
	takes in the name of a file containing graph edge data
	and returns a networkx.Graph object representing the edges in that file
	"""
	edge_list = list()
	fhand = open(edge_filename) #open the .edge file
	for line in fhand: #each line represents an edge with the starting node and the ending node
		from_to = line.split() #extract the starting node and the ending node in an edge
		edge = (from_to[0], from_to[1])
		edge_list.append(edge) #store edges into a list of tuples
	G = nx.Graph()
	G.add_edges_from(edge_list) #generate the graph based on edges info
	return G

def analyze_graph(object):
	"""
	graph analysis
	"""
	print('Number of Nodes: ', G.number_of_nodes())
	print('Number of Edges: ', G.number_of_edges())
	print('Number of Components: ', nx.number_connected_components(G))
	
	#calculate the diameter
	diameter_list = list() 
	#store diameter of each connected component into a list
	for subgraph in nx.connected_component_subgraphs(G):
		diameter_list.append(nx.diameter(subgraph))
	print('Graph diameter: ', max(diameter_list)) #assign the max diameter among subgroups to the graph diameter

	#calculate the avg shortest path length
	path_dict = nx.all_pairs_shortest_path_length(G) #get a dict of dict with shortest path lengths keyed by source and target
	total_shortest_length = 0 
	count_path = 0
	for source, target_pathLength in path_dict.items():
		total_shortest_length += sum(target_pathLength.values()) #for each source node, sum up the lenghts of all the reacheable paths it has
		count_path += len(target_pathLength) - 1 #the path from a node to itself doesn't count
	print('Average shortest path length:', total_shortest_length/count_path)
	
	print('Clustering coefficient: ', nx.average_clustering(G))

	#calculate the degree centrality
	degree_dict = nx.degree_centrality(G) #store the dictionary of nodes with degree centrality as the value
	degree_list = list() #create a list for sorting
	for node, degree in degree_dict.items():
		degree_list.append((degree, node)) #store degree-node as a list of tuples for sorting
	degree_list.sort(reverse=True)
	print('Nodes with highest degree centrality: ')
	i = 0 #count all nodes in the top 10 list， including nodes with the same degree centrality
	j = 0 #count from 0 to 10 for displaying the top 10 nodes
	tie_list = list() #store nodes with same degree centrality in a list
	while j < 10:
		if degree_list[i][0] > degree_list[i+1][0]: 
		#when there is no tie between the current one and the next one
		#display the tied nodes, if existed, and the current node with the same value of degree centrality in the same line
			print(" ".join(node for node in tie_list), degree_list[i][1],  #to display the tie_list without brackets
				"(centrality: ", degree_list[i][0], ")")
			j += 1
			tie_list =[] #empty the tie_list
		else: #when there is a tie
			tie_list.append(degree_list[i][1]) #store the tied nodes into the tie_list
		i += 1

			
def plot_graph(object):
	"""
	displays a visualization of that graph by using plotly and networkx
	"""	
	# node positions assigned by Fruchterman Reingold layout algorithm
	# get a dictionary of positions keyed by node
	# iterate 150 times to make it look good
	pos = nx.spring_layout(G, iterations=150) 


    #sets the position of nodes and their attributes
	node_trace = Scatter(
	    x=[], #create an empty x position list to store the x position value
	    y=[], #create an empty y position list to store the y position value
	    text=[], #specify an empty text list to store the hoverinfo
	    mode='markers', #specify the shape of scatter
	    hoverinfo='text',
	    marker=Marker(
	        color='rgb(24, 119, 191)', #specify the blue color of nodes
	        size=[]))     #specify an empty size list for storing each node's size based on the centrality of the node  

	#pull the node position values from the dictionary 'pos' to 'node_trace'
	for node, position in pos.items():
	    node_trace['x'].append(position[0])
	    node_trace['y'].append(position[1])
	   
    #specify the node attribute
	for node, degree_centrality in nx.degree_centrality(G).items():
	    node_trace['marker']['size'].append(4+150 * degree_centrality) #the larger the centrality, the larger the node. Multiple 200 to make nodes more visible
	    node_info = str(node) + ' (degree: '+ str(G.degree(node)) + ')' #the hover info displays the degree of the nodes
	    node_trace['text'].append(node_info)

	#sets the position of edges and their attributes
	edge_trace = Scatter(
	    x=[], #create an empty x position list to store the x position value
	    y=[], #create an empty y position list to store the y position value
	    line=Line(width=0.5,color='#888'), #line attribute
	    hoverinfo='none',
	    mode='lines') #specify the shape of scatter

	for edge in G.edges():
		edge_trace['x'] += [pos[edge[0]][0],pos[edge[1]][0], None]#extend the x list with x position values of the source and the target in an edge
		edge_trace['y'] += [pos[edge[0]][1],pos[edge[1]][1], None]#extend the y list with y position values of the source and the target in an edge
	

	axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title='' 
          )

	#Create figure and send to Plotly
	fig = Figure(data=Data([edge_trace, node_trace]), #specify data source
             layout=Layout(
                title='Social Network', #specify the title
                titlefont=dict(size=26), 
                showlegend=False, 
                width=800,
                height=800,
                xaxis=XAxis(axis),
			    yaxis=YAxis(axis),
			  
                hovermode='closest' ))

	plot(fig, output_type='file', filename='plot.html', auto_open=True)#generate the graph in offline mode



	
	
	







####################################
## DO NOT EDIT BELOW THIS POINT!! ##
## #################################

# Run the method specified by the command-line
if __name__ == '__main__':
	import sys
	cmd = None
	datafile = None
	INVALID_MSG = """
Invalid arguments. Commands available: 
	load <filename> 
	analyze <filename>
	plot <filename>
"""[1:-1] #bad command message

	try: #catch invalid argument lengths
		cmd = sys.argv[1]
		datafile = sys.argv[2]
	except:
		print(INVALID_MSG)
	else:
		if cmd == 'load':
			G = load_graph(datafile)
			print("loaded graph with", len(G), "nodes and", G.size(), "edges")
		elif cmd == 'analyze':
			G = load_graph(datafile)
			analyze_graph(G)
		elif cmd == 'plot':
			G = load_graph(datafile)
			plot_graph(G)
		else:
			print(INVALID_MSG)
