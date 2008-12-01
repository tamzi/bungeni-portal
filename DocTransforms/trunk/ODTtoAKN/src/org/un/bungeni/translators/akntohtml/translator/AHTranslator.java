	package org.un.bungeni.translators.akntohtml.translator;

import java.io.File;
import java.io.IOException;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.stream.StreamSource;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.utility.dom.DOMUtility;
import org.un.bungeni.translators.utility.streams.StreamSourceUtility;
import org.un.bungeni.translators.utility.xslttransformer.XSLTTransformer;
import org.w3c.dom.Document;
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
	 * @throws TransformerException 
	 * @throws TransformerFactoryConfigurationError 
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws XPathExpressionException 
	 */
	public File translate(String documentPath, String pipelinePath) throws XPathExpressionException, SAXException, IOException, ParserConfigurationException, TransformerFactoryConfigurationError, TransformerException
	{
		//build the XSLT from the pipeline
		File xslt = this.buildXSLT(pipelinePath);
		
		//apply the XSLT to the document 
		StreamSource result = XSLTTransformer.getInstance().transform(new StreamSource(new File(documentPath)), new StreamSource(xslt));
		
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
	public File buildXSLT(String aPipelinePath) throws XPathExpressionException, SAXException, IOException, ParserConfigurationException, TransformerFactoryConfigurationError, TransformerException
	{
		//create the XSLT document starting from the pipeline
		Document pipeline = PipelineResolver.resolve(aPipelinePath);
				
		//write the document to a File
		File resultFile = DOMUtility.getInstance().writeToFile(pipeline);
		
		//return the file
		return resultFile;
	}
}
