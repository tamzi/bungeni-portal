### Author : Ashok Hariharan
### Description :
### deploy.erb for setting up bungeni using capistrano
### checks out svn source , sets up python correctly, sets up the config files (supervisord.conf) using erb templatss
### 

### commmon functions used by other scripts
require "config/commonfunctions"

### config variables used by the deployment.  edit this for customized installation
require "config/bungeniconfigvars"

### all the core tasks for installing and updating bungeni
require "config/bungeni_tasks"

### grouped tasks for updating bungeni (composed of core tasks)
require "config/bungeni_update"

### grouped tasks for installing bungeni (composed of core tasks)
require "config/bungeni_install"




  

