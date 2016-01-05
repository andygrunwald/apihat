import os

"""
We don`t support the configuration file of sortinghat.
We only support the env vars of sortinghat.

This make several things much more easier:
* We don`t have I/O here.
* We follow 12factor apps
* We can supply env vars easy in a docker / cloud env

We store the configuration in a global way here.
At the moment i don`t know how to inject args into a Flask Restful Resource
(without the use of another Flask extension (flash-inject).
"""
args = dict()


def initialize_config():
    global args
    args = dict(user=os.getenv('SORTINGHAT_DB_USER', 'root'),
                password=os.getenv('SORTINGHAT_DB_PASSWORD', ''),
                database=os.getenv('SORTINGHAT_DB_DATABASE', ''),
                host=os.getenv('SORTINGHAT_DB_HOST', 'localhost'),
                port=os.getenv('SORTINGHAT_DB_PORT', '3306'))


def get_config():
    return args