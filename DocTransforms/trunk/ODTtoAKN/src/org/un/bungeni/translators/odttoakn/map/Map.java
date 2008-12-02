 package org.un.bungeni.translators.odttoakn.map;

import java.util.HashMap;

import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.steps.MapStep;
import org.w3c.dom.Document;

/**
 * This is the map object. It is used to read a map, write a map and to create a new map
 */
public class Map implements MapInterface
{
	//the map reader
	private MapReader reader;
		
	/**
	 * Create a new map based on a given map XML file
	 * @param aMapXML the XML Document in witch the map is written 
	 */
	public Map(Document aMapXML)
	{
		//create the reader
		this.reader = new MapReader(aMapXML);
	}
	
	/**
	 * Get an hash map containing all the steps of the xml map indexed by their id 
	 * @return an hash map containing all the steps of the xml map indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,MapStep> getMapSteps() throws XPathExpressionException
	{
		//ask the reader to get all the map steps
		HashMap<Integer,MapStep> resultStep = this.reader.getMapSteps();
		
		//return the gotten step 
		return resultStep;
	}
	
}
