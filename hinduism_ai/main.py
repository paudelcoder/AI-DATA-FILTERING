import spacy
from collections import Counter

class HinduismAI:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.data = []

    def load_text(self, text):
        return self.nlp(text)

    def filter_content(self, doc, keywords):
        # simple keyword-based filtering
        filtered_sentences = []
        for sent in doc.sents:
            if any(keyword.lower() in sent.text.lower() for keyword in keywords):
                filtered_sentences.append(sent.text)
        return filtered_sentences

    def save_data(self, filtered_content):
        self.data.extend(filtered_content)

    def get_saved_data(self):
        return self.data

    def get_common_words(self, num_words=10):
        words = " ".join(self.data).split()
        return Counter(words).most_common(num_words)

def main_cli():
    ai = HinduismAI()
    print("Hinduism Content Filter AI")
    print("==========================")

    while True:
        print("\nOptions:")
        print("1. Load text from a file")
        print("2. Enter text directly")
        print("3. View saved data")
        print("4. Get most common words")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            filepath = input("Enter the path to the text file: ")
            try:
                with open(filepath, 'r') as f:
                    text = f.read()
                doc = ai.load_text(text)
                keywords = input("Enter keywords to filter by (comma-separated): ").split(',')
                filtered = ai.filter_content(doc, [k.strip() for k in keywords])
                ai.save_data(filtered)
                print("Content filtered and saved.")
            except FileNotFoundError:
                print("Error: File not found.")

        elif choice == "2":
            text = input("Enter the text: ")
            doc = ai.load_text(text)
            keywords = input("Enter keywords to filter by (comma-separated): ").split(',')
            filtered = ai.filter_content(doc, [k.strip() for k in keywords])
            ai.save_data(filtered)
            print("Content filtered and saved.")

        elif choice == "3":
            print("\nSaved Data:")
            saved_data = ai.get_saved_data()
            if not saved_data:
                print("No data saved yet.")
            for item in saved_data:
                print(f"- {item}")

        elif choice == "4":
            num_words = int(input("Enter the number of common words to display: "))
            print("\nMost Common Words:")
            print(ai.get_common_words(num_words))

        elif choice == "5":
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_cli()
