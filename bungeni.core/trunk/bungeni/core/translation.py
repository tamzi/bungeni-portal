from bungeni.core.i18n import  _

def get_default_language():
    return "en"

def get_language(context):
    return "en"

def has_language(context, name):
    return False

def available_languages():
    return (
        ('en', _(u"English")),
        ('fr', _(u"French")),
        ('sw', _(u"Swahili")),
        )
