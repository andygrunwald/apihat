import argparse
import ConfigParser
import os.path

"""
These functions are a subset of the original configuration functionality of sortinghat.

Sadly we are not able to import the functions itself,
so we have to copy part of the functionality to support their configuration.

Mainly we copied (and maybe modified / stripped down) four functions:
    * create_config_arguments_parser
    * parse_args
    * create_common_arguments_parser
    * read_config_file

The original source can be found at
https://github.com/MetricsGrimoire/sortinghat/blob/master/bin/sortinghat
"""


def create_config_arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config_file', help=argparse.SUPPRESS)

    # Set default values
    defaults = {
        'config_file' : os.path.expanduser('~/.sortinghat'),
    }
    parser.set_defaults(**defaults)

    return parser


def parse_args():
    # Parse first configuration file parameter
    config_parser = create_config_arguments_parser()
    config_args, args = config_parser.parse_known_args()

    # And then, read default parameters from a configuration file
    if config_args.config_file:
        defaults = read_config_file(config_args.config_file)
    else:
        defaults = {}

    # Parse common arguments using the command parser
    parser = create_common_arguments_parser(defaults)

    # Parse arguments
    return parser.parse_args(args)


def create_common_arguments_parser(defaults):
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)

    # Options
    group = parser.add_argument_group('General options')
    group.add_argument('-u', '--user', dest='user', default='root',
                       help=argparse.SUPPRESS)
    group.add_argument('-p', '--password', dest='password', default='',
                       help=argparse.SUPPRESS)
    group.add_argument('-d', '--database', dest='database',
                       help=argparse.SUPPRESS)
    group.add_argument('--host', dest='host', default='localhost',
                       help=argparse.SUPPRESS)
    group.add_argument('--port', dest='port', default='3306',
                       help=argparse.SUPPRESS)

    # Set default values
    parser.set_defaults(**defaults)

    return parser


def read_config_file(filepath):
    config = ConfigParser.SafeConfigParser()
    config.read(filepath)

    if 'db' in config.sections():
        return dict(config.items('db'))
    else:
        return {}

"""
Global args
We store the parsed arguments of the configuration file
in a global way here to avoid I/O (reading the configuration file)
at every request.

At the moment i don`t know how to inject args into a Flask Restful Resource
(without the use of another Flas extension (flash-inject).
"""
args = ""


def set_parsed_args(parsed_args):
    global args
    args = parsed_args


def get_parsed_args():
    return args