set JAVA_HOME=e:\Java\jdk1.6.0
set LOG4J_PROPS="file:///e:/projects/workingprojects/bungenieditor/trunk/BungeniEditorClient/dist/settings/log4j.properties"
%JAVA_HOME%\bin\java -Dlog4j.ignoreTCL -Dlog4j.configuration=%LOG4J_PROPS% -jar BungeniEditorClient.jar