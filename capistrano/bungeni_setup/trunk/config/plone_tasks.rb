
namespace :plone_tasks do

    ## setup easy_install for the python and then install supervisord
    task :python_setup, :roles => [:app] do
      run "cd #{user24_python_home} && [ -f ./ez_setup.py ] && echo 'ez_setup.py exists' || wget http://peak.telecommunity.com/dist/ez_setup.py"
      run "cd #{user24_python_home} && #{user24_python} ./ez_setup.py"
      run "#{user24_python_home}/bin/easy_install supervisor"
    end

    desc "write local buildout file"
    task :localbuildout_config, :roles => [:app] do
        file = File.join(File.dirname(__FILE__), "templates", plone_local_buildout_config_file+".erb")
        template = File.read(file)
        buffer = ERB.new(template).result(binding)
        put buffer, "#{plone_buildout_dir}/#{plone_local_buildout_config_file}", :mode => 0644
	run "echo 'Local buildout configuration has been generated'"
    end


    task :plone_checkout, :roles => [:app] do
	run "mkdir -p #{plone_buildout_dir}"
	run "svn co #{plone_respository} #{plone_buildout_dir} --username=#{scm_username} --password=#{scm_password} --no-auth-cache"
    end 

    desc "bootstrap"
    task :bootstrap_bo, :roles=> :app do
      run  "cd #{plone_buildout_dir} && #{user24_python} ../bootstrap.py"
    end


    desc "full buildout"
    task :buildout_full, :roles=> :app do
      run "cd #{plone_buildout_dir} && PYTHON=#{user24_python} ./bin/buildout -t 3600"
    end

    desc "full buildout"
    task :buildout_full_local, :roles=> :app do
      run "cd #{plone_buildout_dir} && PYTHON=#{user24_python} ./bin/buildout -t 3600 -c #{plone_local_buildout_config_file} -v"
    end

    desc "optimisitic builout"
    task :buildout_opt, :roles=> :app do
      run "cd #{plone_buildout_dir} && PYTHON=#{user24_python} ./bin/buildout -N"
    end

    
    desc "optimisitic builout local"
    task :buildout_opt_local, :roles=> :app do
      run "cd #{plone_buildout_dir} && PYTHON=#{user24_python} ./bin/buildout -Ni -c #{plone_local_buildout_config_file} -v"
    end

    desc "update source"
    task :plone_upd, :roles=> :app do
      run "cd #{plone_buildout_dir} && svn up"
      run "cd #{plone_buildout_dir}/src && svn up"
    end


end
