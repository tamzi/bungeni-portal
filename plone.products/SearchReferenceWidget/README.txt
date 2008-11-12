Purpose
-------

  An AJAX AT field for references. Useful for large numbers of targets.
  
  - Uses livesearch/AJAX for autocomple type functionality
  - Searches by title rather than all content
  - Has a type dropdown for searching from a single allowed type
  - Has Addable support

Installation
------------

  unpack the archive into youe zope's Products dir
  install Archetypes + SearchReferenceWidget inside your portal 
  with QuickInstaller

Usage
-----

  in your AT Project set the Widget for your ReferenceField or BiReferenceField
  to SearchReferenceWidget. 
  
Copyright, License, Author
--------------------------

  Copyright (c) 2007, PretaWeb, Australia,
   and the respective authors. All rights reserved.
 
  Author: Dylan Jay <software@pretaweb.com>

  License BSD-ish, see LICENSE.txt


Credits
-------

  Thanks to Duncan Booth and enfold systems for their
  PopupReferenceWidget which I borrowed lots of code from
  and the livesearch code from plone which I also repurposed.
