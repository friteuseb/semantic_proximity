import sys
import os
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import Counter

# Ajouter dynamiquement le répertoire du script de crawler
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from crawler import Page  # Importez la classe Page depuis votre script de crawler

# Connect to the database
engine = create_engine('sqlite:///site_content.db')
Session = sessionmaker(bind=engine)
session = Session()

# Query the database for theme counts
theme_counts = Counter(page.theme for page in session.query(Page).all())

# Close the database session
session.close()

# Prepare data for plotting
themes = list(theme_counts.keys())
counts = list(theme_counts.values())

# Create the bar plot
plt.figure(figsize=(10, 6))
plt.bar(themes, counts, color='skyblue')
plt.xlabel('Thématiques')
plt.ylabel('Nombre de pages')
plt.title('Nombre de pages par thématique')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Show the plot
plt.show()

