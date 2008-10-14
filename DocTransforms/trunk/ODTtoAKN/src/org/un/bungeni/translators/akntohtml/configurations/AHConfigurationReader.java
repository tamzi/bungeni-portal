package org.un.bungeni.translators.akntohtml.configurations;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.stream.StreamSource;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.steps.XSLTStep;
import org.un.bungeni.translators.streams.StreamSourceUtility;
import org.un.bungeni.translators.xpathresolver.XPathResolver;
import org.un.bungeni.translators.xslttransformer.XSLTTransformer;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

/**
 * This is the pipeline reader. It is builded on a pipeline.xsl file and read the pipeline creating the XSLT path
 *
 */
public class AHConfigurationReader 
{
	//the pipeline of this configuration reader
	private StreamSource pipeline;
	
	/**
	 * Create a new AHConfigurationReader based on the given pipeline.
	 * @param aPipelinePath the path of the pipeline to apply to a document in order to translate it
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 */
	public AHConfigurationReader(String aPipelinePath) throws SAXException, IOException, ParserConfigurationException
	{
		//create a stream source by the href of the XSLT
		this.pipeline = new StreamSource(new File(aPipelinePath));
		
		System.out.println(this.pipeline.toString());
	}
	
	/**
	 * Return the hash map containing all the XSLT steps that must be applied to the document in order to translate it
	 * @param aDocument the document to translate 
	 * @return the hash map containing all the XSLT steps that must be allied to the document in order to translate it
	 * @throws TransformerException
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,XSLTStep> getStepsForDocumentTranslation(File aDocument) throws TransformerException, SAXException, IOException, ParserConfigurationException, XPathExpressionException
	{
		
		//the HashMap to return 
		HashMap<Integer,XSLTStep> resultMap = new HashMap<Integer,XSLTStep>();

		//apply the pipeline to the document
		StreamSource xsltStepsContainer = XSLTTransformer.getInstance().transform(new StreamSource(aDocument), this.pipeline);
		
		//write the StreamSource of the XSLTStepsContainer to a DOM Document
		Document xsltStepsContainerDOM = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(StreamSourceUtility.getInstance().writeToFile(xsltStepsContainer));
		
		//get the steps 
		NodeList XSLTSteps = (NodeList) XPathResolver.getInstance().evaluate(xsltStepsContainerDOM, "//xslt", XPathConstants.NODESET);
		
		//get all the steps and creates a Step object for each one of them
		for (int i = 0; i < XSLTSteps.getLength(); i++) 
		{
			//get the step node
			Node stepNode = XSLTSteps.item(i);
			
			//create the Step 
			XSLTStep resultStep = new XSLTStep( stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  						stepNode.getAttributes().getNamedItem("href").getNodeValue(),
						  						Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()));
			
			//add the node to the hash map set its key as its position (step attribute)
			resultMap.put(Integer.parseInt(stepNode.getAttributes().getNamedItem("step").getNodeValue()),resultStep);		
		}		
		
		//return the HASHMAP containing the step 
		return resultMap;
	}
	
}
