package org.un.bungeni.translators.odttoakn.configurations;

import java.util.HashMap;

import javax.xml.xpath.XPathExpressionException;
import org.un.bungeni.translators.odttoakn.steps.MapStep;
import org.un.bungeni.translators.odttoakn.steps.XSLTStep;
import org.un.bungeni.translators.odttoakn.steps.ReplaceStep;

/**
 * This is the interface for the configuration reader. A configuration reader has a singleton
 * pattern and is used to read a specific configuration 
 */
public interface ConfigurationReaderInterface 
{	
	/**
	 * Used to get an HashMap containing all the INPUT XSLT Steps of the configuration with their position 
	 * as key. The input step are applied to the document before the resolution of its names according to the map 
	 * @return the HashMap containing all the Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,XSLTStep> getInputSteps() throws XPathExpressionException;

	/**
	 * Used to get an HashMap containing all the OUTPUT XSLT Steps of the configuration with their position 
	 * as key. The output step are applied to the document after the resolution of its names according to the map 
	 * @return the HashMap containing all the Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,XSLTStep> getOutputSteps() throws XPathExpressionException;

	/**
	 * Used to get an HashMap containing all the ReplaceStep of the configuration  
	 * @return the HashMap containing all the ReplaceSteps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,ReplaceStep> getReplaceSteps() throws XPathExpressionException;
	
	/**
	 * Return an HashMap containing all the step of the map indexed by their id 
	 * @return the HashMap containing all the step of the map indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapSteps() throws XPathExpressionException;
	
	/**
	 * Returns a String containing the path of the map resolver 
	 * @return a String containing the path of the map resolver 
	 * @throws XPathExpressionException
	 */
	public String getMapResolver() throws XPathExpressionException;
}
