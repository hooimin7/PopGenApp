import pandas as pd
import networkx as nx
from pyvis.network import Network

# Read the data from HaplogroupBPE.tsv into a DataFrame
df = pd.read_csv('RootHaplogroupBPE.tsv', sep='\t')

# Create a directed graph
G = nx.DiGraph()

# Add nodes to the graph for each haplogroup in the DataFrame
for index, row in df.iterrows():
    G.add_node(row['Haplogroup'])  # Removed date_mean attribute

# Open the outfile.txt file and read it line by line
with open('outfile.txt', 'r') as file:
    for line in file:
        # Split the line into haplogroups
        haplogroups = line.strip().split(' -> ')
        
        # Add edges to the graph based on the information in outfile.txt
        for i in range(len(haplogroups) - 1):
            G.add_edge(haplogroups[i], haplogroups[i + 1])

# Get user input
user_input1 = input("Enter the first haplogroup: ")
user_input2 = input("Enter the second haplogroup: ")

# Check if the haplogroups are in the graph
if user_input1 not in G or user_input2 not in G:
    print("No such haplogroup, try again.")
else:
    # Get the paths from the root to the leaves for the two haplogroups
    paths = []
    for node in G:
        if node != user_input1:
            try:
                paths.append(nx.shortest_path(G, source=node, target=user_input1))
            except nx.NetworkXNoPath:
                continue
        if node != user_input2:
            try:
                paths.append(nx.shortest_path(G, source=node, target=user_input2))
            except nx.NetworkXNoPath:
                continue

    # Flatten the list of paths and remove duplicates
    nodes = list(set([node for path in paths for node in path]))
    print(nodes)
    
    # Create a subgraph with the nodes in the paths
    H = G.subgraph(nodes)

    # Convert the NetworkX graph to a PyVis graph
    net = Network(notebook=True)
    net.options = {
        'configure': {
            'enabled': False},
        'edges': {
            'color': 'lightgray'},
        'physics': {
            'enabled': False},
        'interaction': {
            'dragNodes': True},
        'layout': {
            'improvedLayout': True  # Non-hierarchical layout
        }
    }
    net.from_nx(H)

    # Set the cdn option
    net.cdn = 'remote'

    # Show the graph
    net.show("graph.html")

