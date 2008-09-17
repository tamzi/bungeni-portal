package org.un.bungeni.translators.odttoakn.configurations;

import java.util.HashMap;

import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.steps.Step;
import org.un.bungeni.translators.xpathresolver.XPathResolver;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

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
	 * @throws XPathExpressionException if the XPath is not well formed 
	 */
	public Step getStepByName(String aName) throws XPathExpressionException
	{
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the step with the given name in this configuration
		Node stepNode = (Node)xresolver.evaluate(this.configXML, "//xslt[@name='" + aName + "]", XPathConstants.NODE);
		
		//create the Step 
		Step resultStep = new Step( stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  			stepNode.getAttributes().getNamedItem("href").getNodeValue(),
						  			Integer.getInteger(stepNode.getAttributes().getNamedItem("step").getNodeValue()));
		//return the created Step
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
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the step with the given uri in this configuration
		Node stepNode = (Node)xresolver.evaluate(this.configXML, "//xslt[@href='" + aURI + "]", XPathConstants.NODE);
		
		//create the Step 
		Step resultStep = new Step( stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  			stepNode.getAttributes().getNamedItem("href").getNodeValue(),
						  			Integer.getInteger(stepNode.getAttributes().getNamedItem("step").getNodeValue()));
		//return the created Step
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
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the step with the given nama in this configuration
		Node stepNode = (Node)xresolver.evaluate(this.configXML, "//xslt[@step='" + aPosition.toString() + "]", XPathConstants.NODE);
		
		//create the Step 
		Step resultStep = new Step( stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  			stepNode.getAttributes().getNamedItem("href").getNodeValue(),
						  			Integer.getInteger(stepNode.getAttributes().getNamedItem("step").getNodeValue()));
		//return the created Step
		return resultStep;
	}
	
	/**
	 * Used to get an HashMao containing all the Steps of the configuration with their position 
	 * as key 
	 * @return the HashMap containing all the Steps of the configuration
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,Step> getSteps() throws XPathExpressionException
	{
		//the HashMap to return 
		HashMap<Integer,Step> resultMap = new HashMap<Integer,Step>();
		
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
			Step resultStep = new Step( stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  				stepNode.getAttributes().getNamedItem("href").getNodeValue(),
						  				Integer.getInteger(stepNode.getAttributes().getNamedItem("step").getNodeValue()));
			
			//add the node to the hash map set its key as its position (step attribute)
			resultMap.put(Integer.getInteger(stepNode.getAttributes().getNamedItem("step").getNodeValue()),resultStep);		
		}
		
		//return the hash map containing all the Steps
		return resultMap;
	}

}
