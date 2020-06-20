import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    return app


app = create_app()
db = setup_db(app)


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, true'
    header['Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE,PATCH,OPTIONS'
    return response


@app.route('/')
def homepage():
    return jsonify({
        "success": 200
    })


@app.route("/movies")
@requires_auth("get:movies")
def get_movies(token):
    try:
        movies = Movie.query.all()
        movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': movies
        })
    except:
        abort(422)


@app.route("/actors", methods=['GET'])
@requires_auth("get:actors")
def get_actors(token):
    try:
        actors = Actor.query.all()
        actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': actors
        })
    except:
        abort(422)


@app.route('/actors', methods=['POST'])
@requires_auth("post:actors")
def create_actor(token):
    body = request.get_json()

    Id = body.get('id')
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')

    if(Id is None or name is None or age is None or gender is None):
        abort(400)

    try:
        actor = Actor(Id, name, age, gender)
        actor.insert()
        actors = Actor.query.all()
        actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": actors,
            "total_actors": len(Actor.query.all())
        })
    except:
        abort(422)


@app.route('/movies', methods=['POST'])
@requires_auth("post:movies")
def create_movie(token):
    body = request.get_json()

    Id = body.get('id')
    title = body.get('title')
    release_date = body.get('release_date')

    if(Id is None or title is None or release_date is None):
        abort(400)

    try:
        movie = Movie(Id, title, release_date)
        movie.insert()
        movies = Movie.query.all()
        movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": movies,
            "total_movies": len(Movie.query.all())
        })
    except:
        abort(422)


@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth("patch:actors")
def update_actors(token, id):
    body = request.get_json()

    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')

    if(name is None and age is None and gender is None):
        abort(400)

    actor = Actor.query.get(id)

    if actor is None:
        abort(404)

    try:
        if name is not None:
            actor.name = name

        if age is not None:
            actor.age = age

        if gender is not None:
            actor.gender = gender

        actor.update()

        return jsonify({
            'success': True,
            'actor': Actor.query.get(id).format()
        })
    except:
        abort(422)


@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth("patch:movies")
def update_movies(token, id):
    body = request.get_json()

    title = body.get('title')
    release_date = body.get('release_date')

    if(title is None and release_date and None):
        abort(400)

    movie = Movie.query.get(id)

    if movie is None:
        abort(404)

    try:
        if title is not None:
            movie.title = title

        if release_date is not None:
            movie.release_date = release_date

        movie.update()

        return jsonify({
            'success': True,
            'movie': Movie.query.get(id).format()
        })
    except:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth("delete:actors")
def delete_actors(token, actor_id):
    actor = Actor.query.get(actor_id)

    if actor is None:
        abort(404)

    try:
        actor.delete()
        return jsonify({
            "success": True,
            "id": actor_id
        })
    except:
        abort(422)


@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth("delete:movies")
def delete_mpvies(token, id):
    movie = Movie.query.get(id)

    if movie is None:
        abort(404)

    try:
        movie.delete()
        return jsonify({
            "success": True,
            "id": id
        })
    except:
        abort(422)


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


@app.errorhandler(405)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(500)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify(error.error), error.status_code


if __name__ == '__main__':
    app.run()
