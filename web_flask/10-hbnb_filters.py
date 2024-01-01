#!/usr/bin/python3
''' a script that starts a flask app '''


from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    ''' return the states and amenities filters '''
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template("10-hbnb_filters.html",
                           states=states,
                           amenities=amenities)


@app.teardown_appcontext
def teardown(self):
    ''' tear down method to remove current SQLAlchemy Session '''
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
