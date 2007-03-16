RDF Site Summary 1.0 Modules: Content
=====================================

:Authors: Jean Jordaan, Ashok Hariharan
:Date: 2007-03-07
:Version: 0.1

Description
-----------

A module describing all the extra information that clients of the
Bungeni portal may be interested in.

Namespace Declarations
----------------------

- ``xmlns:bungeni="http://bungeni.org/ns/1.0/bungeni/"``

Syntax
------

bungeni:from
````````````

``bungeni:from`` enumerates the person, people or groups making a
contribution. This could be, for example, asking a question in
parliament, or making an annotation. It is used as follows::

  <bungeni:from>
    <rdf:Bag>
      <rdf:li>
        <bungeni:principal>
          <!-- Use bungeni:principal as described below -->
        </bungeni:principal>
      </rdf:li>
      <!-- Optionally, include as many more bungeni:principal elements as needed. -->
    </rdf:Bag>
  </bungeni:from>

.. The current implementation assumes that principals will be site members.

If you don't feel like obliging RDF parsers, that looks like::

  <bungeni:from>
    <bungeni:principal>
      <!-- Use bungeni:principal as described below -->
    </bungeni:principal>
  </bungeni:from>

bungeni:to
``````````

``bungeni:to`` enumerates the person, people or groups being asked a
question in parliament. It is used similarly to ``bungeni:from``.

bungeni:principal
`````````````````

``bungeni:principal`` identifies a principal (normally a site member,
but possibly a group or an organisation) addressing someone or being
addressed. If it is for display purposes, it could be the name::

  <bungeni:principal>John Smith</bungeni:principal>

If more information is required, the following optional sub-elements are
available: `bungeni:name`_, `bungeni:identifier`_, `bungeni:uri`_, and
`bungeni:type`_. Here is an example with all of the sub-elements::

  <bungeni:principal>
    <bungeni:name>John Smith</bungeni:name> 
    <bungeni:identifier>265d3a4f2164e4d9a3ad5545d8135c3c</bungeni:identifier>
    <bungeni:uri>http://www.parliament.gh/minutes/2005/0719</bungeni:uri>
    <bungeni:type>MemberOfParliament</bungeni:type>
  </bungeni:principal>

If you use any sub-elements, the ``bungeni:principal`` tag shouldn't
have text content.

bungeni:name
````````````

The name of the person or group.

bungeni:identifier
``````````````````
An identifier that identifies this resource uniquely. In the context of
the Bungeni portal, this will be an Archetypes UID string, e.g.::

  <bungeni:identifier>265d3a4f2164e4d9a3ad5545d8135c3c</bungeni:identifier>

bungeni:uri
```````````

The URI identifying this principal in the Norma Africa storage for a
Parliament. The Norma Africa server is the authoritative source of the
URI. Only content stored by Norma Africa have URIs.

.. In future we may want to include URIs as ``rdf:about`` attributes as well.

bungeni:type
````````````

The type of the principal. In the context of the Bungeni portal, this
will be the ``portal_type`` of the referenced object::

  <bungeni:type>MemberOfParliament</bungeni:type>

bungeni:range
`````````````

The range of text to which an annotation applies. This element may have
several sub-elements with different information about the range::

  <bungeni:range>
    <bungeni:marginalia>/1/5/3.0:/1/5/3.4</bungeni:marginalia>
    <bungeni:closest_id>clause02-art03-part002</bungeni:closest_id>
    <bungeni:range_from_closest_id>/5/3.0</bungeni:range_from_closest_id>
  </bungeni:range>

bungeni:marginalia
``````````````````

A range specification as defined by the marginalia annotation
application. See marginalia-20070121/www/lib/ranges.js

bungeni:closest_id
``````````````````

The closest ID preceding the start of the annotation, to help external
systems (e.g. OpenOffice) to locate the position in the document.

bungeni:range_from_closest_id
`````````````````````````````

The Marginalia range specification, but starting from the element with
the closest ID.

bungeni:quote
`````````````

The text in the original document to which the annotation applies. (The
text of the annotation is in the ``content:encoded`` tag.)

