import spacy
from collections import Counter
import re

class HinduismAI:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.data = []

    def load_text(self, text):
        return self.nlp(text)

    def extract_concepts(self, doc, concept_keywords):
        """Extracts sentences containing philosophical concepts."""
        concept_sentences = []
        for sent in doc.sents:
            if any(keyword.lower() in sent.text.lower() for keyword in concept_keywords):
                # Simple check for noun phrases that might represent concepts
                for chunk in sent.noun_chunks:
                    if any(keyword.lower() in chunk.text.lower() for keyword in concept_keywords):
                        concept_sentences.append(sent.text)
                        break # Avoid duplicating the sentence
        return concept_sentences

    def extract_verses(self, doc):
        """A simple verse extraction heuristic (e.g., lines with numbers)."""
        verses = []
        for line in doc.text.split('\n'):
            # This is a basic heuristic and would need to be adapted for specific text formats
            if re.match(r'^\d+\.', line.strip()):
                verses.append(line.strip())
        return verses

    def save_data(self, filtered_content):
        self.data.extend(filtered_content)

    def get_saved_data(self):
        return self.data

    def get_common_words(self, num_words=10):
        words = " ".join(self.data).split()
        return Counter(words).most_common(num_words)

import requests
from bs4 import BeautifulSoup
import sqlite3
import re

class DatabaseManager:
    def __init__(self, db_name="hinduism_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL
            );
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS verses (
                id INTEGER PRIMARY KEY,
                source_id INTEGER,
                verse_text TEXT NOT NULL,
                FOREIGN KEY (source_id) REFERENCES sources (id)
            );
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id INTEGER PRIMARY KEY,
                source_id INTEGER,
                concept_text TEXT NOT NULL,
                FOREIGN KEY (source_id) REFERENCES sources (id)
            );
            """)

    def add_source(self, url, title):
        with self.conn:
            cursor = self.conn.execute("INSERT OR IGNORE INTO sources (url, title) VALUES (?, ?)", (url, title))
            return cursor.lastrowid if cursor.lastrowid else self.conn.execute("SELECT id FROM sources WHERE url = ?", (url,)).fetchone()[0]

    def add_verses(self, source_id, verses):
        with self.conn:
            self.conn.executemany("INSERT INTO verses (source_id, verse_text) VALUES (?, ?)",
                                  [(source_id, v) for v in verses])

    def add_concepts(self, source_id, concepts):
        with self.conn:
            self.conn.executemany("INSERT INTO concepts (source_id, concept_text) VALUES (?, ?)",
                                  [(source_id, c) for c in concepts])

def main_cli():
    ai = HinduismAI()
    db_manager = DatabaseManager()
    print("Hinduism Content Filter AI")
    print("==========================")

    while True:
        print("\nOptions:")
        print("1. Scrape and process a new text")
        print("2. View all sources in the database")
        print("3. View verses from a specific source")
        print("4. View concepts from a specific source")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            url = input("Enter the URL to scrape: ")
            title = input("Enter a title for this text: ")
            try:
                response = requests.get(url)
                response.raise_for_status()
                text = BeautifulSoup(response.text, 'html.parser').get_text(separator='\n')

                source_id = db_manager.add_source(url, title)
                doc = ai.load_text(text)

                verses = ai.extract_verses(doc)
                if verses:
                    db_manager.add_verses(source_id, verses)
                    print(f"Found and stored {len(verses)} verses.")

                concept_keywords = input("Enter concept keywords (comma-separated): ").split(',')
                concepts = ai.extract_concepts(doc, [k.strip() for k in concept_keywords])
                if concepts:
                    db_manager.add_concepts(source_id, concepts)
                    print(f"Found and stored {len(concepts)} sentences with concepts.")

            except requests.exceptions.RequestException as e:
                print(f"Error scraping {url}: {e}")

        elif choice == "2":
            sources = db_manager.conn.execute("SELECT id, title FROM sources").fetchall()
            print("\n--- Sources in Database ---")
            for id, title in sources:
                print(f"{id}: {title}")
            print("--------------------------")

        elif choice == "3":
            source_id = input("Enter the source ID to view verses from: ")
            verses = db_manager.conn.execute("SELECT verse_text FROM verses WHERE source_id = ?", (source_id,)).fetchall()
            print(f"\n--- Verses from Source {source_id} ---")
            for v in verses:
                print(v[0])
            print("---------------------------------")

        elif choice == "4":
            source_id = input("Enter the source ID to view concepts from: ")
            concepts = db_manager.conn.execute("SELECT concept_text FROM concepts WHERE source_id = ?", (source_id,)).fetchall()
            print(f"\n--- Concepts from Source {source_id} ---")
            for c in concepts:
                print(c[0])
            print("----------------------------------")

        elif choice == "5":
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_cli()
