from httplib import CREATED, CONFLICT, BAD_REQUEST, NOT_FOUND

from flask_restful import Resource, abort, reqparse
from sortinghat.exceptions import CODE_MATCHER_NOT_SUPPORTED_ERROR, CODE_ALREADY_EXISTS_ERROR, CODE_NOT_FOUND_ERROR, CODE_VALUE_ERROR
from sortinghat.matching import SORTINGHAT_IDENTITIES_MATCHERS

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
from sortinghat.cmd.add import Add


class IdentitiesAPI(Resource):

    def __init__(self, **kwargs):
        self.config = kwargs['config']

    def get(self):
        """
        sortinghat command:
            show        Show information about a unique identity

        REST command:
            GET	        http://[hostname]/identities      Retrieve identities
        """
        # Request arguments
        parser = reqparse.RequestParser()
        parser.add_argument('term', type=str, location='args')
        args = parser.parse_args()

        # Sortinghat action
        c = self.config
        cmd = Show(user=c['user'], password=c['password'], database=c['database'], host=c['host'], port=c['port'])
        code = cmd.show(None, args.term)

        # In failure case
        # TODO Switch constant if show has new error codes
        if code == SortinghatCommand.CMD_FAILURE:
            v = cmd.get_error_vars()
            abort(NOT_FOUND, message=v)

        # If everything went well
        v = cmd.get_display_vars()
        identities = [i.to_dict() for i in v['uidentities']]

        return {"identities": identities}

    def post(self):
        """
        sortinghat command:
            add         Add identities

        REST command:
            POST	    http://[hostname]/identities      Add identities
        """
        # Request arguments
        parser = reqparse.RequestParser()
        parser.add_argument('name', default=None, location='form')
        parser.add_argument('email', default=None, location='form')
        parser.add_argument('username', default=None, location='form')
        parser.add_argument('uuid', default=None, location='form')
        parser.add_argument('source', default='unknown', location='form')
        parser.add_argument('matching', default=None, location='form', choices=SORTINGHAT_IDENTITIES_MATCHERS)
        args = parser.parse_args()

        # Sortinghat action
        c = self.config
        cmd = Add(user=c['user'], password=c['password'], database=c['database'], host=c['host'], port=c['port'])
        code = cmd.add(
            source=args.source,
            email=args.email,
            name=args.name,
            username=args.username,
            uuid=args.uuid,
            matching=args.matching,
            interactive=False
        )

        v = cmd.get_error_vars()
        # In failure case: Wrong matcher supplied
        if code == CODE_MATCHER_NOT_SUPPORTED_ERROR:
            abort(BAD_REQUEST, message=v)

        # In failure case: Identity already exists
        if code == CODE_ALREADY_EXISTS_ERROR:
            abort(CONFLICT, message=v)

        # In failure case: When the unique identity associated to the given 'uuid' is not in the registry.
        if code == CODE_NOT_FOUND_ERROR:
            abort(NOT_FOUND, message=v)

        # In failure case: When source is None or empty; each one of the parameters is None; parameters are empty.
        if code == CODE_VALUE_ERROR:
            abort(BAD_REQUEST, message=v)

        # If everything went well
        v = cmd.get_display_vars()
        return {"id": v['id'], "uuid": v['uuid']}, CREATED
