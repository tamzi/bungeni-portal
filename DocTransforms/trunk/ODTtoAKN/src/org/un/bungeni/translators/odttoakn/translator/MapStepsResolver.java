package org.un.bungeni.translators.odttoakn.translator;

import java.io.File;
import java.util.HashMap;
import java.util.Iterator;

import javax.xml.transform.TransformerException;
import javax.xml.transform.stream.StreamSource;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.configurations.Configuration;
import org.un.bungeni.translators.odttoakn.map.Map;
import org.un.bungeni.translators.odttoakn.steps.MapStep;
import org.un.bungeni.translators.utility.xslttransformer.XSLTTransformer;

/**
 * Used to resolve the MAP STEPS of a configuration file
*/
public final class MapStepsResolver 
{
	/**
	 * Return the StreamSource obtained after all the MAP steps of the given 
	 * configuration Document are applied to the given Stream source of the document
	 * @param aMap the map file that contains the MAP STEPS
	 * @return a new StreamSource Obtained applying all the steps of the configuration to the 
	 * 			given StreamSource
	 * @throws XPathExpressionException 
	 * @throws TransformerException 
	 */
	protected static StreamSource resolve(Map aMap) throws XPathExpressionException, TransformerException
	{
		//get the map steps from the map 
		HashMap<Integer,MapStep> mapSteps = aMap.getMapSteps();
	
		//create an iterator on the hash map
		Iterator<MapStep> mapStepsIterator = mapSteps.values().iterator();
		
		//while the Iterator has steps apply the transformation
		while(mapStepsIterator.hasNext())
		{
			//get the next step
			MapStep nextMapStep = (MapStep)mapStepsIterator.next();

			//the hash map that will contains the parametes
			HashMap<String,Object> paramMap = new HashMap<String,Object>();
			
			//get the map step info and fill them into the params map  
			paramMap.put("id", (Integer)nextMapStep.getId());
			paramMap.put("bungeniSectionType", (String)nextMapStep.getBungeniSectionType());
			paramMap.put("result", (String)nextMapStep.getResult());
		}
		
		//return the transformed document
		return null;
	}
}
