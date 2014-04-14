# -*- coding: utf-8 -*-
from . import release


PROMPT = "%(processName)s - %(version)s"


def start(processName, version=release.version, prompt=PROMPT,
          argsparse_groups=None, parts_to_load=None, logger=None):
    """ Initialise the application

    ::

        registry = start('My application',
                         argsparse_groups=['config', 'database'],
                         parts_to_load=['AnyBlok'])

    :param processName: Name of the application
    :param version: Version of the application
    :param prompt: Prompt message for the help
    :param argsparse_groups: list of the group of option for argparse
    :param parts_to_load: group of blok to load
    :param logger: option to configure  logging
    :rtype: registry if the database is configurate
    """
    from .blok import BlokManager
    from ._argsparse import ArgsParseManager
    from .registry import RegistryManager

    if parts_to_load is None:
        parts_to_load = ['AnyBlok']

    BlokManager.load(*parts_to_load)
    description = prompt % {'processName': processName, 'version': version}
    if argsparse_groups is not None:
        ArgsParseManager.load(description=description,
                              argsparse_groups=argsparse_groups,
                              parts_to_load=parts_to_load)

    if logger is None:
        logger = {}
    ArgsParseManager.init_logger(**logger)
    dbname = ArgsParseManager.get('dbname')
    if not dbname:
        return None

    registry = RegistryManager.get(dbname)
    registry.commit()
    return registry


from .declarations import Declarations  # noqa
from . import exception  # noqa
from . import _imp  # noqa
from . import databases  # noqa
from . import core  # noqa
from . import field  # noqa
from . import column  # noqa
from . import relationship  # noqa
from . import model  # noqa
from . import mixin  # noqa
from . import bloks  # noqa
