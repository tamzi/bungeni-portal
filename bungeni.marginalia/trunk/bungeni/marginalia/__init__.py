import os, os.path
from Globals import package_home

from Products.CMFCore import utils as cmfutils
from Products.CMFCore import permissions as cmfpermissions
from Products.CMFCore import DirectoryView
from Products.CMFPlone.utils import ToolInit

from Products.Archetypes.atapi import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize

from config import *

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.GenericSetup import EXTENSION, profile_registry

def initialize(context):
    import plone

    # initialize portal tools
    tools = [plone.AnnotationTool]
    ToolInit(
        PROJECTNAME +' Tools',
        tools = tools,
        icon='tool.gif'
        ).initialize(context)

    # initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
