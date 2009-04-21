set :application, "bungeni"
set :bungeni_username, "bungeni"
set :repository,  "https://bungeni-portal.googlecode.com/svn/bungeni.buildout/trunk"
set :scm, :subversion
set :scm_username, Proc.new { Capistrano::CLI.password_prompt('SVN Username: ') }
set :scm_password, Proc.new { Capistrano::CLI.password_prompt('SVN Password: ') }
set :user_python_home, Proc.new { Capistrano::CLI.password_prompt('User Python Home Directory: ') }

#was "/home/bungeni/apps/python"
set :user_python, "#{user_python_home}/bin/python"
set :adm_python_home, "#{user_python_home}"
set :adm_python, "#{adm_python_home}/bin/python"
### Author : Ashok Hariharan
### Description :
### deploy.erb for setting up bungeni using capistrano
### checks out svn source , sets up python correctly, sets up the config files (supervisord.conf) using erb templatss
### 

##generate supervisord config files
set :supervisord, "#{adm_python_home}/bin/supervisord"
## erb template to supervisord.conf
set :supervisord_config_file, "supervisord.conf.erb"

#force prompt if any unknown prompts pop up
default_run_options[:pty] = true

set :deploy_to_root, Proc.new { Capistrano::CLI.password_prompt('Deploy within this folder: ') }
set :deploy_to, "#{deploy_to_root}/#{application}"
#was set :deploy_to, "/home/bungeni/bungeni_deploy/#{application}"
set :buildout_dir, "#{deploy_to}/current"


set :user, "#{bungeni_username}"
set :use_sudo, false
set :app_host, "localhost"

role :app, "#{bungeni_username}@#{app_host}"
#
# db role is not required for capistrano 
# for webistrano, a db role is mandatory. so we add the following line for webistrano
# which adds the db role but never deploys or releases it
# role :db, "demo.bungeni.org", {:no_release=>true, :primary=>true}
#


namespace :bungeni do


desc "write supervisor config file"
task :supervisord_config, :roles => [:app] do
	file = File.join(File.dirname(__FILE__), "templates", supervisord_config_file)
	template = File.read(file)
	buffer = ERB.new(template).result(binding)
	put buffer, "#{buildout_dir}/supervisord.conf", :mode => 0644
end

## setup easy_install for the python and then install supervisord 
task :python_setup, :roles => [:app] do 
	run "cd #{user_python_home} && [ -f ./ez_setup.py ] && echo 'ez_setup.py exists' || wget http://peak.telecommunity.com/dist/ez_setup.py"
	run "cd #{user_python_home} && #{user_python} ./ez_setup.py"
	run "#{user_python_home}/bin/easy_install supervisor"
end

## run python_setup automatically aftter deploy:setup
after "deploy:setup", "bungeni:python_setup"
## after python_setup automatically do a deploy:update to setup the svn repo
after "bungeni:python_setup", "deploy:update"


desc "bootstrap"
task :bootstrap_bo, :roles=> :app do
	run  "cd #{buildout_dir} && #{user_python} ./bootstrap.py"
end

## after deploy:update, setup supervisord config
after "deploy:update", "bungeni:supervisord_config"


desc "full buildout"
task :buildout_full, :roles=> :app do
	run "cd #{buildout_dir} && PYTHON=#{user_python} ./bin/buildout"
end

desc "optimisitic builout" 
task :buildout_opt, :roles=> :app do
	run "cd #{buildout_dir} && PYTHON=#{user_python} ./bin/buildout -N"
end

desc "start postgres"
task :postgres_start, :roles=> :app do
	run "cd #{buildout_dir} && ./bin/pg_ctl start"
end

desc "stop postgres"
task :postgres_stop, :roles=> :app do
	run "cd #{buildout_dir} && ./bin/pg_ctl stop"
end


desc "setup database"
task :setup_db, :roles=> :app do
	run "cd #{buildout_dir} && ./bin/setup-database"
end

desc "reset databse"
task :reset_db, :roles=> :app do
	run "cd #{buildout_dir} && ./bin/reset-db"
end

desc "load demo data"
task :install_demo_data, :roles=> :app do
	run "cd #{buildout_dir} && ./bin/load-demo-data"
end


desc "start supervisor"
task :start_supervisor, :roles=> :app do
	run "#{supervisord} -c #{buildout_dir}/supervisord.conf"
end



end
  

