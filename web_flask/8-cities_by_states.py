#!/usr/bin/python3
''' a script that starts a flask app '''


from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    ''' return HBNB to the user '''
    states = storage.all(State)
    for state in states.values():
        print(state)
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(self):
    ''' tear down method to remove current SQLAlchemy Session '''
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
