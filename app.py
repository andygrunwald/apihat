#!/usr/bin/env python

import os
from flask import Flask
from flask_restful import Api

from sortinghat import api
from apihat.api.specific_identity import SpecificIdentityAPI
from apihat.api.identities import IdentitiesAPI
from apihat.api.ping import PingAPI


def get_configuration():
    """
    get_configuration will read the configuration from
    env vars and return it.
    This configuration contains env vars from sortinghat as well.

    We don`t support the configuration file of sortinghat.
    We only support the env vars of sortinghat.

    This make several things much more easier:
    * We don`t have I/O here.
    * We follow 12factor apps
    * We can supply env vars easy in a docker / cloud env
    """
    args = dict(user=os.getenv('SORTINGHAT_DB_USER', 'root'),
                password=os.getenv('SORTINGHAT_DB_PASSWORD', ''),
                database=os.getenv('SORTINGHAT_DB_DATABASE', ''),
                host=os.getenv('SORTINGHAT_DB_HOST', 'localhost'),
                port=os.getenv('SORTINGHAT_DB_PORT', '3306'))
    return args


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    # Initialize / Read the configuration
    # We support here the same env vars as sortinghat does
    config = get_configuration()
    kwargs = {'config': config}

    api.add_resource(PingAPI, '/ping')

    api.add_resource(SpecificIdentityAPI, '/identities/<string:uuid>', resource_class_kwargs=kwargs)
    api.add_resource(IdentitiesAPI, '/identities', resource_class_kwargs=kwargs)

    app.run(host=os.getenv('APIHAT_HOST', '0.0.0.0'),
            port=int(os.getenv('APIHAT_PORT', 5000)),
            debug=os.getenv('APIHAT_DEBUG', False))
