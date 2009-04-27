### Defines a sequence of tasks for updating bungeni ###

require "config/bungeni_tasks"

namespace :bungeni_update do

    task :quick_update, :roles=> :app do
      run "echo 'Running optimistic update of bungeni'"
    end


    after ":bungeni_update:quick_update", "bungeni_tasks:stop_bungeni", "bungeni_tasks:bungeni_upd", "bungeni_tasks:buildout_opt", "bungeni_tasks:start_bungeni"

    task :quick_update_with_db, :roles=> :app do
      run "echo 'Runnning quick update with db update'"
    end

    after ":bungeni_update:quick_update_with_db",  "bungeni_tasks:stop_bungeni", "bungeni_tasks:bungeni_upd", "bungeni_tasks:buildout_opt", "bungeni_tasks:reset_db", "bungeni_tasks:install_demo_data", "bungeni_tasks:start_bungeni"

end