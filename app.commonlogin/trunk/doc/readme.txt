Setting up the common login

- enable mod_proxy, mod_proxy_http and mod_rewrite on apache

- setup plone to run on port 8080, and bungeni to run on port 8081

- install the sites provided under apache/sites to /etc/apache2/sites-available and link them up to /etc/apache2/sites-enabled.

- you may have to adjust the plone rewrite url to the appropriate plone site within the apache site config for plone

- install the custom login_proxy script provided under plone/ into the plone site as an ExternalMethod.

- copy the login_proxy script provided under bungeni-portal/ into 'bungeni.ui/bungeni/ui/viewlets' in the bungeni portal source tree. also add the browser:page directive as specified in bungeni.ui-viewlets-configure.zcml to the configure.zcml file under bungeni.ui/bungeni/ui/viewlets

- adding the following entries to the /etc/hosts file (or set it up within your BIND dns config as subdomains mapped to appropriate IPs ) :
plone.bugenisrv.local 127.0.0.1
portal.bungenisrv.local 127.0.0.1
www.bungenisrv.local 127.0.0.1

- add the login.php file and bungeni.html form into /var/www (which is the folder that the domain www.bungenisrv.local maps to)

Note : plone needs to be switched to use exclusively cookie authentication. Since plone 3.1 the authentication mechansim was switched to use a session based authentication. To revert plone to a cookie based authentication, go the acl_users folder in the plone site, and delete the object called 'sessions'
