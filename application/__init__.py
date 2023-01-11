#####################################################################
# This script sets up a Flask application
# and configures it with a secret key and a MongoDB URI.
# The secret key is used for protecting the application from various security threats
# and the MongoDB URI specifies the location of the MongoDB server and the database to be used.
#####################################################################

from flask import Flask
from flask_pymongo import PyMongo

# create an instance of the PyMongo client,
# which allows the application to interact with MongoDB,
# by passing it the Flask application instance
app = Flask(__name__)
app.config["SECRET_KEY"] = "db24c608640f5034b30b8e1e1eb5618ed0ffdbf5"
app.config["MONGO_URI"] = "mongodb://localhost:35000/benchmark"

# mongodb database
# assigns the benchmark database as the default database
# to be used by the application via the db object
mongodb_client = PyMongo(app)
db = mongodb_client.db

# import the routes module and register the routes for the application,
# routes module is responsible for defining how the application should handle different URL requests
from application import routes
