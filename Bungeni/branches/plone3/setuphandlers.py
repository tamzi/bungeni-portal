# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta5
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('Bungeni: setuphandlers')
from Products.Bungeni.config import PROJECTNAME
from Products.Bungeni.config import DEPENDENCIES
from config import product_globals
import os
from Globals import package_home
from Products.CMFCore.utils import getToolByName
##code-section HEAD
##/code-section HEAD

def installGSDependencies(context):
    """Install dependend profiles."""
    
    # XXX Hacky, but works for now. has to be refactored as soon as generic
    # setup allows a more flexible way to handle dependencies.
    
    dependencies = []
    if not dependencies:
        return
    
    site = context.getSite()
    setup_tool = getToolByName(site, 'portal_setup')
    for dependency in dependencies:
        if dependency.find(':') == -1:
            dependency += ':default'
        old_context = setup_tool.getImportContextID()
        setup_tool.setImportContext('profile-%s' % dependency)
        importsteps = setup_tool.getImportStepRegistry().sortSteps()
        excludes = [
            u'Bungeni-QI-dependencies',
            u'Bungeni-GS-dependencies'
        ]
        importsteps = [s for s in importsteps if s not in excludes]
        for step in importsteps:
            setup_tool.runImportStep(step) # purging flag here?
        setup_tool.setImportContext(old_context)
    
    # re-run some steps to be sure the current profile applies as expected
    importsteps = setup_tool.getImportStepRegistry().sortSteps()
    filter = [
        u'typeinfo',
        u'workflow',
        u'membranetool',
        u'factorytool',
        u'content_type_registry',
        u'membrane-sitemanager'
    ]
    importsteps = [s for s in importsteps if s in filter]
    for step in importsteps:
        setup_tool.runImportStep(step) # purging flag here?
        
def installQIDependencies(context):
    """This is for old-style products using QuickInstaller"""
    site = context.getSite()
    qi = getToolByName(site, 'portal_quickinstaller')

    for dependency in DEPENDENCIES:
        if qi.isProductInstalled(dependency):            
            logger.info("Re-Installing dependency %s:" % dependency)
            qi.reinstallProducts([dependency])
        else:
            logger.info("Installing dependency %s:" % dependency)
            qi.installProducts([dependency])

def setupHideToolsFromNavigation(context):
    """hide tools"""
    # uncatalog tools
    site = context.getSite()
    toolnames = ['portal_bungenimembershiptool', 'portal_rotatool']
    portalProperties = getToolByName(site, 'portal_properties')    
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    if navtreeProperties.hasProperty('idsNotToList'):
        for toolname in toolnames:
            try:
                portal[toolname].unindexObject()
            except:
                pass        
            current = list(navtreeProperties.getProperty('idsNotToList') or [])
            if toolname not in current:
                current.append(toolname)
                kwargs = {'idsNotToList': current}
                navtreeProperties.manage_changeProperties(**kwargs)
                
def installRelations(context):
    """imports the relations.xml file"""
    site = context.getSite()
    relations_tool = getToolByName(site, 'relations_library')
    xmlpath = os.path.join(package_home(product_globals), 'data', 
                           'relations.xml')
    f = open(xmlpath)
    xml = f.read()
    f.close()
    relations_tool.importXML(xml)    
    
##code-section FOOT
##/code-section FOOT
