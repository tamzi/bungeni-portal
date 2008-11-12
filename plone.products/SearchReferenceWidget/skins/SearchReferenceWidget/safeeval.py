## Script (Python) "safeeval"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=str_rep=''
##title=Safely transform a string to a Python constant

from Products.PopupReferenceWidget.safe_eval import const_eval

# LOAD_NAME opcode is not available without much pain
if str_rep in ('None', None):
    return None
if str_rep in ('True', True):
    return True
if str_rep in ('False', False):
    return False
return const_eval(str_rep)
