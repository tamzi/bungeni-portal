require 'rexml/document'



=begin
generate <Context> element for tomcat server.xml
=end
def dspace_context ctxPath, ctxDocbase
	# path="/jspui" docBase="/home/undesa/apps/dspacesrv/webapps/jspui" debug="0" reloadable="true" cachingAllowed="false" allowLinking="true"/>
	ctxJsp = REXML::Element.new "Context"
	ctxJsp.add_attribute("path", ctxPath)
	ctxJsp.add_attribute("docBase", ctxDocbase)
	ctxJsp.add_attribute("debug", "0")
	ctxJsp.add_attribute("reloadable", "true")
	ctxJsp.add_attribute("cachingAllowed", "false")
	ctxJsp.add_attribute("allowLinking", "true")
	return ctxJsp
end



=begin 
Parse and Edit tomcat server.xml
=end
def update_tomcat_serverxml strFile

	File.open(strFile) do |serverxmlfile|
		serverxml = REXML::Document.new(serverxmlfile)
		#update the server port number 
		serverxml.root.elements['Service/Connector'].attributes['port'] = tomcat_port
		#add the dspace context elements to the host element
		serverhost = serverxml.root.elements['Service/Engine/Host']
		#<Context path="/jspui" docBase="/home/undesa/apps/dspacesrv/webapps/jspui" debug="0" 
		#reloadable="true" cachingAllowed="false" allowLinking="true"/>
		serverhost.add_element(dspace_context('/jspui' , "#{dspace_home}" + "/webapps/jspui"))
		serverhost.add_element(dspace_context('/xmlui' , "#{dspace_home}" + "/webapps/xmlui"))
		serverhost.add_element(dspace_context('/oai' , "#{dspace_home}" + "/webapps/oai"))
		fdspaceServerXml = File.open("#{dspace_server_xml}", "w")
		fdspaceServerXml.puts serverxml 
		dspaceXmlPath = fdspaceServerXml.path
		fdspaceServerXml.close
		end
end

