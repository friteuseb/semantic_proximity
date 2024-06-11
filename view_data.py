from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crawler import Page

# Connect to the database
engine = create_engine('sqlite:///site_content.db')
Session = sessionmaker(bind=engine)
session = Session()

# Query the database for all pages
pages = session.query(Page).all()

# Display the data
if pages:
    for page in pages:
        print(f"URL: {page.url}")
        print(f"Content: {page.content[:200]}...")  # Display only the first 200 characters for brevity
        print(f"Theme: {page.theme}")
        print(f"Strength: {page.theme_strength}")
        print("-" * 40)
else:
    print("No pages found in the database.")

# Close the database session
session.close()
