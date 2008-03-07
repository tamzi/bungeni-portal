"""
zope3 authenticator plugin against a relational database
"""

from zope import interface, component
from domain import User
from alchemist.security.interfaces import IAlchemistUser, IAlchemistAuth

@interface.implementer( IAlchemistUser )
@component.adapter( IAlchemistAuth )
def authUser( util ):
    return User
