## Script (Python) "popupstringize"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=strng
##title=Properly stringize and quote for Javascript

return str(strng).replace("'","\\'")
