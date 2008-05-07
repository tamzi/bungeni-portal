export JAVA_HOME=/usr/java/jdk1.5.0_11
export BUNGENI_EDITOR_HOME=.
export LOG4J_HOME=$BUNGENI_EDITOR_HOME/lib
$JAVA_HOME/bin/java -Dlog4j.ignoreTCL=true -jar BungeniEditorClient.jar
