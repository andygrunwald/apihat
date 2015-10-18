from flask_restful import Resource, abort
from apihat.config import get_parsed_args

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


class SpecificIdentityAPI(Resource):
    def get(self, uuid):
        """
        sortinghat command:
            show        Show information about a unique identity

        REST command:
            GET	    http://[hostname]/v1.0/identity/[uuid]      Retrieve an identity
        """
        args = get_parsed_args()
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