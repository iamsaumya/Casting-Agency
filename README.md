# Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

The migration folder contains the versions of database. Use the migration folder to set up the database.

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_DEBUG=True
flask run
```

Setting the `FLASK_DEBUG` variable to `True` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use app.py file.

## Hosting

The application is hosted using Heroku. You can find the application [here](https://myudacitycapstoneproject.herokuapp.com/).

## Authentication

There is not frontend of the application, please use the JWT tokens shared by me.

## API

### Introduction

This API is used by Trivia App frontend to fetch the data from database.

### Getting Started with API

1. Base URL
        The base URL of the API is ``` http://127.0.0.1:5000/ ```
1. Authentication
        The API requires Bearer token authentication, you will have to send the JWT token in the header to access endpoints.

### Error Handling

The API returns a JSON response with Success validation, Response code and a guiding message.

```JSON
{
    "success": False,
    "error": 404,
    "message": "Resource not found"
}
```

### Endpoints

GET '/'

- The landing page of the website.
- No request parameter
- Return: A JSON with success key, set to 200.

GET '/actors'

- All the actors stored in the database.
- No request parameter required.
- Returns: A JSON object with actors and success keys. actors is a list of all the actor object and success with 200 status code.

```curl http://127.0.0.1:5000/actors -X GET -H "Bearer: XXX"'```

```JSON
{
    "actors": [
        {
            "age": 54,
            "gender": "Male",
            "id": 1,
            "name": "SRK"
        }
    ],
    "success": true
}
```

GET '/movies'

- All the movies stored in the database.
- No request parameter required.
- Returns: A JSON object with movies and success keys. movies is a list of all the movie object and success with 200 status code.

```curl http://127.0.0.1:5000/movies -X GET -H "Bearer: XXX"'```

```JSON
{
    "movies": [
        {
            "id": 1,
            "release_date": "1987-11-19 14:40:44",
            "title": "DDLJ"
        }
    ],
    "success": true
}
```

POST '/actors'

- Add a actor in the batabase.
- Only Executive Producer Role can perform this operation.
- Request parameter is a JSON object.

```JSON
    {
      "id": 2,
      "name": "SRK",
      "age": 54,
      "gender": "Male"
    }
```

- Returns a JSON with actors, success and total_actors as keys.

```curl http://127.0.0.1:5000/movies -X POST -d '{ "id": 2, "name": "Tom cruise", "age": 54, "gender": "Male"}' -H "Bearer: XXX"'```

```JSON
{
    "actors": [
        {
            "age": 54,
            "gender": "Male",
            "id": 1,
            "name": "SRK"
        },
        {
            "age": 54,
            "gender": "Male",
            "id": 2,
            "name": "Tom cruise"
        }
    ],
    "success": true,
    "total_actors": 2
}
```

POST '/movies'

- Add a movie in the batabase.
- Only Executive Producer Role can perform this operation.
- Request parameter is a JSON object.

```JSON
    {
      "id": 2,
      "release_date": 1041244,
      "title": "Dark Knight"
    }
```

- Returns a JSON with movies, success and total_movies as keys.

```curl http://127.0.0.1:5000/movies -X POST -d '{"id": 2,"release_date": 1041244, "title": "Dark Knight"}' -H "Bearer: XXX"'```

```JSON
{
    "movies": [
        {
            "id": 1,
            "release_date": "1987-11-19 14:40:44",
            "title": "DDLJ"
        },
        {
            "id": 2,
            "release_date": "1973-01-11 23:00:44",
            "title": "Dark Knight"
        }
    ],
    "success": true,
    "total_movies": 2
}
```

PATCH '/actors'

- Update the details of an actor by id.
- Only Executive Producer and Casting Director Roles can perform this operation.
- Request a JSON object with the property to update.
- Response contains the actor object with success result.

```curl http://127.0.0.1:5000/movies/1 -X PATCH -d '{"name" : "Al pacino"}' -H "Bearer: XXX"'```

```JSON
{
    "actor": {
        "age": 54,
        "gender": "Male",
        "id": 1,
        "name": "Al pacino"
    },
    "success": true
}
```

PATCH '/movies'

- Update the details of an movie by id.
- Only Executive Producer and Casting Director Roles can perform this operation.
- Request a JSON object with the property to update.
- Response contains the movie object with success result.

```curl http://127.0.0.1:5000/movies/2 -X PATCH -d '{"release_date": 1095641244}' -H "Bearer: XXX"'```

```JSON
{
    "movie": {
        "id": 2,
        "release_date": "2004-09-20 00:47:24",
        "title": "Dark Knight"
    },
    "success": true
}
```

DELETE '/actors/\<int:actor_id>'

- Delete the record of an actor from database.
- Only Executive Producer and Casting Director Roles can perform this operation.
- No request object is required.
- Response contain a JSON object with delete actor's id and success status.

```curl http://127.0.0.1:5000/actors/3 -X PATCH -H "Bearer: XXX"'```

```JSON
{
    "id": 3,
    "success": true
}
```

DELETE '/movies/\<int:movie_id>'

- Delete the record of a movie from database.
- Only Executive Producer and Casting Director Roles can perform this operation.
- No request object is required.
- Response contain a JSON object with delete movie's id and success status.

```curl http://127.0.0.1:5000/movies/3 -X PATCH -H "Bearer: XXX"'```

```JSON
{
    "id": 3,
    "success": true
}
```
