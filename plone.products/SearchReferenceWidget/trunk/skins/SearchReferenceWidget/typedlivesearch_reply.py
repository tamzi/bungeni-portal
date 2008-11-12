## Script (Python) "livescript_reply"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=q,limit=10,path=None,allowed_types=[],portal_type=None,toolname=None
##title=Determine whether to show an id in an edit form

catalog = context.portal_catalog
def quote(s):
    return s.replace("'","\\'").replace(">","&gt;").replace('"','\\"')

def anchor_func(result,display_title):
    uid = result.getObject().UID()
    js = "window.%s.addReference('%s', '%s'); return false" % \
        (toolname, quote(uid), quote(display_title))
    #js = "alert(window.%s.addreference.allowed_types); return false;" %(toolname)
    return'''<a href="#" title="%s" onClick="%s">%s</a>''' % (display_title, js, display_title)
    
def query_func(SearchableText, path):
    query = {'sort-on':'modified','sort-order':'reverse', 'sort-limit':10}
    query['portal_type'] = portal_type or allowed_types
    if SearchableText != '*':
        query['Title'] = SearchableText
    if path:
        query['path'] = path
        
    return catalog(query,limit=10)
        
    

return context.livesearch_reply(q=q,limit=limit,
                                path=path,
                                query_func=query_func,
                                anchor_func=anchor_func,
                                advanced_search=False)