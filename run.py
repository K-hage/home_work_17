# run.py

from flask import Flask
from flask_restx import Api

from api.director.namespaces import director_ns
from api.genre.namespaces import genre_ns
from api.movie.namespaces import movie_ns
from models.models import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')  # получаем конфигурации из config.py

db.init_app(app)
app.app_context().push()

api = Api(app)

api.add_namespace(movie_ns) # добавляем импортированный namespace фильмов в api
api.add_namespace(director_ns) # добавляем импортированный namespace режиссеров в api
api.add_namespace(genre_ns) # добавляем импортированный namespace жанров в api

if __name__ == '__main__':
    app.run()
