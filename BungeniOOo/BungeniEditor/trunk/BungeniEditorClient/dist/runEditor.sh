export JAVA_HOME=/usr/java/jdk1.5.0_11
export BUNGENI_EDITOR_HOME=${PWD}
export LOG4J_PROPS=file://$BUNGENI_EDITOR_HOME/settings/log4j.properties
$JAVA_HOME/bin/java -Dlog4j.ignoreTCL=true -Dlog4j.configuration=$LOG4J_PROPS -jar BungeniEditorClient.jar
