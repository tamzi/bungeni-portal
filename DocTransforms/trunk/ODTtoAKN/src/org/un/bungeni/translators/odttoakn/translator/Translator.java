package org.un.bungeni.translators.odttoakn.translator;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringWriter;
import java.util.HashMap;
import java.util.Iterator;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.configurations.Configuration;
import org.un.bungeni.translators.odttoakn.map.Map;
import org.un.bungeni.translators.odttoakn.steps.ConfigStep;
import org.un.bungeni.translators.odttoakn.steps.MapStep;
import org.un.bungeni.translators.odttoakn.steps.ReplaceStep;
import org.un.bungeni.translators.xslttransformer.XSLTTransformer;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;
import javax.xml.transform.*;
import javax.xml.transform.stream.StreamResult;
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
	public File translate(String aDocumentPath, String aConfigurationPath) throws SAXException, IOException, ParserConfigurationException, XPathExpressionException, TransformerException
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
		
		//while the Iterator has steps apply the transformation
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
		
		//get the replacement step from the configuration
		HashMap<Integer,ReplaceStep> replaceSteps = configuration.getReplaceSteps();
		
		//create an iterator on the hash map
		Iterator<ReplaceStep> replaceIterator = replaceSteps.values().iterator();

		/*first reading of the document*/
		//get the Document String
		String iteratedStringDocument = new String();
		
		//create an instance of TransformerFactory
		TransformerFactory transFact = TransformerFactory.newInstance();
	 
	    //create a new transformer
	    Transformer trans = transFact.newTransformer();
	    
	    //create the writer for the transformation
	    StringWriter resultString = new StringWriter();
	    
	    //perform the transformation
	    trans.transform(iteratedDocument, new StreamResult(resultString));

	    //copy the obtained string into the string to iterate
	    iteratedStringDocument = resultString.toString();
	    /*end of the first reading of the file into a string*/

		//while the Iterator has replacement steps apply the replacement
		while(replaceIterator.hasNext())
		{
			//get the next step
			ReplaceStep nextStep = (ReplaceStep)replaceIterator.next();

			//get the pattern of the replace
			String pattern = nextStep.getPattern();
			
			//get the replacement of the step 
			String replacement = nextStep.getReplacement();
			
			//apply the replacement
			iteratedStringDocument = iteratedStringDocument.replaceAll(pattern, replacement);
		}

	    //create a file for the result  
		File resultFile = File.createTempFile("result", ".xml");
		
		//delete the temp file on exit
		resultFile.deleteOnExit();
		
		//write the result on the temporary file
		BufferedWriter out = new BufferedWriter(new FileWriter(resultFile));
	    out.write(iteratedStringDocument);
	    out.close();
	        
		//return the Source of the new document
	    return resultFile;
	}

}
