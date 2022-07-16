from flask import request
from flask_restx import Resource, Namespace

from models.models import Genre, db
from models.schema import GenreSchema

genre_ns = Namespace('genres')  # создаем namespace жанров

genre_schema = GenreSchema()  # схема для сериализации одного жанра в словарь
genres_schema = GenreSchema(many=True)  # схема для сериализации нескольких жанров в список словарей


@genre_ns.route('/')
class GenresView(Resource):
    """
    CBV жанров
    GET - получение данных всех жанров
    POST - добавление данных нового жанра
    """

    def get(self):
        genres = db.session.query(Genre).all()
        return genres_schema.dump(genres), 200

    def post(self):
        new_genre_json = request.json
        new_genre = Genre(**new_genre_json)
        with db.session.begin():
            db.session.add(new_genre)
        return genre_schema.dump(new_genre), 201


@genre_ns.route('/<int:genre_id>/')
class GenreView(Resource):
    """
    CBV жанра
    GET - получение данных жанра по id
    PUT - обновление данных жанра по id
    DELETE - удаление жанра по id
    каждый метод в случае ошибки выдаст ошибку 404
    """

    def get(self, genre_id):
        try:
            genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    def put(self, genre_id):
        try:
            genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
            update_json = request.json

            genre.id = update_json.get('id')
            genre.name = update_json.get('name')

            db.session.add(genre)
            db.session.commit()
            return genre_schema.dump(genre), 204
        except Exception as e:
            return str(e), 404

    def delete(self, genre_id):
        try:
            genre = db.session.query(Genre).filter(Genre.id == genre_id).one()

            db.session.delete(genre)
            db.session.commit()
            return '', 204
        except Exception as e:
            return str(e), 404
