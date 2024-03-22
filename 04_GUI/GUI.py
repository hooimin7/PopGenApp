import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import numpy as np
import time

# Display the DataFrame in Streamlit
_Ancient_connection = """
Discover your genetic heritage by exploring the most common ancestral haplogroups. 
If you're curious about your ancient ancestors, 
delve into the connections between input haplogroups over time. 
Unravel the fascinating story of your genetic past today!
"""

_Have_you = """
Have you ever wondered how you are connected to the ancient world?
"""


def stream_data():
    for word in _Have_you.split(" "):
        yield word + " "
        time.sleep(0.02)

    df = pd.read_excel('/Users/med-snt/PopGenApp/04_GUI/timeline.xlsx')
    yield df
    time.sleep(0.02)

    for word in _Ancient_connection.split(" "):
        yield word + " "
        time.sleep(0.02)


if st.button("Introduction"):
    st.write_stream(stream_data)


# Read the data from HaplogroupBPE.tsv into a DataFrame
# df = pd.read_csv('RootHaplogroupBPE.tsv', sep='\t')
df = pd.read_csv('FinalMergedHaplo.tsv', sep='\t')

# Create a directed graph
G = nx.DiGraph()

# Add nodes to the graph for each haplogroup in the DataFrame
for index, row in df.iterrows():      
    G.add_node(row['Haplogroup'], date_mean=row['Date Mean'], label=f"{row['Haplogroup']} ({row['Date Mean']})")
    


# Open the outfile.txt file and read it line by line
with open('outfile.txt', 'r') as file:
    for line in file:
        # Split the line into haplogroups
        haplogroups = line.strip().split(' -> ')
        
        # Add edges to the graph based on the information in outfile.txt
        for i in range(len(haplogroups) - 1):
            G.add_edge(haplogroups[i], haplogroups[i + 1])


# Create the Streamlit app
st.title('Ancient Connections')

user1 = st.text_input('Enter the first haplogroup')
user2 = st.text_input('Enter the second haplogroup')

if st.button('Submit'):
    # Check if the haplogroups are in the graph
    if user1 not in G or user2 not in G:
        st.write("No such haplogroup, try again.")
    else:
        # Get the paths from the root to the leaves for the two haplogroups
        paths = []
        for node in G:
            if node != user1:
                try:
                    paths.append(nx.shortest_path(G, source=node, target=user1))
                except nx.NetworkXNoPath:
                    continue
            if node != user2:
                try:
                    paths.append(nx.shortest_path(G, source=node, target=user2))
                except nx.NetworkXNoPath:
                    continue

        # Flatten the list of paths and remove duplicates
        nodes = list(set([node for path in paths for node in path]))
        

        # Create a subgraph with the nodes in the paths
        H = G.subgraph(nodes)


        # Convert the NetworkX graph to a PyVis graph
        net = Network(notebook=True)
        net.options = {
            'configure': {
                'enabled': True},
            'edges': {
                'color': 'lightgray'},
            'physics': {
                'enabled': True},
            'interaction': {
                'dragNodes': True},
            'layout': {
                'improvedLayout': False  # Hierarchical layout
            }
        }
        net.from_nx(H)

        # Set the cdn option
        net.cdn = 'remote'

        # Save the graph as an HTML file
        net.save_graph("graph.html")

        # Read the HTML file
        with open("graph.html", "r") as f:
            html_string = f.read()

        # Display the HTML in the Streamlit app
        st.components.v1.html(html_string, width=800, height=600)


