

# from flask import request, Blueprint
# from flask_restful import Api, Resource

# from .schemas import FilmSchema
# from ..models import Film, Actor

# films_v1_0_bp = Blueprint('films_v1_0_bp', __name__)

# film_schema = FilmSchema()

# api = Api(films_v1_0_bp)

# api.add_resource(FilmListResource, '/api/v1.0/films/', endpoint='film_list_resource')
# api.add_resource(FilmResource, '/api/v1.0/films/<int:film_id>', endpoint='film_resource')