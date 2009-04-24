
### Defines a sequence of tasks for installing bungeni from scratch ###
namespace :bungeni_install do

    task :full, :roles=> :app do
      run "echo 'bootstraping and running a full buildout'"
    end

    after "bungeni_install:full", "bungeni_tasks:bootstrap_bo", "bungeni_tasks:buildout_full"

end
