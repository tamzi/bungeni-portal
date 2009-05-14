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
### Can be set to a http / ftp url or an absolute path to the file on the computer
### Edit these as desired ####
set :java6_download_url, "/home/undesa/Software/Software/jdk-6u14-ea-bin-b06-linux-i586-06_may_2009.bin"
set :tomcat_download_url, "http://mirror.cinquix.com/pub/apache/tomcat/tomcat-5/v5.5.27/bin/apache-tomcat-5.5.27.tar.gz"
set :maven_download_url, "http://www.apache.org/dist/maven/binaries/apache-maven-2.1.0-bin.tar.gz"
set :ant_download_url, "http://archive.apache.org/dist/ant/binaries/apache-ant-1.7.1-bin.tar.gz"
##### Component Specific Parameters ##### 

### do not edit any of these parameters (unless you know what you are doing) #### 

#### Java 6  #####
set :java6_install_binary, "jdk6.bin"
set :java6_install_dir_name, File.basename(java6_install_binary, ".bin")
set :java6_download_command, get_download_command(java6_download_url, java6_install_binary)
set :java6_home, "#{user_install_root}/#{java6_install_dir_name}"
set :java6_download_dir, "#{user_build_root}/#{java6_install_dir_name}"

#### Tomcat 5.5  #####
set :tomcat_install_archive, "tomcat.tar.gz"
set :tomcat_install_dirname, File.basename(tomcat_install_archive, ".tar.gz")
set :tomcat_download_command, get_download_command(tomcat_download_url, tomcat_install_archive)
set :tomcat_home, "#{user_install_root}/#{tomcat_install_dirname}"
set :tomcat_download_dir, "#{user_build_root}/#{tomcat_install_dirname}"

##### Maven #####
set :maven_install_archive, "maven.tar.gz"
set :maven_install_dirname, File.basename(maven_install_archive, ".tar.gz")
set :maven_download_command, get_download_command(maven_download_url, maven_install_archive)
set :maven_home, "#{user_install_root}/#{maven_install_dirname}"
set :maven_download_dir, "#{user_build_root}/#{maven_install_dirname}"

##### Ant #####
set :ant_install_archive, "ant.tar.gz"
set :ant_install_dirname, File.basename(ant_install_archive, ".tar.gz")
set :ant_download_command, get_download_command(ant_download_url, ant_install_archive)
set :ant_home, "#{user_install_root}/#{ant_install_dirname}"
set :ant_download_dir, "#{user_build_root}/#{ant_install_dirname}"


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
	"mkdir -p #{java6_download_dir}",
	"mkdir -p #{tomcat_download_dir}",
	"mkdir -p #{maven_download_dir}",
	"mkdir -p #{ant_download_dir}"
	].each {|cmd| run cmd}
    end

    desc "Install java6 jvm"
    task :setup_jvm, :roles=> [:app] do
	[
	"rm -rf #{java6_home}",
	"cd #{java6_download_dir} && #{java6_download_command} && chmod ug+x ./#{java6_install_binary}",
	"cd #{java6_download_dir} && echo y > answer.txt",
	"cd #{java6_download_dir}  && ./#{java6_install_binary} <answer.txt &>/dev/null",
	"cd #{java6_download_dir}  &&  mv ./jdk1.6* #{java6_home}"
	].each {|cmd| run cmd}
    end

    desc "Install Tomcat"
    task :setup_tomcat, :roles=> [:app] do
	[
	"rm -rf #{tomcat_home}",
	"cd #{tomcat_download_dir} && #{tomcat_download_command}",
	"cd #{tomcat_download_dir} && mkdir ./#{tomcat_install_dirname} && tar xvzf #{tomcat_install_archive} -C ./#{tomcat_install_dirname} --strip-components=1",
	"cd #{tomcat_download_dir} &&  mv ./#{tomcat_install_dirname} #{tomcat_home}"
	].each {|cmd| run cmd}
    end
	
    desc "Install Maven"
    task :setup_maven, :roles=> [:app] do
	[
	"rm -rf #{maven_home}",
	"cd #{maven_download_dir} && #{maven_download_command}",
	"cd #{maven_download_dir} && mkdir ./#{maven_install_dirname} && tar xvzf #{maven_install_archive} -C ./#{maven_install_dirname} --strip-components=1",
	"cd #{maven_download_dir} &&  mv ./#{maven_install_dirname} #{maven_home}"
	].each {|cmd| run cmd}
    end

    desc "Install Ant"
    task :setup_ant, :roles=> [:app] do
	[
	"rm -rf #{ant_home}",
	"cd #{ant_download_dir} && #{ant_download_command}",
	"cd #{ant_download_dir} && mkdir ./#{ant_install_dirname} && tar xvzf #{ant_install_archive} -C ./#{ant_install_dirname} --strip-components=1",
	"cd #{ant_download_dir} &&  mv ./#{ant_install_dirname} #{ant_home}"
	].each {|cmd| run cmd}
    end
	
   
end
