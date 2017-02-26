#!/usr/bin/python3

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

# any needed Flask configuration can be passed as arguments to this
app = Flask(__name__)

# We'll configure the SQLalchemy stuff here for the moment
# TODO split ORM stuff into its own file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///musicfan.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # this squelches the
#                                                       console warning
db = SQLAlchemy(app)


##########
# Routes
##########

@app.route('/', methods=["POST", "GET"])
def index():

    # Do this stuff only if we are submitting the form
    if request.method == "POST":
        pass
        # TODO try/except...
        # TODO create an object based on submitted form data
        # TODO apply any other logic to that object
        # db.session.add(that object)
        # db.session.commit()
        # TODO return render_template the next page?

    # Otherwise, display the main form

    return render_template("main.html")

# Leave this as the last route
@app.route("/<path:path>")
def serve_static(path):
    """
    Assume any request not matching above routes is request for static resource
    :param path:
    :return:
    """
    return app.send_static_file(path)

#########
# Run application
#########

if __name__ == '__main__':
    app.run()
