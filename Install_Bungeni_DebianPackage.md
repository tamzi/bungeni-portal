# Introduction #
Install Bungeni using the Debian packaging system

# Download the Bungeni Debian Package #

## [Ubuntu 12.04 64 bit](http://releases.ubuntu.com/precise/) release 18-11-2014 (Development Build) ##

|Operating System | Download Link |
|:----------------|:--------------|
| Ubuntu 12.04 64 bit | [bungeni-workflow](https://drive.google.com/open?id=0B_uFxV_V1PC8SmY0R3IxTTFjckU&authuser=0) |
| Ubuntu 12.04 64 bit | [bungeni-postgresql](https://drive.google.com/open?id=0B_uFxV_V1PC8R0tOZkh5ZGZvYzg&authuser=0) |
| Ubuntu 12.04 64 bit | [bungeni-xml](https://drive.google.com/open?id=0B_uFxV_V1PC8MDVaYktOWTd6QTQ&authuser=0) |
| Ubuntu 12.04 64 bit | [bungeni-plone-cms](https://drive.google.com/open?id=0B_uFxV_V1PC8Qm15djdMbGViUzA&authuser=0) |
| Ubuntu 12.04 64 bit | [bungeni-proxy](https://drive.google.com/open?id=0B_uFxV_V1PC8eXRmbmdWVW53bG8&authuser=0) |

[Archived Releases](Older_Releases.md)

# Requirements #

Operating System as stated on the list above, at least 1 GB of free RAM, 15 GB of free disk space on the /opt partition (which is generally mapped to the root partition )

# How to Install #

First update your Operating system, either update using Ubuntu update manager or --  :
```
sudo apt-get update 
sudo apt-get upgrade
```

Once this has completed, download the packages, right click on it in Nautilus and click "Open With" -> "GDebi Package manager" (DO NOT use "Ubuntu Software Center")

The system will prompt you to enter your password, once you have entered that the installation will commence by installing the dependencies and then complete.

The packages need to be installed in the order listed above.

To install from the command line :
```
sudo gdebi bungeni_1.0+11113-2013-05-28_amd64.deb
sudo gdebi bungeni-postgresql_9.2+2013-05-28_amd64.deb
sudo gdebi bungeni-exist-db_2.0.0+18252-2013-05-28_amd64.deb
sudo gdebi bungeni-plone_4.3+11131-2013-05-29.deb
sudo gdebi bungeni-portal_0.6.1+11085-2013-05-28_amd64.deb
```

If you need to install gdebi you can install it using :
```
 sudo apt-get install gdebi-core
```

**NOTE: We don't recommend installing using `apt-get install bungeni_1.0+XXXXXX.deb` since it doesn't install the dependencies.**

# Starting and Stopping Bungeni #

Once the installation is complete, you can start and stop Bungeni from the terminal window :

To start:
```
sudo service bungeni_services start
```

You can now launch the web browser and browse to `http://localhost:8888` - enter user name and password : admin / admin and then you can start access the different Bungeni services. All the services need to be running for Bungeni to be accessible.

To stop:
```
sudo service bungeni_services stop
```

# Accessing the Services #

Once all the services have been started via service manager, you can access individual services via the web browser

`http://localhost:8081` - Bungeni legislative management
`http://localhost:8082` - Bungeni Plone content management
`http://localhost:8088` - Bungeni XML Repository

These can be proxied behind Nginx - see [Proxying Bungeni behind nginx](HowTo_ProxyBungeniBehindWebServer.md)

# Ports Used #

The following ports are used by Bungeni:

8888 (supervisor) , 8080 (bungeni proxy), 8081 (bungeni), 8082 (plone), 8088 & 8443 (exist), 5432 (postgres), 55672 & 4369 & 35197 & 5672 (all used by rabbitmq)

# Installation Structure & Details #

Please see [Installation Structure](InstallationStructure_Debian.md)

# To Uninstall #

You can uninstall using the package manager, by removing the `bungeni-XXXXX` packages via synaptic or update manager.

Or alternatively from the command line type :

```
sudo apt-get autoremove bungeni
```

Or to individually remove the packages :

```
sudo apt-get remove bungeni-portal
sudo apt-get remove bungeni-plone
sudo apt-get remove bungeni-exist-db
sudo apt-get remove bungeni-postgresql
sudo apt-get remove bungeni
```