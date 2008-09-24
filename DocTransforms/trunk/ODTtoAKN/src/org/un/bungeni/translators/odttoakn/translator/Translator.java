package org.un.bungeni.translators.odttoakn.translator;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.configurations.Configuration;
import org.un.bungeni.translators.odttoakn.map.Map;
import org.un.bungeni.translators.odttoakn.steps.ConfigStep;
import org.un.bungeni.translators.odttoakn.steps.MapStep;
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
		
		//while the Iterator has steps aplly the transformation
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
		
		//get the map for this configuration 
		Map configurationMap = configuration.getConfigurationMap();
		
		//get the map resolver from the map 
		String mapResolverPath = configurationMap.getMapResolver();
		
		//create the stream source of the XSLT resolver
		StreamSource mapResolverStream = new StreamSource(new File(mapResolverPath));

		//get the map steps from the map 
		HashMap<Integer,MapStep> mapSteps = configurationMap.getMapSteps();
		
		//create an iterator on the hash map
		Iterator<MapStep> mapStepsIterator = mapSteps.values().iterator();
		
		//while the Iterator has steps aplly the transformation
		while(mapStepsIterator.hasNext())
		{
			//get the next step
			MapStep nextMapStep = (MapStep)mapStepsIterator.next();
			
			//the hash map that will contains the parametes
			HashMap<String,Object> paramMap = new HashMap<String,Object>();
			
			//get the map step info and fill them into the params map  
			paramMap.put("type", (String)nextMapStep.getType());
			paramMap.put("name", (String)nextMapStep.getName());
			paramMap.put("bungeniSectionType", (String)nextMapStep.getBungeniSectionType());
			paramMap.put("result", (String)nextMapStep.getResult());
			paramMap.put("attributes", (String)nextMapStep.getAttributes());
				
			//start the transformation
			iteratedDocument = XSLTTransformer.getInstance().transformWithParam(iteratedDocument, mapResolverStream,paramMap);
		}
		//return the Source of the new document
	    return iteratedDocument;
	}

}
