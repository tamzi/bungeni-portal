set :application, "bungeni"
set :bungeni_username, "undesa"
set :repository,  "https://bungeni-portal.googlecode.com/svn/bungeni.buildout/trunk"
set :user_python, "/home/undesa/dev/bungeni/python/254/bin/python"

# If you aren't deploying to /u/apps/#{application} on the target
# servers (which is the default), you can specify the actual location
# via the :deploy_to variable:
set :deploy_to, "/home/undesa/dev/capdeploy/#{application}"
set :buildout_dir, "#{deploy_to}/current"

# If you aren't using Subversion to manage your source code, specify
# your SCM below:

set :scm, :subversion
set :scm_username, "listmanster"
set :scm_password, "y5k3h3g8"
set :user, "#{bungeni_username}"
set :use_sudo, false


role :app, "undesa@demo.bungeni.org"
#role :db,  "192.168.0.122", :primary => false
#role :db,  "192.168.0.122", :no_release => true

#role :web, "bungeni@bungeni.org"
#role :db,  "bungeni@ubuntu-server", :primary => true

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
task :put_demo_data, :roles=> :app do
	run "cd #{buildout_dir} && ./bin/load-demo-data"
end


end
  

