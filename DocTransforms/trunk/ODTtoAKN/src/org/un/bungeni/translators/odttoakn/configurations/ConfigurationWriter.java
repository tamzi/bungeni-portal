package org.un.bungeni.translators.odttoakn.configurations;

import org.un.bungeni.translators.odttoakn.steps.Step;
import org.w3c.dom.Document;

public class ConfigurationWriter implements ConfigurationWriterInterface 
{
	//the XML that contains the configurations
	private Document configXML; 

	/**
	 * Create a new Configuration File builded on the given config XML file 
	 * @param aConfigXML the XML file in witch that contains the configuration
	 */
	public ConfigurationWriter(Document aConfigXML)
	{
		//save the config XML file 
		this.configXML = aConfigXML;
	}
	
	/**
	 * Add a step to the configuration file 
	 * @param aStep the step that you want to add to the configuration object
	*/
	public void writeStep(Step aStep)
	{
		System.out.println(this.configXML.toString());
	}

}
