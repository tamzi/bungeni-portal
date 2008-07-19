import os
from Products.CMFCore.utils import getToolByName
from Products.Bungeni.config import product_globals
from Globals import package_home

def relload(  self ):
    # configuration for Relations
    relations_tool = getToolByName(self,'relations_library')
    xmlpath = os.path.join(package_home(product_globals),'data', 'relations.xml')
    f = open(xmlpath)
    xml = f.read()
    f.close()
    relations_tool.importXML(xml)
    return 'loaded relations'
