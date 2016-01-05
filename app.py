#!/usr/bin/env python

from flask import Flask
from flask_restful import Api

from sortinghat import api
from apihat.config import initialize_config
from apihat.api.specific_identity import SpecificIdentityAPI
from apihat.api.identities import IdentitiesAPI

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    # Initialize the configuration
    # We support here the same env vars as sortinghat does
    initialize_config()

    api.add_resource(SpecificIdentityAPI, '/identities/<string:uuid>', endpoint='specific_identity')
    api.add_resource(IdentitiesAPI, '/identities', endpoint='identities')

    app.run(debug=True)
