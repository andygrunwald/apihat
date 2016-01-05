from flask import make_response
from flask_restful import Resource


class PingAPI(Resource):
    def get(self):
        """
        REST command:
            GET	        http://[hostname]/ping      Ping <-> Pong endpoint
        """
        response = make_response("pong")
        response.headers['content-type'] = 'text/plain'
        return response