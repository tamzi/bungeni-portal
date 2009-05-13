#### CONFIG VARIABLE SETTING ####

set :application, "bungeni-dspace"
set :bungeni_username, "undesa"

## set :deploy_to_root, Proc.new { Capistrano::CLI.password_prompt('Deploy within this folder: ') }
#set :deploy_to, "#{user_install_root}/#{application}"
#was set :deploy_to, "/home/bungeni/bungeni_deploy/#{application}"
#set :install_dir, "#{deploy_to}/current"

set :user, "#{bungeni_username}"
set :use_sudo, false
set :app_host, "localhost"

#### ROLE SETTING ####
#
# db role is not required for capistrano 
# for webistrano, a db role is mandatory. so we add the following line for webistrano
# which adds the db role but never deploys or releases it
# role :db, "demo.bungeni.org", {:no_release=>true, :primary=>true}
#

role :app, "#{bungeni_username}@#{app_host}"

