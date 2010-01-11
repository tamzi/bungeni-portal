export JAVA_HOME=/usr/lib/jvm/java-6-sun
export BUNGENI_EDITOR_HOME=${PWD}
export LOG4J_PROPS=file://$BUNGENI_EDITOR_HOME/settings/log4j.properties
$JAVA_HOME/bin/java -Dlog4j.ignoreTCL=true -Dlog4j.configuration=$LOG4J_PROPS -jar BungeniEditorClient.jar
