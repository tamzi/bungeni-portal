-------------------------
Installing Bungeni Portal
-------------------------


to install the portal using buildout, you'll first need to bootstrap the system via::

   python2.4 bootstrap.py

this will download the required buildout software. next you'll need to build the system,
the first time this is run it will take a while, and require a network connection, as it 
will download, compile, and install all the required component ( zope, plone, bungeni)::

   ./bin/buildout -v

after which you can start the instance and visit the zope management interface  to add 
and configure the bungeni portal::

   ./bin/instance fg

by default the instance is running at localhost:8080, and has a default user
admin, with password admin. any production site, should change this immediately 
or change it directly in the buildout.cfg configuration file.

on subsequent changes you can avoid a full rebuild via telling buildout to
perform an optimistic update::

   ./bin/buildout -N -v


  

  
