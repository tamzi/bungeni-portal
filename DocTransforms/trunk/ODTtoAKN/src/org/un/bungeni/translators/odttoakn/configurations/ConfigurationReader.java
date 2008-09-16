package org.un.bungeni.translators.odttoakn.configurations;

import java.util.HashMap;

import org.un.bungeni.translator.odttoakn.steps.Step;
import org.w3c.dom.Document;

public class ConfigurationReader implements ConfigurationReaderInterface 
{
	//the XML that contains the configurations
	private Document configXML; 
	
	/**
	 * Create a new Configuration reader object builded on the given Config XML file 
	 * @param aConfigXML the XML file that contains the configuration 
	 */
	public ConfigurationReader(Document aConfigXML)
	{
		//save the config XML
		this.configXML = aConfigXML;
	}
	
	/**
	 * Get the step of the configuration with the given name
	 * @param aName the name of the step that you want to retreive
	 * @return a Step with the given name
	 */
	public Step getStepByName(String aName)
	{
		return null;
	}

	/**
	 * Get the step of the configuration with the given href
	 * @param aURI the href of the step that you want to retreive
	 * @return a Step with the given href
	 */
	public Step getStepByHref(String aURI)
	{
		return null;
	}

	/**
	 * Get the step of the configuration with the given position
	 * @param aPosition the position of the step that you want to retreive
	 * @return a Step with the given position
	 */
	public Step getStepByPosition(Integer aPosition)
	{
		return null;
	}
	
	/**
	 * Used to get an HashMao containing all the Steps of the configuration with their position 
	 * as key 
	 * @return the HashMap containing all the Steps of the configuration
	 */
	public HashMap<Integer,Step> getSteps()
	{
		return null;
	}

}
