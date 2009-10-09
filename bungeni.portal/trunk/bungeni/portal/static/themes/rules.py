from pyquery import PyQuery as pq
from urlparse import urlsplit

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

def drop_workspace(content, theme, resource_fetcher, log):
    member_workspace_content_id = theme('#user-workspace-id').val()
    group_workspace_content_id = theme('#workgroup-id').val()
    if member_workspace_content_id is None  and group_workspace_content_id is None:
        theme('.workspace-tab').remove()


def nextprev_links(content, theme, resource_fetcher, log):
    """
    Modify calendar 'next and 'previous' links so that the page refreshes.
    """
    calendar_next_link_node = theme('.next-link')
    calendar_previous_link_node = theme('.previous-link') \
                               
    if calendar_next_link_node:
        calendar_next_link_node.replaceWith('<a class="navigation next-link" onClick="document.location=&#39;' + str(theme('.next-link').attr('href'))  + '&#39;">&#8594;</a>')
        
    if calendar_previous_link_node:
        calendar_previous_link_node.replaceWith('<a class="navigation previous-link" onClick="document.location=&#39;' + str(theme('.previous-link').attr('href'))  + '&#39;">&#8592;</a>')    

   

def rewrite_links(content, theme, resource_fetcher, log):
    """
    Fix links in folders that have been set up to act as root nodes.
    Relative links can end up with the root folder entry repeated twice.
    In addition some links are not children of the current root node i.e.
    they may belong to another root node but accesible from here.
    Remove the first root folder entry if necessary.
    """

    repeating_link_values = ['calendar']
    strip_link_values = {'/calendar/business': '/business'}
    content_items = [['#portal-breadcrumbs','id', 'div']]

    for link_value in repeating_link_values:
        for content_item in content_items:
            theme_node = theme(content_item[0])
            theme_value = theme(content_item[0]).html()
            content_node = content(content_item[0])
            content_value = content(content_item[0]).html()

            if '/' + link_value + '/' + link_value in (unicode(content_value)):
                new_content = content_value.replace('/'+link_value+'/'+link_value, '/'+link_value)
                content_node.replaceWith('<' + content_item[2]  + ' ' + content_item[1] +'="' + str(content_item[0])[1:] +'">' + new_content + '</' + content_item[2] + '>')

            if '/' + link_value + '/' + link_value in (unicode(theme_value)):
                new_theme = theme_value.replace('/'+link_value+'/'+link_value, '/'+link_value)
                theme_node.replaceWith('<' + content_item[2]  + ' ' + content_item[1] +'="' + str(content_item[0])[1:] +'">' + new_theme + '</' + content_item[2] + '>')

    for link_value in strip_link_values:
        for content_item in content_items:
            theme_node = theme(content_item[0])
            theme_value = theme(content_item[0]).html()            
            content_node = content(content_item[0])
            content_value = content(content_item[0]).html()

            if link_value in (unicode(theme_value)):
                new_theme = theme_value.replace(link_value, strip_link_values[link_value])
                theme_node.replaceWith('<'+content_item[2]  + ' ' + content_item[1] +'="' + str(content_item[0])[1:] +'">' + new_theme + '</' + content_item[2] + '>')

            
            if link_value in (unicode(content_value)):
                new_content = content_value.replace(link_value, strip_link_values[link_value])
                content_node.replaceWith('<'+content_item[2]  + ' ' + content_item[1] +'="' + str(content_item[0])[1:] +'">' + new_content + '</' + content_item[2] + '>')


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
