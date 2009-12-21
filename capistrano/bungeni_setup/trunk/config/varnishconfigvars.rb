#### CONFIG VARIABLE SETTING ####

set :varnish_port, "8080"
set :varnish_admin_host, "localhost"
set :varnish_admin_port, "6082"
set :varnish_vcl_config, "#{varnish_runtime}/etc/varnish/bungeni.vcl"
set :varnish_cache_folder, "#{varnish_runtime}/cache"
set :varnish_cache_file, "varnish.cache"
set :varnish_cache, "#{varnish_cache_folder}/#{varnich_cache_file}"
set :varnish_cache_mem, "64M"



