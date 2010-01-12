from pyquery import PyQuery as pq
from urlparse import urlsplit

def add_member_workspace_links(content, theme, resource_fetcher, log, link_id):
    """
    Add the private and public folders from the member workspace.
    """
    link_val= None
    host_url = urlsplit(log.theme_url)
    workspace_links_content = theme('.level1')
    if link_id == "#user-workspace-id":
        #we are in the workspace section
        if theme('#user-workspace-id').val() is not None:
            member_workspace_content_id = theme('#user-workspace-id').val()
        else:
            member_workspace_content_id = content('#user-workspace-id').val()
        if member_workspace_content_id is not None:
            link_val = host_url[0] + '://' +  host_url[1]+ "/" + member_workspace_content_id
            workspace_links_content.append("<li class='navigation'><a href='" + link_val + "/private_folder" + "'>Private folders</a></li>")
            workspace_links_content.append("<li class='navigation'><a href='" + link_val + "/web_pages?ct=ws" + "'>Web pages</a></li>")
    else:
        #we are on the membership page and there are 3 sets of users
        #anonymous, logged-in, owner
        if not content('#portal-personaltools li a#user-name span'):
            content('#portal-logo img').attr('src', host_url[0] + '://' +  host_url[1] +'/++resource++portal/logo_member-space.png')
            content('.level1').remove()
            theme('.level1').remove()
            theme('.level0').replaceWith('<ul class="level0"><li id="portaltab-member-profiles" class="selected" x-a-marker-attribute-for-deliverance="1"><a title="" href="' + str(content('#portal-breadcrumbs span:nth-child(7) a').attr('href')) +'/web_pages' +'">Member Web Pages</a></li><li id="portaltab-portal" class="plain" x-a-marker-attribute-for-deliverance="1"><a title="" href="' + host_url[0] + '://' +  host_url[1]+'/">Portal</a></li></ul>')
            theme('body').addClass('template-member-space')                    
        elif content('#portal-personaltools li a#user-name span').html() in content('#portal-breadcrumbs').html():
            content('#portal-logo img').attr('src', host_url[0] + '://' +  host_url[1] +'/++resource++portal/logo-workspace.png')
            content('#portal-logo img').attr('width', '803px')
            content('#portal-logo img').attr('height', '60px')             
        else:
            content('#portal-logo img').attr('src', host_url[0] + '://' +  host_url[1] +'/++resource++portal/logo_member-space.png')
            content('.level1').remove()
            theme('.level1').remove()
            
def add_section_links(content, theme, resource_fetcher, log):
    """
    Add top level class links abd logos for the different sections (workspace and portal).
    """
    link_val= None
    host_url = urlsplit(log.theme_url)
    link_items = str(theme("ul.level0 li.selected")).split("</li>")
    if "Workspace" not in link_items[0] and "Workspace" not in link_items[1] and not content('.section-membership'):
        theme('body').addClass('template-portal')        
    elif ("Workspace" in link_items[0] or  "Workspace" in link_items[1]) and not content('.section-membership'):
        theme('#portal-logo img').attr('src', host_url[0] + '://' +  host_url[1] +'/++resource++portal/logo-workspace.png')
        theme('#portal-logo img').attr('width', '803px')
        theme('#portal-logo img').attr('height', '60px')
        theme('body').addClass('template-workspace')

def add_member_workspace_styles(content, theme, resource_fetcher, log):
    """
    Add the necessary styles to any sub-pages of the members private and public folders.    """
    if "web_pages" in content('#portal-breadcrumbs').html() and not content('.template-web_pages'):
        content('body').addClass('template-web_pages')
    elif "private_folder" in content('#portal-breadcrumbs').html() and not content('.template-private_folder') is None:
        content('body').addClass('template-private_folder')

def add_workspace(content, theme, resource_fetcher, log, workspace_id):
    """Get the workspace content from plone using the hidden id from bungeni
       or drop the tabs.
    """
    workspace_item = theme('dl.workspace-tab dd#fieldset-display-form-workspace div.workspace-content')
    
    workspace_content_id = theme(workspace_id).val()
    if workspace_content_id is not None:
        try:
            host_url = urlsplit(log.theme_url)
            if workspace_id == "#user-workspace-id":
                workspace_url = pq(url=host_url[0] + '://' +  host_url[1]+ "/" + workspace_content_id + "web_pages")
            else:
                 workspace_url = pq(url=host_url[0] + '://' +  host_url[1]+ "/" + workspace_content_id)
                
            workspace_content = workspace_url('#portal-column-content').html()
            workspace_item.append(workspace_content)
        except:
            pass

def add_workspace_link(content, theme, resource_fetcher, log, workspace_id):
    """
    Add a link to the members workspace.
    """
    if content('#user-workspace-id').val is not None:
        host_url = urlsplit(log.theme_url)
        #check if the personal web page exists
        try:
            workspace_url = pq(url=host_url[0] + '://' +  host_url[1]+ '/' +  content('#user-workspace-id').val()  + '/web_pages')
            if workspace_url('#portal-column-content').html() is not None:
                new_value = "<h2>" + content('h2').html() + "</h2> For the personal web page click <a href ='" + host_url[0] + '://' + host_url[1] + "/" + content('#user-workspace-id').val() + "/web_pages'>here.</a>"
                content('h2').replaceWith(new_value)
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
    calendar_next_link_node = content('.next-link')
    calendar_previous_link_node = content('.previous-link') \
                               
    if calendar_next_link_node:
        calendar_next_link_node.replaceWith('<a class="navigation next-link" onClick="document.location=&#39;' + str(content('.next-link').attr('href'))  + '&#39;">&#8594;</a>')
        
    if calendar_previous_link_node:
        calendar_previous_link_node.replaceWith('<a class="navigation previous-link" onClick="document.location=&#39;' + str(content('.previous-link').attr('href'))  + '&#39;">&#8592;</a>')    

def image_links(content, theme, resource_fetcher, log):
    """
    Use absolute links to the members profile image.
    """
    link_value  = str(content('#region-content').html())
    if '@@file-image/image' in link_value:    
        link_id= content('#portal-breadcrumbs a:last-child')
        link_id = str(link_id).split('href="')
        link_id = str(link_id[1]).split('">')[0]
        link_node = content('#region-content')
        new_value = link_value.replace('@@file-image/image', str(link_id) +'/@@file-image/image')
        link_node.replaceWith(new_value)

def rewrite_links(content, theme, resource_fetcher, log):
    """
    Fix links in folders that have been set up to act as root nodes.
    Relative links can end up with the root folder entry repeated twice.
    In addition some links are not children of the current root node i.e.
    they may belong to another root node but accesible from here.
    Remove the first root folder entry if necessary.
    """

    repeating_link_values = ['business', 'calendar', 'workspace_archive']
    strip_link_values = {'/calendar/business': '/business', '/business/calendar': '/calendar' }
    content_items = [['#portal-breadcrumbs','id', 'div'], ['#portal-column-content', 'id', 'td']]

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
    link_values = ['business', 'calendar', 'members', 'archive', 'workspace_acrhiv']

    for link_value in link_values:
        content_value = theme('.documentActions').html()
        content_node = theme('.documentActions')
        if link_value in (unicode(content_value)):
            new_content = content_value.replace('/'+link_value, '/plone/'+link_value)
            content_node.replaceWith('<div class="documentActions">' + new_content + '</div>')
