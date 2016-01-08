from httplib import NOT_FOUND
from flask_restful import Resource, abort
from sortinghat.exceptions import CODE_NOT_FOUND_ERROR

'''
In the next few lines we get a little bit tricky.

We replace sortinghat.command with apihat.api_command
to be able to use the original sortinghat source code as much as possible.

For a detailed description have a look at the apihat.api_command class.
'''
import sortinghat.command as SortinghatCommand
from apihat.resources.api_command import ApiCommand


SortinghatCommand.Command = ApiCommand

from sortinghat.cmd.show import Show


class SpecificIdentityAPI(Resource):

    def __init__(self, **kwargs):
        self.config = kwargs['config']

    def get(self, uuid):
        """
        sortinghat command:
            show        Show information about a unique identity

        REST command:
            GET	        http://[hostname]/identity/[uuid]      Retrieve an identity
        """
        # Sortinghat action
        c = self.config
        cmd = Show(user=c['user'], password=c['password'], database=c['database'], host=c['host'], port=c['port'])
        code = cmd.show(uuid, None)

        # In failure case
        if code == CODE_NOT_FOUND_ERROR:
            v = cmd.get_error_vars()
            abort(NOT_FOUND, message=v)

        # If everything went well
        v = cmd.get_display_vars()
        identity = v['uidentities'][0]

        return identity.to_dict()