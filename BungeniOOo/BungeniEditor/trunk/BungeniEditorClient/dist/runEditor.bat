LOG4J_PROPS=%CD%\settings\log4j.properties
java -Dlog4j.ignoreTCL -Dlog4j.configuration=%LOG4J_PROPS% -jar BungeniEditorClient.jar