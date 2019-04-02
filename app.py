from flask import Flask, request, Response, session
from functools import wraps

app = Flask(__name__)


def check_auth(username, password):
    """This function is called to check if a username/password combination is valid."""
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enabled basic auth."""
    return Response(
            'Could not verify your access level for that URL.\n'
            'You have to log in with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def hello():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    return 'Hello, World!'


@app.route('/clear')
def clear():
    session.clear
    return 'cleared'
