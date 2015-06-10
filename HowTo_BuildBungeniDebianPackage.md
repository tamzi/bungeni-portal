# Introduction #

This page documents the steps to create a debian package for Bungeni.

# Step 1 - Building Bungeni #

## Preparing the Environment ##

First we need to build Bungeni using a particular structure.

For the debian package distribution, Bungeni is always installed in the `/opt/bungeni` folder and run using a `bungeni` user.

So we need to create the environemnt for the build first. Check out the debian\_package project from svn into a folder

```
svn co https://bungeni-portal.googlecode.com/svn/debian_package_devscripts/ debian_package_devscripts
```

This will give you a list of utility scripts and will also checkout debian\_package and debian\_package\_update repositories via externals.

The structure you get should look like this:

```
	debian_package_devscripts
	├── clean_today
	├── debian_package - Folder
	├── debian_package_update - Folder
	├── externals.txt
	├── inst_all
	├── mk_dev
	├── mv_2_dist
	├── prepare_userenv.sh
	├── README
	├── rm_rf_bungeni
	└── svn_set_xtrnls.sh
```

This is what the scripts do:

**clean\_today** - When building you may need to clean out broken packages and their related archives inorder to rebuild a fresh.

The generated archives are scattered in the packager and to manually remove them would be tidious because of

the use of sudo to build the packages, a clean up script is recommended inorder to speed up the build process.

```
clean_today <packager folder>

e.g 

$ sudo ./clean_today debian_package
```

**inst\_all** - You may need to install all the debian packages of a single release without always prompting a yes during the procees.

```
inst_all <dist release folder>

e.g

$ sudo ./inst_all dist/bungeni_debs32_snapshot_2012-12-21
```

Note : No trailing back slash

**mk\_dev** - This script takes the original debian packager (production packager) and creates a development packager. Appends "dev" to new packager folder.

```
mk_dev <debian packager folder>

e.g

$ sudo ./mk_dev debian_packager
```

**mv\_2\_dist** - Takes the packages and deposits them in dist under a folder with proper naming

```
mv_2_dist <debian packager folder>

e.g

$ sudo ./mv_2_dist debian_packger
```

**rm\_rf\_bungeni** - Forces removal of bungeni. Use only  when the bungeni package is broken.

```
$ sudo ./rm_rf_bungeni
```

**svn\_set\_xtrnls.sh** - Sets externals, you can define the specific releases in the externals.txt file

```
./svn_set_xtrnls.sh
```

**prepare\_userenv.sh** - This script should be the first to run after checking out development scripts.

It creates a `/opt/bungeni` folder and also creates a `bungeni` user with a default `bungeni` password which will be used to

create the deployment and packaging installation, additionally we also set the home directory for the `bungeni` user to `/opt/bungeni`.

```
sudo ./prepare_userenv.sh
```

## Building Bungeni ##

First login as the `bungeni` user :

```
ssh bungeni@localhost
```

You will be logged into the  /opt/bungeni folder

Check out the fabric scripts into a folder called `exec` :

```
svn co https://bungeni-portal.googlecode.com/svn/fabric/trunk/ exec
```

Edit the release.ini and setup.ini appropriately for the revision that you want to create the package for.

Finally build bungeni using the documented procedures (see Install\_Bungeni\_Fabric)

# Step 2 - Building the Debian Package #

When you have built and tested the bungeni installation, you are ready to package in a debian distribution file.

First, stop the Bungeni and Postgres service and stop the supervisor monitor via the fabric command :

```
./fab -u bungeni stop_monitor
```

Now exit from the `bungeni` user login to return back to your default login :

```
exit
```

Switch to the debian\_package\_devscripts folder :

```
cd ~/debian_package_devscripts/debian_package
```

There are 4 debian packages that can be built using the deb pack (bungeni, exist-db, plone and bungeni portal) The scripts uses the following syntax :

```
sudo ./bungeni.sh <version>
```
Do sudo for bungeni script because the compress command needs to get database configuration into the zip file.

```
./exist.sh <release>
```

No arguments for plone shell script
```
./plone.sh
```

No arguments for portal shell script
```
./portal.sh
```

You can also build all the debian packages
```
sudo ./build_all.sh
```