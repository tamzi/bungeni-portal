package org.un.bungeni.translators.odttoakn.configurations;

import java.io.IOException;
import java.util.HashMap;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.map.Map;
import org.un.bungeni.translators.odttoakn.steps.ConfigStep;
import org.un.bungeni.translators.xpathresolver.XPathResolver;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

/**
 * This is the reader of the configuration.
 * It supplies several methods to retrieve the Steps of a configuration 
 */
public class ConfigurationReader implements ConfigurationReaderInterface 
{
	//the XML that contains the configurations
	private Document configXML; 
	
	//this is the map object for this configuration reader 
	private Map configMap;
	
	/**
	 * Create a new Configuration reader object builded on the given Config XML file 
	 * @param aConfigXML the XML file that contains the configuration 
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws XPathExpressionException 
	 */
	public ConfigurationReader(Document aConfigXML) throws XPathExpressionException, SAXException, IOException, ParserConfigurationException
	{
		//save the config XML
		this.configXML = aConfigXML;
		
		//create the map object 
		this.configMap = this.createMap();
	}
	
	/**
	 * Get the step of the configuration with the given name
	 * @param aName the name of the step that you want to retreive
	 * @return a Step with the given name
	 * @throws XPathExpressionException if the XPath is not well formed 
	 */
	public ConfigStep getStepByName(String aName) throws XPathExpressionException
	{
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the step with the given name in this configuration
		Node stepNode = (Node)xresolver.evaluate(this.configXML, "//xslt[@name='" + aName + "]", XPathConstants.NODE);
		
		//create the Step 
		ConfigStep resultStep = new ConfigStep( stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  			stepNode.getAttributes().getNamedItem("href").getNodeValue(),
						  			Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()));
		//return the created Step
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
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the step with the given uri in this configuration
		Node stepNode = (Node)xresolver.evaluate(this.configXML, "//xslt[@href='" + aURI + "]", XPathConstants.NODE);
		
		//create the Step 
		ConfigStep resultStep = new ConfigStep( stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  			stepNode.getAttributes().getNamedItem("href").getNodeValue(),
						  			Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()));
		//return the created Step
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
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the step with the given nama in this configuration
		Node stepNode = (Node)xresolver.evaluate(this.configXML, "//xslt[@step='" + aPosition.toString() + "]", XPathConstants.NODE);
		
		//create the Step 
		ConfigStep resultStep = new ConfigStep( stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  			stepNode.getAttributes().getNamedItem("href").getNodeValue(),
						  			Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()));
		//return the created Step
		return resultStep;
	}
	
	/**
	 * Used to get an HashMao containing all the Steps of the configuration with their position 
	 * as key 
	 * @return the HashMap containing all the Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,ConfigStep> getSteps() throws XPathExpressionException
	{
		//the HashMap to return 
		HashMap<Integer,ConfigStep> resultMap = new HashMap<Integer,ConfigStep>();
		
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the step with the given nama in this configuration
		NodeList stepNodes = (NodeList)xresolver.evaluate(this.configXML, "//xslt", XPathConstants.NODESET);
		
		//get all the steps and creates a Step object for each one of them
		for (int i = 0; i < stepNodes.getLength(); i++) 
		{
			//get the step node
			Node stepNode = stepNodes.item(i);
			
			//create the Step 
			ConfigStep resultStep = new ConfigStep( stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  				stepNode.getAttributes().getNamedItem("href").getNodeValue(),
						  				Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()));
			
			//add the node to the hash map set its key as its position (step attribute)
			resultMap.put(Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()),resultStep);		
		}
		
		//return the hash map containing all the Steps
		return resultMap;
	}
	
	/**
	 * Returns the Map object related to this Configuration object
	 * @return the map object related to this configuration object
	 */
	public Map getConfigurationMap()
	{
		//copy the configMap object
		Map aConfigMap = this.configMap;
		//return the configMap object
		return aConfigMap;
	}
	
	/**
	 * Private method that creates the Map object builded on the map referred in this configuration
	 * @return the map object contained in this configuration
	 * @throws XPathExpressionException 
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 */
	private Map createMap() throws XPathExpressionException, SAXException, IOException, ParserConfigurationException
	{
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the step with the given nama in this configuration
		String mapLocation = (String)xresolver.evaluate(this.configXML, "//map/@href", XPathConstants.STRING);
		
		//create the map DOM 
		Document mapDoc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(mapLocation);
		
		//create the Map Object builded on the mapDoc
		Map resultMap = new Map(mapDoc);
		
		//returns the map object
		return resultMap;
	}
}
