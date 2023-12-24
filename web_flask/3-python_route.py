#!/usr/bin/python3
''' a script that starts a flask app '''


from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    ''' return hello HBNB! to the user '''
    return ('Hello HBNB!')


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    ''' return HBNB to the user '''
    return ('HBNB')


@app.route('/c/<text>', strict_slashes=False)
def variable_route(text):
    ''' return the C plus a custom text entred by the user '''
    return ("C {}".format(text.replace('_', ' ')))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text):
    ''' return the C plus a custom text entred by the user '''
    return ("Python {}".format(text.replace('_', ' ')))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
