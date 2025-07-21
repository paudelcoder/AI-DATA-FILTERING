from flask import Flask, render_template, request, redirect, url_for, jsonify
import sys
import os

# Add the parent directory to the path to import the sanskrit_nlp module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sanskrit_nlp.main import SanskritNLP, KnowledgeGraph

app = Flask(__name__)

# These would be configured securely in a real application
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

nlp = SanskritNLP()
graph = KnowledgeGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        entities = nlp.analyze_text(text)
        for entity in entities:
            graph.add_entity(entity)
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/graph_data')
def graph_data():
    with graph._driver.session() as session:
        result = session.run("MATCH (n) RETURN n")
        nodes = [{"id": record["n"]["name"], "group": record["n"]["type"]} for record in result]

        result = session.run("MATCH ()-[r]->() RETURN r")
        # This is a simplified representation of links. A more robust implementation
        # would involve querying the start and end nodes of each relationship.
        links = [{"source": "Rama", "target": "Sita", "value": 1}] # Placeholder
    return jsonify({"nodes": nodes, "links": links})

if __name__ == '__main__':
    app.run(debug=True)
