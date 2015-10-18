#!/usr/bin/env python

from flask import Flask
from flask_restful import Api

from sortinghat import api
from apihat.config import parse_args, set_parsed_sortinghat_args
from apihat.api.specific_identity import SpecificIdentityAPI
from apihat.api.identities import IdentitiesAPI

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    # Just parse the sortinghat configuration once
    args = parse_args()
    set_parsed_sortinghat_args(args)

    api.add_resource(SpecificIdentityAPI, '/v1.0/identities/<string:uuid>', endpoint='specific_identity')
    api.add_resource(IdentitiesAPI, '/v1.0/identities', endpoint='identities')

    app.run(debug=True)
