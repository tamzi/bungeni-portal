Overview
========

This product subscribes to add/modify/delete/transition events, and logs
them.

Dependencies
============

Requires patched DCWorkflow (CMF-1.6.2-bungeni) from
http://bungeni-portal.googlecode.com/svn/DCWorkflow/

TODO
====

- Allow configuration of marshaller to be used for audit trail.
- Integrate the Marshall product, so that we can define our own
  marshallers for auditing.
- Consider filtering before logging: only log certain fields, etc.
