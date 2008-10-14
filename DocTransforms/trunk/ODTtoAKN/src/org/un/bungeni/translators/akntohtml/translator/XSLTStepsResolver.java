package org.un.bungeni.translators.akntohtml.translator;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.stream.StreamSource;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.akntohtml.configurations.AHConfiguration;
import org.un.bungeni.translators.odttoakn.steps.XSLTStep;
import org.un.bungeni.translators.xslttransformer.XSLTTransformer;
import org.xml.sax.SAXException;

public final class XSLTStepsResolver 
{
	/**
	 * Returns a stream source obtained after all the XSLT steps of the AHConfiguration are applied to the document 
	 * to translate
	 * @param AHConfigurartion the AHconfiguration that must be resolved
	 * @return a new StreamSource Obtained applying all the steps of the configuration to the 
	 * 			given StreamSource
	 * @throws XPathExpressionException 
	 * @throws TransformerException 
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 */
	protected static StreamSource resolve(StreamSource fileToTranslate, AHConfiguration aConfiguration) throws XPathExpressionException, TransformerException, SAXException, IOException, ParserConfigurationException
	{
		//get the HashMap of all the steps of the document
		HashMap<Integer, XSLTStep> XSLTSteps = aConfiguration.getXSLTSteps();
		
		//create an iterator on the hash map
		Iterator<XSLTStep> mapIterator = XSLTSteps.values().iterator();
		
		//copy the document to translate
		StreamSource iteratedDocument = fileToTranslate;	
		
		//while the Iterator has steps apply the transformation
		while(mapIterator.hasNext())
		{
			//get the next step
			XSLTStep nextStep = (XSLTStep)mapIterator.next();
			
			//get the href from the step 
			String stepHref = nextStep.getHref();
			
			//create a stream source by the href of the XSLT
			StreamSource xsltStream = new StreamSource(new File(stepHref));
			
			//start the transformation
			iteratedDocument = XSLTTransformer.getInstance().transform(iteratedDocument, xsltStream);
		}
		
		//return the StreamSource of the transformed document
		return iteratedDocument;
	}

}
