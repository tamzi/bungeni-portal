from webob import Request, Response
from pyquery import PyQuery as pq
from pyquery.ajax import PyQuery as apq
from urlparse import urlsplit
from pprint import pprint


def add_workspace(content, theme, resource_fetcher, log, workspace_id):
    """Get the workspace content from plone using the hidden id from bungeni
       or drop the tabs.
    """
    workspace_item = theme('dl.workspace-tab dd#fieldset-display-form-workspace div.workspace-content')
    
    workspace_content_id = theme(workspace_id).val()
    if workspace_content_id is not None:
        try:
            host_url = urlsplit(log.theme_url)
            workspace_url = pq(url=host_url[0] + '://' +  host_url[1]+ "/" + workspace_content_id)
            workspace_content = workspace_url('#portal-column-content').html()
            workspace_item.append(workspace_content)
        except:
            pass
    else:
        content_item = theme('.maincontent')
        print content_item
        content_item.remove('.workspace-tab')


def rewrite_links(content, theme, resource_fetcher, log):
    """Fix links in folders that have been set up to act as root nodes.
    Relative links can end up with the root folder entry repeated twice.
    In additions some links are not children of the current root node i.e.
    they may belong to another root node but accesible from here.
    Remove the first root folder entry if necessary.
    """
    repeating_link_values = ['business', 'calendar']
    strip_link_values = {'/calendar/business': '/business'}
    content_items = {'#portal-breadcrumbs':'id', '.contentActions':'class', '#calendar-table':'id'}

    for link_value in repeating_link_values:
        for content_item in content_items:
            content_node = theme(content_item)
            content_value = theme(content_item).html()
            
            if link_value + '/' + link_value +'/' in (unicode(content_value)):
                new_content = content_value.replace('/'+link_value+'/'+link_value, '/'+link_value)
                content_node.replaceWith('<div ' + content_items[content_item] +'="' + content_item[1:] +'">' + new_content + '</div>')

    for link_value in strip_link_values:
        for content_item in content_items:
            content_node = theme(content_item)
            content_value = theme(content_item).html()
            
            if link_value in (unicode(content_value)):
                new_content = content_value.replace(link_value, strip_link_values[link_value])
                content_node.replaceWith('<div ' + content_items[content_item] +'="' + content_item[1:] +'">' + new_content + '</div>')


def drop_contentActions(content, theme, resource_fetcher, log):
    """If the user is anonymous drop the 'contentActions' bar.
    """
    content_item = pq(theme('#portal-column-content'))
    if not pq(theme('#portal-personaltools')).filter('#user-name'):
        content_item.remove('.contentActions')

        
def move_portlet(content, theme, resource_fetcher, log):
    """Users with no workspace (admin) get their review portlet on the right column.
    """
    if not pq(theme('html').filter('body#bungeni-workspace')):
        theme('#portal-column-two').append(theme('#review-portlet'))

def documentActions_links(content, theme, resource_fetcher, log):
    """Fix the 'documentActions' for the business, members, archive and
    calendar folders.
    """
    link_values = ['business', 'calendar', 'members', 'archive']

    for link_value in link_values:
        content_value = theme('.documentActions').html()
        content_node = theme('.documentActions')
        if link_value in (unicode(content_value)):
            new_content = content_value.replace('/'+link_value, '/plone/'+link_value)
            content_node.replaceWith('<div class="documentActions">' + new_content + '</div>')
