################################################################
#### Namespace to setup the runtime environment for bungeni ####
####  - Does an apt-get to install all the OS libraries
####  - Downloads and installs a user python 
####  - Installs all the required python libraries 
####  	- Python Imaging
####	- Python ssl
#### 	- Python svn
##################################################################

### Common functions ####
### add a starts with API to string ###
class String
  def startsWith str
    return self[0...str.length] == str
  end
end

### use wget if its a url or use a local 'cp' command if its on a folder 
### on the same computer
def get_python_download_command strUrl
	if (strUrl.startsWith("http") or strUrl.startsWith("ftp"))
		return "wget " + strUrl
	else
		return "cp " + strUrl + " ."
	end
end

### Defines a sequence of tasks for installing bungeni from scratch ###

#### General Build Parameter #####

### only the following 2 parameters need to be set by the user to customize
### this installation script for different computers
set :user_build_root, "/home/bungeni/cap_builds"
set :user_install_root, "/home/bungeni/cap_installs"

#### Python build parameters #####

set :user_python_build_path, "#{user_build_root}/python"
set :user_python25_runtime, "#{user_install_root}/python25"
set :python_download_url, "/home/bungeni/Python-2.5.4.tgz"
set :python_download_file, File.basename(python_download_url)
set :python_src_dir, File.basename(python_download_file, ".tgz")
set :python_download_command, get_python_download_command(python_download_url)

#### python imaging parameters ####

set :python_imaging_download_url, "http://effbot.org/media/downloads/Imaging-1.1.7b1.tar.gz"
set :python_imaging_download_file, File.basename(python_imaging_download_url)
set :python_imaging_src_dir, File.basename(python_imaging_download_file, ".tar.gz")

#### libneon parameters ####
set :neon_src_dir, "#{user_build_root}/neon"
set :neon_install_dir, "#{user_install_root}/neon"
set :neon_svn_source, "http://svn.webdav.org/repos/projects/neon/tags/0.28.3"


namespace :bungeni_presetup do
	
    task :essentials, :roles=> [:app] do
	sudo "apt-get install build-essential libjpeg62-dev libfreetype6-dev libpng12-dev openssl libssl-dev bison flex libreadline5-dev zlib1g-dev libtool automake autoconf libaprutil1-dev swig -y"
    end

    task :build_python, :roles=> [:app] do
	[
	"mkdir -p #{user_python_build_path}",
	"rm -rf #{user_python_build_path}/*.*",
	"mkdir -p #{user_python25_runtime}",
	"cd #{user_python_build_path} && #{python_download_command}",
 	"cd #{user_python_build_path} && tar xvzf #{python_download_file}",
	"cd #{user_python_build_path}/#{python_src_dir} && CPPFLAGS=-I/usr/include/openssl LDFLAGS=-L/usr/lib/ssl ./configure --prefix=#{user_python25_runtime}",
	"cd #{user_python_build_path}/#{python_src_dir} && CPPFLAGS=-I/usr/include/openssl LDFLAGS=-L/usr/lib/ssl make",
	"cd #{user_python_build_path}/#{python_src_dir} && make install"
	].each {|cmd| run cmd}
    end

    task :build_imaging, :roles=> [:app] do
	[
	"cd #{user_python_build_path} && rm -rf #{python_imaging_download_file}",
	"cd #{user_python_build_path} && wget #{python_imaging_download_url}",
	"rm -rf #{user_python_build_path}/#{python_imaging_src_dir}",
 	"cd #{user_python_build_path} && tar xvzf #{python_imaging_download_file}",
	"cd #{user_python_build_path}/#{python_imaging_src_dir} && #{user_python25_runtime}/bin/python setup.py build_ext -i",
	"cd #{user_python_build_path}/#{python_imaging_src_dir} && #{user_python25_runtime}/bin/python setup.py install"
	].each {|cmd| run cmd}
    end


end
