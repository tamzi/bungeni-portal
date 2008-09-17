package org.un.bungeni.translators.odttoakn.configurations;

import java.util.HashMap;

import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.steps.Step;
import org.w3c.dom.Document;

public class Configuration implements ConfigurationInterface 
{
	//the configuration reader
	private ConfigurationReader reader;
	
	//the configuration writer
	private ConfigurationWriter writer;
	
	/**
	 * Create a new configuration based on a given Configuration XML file
	 * @param aConfigXML the XML Document in witch the configuration is written 
	 */
	public Configuration(Document aConfigXML)
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
	public Step getStepByName(String aName) throws XPathExpressionException 
	{
		//ask the reader to get the step with the given name
		Step resultStep = this.reader.getStepByName(aName);
		
		//return the gotten step 
		return resultStep;
	}

	/**
	 * Get the step of the configuration with the given href
	 * @param aURI the href of the step that you want to retreive
	 * @return a Step with the given href
	 * @throws XPathExpressionException 
	 */
	public Step getStepByHref(String aURI) throws XPathExpressionException 
	{
		//ask the reader to get the step with the given URI
		Step resultStep = this.reader.getStepByHref(aURI);
		
		//return the gotten step 
		return resultStep;
	}

	/**
	 * Get the step of the configuration with the given position
	 * @param aPosition the position of the step that you want to retreive
	 * @return a Step with the given position
	 * @throws XPathExpressionException 
	 */
	public Step getStepByPosition(Integer aPosition) throws XPathExpressionException 
	{
		//ask the reader to get the step with the given URI
		Step resultStep = this.reader.getStepByPosition(aPosition);
		
		//return the gotten step 
		return resultStep;
	}

	/**
	 * Used to get an HashMao containing all the Steps of the configuration with their position 
	 * as key 
	 * @return the HashMap containing all the Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, Step> getSteps() throws XPathExpressionException 
	{
		//ask the reader to get the steps of the configuration
		HashMap<Integer, Step> resultSteps = this.reader.getSteps();
		
		//return the gotten steps 
		return resultSteps;
	}

	public void writeStep(Step step) {
		// TODO Auto-generated method stub

	}

}
