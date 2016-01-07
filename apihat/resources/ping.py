from flask_restful import Resource


class PingAPI(Resource):
    def get(self):
        """
        REST command:
            GET	        http://[hostname]/ping      Ping <-> Pong endpoint
        """

        return {
            "content": "pong"
        }