package org.un.bungeni.translators.akntohtml.configurations;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.steps.XSLTStep;
import org.xml.sax.SAXException;


/**
 * This Object is a AKN->HTML configuration. It is used to create a new configuration for the translation to HTML based on a
 * pipeline.xsl file
 *
 */
public class AHConfiguration 
{
	//the pipeline document
	private AHConfigurationReader reader;
	
	//the document that will be translated by this configuration
	private File documentToTranslate;
	
	/**
	 * Create a new AHConfiguration file based on the given pipeline and the given document (the document to translate)
	 * @param aPipelinePath the path of the pipeline for that will be applied to transform the document 
	 * @param aDocument the Document to translate
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 */
	public AHConfiguration(String aPipelinePath, File aDocument) throws SAXException, IOException, ParserConfigurationException
	{
		//create the new configuration reader
		this.reader = new AHConfigurationReader(aPipelinePath);
		
		//save the document to translate
		this.documentToTranslate = aDocument;
	}
	
	/**
	 * @return Return the hash map that contains all the steps to translate the document of this configuration
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws TransformerException 
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,XSLTStep> getXSLTSteps() throws XPathExpressionException, TransformerException, SAXException, IOException, ParserConfigurationException
	{
		//get the HashMap of this configuration
		return this.reader.getStepsForDocumentTranslation(this.documentToTranslate);
	}
}
