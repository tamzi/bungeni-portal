package org.un.bungeni.translators.globalconfigurations;

/**
 * This is the global configuration class. It contains static fields that can be accessed 
 * and modified by all the classes of the project
 */
public class GlobalConfigurations 
{
	//the prefix for all the application path
	private static String applicationPathPrefix = "";
	
	/**
	 * Set the application path prefix to the given one
	 * @param anApplicationPathPrefix the new application path prefix
	 */
	public static void setApplicationPathPrefix(String anApplicationPathPrefix)
	{
		//change the application path prefix to the given one
		GlobalConfigurations.applicationPathPrefix = anApplicationPathPrefix;
	}
	
	/**
	 * Return the application path prefix 
	 * @return the application path prefix
	 */
	public static String getApplicationPathPrefix()
	{
		//return the application path prefix
		return GlobalConfigurations.applicationPathPrefix;
	}
}
