namespace :bungeni_services do

desc "Start Bungeni"

    task :start_bungeni, :roles => [:app] do
	run "echo 'Starting Bungeni...'"
    end

    task :stop_bungeni, :roles => [:app] do
	run "echo 'Stopping Bungeni...'"
    end

    task :restart_bungeni, :roles => [:app] do
	run "echo 'Restarting Bungeni...'"
    end

    after "bungeni_services:start_bungeni", "bungeni_tasks:start_supervisor"
    after "bungeni_services:stop_bungeni", "bungeni_tasks:stop_supervisor"
    after "bungeni_services:restart_bungeni", "bungeni_services:stop_bungeni", "bungeni_services:start_bungeni"



end

