# -*- coding: utf-8 -*-
from zope.component import getUtility
from zope.component import getGlobalSiteManager
gsm = getGlobalSiteManager()

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


class AnyBlok:
    """ Main Class use to work on the registry

        This class is known in the ``sys.modules``::

            import AnyBlok
            from AnyBlok import target_registry

    """

    __registry_name__ = 'AnyBlok'
    current_blok = None

    @classmethod
    def target_registry(cls, registry, cls_=None, **kwargs):
        """ Method to add in registry

            Locate on one registry, this method use the ZCA to know which
            ``Adapter.target_registry`` use

            :param registry: An existing AnyBlok registry
            :param ``cls_``: The ``class`` object to add in the registry
            :rtype: ``cls_``
        """

        def call_adapter(self):
            _interface = ''
            if registry == AnyBlok:
                _interface = self.__name__
            else:
                _interface = registry.__interface__

            name = kwargs.get('name', self.__name__)
            adapter = getUtility(AnyBlok.Interface.ICoreInterface, _interface)
            adapter.target_registry(registry, name, self, **kwargs)

            return self

        if cls_:
            return call_adapter(cls_)
        else:
            return call_adapter

    @classmethod
    def remove_registry(cls, registry, cls_=None, **kwargs):
        """ Method to remove in registry

            Locate on one registry, this method use the ZCA to know which
            ``Adapter.remove_registry`` use

            :param registry: An existing AnyBlok registry
            :param ``cls_``: The ``class`` object to remove in the registry
            :rtype: ``cls_``
        """
        assert cls_

        def call_adapter(self):
            _interface = registry.__interface__

            name = kwargs.get('name', self.__name__)
            adapter = getUtility(AnyBlok.Interface.ICoreInterface, _interface)
            adapter.remove_registry(registry, name, self, **kwargs)

            return self

        return call_adapter(cls_)

    @classmethod
    def add_Adapter(cls, _interface, cls_):
        """ Method to add a adapter

        :param interface: The ZCA interface
        :param cls_: The ``class`` object to add this interface
        """
        instance = cls_()
        gsm.registerUtility(instance, _interface, cls_.__interface__)


from sys import modules
modules['AnyBlok'] = AnyBlok


from . import _imp  # noqa
from . import interface  # noqa
from . import databases  # noqa
from . import core  # noqa
from . import field  # noqa
from . import column  # noqa
from . import relationship  # noqa
from . import model  # noqa
from . import mixin  # noqa
from . import bloks  # noqa
