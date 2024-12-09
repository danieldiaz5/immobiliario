import time
import os
import sys
from flask import Flask
# from .src.routes import routes
# from flask.helpers import make_response
# from flask import request,abort
# from flask_restful import Api
# import routes
# from .src.routes.routes import hello
from src.routes.routes import init_views


app = Flask(__name__)
init_views(app)


if __name__  == '__main__':
    app.run(debug=True,host='localhost',port=5000)