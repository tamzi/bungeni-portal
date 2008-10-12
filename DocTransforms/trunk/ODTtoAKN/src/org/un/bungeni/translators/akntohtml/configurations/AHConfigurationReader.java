package org.un.bungeni.translators.akntohtml.configurations;

public class AHConfigurationReader 
{
	//the instance of this Configuration Reader
	private static AHConfigurationReader instance;
	
	/**
	 * Protected constructor
	 */
	protected AHConfigurationReader()
	{
		
	}
	
	/**
	 * Get a new instance of the ConfigurationBuilderFactory
	 * @return the instance of the configuration builder
	 */
	public static AHConfigurationReader getInstance()
	{
		//if there is already an active instance return the instance 
		if(instance != null)
		{
			//return the instance
			return instance;
		}
		//if the Configuration Reader is not instanciated create a new instance 
		else
		{
			//create the instance
			instance = new AHConfigurationReader();
			//return the instance
			return instance;
		}
	}
}
