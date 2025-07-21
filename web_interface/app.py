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
    # This will query Neo4j and return the graph data in a D3-compatible format.
    # This is a placeholder for now.
    nodes = [{"id": "Rama", "group": 1}, {"id": "Sita", "group": 1}]
    links = [{"source": "Rama", "target": "Sita", "value": 1}]
    return jsonify({"nodes": nodes, "links": links})

if __name__ == '__main__':
    app.run(debug=True)
