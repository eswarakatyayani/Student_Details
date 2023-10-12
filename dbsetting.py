# importing libraries
from flask import Flask, request, Response, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy

# creating an instance of the flask app
app = Flask(__name__)

# Configure our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False