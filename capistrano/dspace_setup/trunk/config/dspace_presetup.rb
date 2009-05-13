################################################################
#### Namespace to setup the runtime environment for bungeni ####
####  - Does an apt-get to install all the OS libraries
####  - Downloads and installs a user python 
####  - Installs all the required python libraries 
####  	- Python Imaging
####	- Python ssl
#### 	- Python svn bindings
#####	Tested on Ubuntu 8.04 
#####   To setup all the pre-requisites simply run :
#####   cap bungeni_presetup:build_all
##################################################################


### Defines a sequence of tasks for installing bungeni from scratch ###

#### General Build Parameter #####

### only the following 2 parameters need to be set by the user to customize
### this installation script for different computers
set :user_root, "/home/undesa/bungeni_dspace"
set :user_build_root, "#{user_root}/cap_builds"
set :user_install_root, "#{user_root}/cap_installs"

#### download URLs for components #####
### can be set to a http / ftp url or an absolute path to the file on the computer
set :java6_download_url, "/home/undesa/Software/Software/jdk-6u14-ea-bin-b06-linux-i586-06_may_2009.bin"
set :java6_install_binary, "jdk6.bin"
set :java6_default_extract_dir, "jdk1.6.0_14"
set :java6_install_dir_name, "java6"
set :java6_download_command, get_download_command(java6_download_url, java6_install_binary)


##### Component Specific Parameters ##### 

#### Java 6  #####

set :java6_home, "#{user_install_root}/#{java6_install_dir_name}"
set :java6_download_dir, "#{user_build_root}/#{java6_install_dir_name}"



namespace :dspace_presetup do
	
    desc "Installs the OS prequisites for DSpace"
    task :essentials, :roles=> [:app] do
	required_libs = [
			"build-essential", # for building from source
			"linux-headers-`uname -r`", # for building from source
			"openssl", # for java ssl
			"libssl-dev", # for java ssl
			"wget"
			]
	install_cmd = "apt-get install " + required_libs * " " 	+ " -y"
	sudo install_cmd
    end

    task :init, :roles=> [:app] do 
	[
	"mkdir -p #{user_build_root}",
	"mkdir -p #{user_install_root}",
	"mkdir -p #{java6_download_dir}"
	].each {|cmd| run cmd}
    end

    desc "Install java6 jvm"
    task :setup_jvm, :roles=> [:app] do
	[
	"rm -rf #{java6_home}",
	"cd #{java6_download_dir} && #{java6_download_command} && chmod ug+x ./#{java6_install_binary}",
	"cd #{java6_download_dir} && echo y > answer.txt",
	"cd #{java6_download_dir}  && ./#{java6_install_binary} <answer.txt &>/dev/null",
	"cd #{java6_download_dir}  &&  mv ./#{java6_default_extract_dir} #{java6_home}"
	].each {|cmd| run cmd}
    end

	
	
   
end
