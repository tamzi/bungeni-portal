package org.un.bungeni.translators.odttoakn.configurations;

import java.io.IOException;
import java.util.HashMap;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.steps.MapStep;
import org.un.bungeni.translators.odttoakn.steps.XSLTStep;
import org.un.bungeni.translators.odttoakn.steps.ReplaceStep;
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
		
	/**
	 * Create the new configuration based on a given Configuration XML file
	 * @param aConfigXML the XML Document in witch the configuration is written 
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws XPathExpressionException 
	 */
	public Configuration(Document aConfigXML) throws XPathExpressionException, SAXException, IOException, ParserConfigurationException
	{
		
		//create the reader
		this.reader = new ConfigurationReader(aConfigXML);
	}

	/**
	 * Used to get an HashMap containing all the INPUT XSLT Steps of the configuration with their position 
	 * as key. The input step are applied to the document before the resolution of its names according to the map 
	 * @return the HashMap containing all the Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, XSLTStep> getInputSteps() throws XPathExpressionException 
	{
		//ask the reader to get the steps of the configuration
		HashMap<Integer, XSLTStep> resultSteps = this.reader.getInputSteps();
		
		//return the gotten steps 
		return resultSteps;
	}

	/**
	 * Used to get an HashMap containing all the OUTPUT XSLT Steps of the configuration with their position 
	 * as key. The output step are applied to the document after the resolution of its names according to the map 
	 * @return the HashMap containing all the Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, XSLTStep> getOutputSteps() throws XPathExpressionException 
	{
		//ask the reader to get the steps of the configuration
		HashMap<Integer, XSLTStep> resultSteps = this.reader.getOutputSteps();
		
		//return the gotten steps 
		return resultSteps;
	}

	/**
	 * Used to get an HashMap containing all the Replace Steps of the configuration with their position 
	 * as key 
	 * @return the HashMap containing all the Replace Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,ReplaceStep> getReplaceSteps() throws XPathExpressionException
	{
		//ask the reader to get the replace steps of the configuration
		HashMap<Integer, ReplaceStep> resultSteps = this.reader.getReplaceSteps();
		
		//return the gotten steps 
		return resultSteps;
	}

	/**
	 * Return an HashMap containing all the step of the map indexed by their id 
	 * @return the HashMap containing all the step of the map indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapSteps() throws XPathExpressionException
	{
		//get the map steps from the map 
		HashMap<Integer,MapStep> mapSteps = this.reader.getMapSteps();
		
		//return the MapSteps hash map
		return mapSteps;
	}
	
	/**
	 * Returns a String containing the path of the map resolver 
	 * @return a String containing the path of the map resolver 
	 * @throws XPathExpressionException
	 */
	public String getMapResolver() throws XPathExpressionException
	{
		//get the location of the map resovlver
		String mapLocation = this.reader.getMapResolver();
		
		//return the location of the map resolver
		return mapLocation;
	}

}
