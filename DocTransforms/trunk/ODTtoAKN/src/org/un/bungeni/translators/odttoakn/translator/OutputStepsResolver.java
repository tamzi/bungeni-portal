package org.un.bungeni.translators.odttoakn.translator;

import java.io.File;
import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.Iterator;

import javax.xml.transform.TransformerException;
import javax.xml.transform.stream.StreamSource;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.configurations.Configuration;
import org.un.bungeni.translators.odttoakn.steps.XSLTStep;
import org.un.bungeni.translators.xslttransformer.XSLTTransformer;

/**
 * Used to resolve the XSLT OUTPUT STEPS of a configuration file
*/
public final class OutputStepsResolver 
{
	/**
	 * Return the StreamSource obtained after all the OUTPUT XSLT steps of the given 
	 * configuration Document are applied to the given Stream source of the document
	 * @param aDocument a Stream Source of an ODF DOM document
	 * @param aConfiguration the configuration file that contains the XSLT STEPS
	 * @return a new StreamSource Obtained applying all the steps of the configuration to the 
	 * 			given StreamSource
	 * @throws XPathExpressionException 
	 * @throws TransformerException 
	 * @throws UnsupportedEncodingException 
	 */
	protected static StreamSource resolve(StreamSource anODFDocument, Configuration aConfiguration) throws XPathExpressionException, TransformerException, UnsupportedEncodingException
	{
		//get the steps from the configuration 
		HashMap<Integer,XSLTStep> stepsMap = aConfiguration.getOutputSteps();
		
		//create an iterator on the hash map
		Iterator<XSLTStep> mapIterator = stepsMap.values().iterator();
		
		//copy the document to translate
		StreamSource iteratedDocument = anODFDocument;
		
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
