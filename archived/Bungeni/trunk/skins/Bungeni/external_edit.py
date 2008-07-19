## Script (Python) "external_edit_take"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Overrides Plone external_edit to edit transcription in case of Take

from Products.PythonScripts.standard import url_quote

if context.portal_type == 'Take':
    transcription_id = context.contentIds(
            filter={'portal_type': 'TakeTranscription'})[0]
    external_edit_url = '%s/externalEdit_/%s' % (
            context.absolute_url(),
            url_quote(context[transcription_id].getId()))
else:
    # The original
    external_edit_url = '%s/externalEdit_/%s' % (
            context.aq_parent.absolute_url(),
            url_quote(context.getId()))

return context.REQUEST['RESPONSE'].redirect(external_edit_url)
