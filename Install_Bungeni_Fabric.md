﻿#summary How to install Bungeni Parliamentary Information System
#labels bungeni-wiki
#sidebar TableOfContents




# Pre-requisites #

[How to setup the Pre-requisites](Install_PreRequisites_Fabric.md)

# Build & Setup #


> _NOTE: You can use the short-hand script ./fl <action name> which prefixes `fab -H localhost ` to any action_

## Option 1: Installing using the online package index ##

Bungeni can be installed and deployed over the internet -- or locally if you have a local python package index cache.

Build & deploy bungeni using the online package index using the following command :

```
fab -H localhost bungeni_install config_ini:bungeni config_supervisord
```

See also [Executing Fabric actions](http://code.google.com/p/bungeni-portal/wiki/HowTo_SetupFabricScripts#Executing_fabric_actions)

Bungeni has a functional dependency on the eXist XMLdb repository component,  You will need to install this component next : [Installing Bungeni XML db repository](Install_eXistdb_Fabric.md)

## Option 2: Installing using the local package index ##

Use this option only if you have a Bungeni package index running on your local network.
Set the fabric parameters for the cached buildout by setting the `local_cache` parameters appropriately See [Using the local\_cache parameter](http://code.google.com/p/bungeni-portal/wiki/HowTo_ConfigureFabricIni#local_cache)

Once the parameter has been set correctly the installation command is the same :

```
fab -H localhost bungeni_install config_ini:bungeni config_supervisord
```

See also [Executing Fabric actions](http://code.google.com/p/bungeni-portal/wiki/HowTo_SetupFabricScripts#Executing_fabric_actions)


# Folder Structure #

At the end of this step your folder structure should look like this :

```
./bungeni_apps
|-- bungeni
|   |-- bin
|   |-- buildconf
|   |-- cache
|   |-- data
|   |-- develop-eggs
|   |-- eggs
|   |-- locales
|   |-- logs
|   |-- parts
|   |-- patch
|   |-- src
|   |-- templates
|   `-- testdatadmp
|-- config
|-- logs
|-- pid
`-- python27
    |-- bin
    |-- include
    |-- lib
    `-- share

```

# Starting and stopping bungeni #

See [using supervisor to start / stop Bungeni](http://code.google.com/p/bungeni-portal/wiki/HowTo_SupervisorServiceManager#bungeni)


# Setting up the admin password #

There are 2 parameters in the Fabric `setup.ini` :

```
[bungeni]
...
admin_user = admin
admin_password = admin
...
```

Set this appropriately and run :

```
fab -H localhost setup_bungeni_admin 
```

You need to have postgres running for this:

```
fab -H localhost start_monitor start_service:postgres
```

# Testing the installation #

After this you can run the unit tests provided in the system to check if you have installed correctly [Run Bungeni Unit Tests](HOWTO_RunBungeniUnitTests.md).

You can also install some demo data which you can use to test-drive the system : [Install demo data sets](HowTo_MaintainAndUpdateInstallation#Load_Demo_Data.md)

# Next Steps #

  * **[How to install eXist-db](Install_eXistdb_Fabric.md)
  ***[How to setup Plone Content Management System](Install_Plone_Fabric.md)*****[How to setup Deliverance Portal](Install_DeliverancePortal_Fabric.md)

# Manual Install #

## 1. Pre-requisites ##

  * Build environment (on ubunutu do a `sudo apt-get install build-essentials` )
  * user Python 2.5 built from source. (on ubuntu /debian you will need to install development libaries/headers for imaging (libjpeg62-dev, libfreetype6-dev, libpng12-dev)  and bz2 (libbz2-dev) libraries) and for ssl support openssl and libssl (openssl, libssl-dev)
    * For comipling the xapian bindings you will have to switch the user python to the primary python on the system either by aliasing it (alias='/my/path/to/myuser/python') or by changing the python referenced by /usr/bin/python (on debian /ubuntu you can switch between system pythons by using the update-alternatives command). [UPDATE: setting the environment variable PYTHON to the path of the user python binary also appears to work : `export PYTHON=/home/user/bungeni/python/bin/python'`
  * PostGreSQL build from source requires development libraries/headers for: bison, flex ,readline (libreadline5-dev), zlib (zlib1g-dev). (on ubuntu installed via apt-get)
  * Xapian requires uuid-dev on updated versions of ubuntu 8.04 / 8.10 / 9.04 / 9.10

## 2. SSL support for Python ##

In ubuntu installing openssl and libssl-dev does not result in Python getting built with ssl support as the default ssl paths for include/ lib referenced by the Python build are different in Ubuntu. To build ssl support into Python on Ubuntu set the CPPFLAGS and LDFLAGS environment variables as follows :

```
 CPPFLAGS=-I/usr/include/openssl LDFLAGS=-L/usr/lib/ssl
```

now run ./configure ; make ; make install

To test if python has ssl support run this in the python shell :

```
import urllib
f = urllib.urlopen('https://svn.openplans.org')
# if it returns no errors ... the ssl support works.. 
```


## Setup ##

Note:
the python setuptools package (a python egg) is used by buildout, if you have an older version of setuptools, you might need to update it manually first (from http://cheeseshop.python.org/pypi/setuptools/) in the python used for zope.
Update instructions at: http://peak.telecommunity.com/DevCenter/EasyInstall#installation-instructions

If you dont have setuptools installed, buildout downloads and installs it automatically.

In order to install it, use buildout. These steps should be all you need to setup a Zope instance with all the required products and libraries:

```
$ svn co https://bungeni-portal.googlecode.com/svn/bungeni.buildout/trunk/ --username <username>
bungeni
$ cd bungeni
$ python bootstrap.py # not the system python! The one you use with Zope, i.e. 2.5.x. 
$ ./bin/buildout  # wait a while..
$ ./bin/setup-database # this will setup the postgres db
$ ./bin/load-demo-data # this will load the demo data
$ ./bin/paster serve debug.ini # this will launch the server in debug mode...
```

On a Mac, you may need to increase shmmax value to get postgresql up and running.

The buildout includes DeadlockDebugger, so if you start Zope in debug mode, it will stop at a debugger prompt if an exception is raised.