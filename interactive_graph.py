"""
Simple interactive graph using PyVis library
"""

from pyvis.network import Network

# Create a network object
net = Network(height='750px', width='100%', directed=False)

# Add nodes
net.add_node(1, label='Node 1', color='red')
net.add_node(2, label='Node 2', color='blue')
net.add_node(3, label='Node 3', color='green')
net.add_node(4, label='Node 4', color='yellow')
net.add_node(5, label='Node 5', color='purple')

# Add edges (connections between nodes)
net.add_edge(1, 2)
net.add_edge(1, 3)
net.add_edge(2, 3)
net.add_edge(2, 4)
net.add_edge(3, 5)
net.add_edge(4, 5)

# Customize physics simulation
net.toggle_physics(True)
net.show_buttons(filter_=['physics'])

# Save and show the graph
net.show('graph.html')
print("Interactive graph created! Open 'graph.html' in your browser.")
