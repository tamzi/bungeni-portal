# Introduction #

Bungeni can also be installed using a set of Debian packages.
When installed via the debian package method - the installation is much faster as the debian packages include pre-built binaries, so there is no build process required using the typical installation method.

# Starting services #

When the debian packages have been installed, the bungeni services can be started using the ubuntu service manager :

```
sudo service bungeni_services start
```

Which will start supervisor on port 8888 , and the user can browse to http://localhost:8888 to start / stop the bungeni services (default user / pass : admin / admin) .

# Folder Structure #

The folder structure for deployment is :

```
/opt/bungeni
├── bungeni_apps
├── exec
```


# Service Execution and Permissions #

All the bungeni services : postgres, bungeni, plone, portal etc are run using the "bungeni" user. The default password for the bungeni user is "bungeni".

The "bungeni" user is also the owner of the /opt/bungeni and its sub-folders.

**bungeni\_apps** - all the software components are installed within this folder, the structure is exactly the same as a built from source Bungeni

**exec** - this folders contains the fabric scripts. You can access them by ssh-ing to localhost using the `bungeni` user.

```
ssh bungeni@localhost
cd exec
```

If you want to install packages using the "bungeni" user, you will need to make the "bungeni" user as the sudo user :

```
sudo visudo
```

and then add the line in the visudo screen :

```
bungeni ALL=(ALL:ALL) ALL
```

**WARNING : Making "bungeni" a sudo user is not recommended for live deployments ! For live deployments the `bungeni` user needs to be disabled to prevent security intrusions.**

# Creating a working bungeni\_custom folder #

The correct way to correct a working bungeni\_custom folder is to use the fabric action `switch_bungeni_custom`. This fabric action will create a new bungeni\_custom folder within `/opt/bungeni/bungeni_apps/` called `customizations`.

e.g if you run :

```
cd exec
./fl switch_bungeni_custom 
```

You will see output like this :

```
[localhost] Executing task 'switch_bungeni_custom'
[localhost] run: cd ~ && pwd
[localhost] Login password:
[localhost] out: /opt/bungeni

[localhost] run: lsb_release --id -s
[localhost] out: Ubuntu

[localhost] run: lsb_release --r -s
[localhost] out: 12.04

[localhost] run: getconf LONG_BIT
[localhost] out: 32

[localhost] run: mkdir -p deploy_custom
[localhost] run: cp -R ./src/bungeni_custom/* deploy_custom
[localhost] run: find . -name '*.svn' -print0 | xargs -0 rm -rf
[localhost] run: echo `pwd` > bungeni_custom.pth

Done.
Disconnecting from localhost... done.
```

The command also switches bungeni to use the /opt/bungeni/bungeni\_apps/customizations folder as the custom folder (and also deletes things like .svn files from the new custom folder).

You can start with making customizations to the system in this folder.