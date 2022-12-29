
import os
from os import environ
import pandas as pd
from datetime import datetime
from flask import Flask
from flask import request,redirect,url_for
from flask import render_template
from training_model.train_model import TrainModel

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    TrainModel().training_model()

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app.run(debug = True)
    

    

