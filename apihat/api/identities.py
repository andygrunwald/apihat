from flask_restful import Resource, abort, reqparse
from apihat.config import get_parsed_sortinghat_args
from sortinghat.matching import SORTINGHAT_IDENTITIES_MATCHERS
from sortinghat.exceptions import CODE_MATCHER_NOT_SUPPORTED_ERROR, CODE_ALREADY_EXISTS_ERROR, CODE_NOT_FOUND_ERROR, CODE_VALUE_ERROR
from httplib import CREATED, CONFLICT, BAD_REQUEST

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
from sortinghat.cmd.add import Add


class IdentitiesAPI(Resource):
    def get(self):
        """
        sortinghat command:
            show        Show information about a unique identity

        REST command:
            GET	    http://[hostname]v1.0/identities      Retrieve identities
        """
        # Request arguments
        parser = reqparse.RequestParser()
        parser.add_argument('term', type=str, location='args')
        args = parser.parse_args()

        # Sortinghat action
        s_args = get_parsed_sortinghat_args()
        cmd = Show(user=s_args.user, password=s_args.password, database=s_args.database, host=s_args.host, port=s_args.port)
        code = cmd.show(None, args.term)

        # In failure case
        if code == SortinghatCommand.CMD_FAILURE:
            v = cmd.get_error_vars()
            abort(404, message=v)

        # If everything went well
        v = cmd.get_display_vars()
        identities = [i.to_dict() for i in v['uidentities']]

        return {"identities": identities}

    def post(self):
        """
        sortinghat command:
            add         Add identities

        REST command:
            POST	    http://[hostname]v1.0/identities      Add identities
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
        s_args = get_parsed_sortinghat_args()
        cmd = Add(user=s_args.user, password=s_args.password, database=s_args.database, host=s_args.host, port=s_args.port)
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

        # In failure case:
        if code == CODE_NOT_FOUND_ERROR:
            # TODO Get correct error code
            abort(400, message=v)

        # In failure case:
        if code == CODE_VALUE_ERROR:
            # TODO Get correct error code
            abort(400, message=v)

        # If everything went well
        v = cmd.get_display_vars()
        return {"id": v['id'], "uuid": v['uuid']}, CREATED
