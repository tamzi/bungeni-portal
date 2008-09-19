package org.un.bungeni.translators.odttoakn.configurations;

import java.io.IOException;
import java.util.HashMap;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.map.Map;
import org.un.bungeni.translators.odttoakn.steps.ConfigStep;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;

/**
 * This is the configuration object. 
 * It is used to read a configuration, write a configuration and to create a new configuration
 */
public class Configuration implements ConfigurationInterface 
{
	//the configuration reader
	private ConfigurationReader reader;
	
	//the configuration writer
	private ConfigurationWriter writer;
	
	/**
	 * Create a new configuration based on a given Configuration XML file
	 * @param aConfigXML the XML Document in witch the configuration is written 
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws XPathExpressionException 
	 */
	public Configuration(Document aConfigXML) throws XPathExpressionException, SAXException, IOException, ParserConfigurationException
	{
		//create the writer
		this.writer = new ConfigurationWriter(aConfigXML);
		
		//create the reader
		this.reader = new ConfigurationReader(aConfigXML);
	}

	/**
	 * Get the step of the configuration with the given name
	 * @param aName the name of the step that you want to retreive
	 * @return a Step with the given name
	 * @throws XPathExpressionException 
	 */
	public ConfigStep getStepByName(String aName) throws XPathExpressionException 
	{
		//ask the reader to get the step with the given name
		ConfigStep resultStep = this.reader.getStepByName(aName);
		
		//return the gotten step 
		return resultStep;
	}

	/**
	 * Get the step of the configuration with the given href
	 * @param aURI the href of the step that you want to retreive
	 * @return a Step with the given href
	 * @throws XPathExpressionException 
	 */
	public ConfigStep getStepByHref(String aURI) throws XPathExpressionException 
	{
		//ask the reader to get the step with the given URI
		ConfigStep resultStep = this.reader.getStepByHref(aURI);
		
		//return the gotten step 
		return resultStep;
	}

	/**
	 * Get the step of the configuration with the given position
	 * @param aPosition the position of the step that you want to retreive
	 * @return a Step with the given position
	 * @throws XPathExpressionException 
	 */
	public ConfigStep getStepByPosition(Integer aPosition) throws XPathExpressionException 
	{
		//ask the reader to get the step with the given URI
		ConfigStep resultStep = this.reader.getStepByPosition(aPosition);
		
		//return the gotten step 
		return resultStep;
	}

	/**
	 * Used to get an HashMao containing all the Steps of the configuration with their position 
	 * as key 
	 * @return the HashMap containing all the Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, ConfigStep> getSteps() throws XPathExpressionException 
	{
		//ask the reader to get the steps of the configuration
		HashMap<Integer, ConfigStep> resultSteps = this.reader.getSteps();
		
		//return the gotten steps 
		return resultSteps;
	}

	/**
	 * Returns the Map object related to this Configuration object
	 * @return the map object related to this configuration object
	 */
	public Map getConfigurationMap()
	{
		//get the map object of this configuration
		Map configurationMap = this.reader.getConfigurationMap();
		
		//return the map object of this configuration
		return configurationMap;
	}

	public void writeStep(ConfigStep step) 
	{
		System.out.println(this.writer.toString());
	}

}
