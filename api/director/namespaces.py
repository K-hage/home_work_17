from flask import request
from flask_restx import Resource, Namespace

from models.models import Director, db
from models.schema import DirectorSchema

director_ns = Namespace('directors')  # создаем namespace режиссеров

director_schema = DirectorSchema()  # схема для сериализации одного режиссера в словарь
directors_schema = DirectorSchema(many=True)  # схема для сериализации нескольких режиссеров в список словарей


@director_ns.route('/')
class DirectorsView(Resource):
    """
    CBV режиссеров
    GET - получение данных всех режиссеров
    POST - добавление данных нового режиссера
    """

    def get(self):
        directors = db.session.query(Director).all()
        return directors_schema.dump(directors), 200

    def post(self):
        new_director_json = request.json
        new_director = Director(**new_director_json)
        with db.session.begin():
            db.session.add(new_director)
        return director_schema.dump(new_director), 201


@director_ns.route('/<int:director_id>/')
class DirectorView(Resource):
    """
    CBV режиссера
    GET - получение данных режиссера по id
    PUT - обновление данных режиссера по id
    DELETE - удаление режиссера по id
    каждый метод в случае ошибки выдаст ошибку 404
    """

    def get(self, director_id):
        try:
            director = db.session.query(Director).filter(Director.id == director_id).one()
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404

    def put(self, director_id):
        try:
            director = db.session.query(Director).filter(Director.id == director_id).one()
            update_json = request.json

            director.id = update_json.get('id')
            director.name = update_json.get('name')

            db.session.add(director)
            db.session.commit()
            return director_schema.dump(director), 204
        except Exception as e:
            return str(e), 404

    def delete(self, director_id):
        try:
            director = db.session.query(Director).filter(Director.id == director_id).one()

            db.session.delete(director)
            db.session.commit()
            return '', 204
        except Exception as e:
            return str(e), 404
