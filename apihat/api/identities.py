from flask_restful import Resource, abort, reqparse
from apihat.config import get_parsed_sortinghat_args

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


class IdentitiesAPI(Resource):
    def get(self):
        """
        sortinghat command:
            show        Show information about a unique identity

        REST command:
            GET	    http://[hostname]v1.0/identities      Retrieve identities
        """
        #
        parser = reqparse.RequestParser()
        parser.add_argument('term', type=str, location='args')
        args = parser.parse_args()

        s_args = get_parsed_sortinghat_args()
        cmd = Show(user=s_args.user, password=s_args.password, database=s_args.database, host=s_args.host, port=s_args.port)
        code = cmd.show(None, args.term)

        # In failure case
        if code == SortinghatCommand.CMD_FAILURE:
            v = cmd.get_error_vars()
            abort(404, message=v)

        # If everything was going well
        v = cmd.get_display_vars()
        identities = [i.to_dict() for i in v['uidentities']]

        # TODO: Add an array as top level? Or chose a different identifier / key?
        return {"u": identities}