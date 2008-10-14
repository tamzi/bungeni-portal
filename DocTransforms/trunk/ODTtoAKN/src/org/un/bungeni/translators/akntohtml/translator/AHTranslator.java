package org.un.bungeni.translators.akntohtml.translator;

import java.io.File;
import java.io.IOException;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.stream.StreamSource;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.akntohtml.configurations.AHConfiguration;
import org.un.bungeni.translators.streams.StreamSourceUtility;
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

}
