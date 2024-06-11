import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from collections import defaultdict
from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

Base = declarative_base()

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    content = Column(Text)
    theme = Column(String)
    theme_strength = Column(Float)

def create_database(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

engine = create_engine('sqlite:///site_content.db')
Session = sessionmaker(bind=engine)
session = Session()

class Crawler:
    def __init__(self, base_url, target_selectors, max_pages=0):
        self.base_url = base_url
        self.target_selectors = target_selectors
        self.max_pages = max_pages
        self.visited = set()
        self.pages = defaultdict(str)
        self.stop_words = list(stopwords.words('french'))
        self.pages_crawled = 0

    def is_internal(self, url):
        return urlparse(url).netloc == urlparse(self.base_url).netloc

    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def extract_target_content(self, soup):
        content = []
        for selector in self.target_selectors:
            elements = soup.select(selector)
            for element in elements:
                content.append(self.clean_text(element.get_text()))
        return ' '.join(content)

    def crawl(self, url):
        if url in self.visited or (self.max_pages > 0 and self.pages_crawled >= self.max_pages):
            return
        self.visited.add(url)
        self.pages_crawled += 1

        print(f"Crawling: {url}")  # Affichage de l'avancement

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for script in soup(["script", "style"]):
            script.extract()

        text = self.extract_target_content(soup)
        if text and not text.isspace():
            self.pages[url] = text
            print(f"Extracted content from {url}: {text[:200]}...")  # Debugging content extraction

        for link in soup.find_all('a', href=True):
            new_url = urljoin(self.base_url, link['href'])
            if self.is_internal(new_url):
                self.crawl(new_url)

    def save_to_db(self):
        if not self.pages:
            print("No pages to save to database.")
            return
        
        for url, content in self.pages.items():
            if not session.query(Page).filter_by(url=url).first():
                page = Page(url=url, content=content)
                session.add(page)
                print(f"Saving page: {url}")  # Debugging database save
        session.commit()

    def analyze_themes(self, n_clusters=5):
        urls = list(self.pages.keys())
        documents = list(self.pages.values())

        if not documents:
            print("Aucun document valide trouvé pour l'analyse.")
            return

        vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words=self.stop_words)
        X = vectorizer.fit_transform(documents)

        if X.shape[1] == 0:
            print("Le vocabulaire est vide après suppression des mots vides.")
            return

        nmf = NMF(n_components=n_clusters, random_state=1).fit(X)
        feature_names = vectorizer.get_feature_names_out()

        topics = self.get_topics(nmf, feature_names, 10)

        for i, topic in enumerate(nmf.transform(X)):
            topic_idx = topic.argmax()
            keywords = topics[topic_idx]
            topic_name = " ".join(keywords[:3])  # Utiliser les 3 mots-clés les plus représentatifs comme nom de thématique
            strength = topic[topic_idx]
            page = session.query(Page).filter_by(url=urls[i]).first()
            page.theme = topic_name
            page.theme_strength = strength
            session.add(page)
            print(f"Analyzed page: {urls[i]} with theme {topic_name} and strength {strength}")  # Debugging theme analysis
        session.commit()

    def extract_keywords(self, feature_names, sorted_items):
        keywords = []
        for idx, score in sorted_items:
            if idx < len(feature_names):
                keywords.append(feature_names[idx])
        return keywords

    def get_topics(self, model, feature_names, n_top_words):
        topics = []
        for topic_idx, topic in enumerate(model.components_):
            sorted_items = sorted(enumerate(topic), key=lambda x: x[1], reverse=True)[:n_top_words]
            keywords = self.extract_keywords(feature_names, sorted_items)
            topics.append(keywords)
        return topics

    @staticmethod
    def clear_db():
        session.query(Page).delete()
        session.commit()

if __name__ == "__main__":
    base_url = sys.argv[1]
    target_selectors = sys.argv[2].split(',')
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    create_database(engine)  # Create database structure

    crawler = Crawler(base_url, target_selectors, max_pages)
    crawler.clear_db()  # Supprimer les anciennes données
    crawler.crawl(base_url)
    print(f"Pages extracted: {len(crawler.pages)}")  # Debugging page extraction
    crawler.save_to_db()
    crawler.analyze_themes()
