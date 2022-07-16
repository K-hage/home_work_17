from flask import request
from flask_restx import Resource, Namespace, fields

from models.models import Movie, db
from models.schema import MovieSchema

movie_ns = Namespace('movies')  # создаем namespace фильмов

movie_schema = MovieSchema()  # схема для сериализации одного фильма в словарь
movies_schema = MovieSchema(many=True)  # схема для сериализации нескольких фильмов в список словарей


# movie_model = movie_ns.model('Movies',
#                              {
#                                  'title': fields.String(required=True),
#                                  'description': fields.String(required=True),
#                                  'trailer': fields.String(required=True),
#                                  'year': fields.Integer(required=True),
#                                  'rating': fields.Float(required=True),
#                                  'genre_id': fields.Integer(required=True),
#                                  'director_id': fields.Integer(required=True)
#                              })


@movie_ns.route('/')
class MoviesView(Resource):
    """
    CBV фильмов
    GET - получение данных всех фильмов,
    фильмов по жанрам или режиссерам,
    фильмов по жанрам и режиссерам
    POST - добавление данных нового фильма
    """

    # создаем документацию и параметры для GET
    @movie_ns.doc(
        description='Оставьте поля пустыми для вывода всех данных\n'
                    'при заполнения id режиссера выведутся данные фильмов по id режиссера\n'
                    'при заполнения id жанра выведутся данные фильмов по id жанра\n'
                    'при заполнения id жанра и режиссера выведутся данные фильмов по их id\n',
        params={
            'director_id': 'id режиссера',
            'genre_id': 'id жанра'
        }
    )
    def get(self):

        director_id = request.args.get('director_id', type=int)  # получаем id режиссера
        genre_id = request.args.get('genre_id', type=int)  # получаем id жанра

        # поиск по id режиссера и жанра
        if director_id and genre_id:
            movies = db.session.query(Movie).filter(Movie.director_id == director_id, Movie.genre_id == genre_id).all()
            if not movies:
                return "", 404

        # поиск по id режиссера
        elif director_id:
            movies = Movie.query.filter(Movie.director_id == director_id).all()

        # поиск по id жанра
        elif genre_id:
            movies = Movie.query.filter(Movie.genre_id == genre_id).all()

        # вывод всех фильмов если не получены id режиссера и жанра
        else:
            movies = db.session.query(Movie).all()

        return movies_schema.dump(movies), 200

    # @movie_ns.doc(description="Заполните данные нового фильма в json формате", body=movie_model)
    def post(self):
        new_movie_json = request.json
        new_movie = Movie(**new_movie_json)
        with db.session.begin():
            db.session.add(new_movie)
        return movie_schema.dump(new_movie), 201


@movie_ns.route('/<int:movie_id>/')
class MovieView(Resource):
    """
    CBV фильма
    GET - получение данных фильма по id
    PUT - обновление данных фильма по id
    DELETE - удаление фильма по id
    каждый метод в случае ошибки выдаст ошибку 404
    """

    def get(self, movie_id):
        try:
            movie = db.session.query(Movie).filter(Movie.id == movie_id).one()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, movie_id):
        try:
            movie = db.session.query(Movie).filter(Movie.id == movie_id).one()
            update_json = request.json

            movie.id = update_json.get('id')
            movie.title = update_json.get('title')
            movie.description = update_json.get('description')
            movie.trailer = update_json.get('trailer')
            movie.year = update_json.get('year')
            movie.rating = update_json.get('rating')
            movie.genre_id = update_json.get('genre_id')
            movie.director_id = update_json.get('director_id')

            db.session.add(movie)
            db.session.commit()
            return movie_schema.dump(movie), 204
        except Exception as e:
            return str(e), 404

    def delete(self, movie_id):
        try:
            movie = db.session.query(Movie).filter(Movie.id == movie_id).one()

            db.session.delete(movie)
            db.session.commit()
            return '', 204
        except Exception as e:
            return str(e), 404
