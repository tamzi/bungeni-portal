from pyquery import PyQuery as pq
from urlparse import urlsplit

def add_section_links(content, theme, resource_fetcher, log):
    """
    Add top level class links and logos for the different sections (workspace and portal).
    """
    host_url = urlsplit(log.theme_url)
    if len(theme('#portal-personaltools li:nth-child(4)')) > 0:

        theme('#portal-logo img').attr('src', host_url[0] + '://' +  host_url[1] +'/++resource++portal/logo-workspace.png')
        theme('#portal-logo img').attr('width', '803px')
        theme('#portal-logo img').attr('height', '60px')
        theme('body').addClass('template-workspace')
    else:
        theme('body').addClass('template-portal')

def image_links(content, theme, resource_fetcher, log):
    """
    Use absolute links to the members profile image.
    """
    link_value  = str(content('#region-content').html())
    to_replace = 'file-image/image'
    if to_replace in link_value:    
        if 'file-image/image' in link_value:
            to_replace = 'file-image/image'
        link_id= content('#portal-breadcrumbs a:last-child')
        link_id = str(link_id).split('href="')
        link_id = str(link_id[1]).split('">')[0]
        link_node = content('#region-content')
        new_value = link_value.replace('./'+to_replace, 
                                        str(link_id)+'/file-image/image')
        link_node.replaceWith(new_value)

        

def add_plone_tabs(content, theme, resource_fetcher, log):
    """
    Add top level dummy menu tabs to represent plone content.
    """
    theme('.level0').append("<li class='plain'><a href='#'>have your say</a></li>")
    theme('.level0').append("<li class='plain'><a href='#'>how we work</a></li>")
    theme('.level0').append("<li class='plain'><a href='#'>reference material</a></li>")
