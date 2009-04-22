### Author : Ashok Hariharan
### Description :
### deploy.erb for setting up bungeni using capistrano
### checks out svn source , sets up python correctly, sets up the config files (supervisord.conf) using erb templatss
### 

#### COMMMON FUNCTIONS ####

def prompt_def(var, askmsg, default)
  set(var) do
	Capistrano::CLI.ui.ask "#{askmsg} [#{default}] : "
  end
  set var, default if eval("#{var.to_s}.empty?")
end



#### CONFIG VARIABLE SETTING ####

set :application, "bungeni"
set :bungeni_username, "bungeni"
set :repository,  "https://bungeni-portal.googlecode.com/svn/bungeni.buildout/trunk"

## prompt for svn user names & passwords
set :scm, :subversion

## all prompts here
prompt_def(:bungeni_username, 'User name to run as:', 'bungeni')
set :scm_username, Proc.new { Capistrano::CLI.ui.ask('SVN Username: ') }
set :scm_password, Proc.new { Capistrano::CLI.password_prompt('SVN Password: ') }
prompt_def(:user_python_home, 'User Python Home Directory', "/home/bungeni/apps/python" )
prompt_def(:deploy_to_root, 'Deploy within this folder: ', '/home/bungeni/bungeni_deploy')


## user python is used to run bungeni in the user context -- this is a pre-requisite
#was "/home/bungeni/apps/python"
set :user_python, "#{user_python_home}/bin/python"

## admin python is used to run supervisord can be same as user python or a different one
set :adm_python_home, "#{user_python_home}"
set :adm_python, "#{adm_python_home}/bin/python"


## generate supervisord config files
## config file for supervisord is generated using a ERB template
## supervisord is installed using ez_setup

set :supervisord, "#{adm_python_home}/bin/supervisord"
set :supervisorctl, "#{adm_python_home}/bin/supervisorctl"

# erb template to supervisord.conf
set :supervisord_config_file, "supervisord.conf.erb"

## force prompt if any unknown prompts pop up
default_run_options[:pty] = true

## set :deploy_to_root, Proc.new { Capistrano::CLI.password_prompt('Deploy within this folder: ') }
set :deploy_to, "#{deploy_to_root}/#{application}"
#was set :deploy_to, "/home/bungeni/bungeni_deploy/#{application}"
set :buildout_dir, "#{deploy_to}/current"

set :user, "#{bungeni_username}"
set :use_sudo, false
set :app_host, "localhost"

#### ROLE SETTING ####

role :app, "#{bungeni_username}@#{app_host}"

#
# db role is not required for capistrano 
# for webistrano, a db role is mandatory. so we add the following line for webistrano
# which adds the db role but never deploys or releases it
# role :db, "demo.bungeni.org", {:no_release=>true, :primary=>true}
#


namespace :libbungeni do
    ## generate supervisord.conf using a ERB template found in config/templates
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



    desc "bootstrap"
    task :bootstrap_bo, :roles=> :app do
      run  "cd #{buildout_dir} && #{user_python} ./bootstrap.py"
    end


    desc "full buildout"
    task :buildout_full, :roles=> :app do
      run "cd #{buildout_dir} && PYTHON=#{user_python} ./bin/buildout"
    end

    desc "optimisitic builout"
    task :buildout_opt, :roles=> :app do
      run "cd #{buildout_dir} && PYTHON=#{user_python} ./bin/buildout -N"
    end

    desc "update source"
    task :bungeni_upd, :roles=> :app do
      run "cd #{buildout_dir} && svn up"
      run "cd #{buildout_dir}/src && svn up"
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

    desc "reset database"
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

    desc "stop bungeni"
    task :stop_bungeni, :roles=> :app do
      run "#{supervisorctl} stop bungeni"
    end

    desc "start bungeni"
    task :start_bungeni, :roles=> :app do
      run "#{supervisorctl} start bungeni"
    end



    desc "stop supervisor"
    task :stop_supervisor, :roles=> :app do
      run "#{supervisorctl} shutdown"
    end

## run python_setup automatically aftter deploy:setup
#after "deploy:setup", "bungeni:python_setup"
## after python_setup automatically do a deploy:update to setup the svn repo
#after "bungeni:python_setup", "deploy:update"
## after deploy:update, setup supervisord config
#after "deploy:update", "bungeni:supervisord_config"

end


### Defines a sequence of tasks for updating bungeni ###
namespace :bungeni_update do

    task :quick_update, :roles=> :app do
      run "echo 'Running optimistic update of bungeni'"
    end


    after ":bungeni_update:quick_update", "libbungeni:stop_bungeni", "libbungeni:bungeni_upd", "libbungeni:buildout_opt", "libbungeni:start_bungeni"

    task :quick_update_with_db, :roles=> :app do
      run "echo 'Runnning quick update with db update'"
    end

    after ":bungeni_update:quick_update_with_db",  "libbungeni:stop_bungeni", "libbungeni:bungeni_upd", "libbungeni:buildout_opt", "libbungeni:reset_db", "libbungeni:install_demo_data", "libbungeni:start_bungeni"

end


### Defines a sequence of tasks for installing bungeni from scratch ###
namespace :bungeni_install do

    task :full, :roles=> :app do
      run "echo 'bootstraping and running a full buildout'"
    end

    after "bungeni_install:full", "bungeni:bootstrap_bo", "bungeni:buildout_full"

end
  

