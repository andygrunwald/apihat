#!/usr/bin/env python

from flask import Flask
from flask_restful import Api, Resource, abort
from sortinghat import api
from apihat.config import parse_args

'''
In the next few lines we get a little bit tricky.

We replace sortinghat.command with apihat.api_command
to be able to use the original sortinghat source code as much as possible.

For a detailed description have a look at the apihat.api_command class.
'''
import sortinghat.command as SortinghatCommand
from apihat.api_command import ApiCommand

SortinghatCommand.Command = ApiCommand

from sortinghat.cmd.show import Show


class IdentityAPI(Resource):
    def get(self, uuid):
        """
        sortinghat command:
            show        Show information about a unique identity

        REST command:
            GET	    http://[hostname]/v1.0/identity/[uuid]      Retrieve an identity
        """
        cmd = Show(user=args.user, password=args.password, database=args.database, host=args.host, port=args.port)
        code = cmd.show(uuid, None)

        # In failure case
        if code == SortinghatCommand.CMD_FAILURE:
            v = cmd.get_error_vars()
            abort(404, message=v)

        # If everything was going well
        v = cmd.get_display_vars()
        identity = v['uidentities'][0]

        return identity.to_dict()

    def delete(self, uuid):
        """
        sortinghat command:
            rm          Remove identities from the registry

        REST command:
            DELETE	    http://[hostname]/v1.0/identity/[uuid]      Delete an identity
        """

        # TODO IMPLEMENT
        pass


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    # Just parse the sortinghat configuration once
    args = parse_args()

    api.add_resource(IdentityAPI, '/v1.0/identity/<string:uuid>', endpoint='identity')

    app.run(debug=True)
