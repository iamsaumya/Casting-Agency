import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from app import app
from models import db, Movie, Actor


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.database_name = "capstone_test"
        self.database_path = "postgres://postgres:postgres@{}/{}".format(
            'localhost:5432', self.database_name)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_path
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        # Imserting the data in database.
        initial_movie = Movie(id=1, title="DDLJ", release_date=21233421)
        initial_movie.insert()

        initial_actor = Actor(id=1, name="SRK", age=54, gender="Male")
        initial_actor.insert()

        # Dummy data for testing purpose.
        self.actor = {
            "id": 3,
            "name": "Sushant Singh Rajput",
            "age": 35,
            "gender": "Male"
        }

        self.movie = {
            "id": 3,
            "title": "Hope",
            "release_date": 999120312
        }

        self.castingdirector = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBLcmstaFN5clFkNTlkdkhMUzFoYiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3B1ZGFjaXR5LmF1dGgwLmNvbS8iLCJzdWIiOiJlYUVKRU1Ob3pPSHRYYkhHaGFnOEFNbzAwMTRJUDBuQ0BjbGllbnRzIiwiYXVkIjoiU1JLIiwiaWF0IjoxNTkyNjY3NjkzLCJleHAiOjE1OTI3NTQwOTMsImF6cCI6ImVhRUpFTU5vek9IdFhiSEdoYWc4QU1vMDAxNElQMG5DIiwic2NvcGUiOiJnZXQ6bW92aWVzIGdldDphY3RvcnMgcGF0Y2g6YWN0b3JzIGRlbGV0ZTphY3RvcnMgcGF0Y2g6bW92aWVzIGRlbGV0ZTptb3ZpZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsInBhdGNoOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJkZWxldGU6bW92aWVzIl19.gf-0oO1zp_1kmCTZeOGoAAUllDXsqkSUMU2o1EczZ-pkb2A2z0fDj0Zzyd0ZmMteEW5fWdoYNkZ0OOUeFKazAJMESq8__J39EvLxkSxe9CPcoyCT_k6P2FfyBBx34bmDapblng2WsmdbnKdbNy2Ik89AeB7XxW-FUq3JufA9cirryw3b6Tw1UnO73KkPShBSuSBS9P4uq9-opSc8li3VZu4H7iCqXOdacZPTzylUnhEHnBKYKMJbwz8m7gcQ3bR9Ebt7G-pkEZ0ZllLUkXOiyPoYlvZU3NpdAWof7dWSs0BwnHFeyZqNMD90u0ZLWTPx_-8UIbgIGcI-aS907JjHqA"
        self.executiveproducer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBLcmstaFN5clFkNTlkdkhMUzFoYiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3B1ZGFjaXR5LmF1dGgwLmNvbS8iLCJzdWIiOiJlYUVKRU1Ob3pPSHRYYkhHaGFnOEFNbzAwMTRJUDBuQ0BjbGllbnRzIiwiYXVkIjoiU1JLIiwiaWF0IjoxNTkyNjY3NDI5LCJleHAiOjE1OTI3NTM4MjksImF6cCI6ImVhRUpFTU5vek9IdFhiSEdoYWc4QU1vMDAxNElQMG5DIiwic2NvcGUiOiJnZXQ6bW92aWVzIGdldDphY3RvcnMgcG9zdDphY3RvcnMgcGF0Y2g6YWN0b3JzIGRlbGV0ZTphY3RvcnMgcG9zdDptb3ZpZXMgcGF0Y2g6bW92aWVzIGRlbGV0ZTptb3ZpZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsInBvc3Q6YWN0b3JzIiwicGF0Y2g6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInBvc3Q6bW92aWVzIiwicGF0Y2g6bW92aWVzIiwiZGVsZXRlOm1vdmllcyJdfQ.eDBTX_tPNCNxnphhJjFu5unPtiDxJvRVHvpVneFl7zq_Jr8eNxb4f7YiRgUWt2cm2_wsEjt2GQ0otlMdzxYeR69Eu5TTNmpNdIfJY2QD1gBYTzu4D4kMOeykfq5DdVFT2rvral1V5u0ssC2pvjb5RKcwiOZhVPiIVoanCZuj6WOlvIrMX6usfdwlAlvK6Ua5Dhzt9hSQFPJfDyIbVmRDeCtLpyMnih8mIMaRPjTKA8_AVVmQ2R1byT-MiFGmLBPu6jX8EgP-c9eocrONB51W1LRni3HhrRshLzne5K3yxVo7vOdtNGdGov0Ez4IqBsI05L5yePqI_PSE-fpbCSc75A"
        self.castingassitant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBLcmstaFN5clFkNTlkdkhMUzFoYiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3B1ZGFjaXR5LmF1dGgwLmNvbS8iLCJzdWIiOiJlYUVKRU1Ob3pPSHRYYkhHaGFnOEFNbzAwMTRJUDBuQ0BjbGllbnRzIiwiYXVkIjoiU1JLIiwiaWF0IjoxNTkyNjY3NzU4LCJleHAiOjE1OTI3NTQxNTgsImF6cCI6ImVhRUpFTU5vek9IdFhiSEdoYWc4QU1vMDAxNElQMG5DIiwic2NvcGUiOiJnZXQ6bW92aWVzIGdldDphY3RvcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyJdfQ.GpruJHzgpVRofEQOAxW_PT8Clz6ng_J0nnq9fBg_71mOFJPflylXjZLpqPVotrFl3CXYHnlM4FpLQnKoqa5sT9EL6X4BEpPp9CFu5wsAV93jotPENXXiZh8RDB8DwC8SP5acZrTJWOhlXulT9BmGLde1B98WwKlsWHmT4Y03CiqKCeJMUzAUUJkw535oeEbbP4tB6I0iOq2RSIGjGy7AiAKpqV10LXaCtEFJGpZktKhiOw8yVywwiSyXZnF6AL8toXMu1sjMtPC-CI-CkWjZb0CmQXb0OpaMKLRLMgHNzKq12yH5QIXJgWtp_G46tiVJrnzfPEFJI7exxITzEmBoRQ"

    def tearDown(self):
        pass

    # GET
    def test_get_actors(self):
        res = self.app.get(
            "/actors", headers={'Authorization': 'Bearer {}'.format(self.executiveproducer)})
        data = json.loads(res.data)
        self.assertTrue(data['actors'])
        self.assertEqual(data['success'], True)

    def test_error_get_actors(self):
        res = self.app.put(
            '/actors', headers={"Authorization": "Bearer {}".format(self.executiveproducer)})
        data = json.loads(res.data)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method not allowed")

    def test_get_movies(self):
        res = self.app.get(
            '/movies', headers={"Authorization": "Bearer {}".format(self.executiveproducer)})
        data = json.loads(res.data)
        self.assertTrue(data['movies'])
        self.assertEqual(data['success'], True)

    def test_error_get_movies(self):
        res = self.app.put(
            '/movies', headers={"Authorization": "Bearer {}".format(self.executiveproducer)})
        data = json.loads(res.data)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method not allowed")

    # DELETE
    def test_delete_actor(self):
        actor = Actor(id=self.actor['id'], name=self.actor['name'], gender=self.actor['gender'],
                      age=self.actor['age'])
        actor.insert()

        actor_id = self.actor["id"]

        res = self.app.delete('/actors/{}'.format(actor_id),
                              headers={"Authorization": "Bearer {}".format(self.executiveproducer)})
        data = json.loads(res.data)
        self.assertEqual(data['id'], actor_id)
        self.assertEqual(data['success'], True)

    def test_error_delete_actor(self):
        res = self.app.delete(
            '/actors/10960', headers={"Authorization": "Bearer {}".format(self.executiveproducer)})
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie(self):
        movie = Movie(
            id=self.movie['id'], title=self.movie['title'], release_date=self.movie['release_date'])
        movie.insert()

        movie_id = self.movie["id"]

        res = self.app.delete('/movies/{}'.format(movie_id), headers={
                              "Authorization": "Bearer {}".format(self.executiveproducer)})
        data = json.loads(res.data)
        self.assertEqual(data['id'], movie_id)
        self.assertEqual(data['success'], True)

    def test_error_delete_movie(self):
        res = self.app.delete('/movies/10960', headers={
                              "Authorization": "Bearer {}".format(self.executiveproducer)})
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # POST

    def test_add_actor(self):
        res = self.app.post("/actors",
                            headers={"Authorization": "Bearer {}".format(self.executiveproducer)}, json=self.actor)
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data['actors'])

    def test_error_actor(self):

        actor = self.actor

        actor.pop('name')
        res = self.app.post("/actors",
                            headers={"Authorization": "Bearer {}".format(self.executiveproducer)}, json=actor)
        data = json.loads(res.data)

        self.assertEqual(data['message'], 'Bad request')
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)

    def test_add_movie(self):
        res = self.app.post("/movies",
                            headers={"Authorization": "Bearer {}".format(self.executiveproducer)}, json=self.movie)
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data['movies'])

    def test_error_movie(self):

        movie = self.movie

        movie.pop('title')
        res = self.app.post("/movies",
                            headers={"Authorization": "Bearer {}".format(self.executiveproducer)}, json=self.movie)
        data = json.loads(res.data)

        self.assertEqual(data['message'], 'Bad request')
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)

    # RBAC
    # 1. Casting Assitant
    def test_create_actors_casting_assitant(self):
        res = self.app.post("/actors",
                            headers={"Authorization": "Bearer {}".format(self.castingassitant)}, json=self.actor)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

        self.assertEqual(data['code'], "invalid_claims")
        self.assertEqual(data['description'], "Permission denied.")

    def test_get_actors_casting_assitant(self):
        res = self.app.get(
            '/actors', headers={"Authorization": "Bearer {}".format(self.castingassitant)})

        data = json.loads(res.data)
        self.assertTrue(data['actors'])
        self.assertEqual(data['success'], True)

    # 2. Executive Producer

    def test_create_movies_executive_producer(self):
        res = self.app.post('/movies',
                            headers={"Authorization": "Bearer {}".format(self.executiveproducer)}, json=self.movie)

        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data['movies'])

    def test_get_actors_executive_producer(self):
        res = self.app.get(
            '/actors', headers={"Authorization": "Bearer {}".format(self.executiveproducer)})

        data = json.loads(res.data)
        self.assertTrue(data['actors'])
        self.assertEqual(data['success'], True)

    # 3. Casting Director

    def test_delete_movies_casting_director(self):
        movie = Movie(
            id=self.movie['id'], title=self.movie['title'], release_date=self.movie['release_date'])
        movie.insert()

        movie_id = movie.id

        res = self.app.delete('/movies/{}'.format(movie_id),
                              headers={"Authorization": "Bearer {}".format(self.castingdirector)})
        data = json.loads(res.data)
        self.assertEqual(data['id'], movie_id)
        self.assertEqual(data['success'], True)

    def test_create_actors_casting_director(self):
        res = self.app.post("/actors",
                            headers={"Authorization": "Bearer {}".format(self.castingdirector)}, json=self.actor)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

        self.assertEqual(data['code'], "invalid_claims")
        self.assertEqual(data['description'], "Permission denied.")


if __name__ == "__main__":
    unittest.main()
