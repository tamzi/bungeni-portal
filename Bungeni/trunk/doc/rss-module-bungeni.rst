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

- ``xmlns:content="http://bungeni.org/rss/1.0/modules/bungeni/"``

Syntax
------

bungeni:questioning
```````````````````

``bungeni:questioning`` enumerates the person, people or groups asking a
question in parliament. It is used as follows::

  <bungeni:questioning>
    <rdf:Bag>
      <rdf:li>
        <bungeni:principal>
          <!-- Use bungeni:principal as described below -->
        </bungeni:principal>
      </rdf:li>
      <!-- Optionally, include as many more bungeni:principal elements as needed. -->
    </rdf:Bag>
  </bungeni:questioning>

bungeni:questioned
``````````````````

``bungeni:questioned`` enumerates the person, people or groups being asked a
question in parliament. It is used similarly to ``bungeni:questioning``.

bungeni:principal
`````````````````

``bungeni:principal`` identifies a principal (normally a site member,
but possibly a group or an organisation) involved addressing someone or
being addressed. If it is necessary to unambiguously identify someone,
then this could be the UID of the principal::

  <bungeni:principal>265d3a4f2164e4d9a3ad5545d8135c3c</bungeni:principal>

However, if it is for display purposes, it could be the name::

  <bungeni:principal>John Smith</bungeni:principal>


