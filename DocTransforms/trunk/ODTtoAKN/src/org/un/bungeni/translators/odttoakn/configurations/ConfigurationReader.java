package org.un.bungeni.translators.odttoakn.configurations;

import java.io.IOException;
import java.util.HashMap;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.map.Map;
import org.un.bungeni.translators.odttoakn.steps.MapStep;
import org.un.bungeni.translators.odttoakn.steps.XSLTStep;
import org.un.bungeni.translators.odttoakn.steps.ReplaceStep;
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
	 * Used to get an HashMap containing all the Steps of the configuration with their position 
	 * as key 
	 * @return the HashMap containing all the Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,XSLTStep> getInputSteps() throws XPathExpressionException
	{
		//the HashMap to return 
		HashMap<Integer,XSLTStep> resultMap = new HashMap<Integer,XSLTStep>();
		
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the step with the given nama in this configuration
		NodeList stepNodes = (NodeList)xresolver.evaluate(this.configXML, "//input/xslt", XPathConstants.NODESET);
		
		//get all the steps and creates a Step object for each one of them
		for (int i = 0; i < stepNodes.getLength(); i++) 
		{
			//get the step node
			Node stepNode = stepNodes.item(i);
			
			//create the Step 
			XSLTStep resultStep = new XSLTStep( stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  				stepNode.getAttributes().getNamedItem("href").getNodeValue(),
						  				Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()));
			
			//add the node to the hash map set its key as its position (step attribute)
			resultMap.put(Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()),resultStep);		
		}
		
		//return the hash map containing all the Steps
		return resultMap;
	}
	
	/**
	 * Used to get an HashMap containing all the OUTPUT XSLT Steps of the configuration with their position 
	 * as key. The output step are applied to the document after the resolution of its names according to the map 
	 * @return the HashMap containing all the Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,XSLTStep> getOutputSteps() throws XPathExpressionException
	{
		//the HashMap to return 
		HashMap<Integer,XSLTStep> resultMap = new HashMap<Integer,XSLTStep>();
		
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the step with the given nama in this configuration
		NodeList stepNodes = (NodeList)xresolver.evaluate(this.configXML, "//output/xslt", XPathConstants.NODESET);
		
		//get all the steps and creates a Step object for each one of them
		for (int i = 0; i < stepNodes.getLength(); i++) 
		{
			//get the step node
			Node stepNode = stepNodes.item(i);
			
			//create the Step 
			XSLTStep resultStep = new XSLTStep( stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  				stepNode.getAttributes().getNamedItem("href").getNodeValue(),
						  				Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()));
			
			//add the node to the hash map set its key as its position (step attribute)
			resultMap.put(Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()),resultStep);		
		}
		
		//return the hash map containing all the Steps
		return resultMap;
		
	}

	/**
	 * Used to get an HashMap containing all the ReplaceStep of the configuration  
	 * @return the HashMap containing all the ReplaceSteps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,ReplaceStep> getReplaceSteps() throws XPathExpressionException
	{
		//the HashMap to return 
		HashMap<Integer,ReplaceStep> resultMap = new HashMap<Integer,ReplaceStep>();
		
		//retrieve the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the step with the given name in this configuration
		NodeList stepNodes = (NodeList)xresolver.evaluate(this.configXML, "//replacement", XPathConstants.NODESET);
		
		//get all the steps and creates a Step object for each one of them
		for (int i = 0; i < stepNodes.getLength(); i++) 
		{
			//get the replace step node
			Node stepNode = stepNodes.item(i);
			
			//the result Step
			ReplaceStep resultStep;
			
			//create the replace Step 
			//if pattern attribute is not empty get the pattern from the attribute 
			if (stepNode.getAttributes().getNamedItem("pattern") != null)
			{
				resultStep = new ReplaceStep( 	stepNode.getAttributes().getNamedItem("name").getNodeValue(),
												stepNode.getAttributes().getNamedItem("replacement").getNodeValue(),
						  					  	stepNode.getAttributes().getNamedItem("pattern").getNodeValue());
			}
			//otherwise get the value from the textValue of the node
			else
			{
				resultStep = new ReplaceStep( 	stepNode.getAttributes().getNamedItem("name").getNodeValue(),
												stepNode.getAttributes().getNamedItem("replacement").getNodeValue(),
		  										stepNode.getFirstChild().getNodeValue());
			}
			
			//add the node to the hash map set its key as its position (step attribute)
			resultMap.put(Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()),resultStep);		
		}
		
		//return the hash map containing all the Steps
		return resultMap;
	}
	
	/**
	 * Return an HashMap containing all the step of the map indexed by their id 
	 * @return the HashMap containing all the step of the map indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapSteps() throws XPathExpressionException
	{
		//get the map steps from the map 
		HashMap<Integer,MapStep> mapSteps = this.configMap.getMapSteps();
		
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
		String mapLocation = this.configMap.getMapResolver();
		
		//return the location of the map resolver
		return mapLocation;
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
