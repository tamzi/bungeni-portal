package org.un.bungeni.translators.akntohtml.translator;

import java.io.File;
import java.io.IOException;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.stream.StreamSource;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.akntohtml.configurations.AHConfiguration;
import org.un.bungeni.translators.dom.DOMUtility;
import org.un.bungeni.translators.streams.StreamSourceUtility;
import org.un.bungeni.translators.xpathresolver.XPathResolver;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

/**
 * This is the AKN->HTML translator object. 
 * It defines the translate method that is used to translate a AKN document into HTML
 */
public class AHTranslator implements AHTranslatorInterface 
{

	/* The instance of this Translator*/
	private static AHTranslator instance = null;
	
	/**
	 * Private constructor used to create the Translator instance
	 */
	private AHTranslator()
	{
		
	}

	/**
	 * Get the current instance of the Translator 
	 * @return the translator instance
	 */
	public static AHTranslator getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			instance = new AHTranslator();
		}
		//otherwise return the instance
		return instance;
	}

	/**
	 * Translate the given document into HTML according to the given pipeline
	 * @param aDocumentPath the path of the document to translate 
	 * @param aPipelinePath the path of the pipeline to apply to the document in order to translate it into HTML
	 * @return a File containing the translated document
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws TransformerException 
	 * @throws XPathExpressionException 
	 */
	public File translate(String documentPath, String pipelinePath) throws SAXException, IOException, ParserConfigurationException, XPathExpressionException, TransformerException 
	{
		//create the new configuration
		AHConfiguration configuration = new AHConfiguration(pipelinePath, new File(documentPath));
		
		//get the HashMap that contains all the step resolver
		StreamSource result = XSLTStepsResolver.resolve(new StreamSource(new File(documentPath)),configuration);
		
		//write the stream to a File and return it
		return StreamSourceUtility.getInstance().writeToFile(result);
	}
	
	/**
	 * Create and return an XSLT builded upon the instructions of the given pipeline. 
	 * @param aPipelinePath the pipeline upon which the XSLT will be created
	 * @return a File containing the created XSLT
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws XPathExpressionException 
	 * @throws TransformerException 
	 * @throws TransformerFactoryConfigurationError 
	 */
	public File buildXSLT(String aPipelinePath) throws SAXException, IOException, ParserConfigurationException, XPathExpressionException, TransformerFactoryConfigurationError, TransformerException
	{
		//open the XSLT file into a DOM document
		Document pipeline = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(new File(aPipelinePath));
		
		//get all the <xslt> elements in the pipeline
		NodeList xsltElements = (NodeList)XPathResolver.getInstance().evaluate(pipeline, "//xslt", XPathConstants.NODESET);
		
		//for each XSLT element get the URI, retrieve the pointed XSLT and replace the content of the template into the pipeline
		for (int i = 0; i < xsltElements.getLength(); i++) 
		{
			//get the <xslt> node
			Node xsltNode = xsltElements.item(i);
			
			//get the URI attribute of the XSLT node
			String xsltURI = xsltNode.getAttributes().getNamedItem("href").getNodeValue();
			
			//get the name of the element
			String elementName = (String)XPathResolver.getInstance().evaluate(pipeline, "//xslt[@href='" + xsltURI + "']/@name", XPathConstants.STRING);
			
			//open the pointed XSLT as a DOM document
			Document XSLTDoc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(new File(xsltURI));
			
			//get the content of the template of the XSLT
			Node templateContent = (Node)XPathResolver.getInstance().evaluate(XSLTDoc, "//*:template[@match='akn:" + elementName + "']/*", XPathConstants.NODE);
			
			//remove the apply templates node
			xsltNode.getParentNode().removeChild((Node)XPathResolver.getInstance().evaluate(pipeline, "//*:template[@match='akn:" + elementName + "']/*:apply-templates",XPathConstants.NODE));
			
			//appends the node to the pipeline 
			xsltNode.getParentNode().replaceChild(pipeline.adoptNode(templateContent.cloneNode(true)), xsltNode);
		}
		
		//get the root element of the pipeline
		Node oldRoot = (Node)XPathResolver.getInstance().evaluate(pipeline, "//*:template[@match='/']/stylesheets",XPathConstants.NODE);
		
		//replace the template that process the root in the pipeline
		Node newPipelineRoot = pipeline.createElement("html");
		Node newHead = pipeline.createElement("head");
		Node newBody = pipeline.createElement("body");
		Node newApplyTemplates = pipeline.createElement("xsl:apply-templates");
		newPipelineRoot.appendChild(newHead);
		newBody.appendChild(newApplyTemplates);
		newPipelineRoot.appendChild(newBody);
		
		//oldRoot.replaceChild((Node)XPathResolver.getInstance().evaluate(pipeline, "//*:template[@match='/']/stylesheets",XPathConstants.NODE), newPipelineRoot);
		oldRoot.getParentNode().replaceChild(newPipelineRoot, oldRoot);
		
		//write the document to a File
		File resultFile = DOMUtility.getInstance().writeToFile(pipeline);
		
		//return the file
		return resultFile;
	}


}
