from StringIO import StringIO
from Products.CMFCore.utils import getToolByName

def install(self):
    """ Tweak settings .. 
    """
    out = StringIO()

    plone = getToolByName(self, 'portal_url').getPortalObject()

    #
    # Tweak portlets
    #
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

    #
    # Tweak actions
    #
    actions_tool = getToolByName(portal, 'portal_actions', None)
    changed_actions = {
        'rss': {'category': 'site_actions',}
        }
    cloned_actions = actions_tool._cloneActions()
    for action in cloned_actions:
        changes = changed_actions.get(action.getId(), None)
        if changes:
            action.edit(**changes)
            print >>out, 'Tweaked %s action.' % action.getId()
    actions_tool._actions = cloned_actions

    print >>out, 'Tweaked actions.'

    return out.getvalue()
