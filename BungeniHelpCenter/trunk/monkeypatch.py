try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions

try:
    from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
    PHCReferenceWidget = ReferenceBrowserWidget
except ImportError:
    PHCReferenceWidget = ReferenceWidget
from Products.Archetypes.ClassGen import generateMethods
import string
from Products.CMFCore.utils import getToolByName

from Products.BungeniHelpCenter.content import roman
from Products.BungeniHelpCenter.config import BUNGENI_REFERENCEABLE_TYPES
#import Products
#Products.PloneHelpCenter.config.REFERENCEABLE_TYPES = BUNGENI_REFERENCEABLE_TYPES

from Products.PloneHelpCenter.config import DEFAULT_CONTENT_TYPES, REFERENCEABLE_TYPES, IMAGE_SIZES
from Products.PloneHelpCenter.content import Definition, Glossary, \
    FAQFolder, LinkFolder, Link, PHCContent, PHCFolder, ReferenceManualPage
from Products.PloneHelpCenter.content import ReferenceManual, ReferenceManualSection, \
    TutorialFolder, TutorialPage, Tutorial, ReferenceManualFolder, \
    FAQ, HowTo, ErrorReference, ErrorReferenceFolder
from Products.PloneHelpCenter.content import HowToFolder

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin, fti_meta_type
from Products.PortalTaxonomy.fields import AttributeField, CategoryField
from Products.ATContentTypes.content import folder

BodyField =  TextField(
        'body',
        searchable=1,
        widget=RichWidget(
                description = "The body text.",
                description_msgid = "phc_desc_body_referencemanual",
                label = "Body text",
                label_msgid = "phc_label_body_referencemanual",
                rows = 25,
                i18n_domain = "plonehelpcenter"
                ),
        **DEFAULT_CONTENT_TYPES
        )

IdentityField = ImageField(
        'identity',
        required=0,
        sizes=IMAGE_SIZES,
        widget=ImageWidget(
            label='Identity Image',
            label_msgid='phc_label_identity_image',
            description='Add an identity image',
            description_msgid='phc_help_identity_image',
            i18n_domain='plonehelpcenter',
            ),
        )

IdentityPosition =  StringField('identity_position',
                                accessor = 'getIdentityPosition',
                                mutator = 'setIdentityPosition',
                                vocabulary = DisplayList((
                                            ('right', 'Top Right'),
                                            ('left', 'Top Left'),)),
                                searchable=0,
                                default= ('right'),
                                widget=
                                SelectionWidget(label='Identity Logo Position',
                                                label_msgid="label_identity_position",
                                                description="Select the positioning of the Identity Logo.",
                                                description_msgid="help_identity_position",
                                                i18n_domain="plone"
                                                ),
                                )

TocType =  StringField('toc_type',
                       accessor = 'getTocType',
                       mutator = 'setTocType',
                       vocabulary = DisplayList((
                                   ('drop', 'Drop Down'),
                                   ('box', 'Box'),)),
                       searchable=0,
                       default= ('drop'),
                       widget=
                       SelectionWidget(label='TOC Display Type',
                                       label_msgid="label_toc_type",
                                       description="Select the TOC display type.",
                                       description_msgid="help_toc_type",
                                       i18n_domain="plone"
                                       ),
                       )

ContributorsField =  LinesField(
        'contributors',
        accessor="Contributors",
        languageIndependent=1,
        widget=LinesWidget(
                label='Contributors',
                label_msgid="label_contributors",
                description="Enter additional names (no need to include the current owner) for those who have contributed to this entry, one per line.",
                description_msgid="help_contributors",
                i18n_domain="plone",
                ),
        )

RelatedItemsField =  ReferenceField(
        'relatedItems',
        relationship='PloneHelpCenter',
        allowed_types=BUNGENI_REFERENCEABLE_TYPES,
        required = 0,
        multiValued=1,
        languageIndependent=1,
        widget=PHCReferenceWidget (
                label="Referenced Items",
                description="Set one or more references to HelpCenter items.",
                description_msgid = "phc_reference",
                label_msgid = "phc_label_reference",
                i18n_domain="plonehelpcenter"
                ),
    )

RightsField =  TextField(
         'rights',
         accessor="Rights",
         widget=TextAreaWidget(
                 label='Copyright',
                 description="Copyright info for all content in the helpcenter.",
                 label_msgid="phc_label_copyrights_referencemanual",
                 description_msgid="phc_copyrights_referencemanual",
                 i18n_domain="plonehelpcenter"
                 ),
         )

PositionField =  StringField('navbar_position',
                             accessor = 'getNavBarPosition',
                             mutator = 'setNavBarPosition',
                             vocabulary = '_navbar',
                             searchable=0,
                             default= ('both'),
                             widget= SelectionWidget(label='Navigation Bar',
                                                     label_msgid="label_navigation_bar",
                                                     description="Select the positioning of the Navigation Bar.",
                                                     description_msgid="help_nav_bar",
                                                     i18n_domain="plone"
                                                     ),
                             )

TaxCategoryField = CategoryField('categories')

TaxAttributesField = AttributeField('attribs')


# Patching PHCContent
PHCContent = PHCContent.PHCContent

def getLayout(self, **kw):
    """Get the current layout or the default layout if the current one is None
    """
    aliases = self.portal_types.getTypeInfo(self.portal_type).getMethodAliases()
    if aliases.has_key("(Default)") and aliases["(Default)"]:
        return aliases["(Default)"]
    if aliases.has_key("view") and aliases["view"]:
        return aliases["view"]
    raise Exception("Current Layout Failed")

PHCContent.getLayout = getLayout.__get__(None, PHCContent)

# Patching PHCFolder
PHCFolder = PHCFolder.PHCFolder

def _sectionCmpByCreation(a, b):
    # depends on cmp(True, False) == 1
    acr = a.created
    bcr = b.created
    if acr == bcr:
        return cmp(a.Title.lower(), b.Title.lower())    
    return cmp(a.created, b.created)

def getLayout(self, **kw):
    """Get the current layout or the default layout if the current one is None
    """
    aliases = self.portal_types.getTypeInfo(self.portal_type).getMethodAliases()
    if aliases.has_key("(Default)") and aliases["(Default)"]:
        return aliases["(Default)"]
    if aliases.has_key("view") and aliases["view"]:
        return aliases["view"]
    raise Exception("Current Layout Failed")

def getItemsBySections(self, **kwargs):
    """Get all items to list, by section only. Returns a list of dicts:

    'id'      : A normalised string representing the section
    'section' : The name of the section
    'items'   : A list of catalog brains for items in this section

    The first item will have an section title of 'No section' and contain
    all items with no section selected.
    """
    plone_utils = getToolByName(self, 'plone_utils')
    brains = self.getFolderContents(contentFilter = kwargs)

    charset = self.getCharset()

    # Set up the dicts listing all sections
    # This is needed because we want it to list the audiences and sections
    # in the order the vocab specifies them.

    sections = []
    for s in ['No section'] + list(self.getSectionsVocab()):
        t = s.encode(charset)
        sections.append({'id'      : plone_utils.normalizeString(t),
                         'section' : t,
                         'items'   : []})

    # Then insert each how-to in the appropriate audience/section
    for b in brains:
        itemSections = b.getSections or ['No section']
        matchedSections = [s for s in sections if s['section'] in itemSections]
        for s in matchedSections:
            s['items'].append(b)

    # Finally clean out empty audiences or sections

    delSections = []
    for j in range(len(sections)):
        if len(sections[j]['items']) == 0:
            delSections.append(j)
    delSections.reverse()
    for j in delSections:
        del sections[j]

    # sort inside sections
    for j in sections:
        j['items'].sort(_sectionCmpByCreation)

    return sections

PHCFolder.getLayout = getLayout.__get__(None, PHCFolder)
PHCFolder.getItemsBySections = getItemsBySections.__get__(None, PHCFolder)

# Patching HelpCenterGlossary
HelpCenterGlossary = Glossary.HelpCenterGlossary

HelpCenterGlossary.schema['description'].required = 0

HelpCenterGlossary.schema = HelpCenterGlossary.schema + \
    Schema((BodyField, IdentityField, IdentityPosition, ContributorsField, RelatedItemsField, TaxCategoryField, TaxAttributesField),)

HelpCenterGlossary.schema.moveField('sectionsVocab', pos='bottom')
HelpCenterGlossary.schema.moveField('contributors', pos='bottom')
HelpCenterGlossary.schema.moveField('relatedItems', pos='bottom')
HelpCenterGlossary.schema.moveField('categories', pos='bottom')
HelpCenterGlossary.schema.moveField('attribs', pos='bottom')

def alphabetise(self):
    items = self.getFolderContents()

    alphabets = {}
    for x in string.uppercase:
        alphabets[x] = []

    for item in items:
        char = item.Title[0].upper()
        if not alphabets.has_key(char):
            continue
        alphabets[char].append(item)

    return [{'letter': x, 'items': alphabets[x]} for x in \
            string.uppercase]

HelpCenterGlossary.alphabetise = alphabetise.__get__(None, HelpCenterGlossary)

generateMethods(HelpCenterGlossary, HelpCenterGlossary.schema.fields())

# Patching HelpCenterDefinition
HelpCenterDefinition = Definition.HelpCenterDefinition

HelpCenterDefinition.schema['description'].widget =RichWidget(
                    description = 'An explanation of the term.',
                    description_msgid = "phc_desc_definition",
                    label = "Definition",
                    label_msgid = "phc_label_definition",
                    rows = 5,
                    i18n_domain = "plonehelpcenter",
                    )

generateMethods(HelpCenterDefinition, HelpCenterDefinition.schema.fields())

# Patching FAQFolder
HelpCenterFAQFolder = FAQFolder.HelpCenterFAQFolder

HelpCenterFAQFolder.schema['description'].required = 0

HelpCenterFAQFolder.schema = HelpCenterFAQFolder.schema +\
Schema((BodyField, IdentityField, IdentityPosition, ContributorsField,\
        RelatedItemsField, RightsField, TaxCategoryField, TaxAttributesField),)

HelpCenterFAQFolder.schema.moveField('contributors', pos='bottom')
HelpCenterFAQFolder.schema.moveField('relatedItems', pos='bottom')
HelpCenterFAQFolder.schema.moveField('rights', pos='bottom')
HelpCenterFAQFolder.schema.moveField('categories', pos='bottom')
HelpCenterFAQFolder.schema.moveField('attribs', pos='bottom')


generateMethods(HelpCenterFAQFolder, HelpCenterFAQFolder.schema.fields())

# Patching FAQ
HelpCenterFAQ = FAQ.HelpCenterFAQ

HelpCenterFAQ.schema['relatedItems'].allowed_types = BUNGENI_REFERENCEABLE_TYPES

# Patching LinkFolder
HelpCenterLinkFolder = LinkFolder.HelpCenterLinkFolder

HelpCenterLinkFolder.schema['description'].required = 0

HelpCenterLinkFolder.schema = HelpCenterLinkFolder.schema + \
    Schema((BodyField, IdentityField, IdentityPosition, RelatedItemsField, TaxCategoryField, TaxAttributesField),)

HelpCenterLinkFolder.schema.moveField('sectionsVocab', pos='bottom')
HelpCenterLinkFolder.schema.moveField('relatedItems', pos='bottom')
HelpCenterLinkFolder.schema.moveField('categories', pos='bottom')
HelpCenterLinkFolder.schema.moveField('attribs', pos='bottom')

HelpCenterLinkFolder.alphabetise = alphabetise.__get__(None, HelpCenterLinkFolder)

generateMethods(HelpCenterLinkFolder, HelpCenterLinkFolder.schema.fields())

# Patching Link
HelpCenterLink = Link.HelpCenterLink

HelpCenterLinkFolder.schema['description'].required = 0

HelpCenterLink.schema = HelpCenterLink.schema + Schema((BodyField),)
HelpCenterLink.schema.moveField('url', pos='bottom')
HelpCenterLink.schema.moveField('relatedItems', pos='bottom')
HelpCenterLink.schema.moveField('sections', pos='bottom')
HelpCenterLink.schema.moveField('contributors', pos='bottom')
HelpCenterLink.schema.moveField('subject', pos='bottom')
HelpCenterLink.schema.moveField('startHere', pos='bottom')
HelpCenterLink.schema.moveField('relatedItems', pos='bottom')

generateMethods(HelpCenterLink, HelpCenterLink.schema.fields())

# Patching ReferenceManualFolder
HelpCenterReferenceManualFolder = ReferenceManualFolder.HelpCenterReferenceManualFolder

HelpCenterReferenceManualFolder.schema = \
    HelpCenterReferenceManualFolder.schema + Schema((RelatedItemsField),)

generateMethods(HelpCenterReferenceManualFolder, HelpCenterReferenceManualFolder.schema.fields())

# Patching ReferenceManual

HelpCenterReferenceManual = ReferenceManual.HelpCenterReferenceManual

def toRoman(self, num):
    """Convert to roman numerials"""
    str = ''
    for number in num.split('.'):
        if number.isdigit():
            str=str+"."+roman.toRoman(int(number))
    if str:
        return str[1:]

def toAlpha(self, num):
    """Convert to alpha"""
    str = ''
    for number in num.split('.'):
        if number.isdigit():
            str=str+"."+roman.toAlpha(int(number))
    if str:
        return str[1:]

HelpCenterReferenceManual.toAlpha = toAlpha.__get__(None, HelpCenterReferenceManual)
HelpCenterReferenceManual.toRoman = toRoman.__get__(None, HelpCenterReferenceManual)

HelpCenterReferenceManual.schema['description'].required = 0

HelpCenterReferenceManual.schema = HelpCenterReferenceManual.schema + \
 Schema((BodyField, IdentityField, IdentityPosition, RightsField,\
 PositionField, TocType),)

HelpCenterReferenceManual.schema.moveField('relatedItems', pos='bottom')
HelpCenterReferenceManual.schema.moveField('sections', pos='bottom')
HelpCenterReferenceManual.schema.moveField('audiences', pos='bottom')
HelpCenterReferenceManual.schema.moveField('contributors', pos='bottom')
HelpCenterReferenceManual.schema.moveField('startHere', pos='bottom')
HelpCenterReferenceManual.schema.moveField('subject', pos='bottom')
HelpCenterReferenceManual.schema.moveField('relatedItems', pos='bottom')
HelpCenterReferenceManual.schema.moveField('rights', pos='bottom')

generateMethods(HelpCenterReferenceManual, HelpCenterReferenceManual.schema.fields())

# Patching ReferenceManualPage

# Patching ReferenceManualSection
HelpCenterReferenceManualSection = ReferenceManualSection.HelpCenterReferenceManualSection

HelpCenterReferenceManualSection.schema['description'].required = 0

HelpCenterReferenceManualSection.schema = \
    HelpCenterReferenceManualSection.schema + Schema((BodyField, RelatedItemsField),)

generateMethods(HelpCenterReferenceManualSection, HelpCenterReferenceManualSection.schema.fields())

# Patching TutorialFolder

HelpCenterTutorialFolder = TutorialFolder.HelpCenterTutorialFolder

HelpCenterTutorialFolder.schema['description'].required = 0
HelpCenterTutorialFolder.schema = HelpCenterTutorialFolder.schema + \
    Schema((BodyField, IdentityField, IdentityPosition, ContributorsField, \
        RelatedItemsField),)

HelpCenterTutorialFolder.schema.moveField('sectionsVocab', pos='bottom')
HelpCenterTutorialFolder.schema.moveField('contributors', pos='bottom')
HelpCenterTutorialFolder.schema.moveField('relatedItems', pos='bottom')

generateMethods(HelpCenterTutorialFolder, HelpCenterTutorialFolder.schema.fields())

# Patching TutorialPage

# Patching Tutorial
HelpCenterTutorial = Tutorial.HelpCenterTutorial

HelpCenterTutorial.schema['description'].required = 0
HelpCenterTutorial.schema = HelpCenterTutorial.schema +\
    Schema((BodyField, PositionField, TocType),)

HelpCenterTutorial.schema.moveField('body', pos='top')
HelpCenterTutorial.schema.moveField('description', pos='top')
HelpCenterTutorial.schema.moveField('title', pos='top')

generateMethods(HelpCenterTutorial, HelpCenterTutorial.schema.fields())

# Patching HelpCenterHowToFolder

HelpCenterHowToFolder = HowToFolder.HelpCenterHowToFolder

HelpCenterHowToFolder.schema = \
    HelpCenterHowToFolder.schema + Schema((RelatedItemsField),)

generateMethods(HelpCenterHowToFolder, HelpCenterHowToFolder.schema.fields())

# Patching HelpCenterHowToxo
HelpCenterHowTo = HowTo.HelpCenterHowTo

HelpCenterHowTo.schema['relatedItems'].allowed_types = BUNGENI_REFERENCEABLE_TYPES

# Patching ErrorReferenceFolder

HelpCenterErrorReferenceFolder = ErrorReferenceFolder.HelpCenterErrorReferenceFolder
HelpCenterErrorReferenceFolder.schema = \
    HelpCenterErrorReferenceFolder.schema + Schema((RelatedItemsField),)

generateMethods(HelpCenterErrorReferenceFolder, HelpCenterErrorReferenceFolder.schema.fields())

# Patching ATFolder

ATFolder = folder.ATFolder
ATFolder.schema = \
    ATFolder.schema + Schema((BodyField),)

generateMethods(ATFolder, ATFolder.schema.fields())
