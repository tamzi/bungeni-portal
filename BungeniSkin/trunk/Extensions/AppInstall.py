from StringIO import StringIO
from Products.CMFCore.utils import getToolByName

def install(self):
    """ Tweak settings .. 
    """
    out = StringIO()

    plone = getToolByName(self, 'portal_url').getPortalObject()

    # Leave only the theme slot on the left; move all the others to the
    # right.
    left_slots = list(plone.getProperty('left_slots'))
    right_slots = list(plone.getProperty('right_slots'))
    theme_slots = [slot for slot in left_slots if 'theme' in slot]
    for s in theme_slots:
        left_slots.remove(s)
    plone.manage_changeProperties({
            'left_slots': theme_slots,
            'right_slots': left_slots + right_slots,
            })

    print >>out, 'Moved all the left slots but the theme(s) to the right.'

    return out.getvalue()
