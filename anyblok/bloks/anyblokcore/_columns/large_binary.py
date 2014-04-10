from sqlalchemy.types import LargeBinary as SA_LargeBinary
from AnyBlok import target_registry, Column


@target_registry(Column)
class LargeBinary(Column):
    """ Large binary column

    ::

        from AnyBlok import target_registry, Model
        from AnyBlok.Column import LargeBinary
        from os import urandom

        blob = urandom(100000)

        @target_registry(Model)
        class Test:

            x = LargeBinary(label="Integer", default=blob)

    """
    sqlalchemy_type = SA_LargeBinary
