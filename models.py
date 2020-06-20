import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
from datetime import datetime

database_name = "casting_agent"
database_path = "postgres://uxudaunxqstjmp:bca5dd2f65c95e484ceb53911b89e344926b63bfb86d441ce13d6049e75ce2ed@ec2-18-214-211-47.compute-1.amazonaws.com:5432/d229l7j4f8007n"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Movie(db.Model):

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Integer, nullable=False)

    def __init__(self, id, title, release_date):
        self.id = id
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': datetime.utcfromtimestamp(self.release_date).strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f"<Movie {self.title} {self.release_date}>"


class Actor(db.Model):

    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def __init__(self, id, name, age, gender):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return f"<Actor {self.name} {self.age} {self.gender}>"
