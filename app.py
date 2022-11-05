from flask import Flask

# Create new flask app instance
app = Flask(__name__)

# Create flask route
@app.route('/')
def hello_world():
    return 'Hello World'
