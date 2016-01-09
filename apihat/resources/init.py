from httplib import CREATED, BAD_REQUEST, INTERNAL_SERVER_ERROR
from flask_restful import Resource, abort, reqparse
from sortinghat.command import CMD_SUCCESS

'''
In the next few lines we get a little bit tricky.

We replace sortinghat.command with apihat.api_command
to be able to use the original sortinghat source code as much as possible.

For a detailed description have a look at the apihat.api_command class.
'''
import sortinghat.command as SortinghatCommand
from apihat.resources.api_command import ApiCommand


SortinghatCommand.Command = ApiCommand

from sortinghat.cmd.init import Init


class InitAPI(Resource):

    def __init__(self, **kwargs):
        self.config = kwargs['config']

    def post(self):
        """
        sortinghat command:
            init         Create an empty registry

        REST command:
            POST	    http://[hostname]/init      Create an empty registry
        """
        # Request arguments
        parser = reqparse.RequestParser()
        parser.add_argument('name', default=None, location='json')
        args = parser.parse_args()

        if args.name is None:
            abort(BAD_REQUEST, message="Name of the database to store the registry is missing")

        # Sortinghat action
        c = self.config
        cmd = Init(user=c['user'], password=c['password'], database=c['database'], host=c['host'], port=c['port'])
        code = cmd.initialize(name=args.name)

        # In failure case
        if code > CMD_SUCCESS:
            v = cmd.get_error_vars()
            abort(INTERNAL_SERVER_ERROR, message=v)

        # If everything went well
        return req, CREATED
