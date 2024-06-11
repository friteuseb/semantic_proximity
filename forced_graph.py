import matplotlib.pyplot as plt
import networkx as nx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crawler import Page
from urllib.parse import urlparse

# Connect to the database
engine = create_engine('sqlite:///site_content.db')
Session = sessionmaker(bind=engine)
session = Session()

# Query the database for all pages
pages = session.query(Page).all()

# Create a graph
G = nx.Graph()

# Add nodes with theme and strength as attributes
for page in pages:
    # Extract the last segment of the URL for node labels
    path = urlparse(page.url).path
    label = path.rstrip('/').split('/')[-1] or 'home'
    G.add_node(page.url, theme=page.theme, label=label, strength=page.theme_strength)

# Add edges (this example assumes you want a fully connected graph within each theme)
theme_groups = {}
for page in pages:
    if page.theme not in theme_groups:
        theme_groups[page.theme] = []
    theme_groups[page.theme].append(page.url)

for theme, urls in theme_groups.items():
    for i in range(len(urls)):
        for j in range(i + 1, len(urls)):
            G.add_edge(urls[i], urls[j])

# Assign colors to nodes based on their theme
theme_colors = {theme: i for i, theme in enumerate(theme_groups.keys())}
node_colors = [theme_colors[G.nodes[node]['theme']] for node in G.nodes]

# Assign sizes to nodes based on their strength
node_sizes = [G.nodes[node]['strength'] * 1000 for node in G.nodes]

# Draw the graph
plt.figure(figsize=(14, 14))
pos = nx.spring_layout(G, seed=42, k=0.5)  # Increase k to spread out the nodes

nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.rainbow, alpha=0.8)
nx.draw_networkx_edges(G, pos, alpha=0.5)

# Add labels for nodes (using the last segment of the URL)
labels = {node: G.nodes[node]['label'] for node in G.nodes}
nx.draw_networkx_labels(G, pos, labels, font_size=8)

# Add a legend with theme names
unique_themes = list(theme_colors.keys())
handles = [plt.Line2D([0], [0], marker='o', color='w', label=theme, markersize=10, 
                      markerfacecolor=plt.cm.rainbow(theme_colors[theme]/len(unique_themes))) for theme in unique_themes]
plt.legend(handles=handles, title="Thématiques", bbox_to_anchor=(1.05, 0.5), loc='center left')

plt.title("Forced Graph of Pages by Theme")
plt.show()

# Close the database session
session.close()

