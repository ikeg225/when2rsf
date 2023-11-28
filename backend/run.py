from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/getCapacity')
def getCapacity():
    return 'Hello, World!'