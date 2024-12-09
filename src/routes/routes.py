# import models
from flask import Flask, render_template
from flask import current_app as app
from flask_restful import Resource,reqparse
# from ...templates import indes


def init_views(app):
    @app.route('/saludo')
    def hello():
        # return 'Hello, World!'
        return render_template('index.html')

