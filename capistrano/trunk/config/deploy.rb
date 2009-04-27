### Author : Ashok Hariharan
### Description :
### deploy.erb for setting up bungeni using capistrano
### checks out svn source , sets up python correctly, sets up the config files (supervisord.conf) using erb templatss
### 

### commmon functions used by other scripts
load "./commonfunctions.rb"

### config variables used by the deployment.  edit this for customized installation
load "./bungeniconfigvars.rb"

### all the core tasks for installing and updating bungeni
load "./bungeni_tasks.rb"

### grouped tasks for updating bungeni (composed of core tasks)
load "./bungeni_update.rb"

### grouped tasks for installing bungeni (composed of core tasks)
load "./bungeni_install.rb"




  

