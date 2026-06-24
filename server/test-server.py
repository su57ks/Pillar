from flask import Flask
from time import time

app = Flask(__name__)

@app.route('/ping')
def hello_world():
    return str(time())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)