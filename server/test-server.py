from flask import Flask
import time

app = Flask(__name__)

@app.route('/ping/<user_time>')
def hello_world(user_time):
    return str(time.time() - int(user_time))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)