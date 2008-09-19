package org.un.bungeni.translators.odttoakn.configurations;
import java.util.HashMap;

import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.map.Map;
import org.un.bungeni.translators.odttoakn.steps.ConfigStep;

/**
 * This is the interface for the configuration object of the ODTtoAKN translator. A configuration
 * stores all the steps needed to perform a specific translation.
 */
public interface ConfigurationInterface 
{
	/**
	 * Get the step of the configuration with the given name
	 * @param aName the name of the step that you want to retreive
	 * @return a Step with the given name
	 * @throws XPathExpressionException 
	 */
	public ConfigStep getStepByName(String aName) throws XPathExpressionException;

	/**
	 * Get the step of the configuration with the given href
	 * @param aURI the href of the step that you want to retreive
	 * @return a Step with the given href
	 * @throws XPathExpressionException 
	 */
	public ConfigStep getStepByHref(String aURI) throws XPathExpressionException;

	/**
	 * Get the step of the configuration with the given position
	 * @param aPosition the position of the step that you want to retreive
	 * @return a Step with the given position
	 * @throws XPathExpressionException 
	 */
	public ConfigStep getStepByPosition(Integer aPosition) throws XPathExpressionException;
	
	/**
	 * Used to get an HashMao containing all the Steps of the configuration with their position 
	 * as key 
	 * @return the HashMap containing all the Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,ConfigStep> getSteps() throws XPathExpressionException;
		
	/**
	 * Returns the Map object related to this Configuration object
	 * @return the map object related to this configuration object
	 */
	public Map getConfigurationMap();

	/**
	 * Add a step to the configuration file 
	 * @param aStep the step that you want to add to the configuration object
	*/
	public void writeStep(ConfigStep aStep);
}
