from marshmallow import Schema, fields


class GenreSchema(Schema):
    """ Схема для сериализации жанров """

    id = fields.Int(dump_only=True)
    name = fields.Str(data_key='genre')


class DirectorSchema(Schema):
    """ Схема для сериализации режиссеров """

    id = fields.Int(dump_only=True)
    name = fields.Str(data_key='director')


class MovieSchema(Schema):
    """ Схема для сериализации фильмов """

    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Pluck('GenreSchema', 'name')  # берем данные из жанров
    director = fields.Pluck('DirectorSchema', 'name')  # берем данные из режиссеров
