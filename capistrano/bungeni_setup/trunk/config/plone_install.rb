
### Defines a sequence of tasks for installing bungeni from scratch ###
namespace :plone_install do
	
    task :setup, :roles=> [:app] do
	run "echo 'setting up plone installation'"
    end

    task :setup_from_cache, :roles=> [:app] do
	run "echo 'setting up plone installation (cached) '"
    end

    task :full, :roles=> [:app] do
      run "echo 'bootstraping and running a full buildout'"
    end

    task :full_from_cache, :roles=> [:app] do
      run "echo 'bootstraping and running a full buildout (cached)'"
    end


end
