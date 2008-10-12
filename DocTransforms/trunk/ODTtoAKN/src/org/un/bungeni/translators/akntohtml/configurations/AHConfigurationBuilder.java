package org.un.bungeni.translators.akntohtml.configurations;

import java.io.IOException;
import java.util.HashMap;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.steps.XSLTStep;
import org.un.bungeni.translators.xpathresolver.XPathResolver;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class AHConfigurationBuilder 
{
	//the instance of this Configuration Builder
	private static AHConfigurationBuilder instance;
	
	//the path of the document that contains the default values
	private String defaultVauesPath = new String("resources/akntohtml/defaultvalues/default_values.xml");
	
	//the path of the document that contains the empty mini XSLT
	private String emptyMiniXSLTPath = new String("resources/akntohtml/defaultvalues/empty_mini_xslt.xsl");
	
	/**
	 * Protected constructor
	 */
	protected AHConfigurationBuilder()
	{
	}
	
	/**
	 * Get a new instance of the Configuration Builder
	 * @return the instance of the configuration builder
	*/
	public static AHConfigurationBuilder newInstance()
	{
		//if there is already an active instance return the instance 
		if(instance != null)
		{
			//return the instance
			return instance;
		}
		//if the Configuration Builder is not instanciated create a new instance 
		else
		{
			//create the instance
			instance = new AHConfigurationBuilder();
			
			//return the instance
			return instance;
		}
	}
	
	/**
	 * Create a new set of mini XSLT and the XSLT (pipeline) that manages all the transformation operations
	 * @param outputDirectory The directory in which the mini XSLT and the pipeline will be written
	 * @throws SAXException
	 * @throws IOException
	 * @throws ParserConfigurationException
	 * @throws XPathExpressionException
	 */
	public void createConfiguration(String outputDirectory) throws SAXException, IOException, ParserConfigurationException, XPathExpressionException
	{
		//get the default values container
		Document defaultValuesDocument = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(this.defaultVauesPath);
		
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get all the elements in the dafault_values XML
		NodeList elements = (NodeList)xresolver.evaluate(defaultValuesDocument, "//element", XPathConstants.NODESET);

		//for each element create a MINI XSLT
		for (int i = 0; i < elements.getLength(); i++) 
		{
			//get the element 
			Node element = elements.item(i);
			
			//open the empty XSLT 
			Document emptyMiniXSLT = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(this.emptyMiniXSLTPath);
		
			//create the new template
			Element newTemplate = emptyMiniXSLT.createElement("xsl:template");
			
			//set the match attribute
			newTemplate.setAttribute("match", element.getAttributes().getNamedItem("name").getNodeValue());
			
			//the element in which the matching pattern will be transformed to 
			Element newNode = emptyMiniXSLT.createElement(element.getAttributes().getNamedItem("name").getNodeValue());
			
		}	
		
	}
	
}
