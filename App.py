from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import psycopg2
import psycopg2.extras

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'