from flask import Flask
import time

app = Flask(__name__)

@app.route('/ping/<user_time>')
def ping(user_time):
    return str(time.time() - int(user_time))

@app.route('/login/<login>/<password>')
def login(login, password):
    return "true"

@app.route('/registration/<login>/<password>')
def registration(login, password):
    return "true"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)