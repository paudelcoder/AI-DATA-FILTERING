from flask import Flask, render_template, request
# I will be using Flask for the web interface.
# This is just the initial setup.

app = Flask(__name__)

@app.route('/')
def index():
    return "Web interface for Hinduism AI coming soon!"

if __name__ == '__main__':
    app.run(debug=True)
