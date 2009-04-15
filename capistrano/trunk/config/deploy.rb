set :application, "bungeni"
set :bungeni_username, "undesa"
set :repository,  "https://bungeni-portal.googlecode.com/svn/bungeni.buildout/trunk"
set :user_python, "/home/undesa/dev/bungeni/python/254/bin/python"
set :adm_python_home, "/home/undesa/dev/bungeni/python/adm"
set :adm_python, "#{adm_python_home}/bin/python"
set :supervisord, "#{adm_python_home}/bin/supervisord"
set :supervisord_config, "/home/undesa/dev/bungeni/supervisor/supervisord.conf"

# If you aren't deploying to /u/apps/#{application} on the target
# servers (which is the default), you can specify the actual location
# via the :deploy_to variable:
set :deploy_to, "/home/undesa/dev/capdeploy/#{application}"
set :buildout_dir, "#{deploy_to}/current"

# If you aren't using Subversion to manage your source code, specify
# your SCM below:

set :scm, :subversion
set :scm_username, Proc.new { Capistrano::CLI.password_prompt('SVN Username: ') }
set :scm_password, Proc.new { Capistrano::CLI.password_prompt('SVN Password: ') }
set :user, "#{bungeni_username}"
set :use_sudo, false


role :app, "undesa@demo.bungeni.org"
#
# db role is not required for capistrano 
# for webistrano, a db role is mandatory. so we add the following line for webistrano
# which adds the db role but never deploys or releases it
# role :db, "demo.bungeni.org", {:no_release=>true, :primary=>true}
#


namespace :deploy do
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
	run "#{supervisord} -c #{supervisord_config}"
end



end
  

