==================================================
Notes regarding implementation of Bungeni in Plone
==================================================

:Author: Jean Jordaan
:Date: 2006-11-13

Background
==========

In this document, I have attempted to set out my understanding of the
Bungeni system in terms of a Plone-based implementation. The document
will most likely reveal gaps in my understanding, and language such as
"should", "will", and so on, is provisory. 

Scope
-----

While reading the specifications, various areas of functionality come to
light, in addition to the core functionality. I will attempt to list
them:

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
  members of the public should be able to register themselves in order
  to annotate bills (alternatively, annotations may be emailed to a
  clerk, who may add them by proxy). 

  Depending on the nature of public input expected, this may introduce
  scaling considerations. 

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

Plone implementation: from 10,000 feet
======================================

To make the most of Plone as a framework for rapid development, the PIS
should be implemented using Archetypes-based content types and existing
Plone products. 

I would like to see the system implemented using a UML model which lays
out the content types, their workflows, and the associated security. 

Currently, this is how I envisage interaction with the system. I'm
sketching only a subset of functionality, leaving out aspects such as
the maintenance of email notifications and configuration of notification
recipients, facilities management, etc.

Adding bills
------------

- A user (MP or clerk) browses to the PIS and selects "Add Bill" from a
  dropdown. They are presented with a web form, which they complete.
  Upon submission, Plone contains an object representing the metadata of
  a bill.
- Next, they click on the ExternalEditor icon, which opens OpenOffice
  with the appropriate stylesheet. They supply the text of the bill
  using OpenOffice, and save and close the document.
- When the document is saved, the OpenOffice document is transformed (if
  valid) to Akoma Ntoso XML, which serves as the authoritative version
  for subsequent transforms (web, PDF, etc).
- The XML is also transformed to a tree of Plone documents similar to
  the Reference Manual provided by the PloneHelpCenter product in use on
  http://plone.org. The point of the transformation to Plone objects is
  to enable leveraging Plone infrastructure for the browsing, editing,
  searching and annotation of bills.

Most likely, there will also need to be a PUT_factory, or at least a
properly configured content type registry, to enable the bulk uploading
of bills via FTP or WebDAV.

Editing bills
-------------

When a bill is edited, the new version should be saved as a different
version, so that it is always clear to which text specific comments or
references refer. CMFEditions can be configured to create a new version
every time a document is saved. 

This can introduce complexities. For example, annotations should always
refer to a specific version of a bill. If new versions are added for
a multitude of trivial edits, and many of these versions are annotated,
then managing the annotations becomes a problem. One way to avoid this
would be to do the writing of a bill offline or in a collaborative
workspace elsewhere in the site, and to restrict edits to bills in the
document library to the minimum required.

Bill workflow
-------------

The workflow state of a bill reflects its progress through parliament
and thus its legal status. The workflow state is managed manually by a
clerk. Changes in workflow state may trigger events such as:

- sending of notifications,
- creation of events that appear on the calendar, 
- changing the access rights to a bill.

Annotations, amendments, questions and motions
----------------------------------------------

These are all content types that relate to bills, and that reference
a specific version of a bill. 

Annotations are either made directly through the web, using a custom
version of PloneStickies, or indirectly, via a clerk, perhaps in the
form of an OpenOffice document with "track changes" switched on. In this
case, a clerk will need to add the annotations (or a question/amendment)
through the web interface. 

Smaller annotations (deletions, insertions, and changes in wording) may
be implemented using stickies, but larger amendments (e.g. rewriting an
entire section) may need to be OpenOffice documents in their own right.
(How this will work requires more thought.)

Annotations are browsable, and editable by their authors. They are not
discussed as-is, but are turned into amendments by a clerk after
checking and editing. Amendments reference annotations they are based
on.

MPs may add question and motion objects, in their own workspaces or in
committee workspaces. They also undergo editing before being submitted
to parliament. When accepted, a date for discussion is assigned.

It may make sense to postpone a fancy finegrained annotation system for
now, and to stick with one based on the site discussion tools.

Plone implementation: at ground level
=====================================

In order to keep development consistent and transparent, as much as
possible should be captured as UML diagrams. Using ArchGenXML, Plone
products may be generated from the diagrams. This also holds for
products derived from existing third-party products.

Custom products
---------------

The specific requirements of the Parliamentary Information System will
be implemented as a (set of) Plone products.

ParliamentaryInformationSystem
  This product defines the custom content types and workflows, and
  installs and configures the required third-party products. Hopefully,
  this will be the only custom product required. This product leaves
  Plone's look & feel intact.

ParliamentaryInformationSystemSkin
  This should be installed in addition to the
  ParliamentaryInformationSystem to customise the look and feel of a
  specific parliament, leading to products such as
  ParliamentaryInformationSystemSkinKenya,
  ParliamentaryInformationSystemSkinTanzania,
  ParliamentaryInformationSystemSkinRwanda.

Third-party products
--------------------

Wherever possible, existing Plone products will be used for aspects of
the PIS. Products will be chosen on the basis of code quality and
maturity, community support, and available expertise.

From an initial consideration, at least the following products come into
consideration:

CMFEditions
  The emerging standard for versioning in Plone.

LinguaPlone
  Enables translation of site content.

PloneStickies (and related products)
  Facilitate annotation.

  While this is a topic that generates a lot of interest in the Plone
  community, there aren't any mature solutions available. This is likely
  to require some development work.

TeamSpace
  Allow creation of workspaces for collaboration.

PloneHelpCenter
  Provides content types for flexible browsing of structured multipart
  documents.

CalendarX, mxmCalendarTypes, Booking, ...
  Provides for events and calendaring.

EasyNewsletter (PloneGazette, CMFNewsletter, ..)
  Handle notifications.
  
Hornet SQL bridge / Alchemist
  Interface with SQL databases.
