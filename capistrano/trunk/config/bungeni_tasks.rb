
namespace :bungeni_tasks do
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
