#!/usr/bin/python3
''' a script that starts a flask app '''


from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_list(id='all'):
    ''' return the state by id '''
    states = storage.all(State)
    mode = 'all'
    state = None
    if id != 'all':
        state = states.get('State.{}'.format(id), None)
        mode = 'found'
        if state is None:
            mode = 'not_found'

    return render_template("9-states.html", states=states, state=state, mode=mode)


@app.teardown_appcontext
def teardown(self):
    ''' tear down method to remove current SQLAlchemy Session '''
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
