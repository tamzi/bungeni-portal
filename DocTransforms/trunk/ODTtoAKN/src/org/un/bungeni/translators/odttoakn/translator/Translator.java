package org.un.bungeni.translators.odttoakn.translator;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.configurations.Configuration;
import org.un.bungeni.translators.odttoakn.steps.ConfigStep;
import org.un.bungeni.translators.xslttransformer.XSLTTransformer;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;
import javax.xml.transform.*;
import javax.xml.transform.stream.StreamSource;

public class Translator implements TranslatorInterface
{
	
	/* The instance of this Translator*/
	private static Translator instance = null;
	
	/**
	 * Private constructor used to create the Translator instance
	 */
	private Translator()
	{
		
	}
	
	/**
	 * Get the current instance of the Translator 
	 * @return the translator instance
	 */
	public static Translator getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			instance = new Translator();
		}
		//otherwise return the instance
		return instance;
	}

	/**
	 * Transforms the document at the given path using the configuration at the given path 
	 * @param aDocumentPath the path of the document to translate
	 * @param aConfigurationPath the path of the configuration to use for the translation 
	 * @return the translated document
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws XPathExpressionException 
	 * @throws TransformerException 
	 */
	public StreamSource translate(String aDocumentPath, String aConfigurationPath) throws SAXException, IOException, ParserConfigurationException, XPathExpressionException, TransformerException
	{
		//get the File of the configuration 
		Document configurationDoc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(aConfigurationPath);
		
		//create the configuration 
		Configuration configuration = new Configuration(configurationDoc);
		
		//get the steps from the configuration 
		HashMap<Integer,ConfigStep> stepsMap = configuration.getSteps();
		
		//create an iterator on the hash map
		Iterator<ConfigStep> mapIterator = stepsMap.values().iterator();
		
		//get the Document Stream
		StreamSource iteratedDocument = new StreamSource(new File(aDocumentPath));
		
		//while the Iterator has steps ally the transformation
		while(mapIterator.hasNext())
		{
			//get the next step
			ConfigStep nextStep = (ConfigStep)mapIterator.next();
			
			//get the href from the step 
			String stepHref = nextStep.getHref();
			
			//create a stream source by the href of the XSLT
			StreamSource xsltStream = new StreamSource(new File(stepHref));
			
			//start the transformation
			iteratedDocument = XSLTTransformer.getInstance().transform(iteratedDocument, xsltStream);
		}
			    
		//return the Source of the new document
	    return iteratedDocument;
	}

}
