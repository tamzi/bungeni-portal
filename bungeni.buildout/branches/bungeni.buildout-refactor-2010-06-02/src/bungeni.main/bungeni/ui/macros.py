"""
$Id: macros.py 6262 2010-03-19 08:29:49Z mario.ruggier $
"""


from zope.app.basicskin.standardmacros import StandardMacros as BaseMacros


class StandardMacros( BaseMacros ):

    macro_pages = ['ploned-layout', 'alchemist-form']

