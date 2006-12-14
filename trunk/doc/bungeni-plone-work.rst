==============================================
Bill of work for implementing Bungeni in Plone
==============================================

:Author: Jean Jordaan
:Date: 2006-12-12

.. contents:

Background
==========

This document outlines the work to be done for an initial implementation
of Bungeni in Plone. Within Bungeni as a whole, Plone functions as an
integration platform, providing a user interface to the various systems
that provide functionality to Bungeni, such as the Parliamentary
Registry and the Norma Africa storage.

The document was written with reference to
Bungeni_Detailed_System_Document_V_05-Ashok-annotations.odt
and the email threads discussing it.

The website of the
`Scottish parliament <http://www.scottish.parliament.uk/home.htm>`_
was mentioned as a reference for the kind of portal required.

Scope
-----

This section lists all the functional areas that are candidates for
inclusion in an initial implementation. Most of them can be included at
least in draft form in the prototype.

Portal
  Out of the box, Plone should provide most of the elements of a portal
  site, including easy content authoring, news items, RSS feeds,
  fulltext search, and multilingual accessibility.

Document repository
  The PIS should function as a versioned repository for bills
  submitted to parliament. All references to bills are to a specific
  version of a bill.

Annotation framework
  The PIS should allow annotation and amendment of bills. Amendments 
  should be possible on word, phrase and paragraph level, as well as on
  larger structural elements of the bill. 

  A clerk should be able to review, edit and order amendments for
  submission to parliament or to a committee. The clerk's submission
  should reference the original annotations. 

Authentication
  Various classes of user should be able to log into the PIS. They
  include MPs, clerical staff, and system administrators. Record of MPs
  are maintained in an external relational database (the Parliament
  Registry). Potentially the PIS can authenticate against this database.
  Other users may be stored in the ZODB, and may authenticate against
  Plone. The PIS also envisages public participation. In this case,
  members of the public should be able to register themselves.

Support for questions and motions
  MPs should be able to submit questions and motions. These undergo
  editing workflow before being submitted. They reference bills, and are
  assigned to a committee or to the house on a particular date.

Parliamentary workflow
  The PIS should support the parliament's workflow, keeping track of due
  dates for e.g. debate and signature, and sending notifications when
  necessary.

Facilities management
  The PIS should allow self-service booking of venues, together with
  services such as catering.
  *(Not this time)*

Calendaring
  Various stages in the workflow of bills have due dates, after which
  reminders should be sent. Also, questions and motions have dates
  assigned for response or discussion. The PIS should enable various
  audiences to browse the calendar from their perspective.

Support for collaborative workspaces for committees
  The PIS should support the notion of workgroups, so that access to
  documents, facilities, notifications and responsibility for work may
  be assigned on a group basis. A workspace can also provide a space
  where working documents may be shared.

Multilingualism
  In countries with more than one official language, this is bound to
  come up. Integration with the implementation sketched below requires
  more thought and research.

This functionality should be prioritised and implemented in a modular
fashion, with the core requirements being addressed first.

Plone implementation: software components
=========================================

In order to keep development consistent and transparent, as much as
possible should be captured as UML diagrams. Using ArchGenXML, Plone
products may be generated from the diagrams. This also holds for
products derived from existing third-party products.

The integration of Plone with external systems should be documented as
a UML deployment diagram.

Custom products
---------------

The specific requirements of the Parliamentary Information System will
be implemented as a (set of) Plone products. 

ParliamentaryInformationSystem
  This product defines the custom content types and workflows, and
  installs and configures the required third-party products.

  The custom content types will derive from and extend content types
  provided by third-party products, such as PloneHelpCenter.

NormaAfricaStorage
  This product persists an Archetypes field to a NormaAfrica server via
  web services.

ParliamentaryInformationSystemSkin[Parliament]
  This should be installed in addition to the
  ParliamentaryInformationSystem to customise the look and feel of a
  specific parliament, leading to products such as
  ParliamentaryInformationSystemSkinKenya,
  ParliamentaryInformationSystemSkinTanzania,
  ParliamentaryInformationSystemSkinRwanda.

PloneStetSkin
  Stet's views for browsing and editing comments need to be integrated
  with Plone in some way. To begin with, we can "fall out of" Plone when
  we browse comments, but eventually it should be a unified experience.

  Plone content items and events will need to be created from stet
  comments. PloneStetSkin should facilitate this.

Third-party products
--------------------

Wherever possible, existing Plone products will be used for aspects of
the PIS. Products will be chosen on the basis of code quality and
maturity, community support, and available expertise.

From an initial consideration, at least the following products come into
consideration:

Plone products
``````````````

`CMFEditions <http://plone.org/products/cmfeditions>`_
  This is the emerging standard for versioning in Plone, and will be
  part of Plone 3.0, due in the first quarter of 2006.

  *Research required*: CMFEditions handles any Archetypes-based content
  type. However, for Bungeni, content needs to integrate with the
  NormaAfrica document repository. There will not be a one-to-one
  correspondence of Plone versions to NormaAfrica versions, as
  documents are only persisted to NormaAfrica upon specific workflow
  transitions.

`LinguaPlone <http://plone.org/products/linguaplone>`_
  Enables translation of site content.

  *Research required*: Integration with NormaAfrica will require some
  thought. LinguaPlone has mechanisms for language negotiation and
  associating translations with source documents. We will need to
  integrate with corresponding mechanisms in NormaAfrica.

`TeamSpace <http://plone.org/products/teamspace>`_
  Allow creation of workspaces for collaboration. Access to workspaces
  can be restricted to workspace members. It is expected that
  parliamentary committees may be modeled using workspaces.
  See `Collaboration Management with Archetypes <http://plone.org/events/conferences/vienna-2004/confwiki/CollaborationWithArchetypes>`_

`PloneHelpCenter <http://plone.org/products/plonehelpcenter>`_
  Provides content types for flexible browsing of structured multipart
  documents.

  It is envisaged to provide browser-based access to legislation using
  PloneHelpCenter. While the editing environment for legislation will be
  a customised OpenOffice environment, this is not convenient for easy
  browsing and searching using a web browser. PloneHelpCenter-based
  content will also provide an integration point for the annotation
  service used, as the annotation service requires a stable web
  representation of the documents to be annotated.

  *Research required*: OpenOffice documents may contain embedded objects
  (graphs, images):

  - Will this be permitted for legislation?
  - If so, how will it be handled in conversion to PloneHelpCenter-based
    documents? Ditto for ANxml documents.

mxmCalendarTypes, Booking, `Plone4Artists Calendar <http://plone.org/products/plone4artistscalendar>`_ , ...
  There is a range of Plone products available for various calendaring
  and event management needs.

  *Research required*: Choose a calendaring product based on Bungeni's
  requirements. Plone4Artists Calendar is a strong contender.

`CMFNotification <http://plone.org/products/cmfnotification>`_, EasyNewsletter, PloneGazette, CMFNewsletter, ...
  As with calendaring, there is a range of products available to handle
  the automated sending of email via Plone.

  *Research required*: Choose mailing product(s) for Bungeni use cases.
  There are likely to be two main use cases:

  - Clerks, administrators or committee members wish to send
    notifications or standard messages to groups of users. Products such
    as EasyNewsletter fit this niche.
  - Users need to be notified of site events (e.g. workflow
    transitions). CMFNotification fits this niche. Note that there
    appears to be a similar product from ObjectRealms:
    `cmfnotifications <https://svn.objectrealms.net/svn/public/cmfnotifications/trunk>`_

`ExternalStorage <http://plone.org/products/externalstorage>`_, `FileSystemStorage <http://ingeniweb.sourceforge.net/Products/FileSystemStorage/>`_
  Bungeni will be storing many potentially large objects, namely
  OpenOffice documents and PDF and ANxml manifestations of bills. These
  should not be kept in the ZODB.

  There is a commercial offering:
  `ZOpen FRS - Plone File Repository System <http://zopen.cn/products-en/frs>`_
  but I don't know anything about it.

  *Research required*: See
  `ES vs FSS <http://plone.org/events/sprints/past-sprints/snow-sprint3/es-vs-fss>`_

`Hornet SQL bridge <http://plone.org/products/hornet>`_
  Hornet allows mounting of a relational database within the ZODB, so
  that the contents of the database may be managed and browsed from
  within Plone. This is required for integration with the Parliamentary
  Registry. See the
  `Hornet Quickstart <http://www.mooball.com/zope/software/hornet/quickstart>`_
  document.

`PloneStickies <http://plone.org/products/stickies>`_ (*Research required*)
  PloneStickies is a product for creating content annotations on
  Archetype Content Types.

  While this is a topic that generates a lot of interest in the Plone
  community, there aren't any mature solutions available. This is likely
  to require some development work. For example: PloneStickies currently
  doesn't support sub-document (e.g. sentence-level) annotation. For
  discussion, see:

  - `PLIP #138: Improved support for User Contributed Content Annotations <http://plone.org/products/plone/roadmap/138/>`_
  - `The Me Generation (isomorphic surprises: stickies, tasty, and the importance of user contributed content) <http://theploneblog.org/blog/archive/2006/04/04/the-me-generation>`_
  - `Mozilla Roadmap Extension <http://rhaptos.org/downloads/browser/roadmap/>`_
  - `Future Of Stickies <http://mrenoch.objectis.net/collab/stickies/FutureOfStickies>`_
  - `Yucca <http://openplans.org/projects/yucca>`_. It aims to be "a
    robust framework which captures the rich set of features which
    complex user contributed content annotation applications demand, so
    that all of the tools built on top of yucca share these features."
  - `Annotea <http://www.w3.org/2001/Annotea/>`_, the W3C annotation
    protocol.

  Related products include `tasty <http://microapps.sourceforge.net/tasty/>`_

`OpenID <http://www.openidenabled.com/software/plone>`_
  Different Bungeni client applications all need to authenticate against
  the same user directory. OpenID was designed to adress this kind of
  need. Dependencies: ZopePAS, PloneOpenID.

Zope products
`````````````

`ZMySQLDA <http://sourceforge.net/projects/mysql-python/>`_
  Hornet depends on ZMySQLDA (or another Zope database adapter), in
  order to mount relational databases.

Python packages
```````````````
`MySQLdb <http://sourceforge.net/projects/mysql-python/>`_ (or a Postgres package)
  This is a Python package to provide access to the relational database
  chosen.

Other packages
``````````````
stet
  See `stet (software) <http://en.wikipedia.org/wiki/Stet_(software)>`_,
  `source code <http://gplv3.fsf.org/comments/source/>`_. See
  `Commentary <http://pythonpaste.org/commentary/>`_ for a less mature
  Python WSGI-based implementation of the same idea.

  Stet has a number of dependencies, including Perl, the
  `RT <http://rt.bestpractical.com/view/HomePage>`_ issue tracker, and
  MySQL.

`OpenID server <http://www.openidenabled.com/openid/libraries/python>`_
  The authentication server for Plone and other Bungeni components to
  authenticate against.

Research to be done
-------------------

I have mentioned some specific points above. In general, it is not yet
known how well the selected products match the requirements, or how much
work will be required customise them for Bungeni. Some of them have not
yet been released as stable versions (although all of them have seen
production use).

It will be necessary to investigate the interactions of various products
with each other, to determine whether they can be used together.

Plone implementation: testbed configuration
===========================================

A development server should be configured. On this server, the targeted
Plone version(s) and ancillary systems should be installed. Plone
instances should be added with various combinations of the
abovementioned products, and test cases to determine suitability for
use within Bungeni should be formulated. Where the desired functionality
cannot be accomplished with the products as is, required work should be
specified.

Version control and issue tracking
----------------------------------

Development should make use of version control and issue tracking.
Either these should be installed on the development server, or we should
use one of the existing open source hosts. I suggest we try
`Google Code <http://code.google.com/hosting/>`_. For an example
project, see
`Google Web Toolkit <http://code.google.com/p/google-web-toolkit/>`_.

Tasks
-----

List Plone use cases
  Enumerate the specific things to be demo-ed at the first showing of
  the system.

Find a baseline
  Setup candidate Plone environments, and play through all the use cases
  in each environment, noting required work. At this stage, use standard
  Plone content types as far as possible, since the custom Plone
  products won't be available yet.

Setup other Bungeni components
  We should have a Parliamentary Registry and Norma Africa server to
  test against.

Develop custom products
  ParliamentaryInformationSystem, NormaAfricaStorage, and PloneStetSkin,
  as mentioned above.

Develop ODT->ANxml->PHC XSLT transformations
  These transformations will form part of the
  ParliamentaryInformationSystem product, but need to be developed by
  XSL specialists.

Visual design work
  Style Plone to look like Bungeni. Implement design as a
  ParliamentaryInformationSystemSkin product.

