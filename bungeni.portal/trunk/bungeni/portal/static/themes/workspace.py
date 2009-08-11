from pyquery import PyQuery as pq
from urlparse import urlsplit

def rules(content, theme, resource_fetcher, log, workspace_id):
    nav = theme('dl.workspace-tab dd#fieldset-display-form-workspace div.workspace-content')
    
    workspace_content = theme(workspace_id).val()
    try:
        url_value = urlsplit(log.theme_url)
        d = pq(url=url_value[0] + '://' +  url_value[1]+ "/" + workspace_content)
        c = d('#portal-column-content').html()
        nav.append(c)
    except:
        pass
