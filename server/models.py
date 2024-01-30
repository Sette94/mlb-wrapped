from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import JSON


metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

# Add models here


class Users(db.Model, SerializerMixin):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    first_year = db.Column(db.DateTime, server_default=db.func.now())

    attended_games = db.relationship('UserGames', back_populates='users')

    serialize_rules = ('-attended_games.users', )

    @validates('username', 'password')
    def non_null(self, key, value):
        if value:
            return value
        else:
            raise ValueError

    def __repr__(self):
        return f'<User Info {self.user_id}, {self.username}, {self.password}, {self.first_year}>'


class Games(db.Model, SerializerMixin):
    __tablename__ = "games"

    gamePk = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    venue_id = db.Column(db.String, db.ForeignKey("ballparks.venue_id"))
    game_data = db.Column(JSON, nullable=True)

    attended_games = db.relationship('UserGames', back_populates='games')
    venues = db.relationship('Ballparks', back_populates='games')

    serialize_rules = ('-attended_games.games', '-venues.games')

    @validates('date', 'venue_id', 'game_data')
    def non_null(self, key, value):
        if value:
            return value
        else:
            raise ValueError

    def __repr__(self):
        return f'<Game Info {self.gamePk}, {self.user_ids}, {self.game_data}>'


class UserGames(db.Model, SerializerMixin):
    __tablename__ = "usergames"

    id = db.Column(db.Integer, primary_key=True)
    gamePk = db.Column(db.Integer, db.ForeignKey("games.gamePk"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    users = db.relationship('Users', back_populates="attended_games")
    games = db.relationship('Games', back_populates="attended_games")

    serialize_rules = ('-users.attended_games', '-games.attended_games',)

    @validates('gamePk', 'user_id')
    def non_null(self, key, value):
        if value:
            return value
        else:
            raise ValueError


class Ballparks(db.Model, SerializerMixin):
    __tablename__ = "ballparks"

    venue_id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String)
    venue_location = db.Column(JSON, nullable=True)

    games = db.relationship('Games', back_populates="venues")

    serialize_rules = ('-games.venues', )

    @validates('venue_id', 'venue_name')
    def non_null(self, key, value):
        if value:
            return value
        else:
            raise ValueError