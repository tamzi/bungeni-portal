package org.un.bungeni.translators.odttoakn.map;

import java.util.HashMap;

import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.steps.MapStep;

/**
 * This is the interface for the map object. 
 * A map object is used to read a map, write a map and create a new map.
 */
public interface MapInterface 
{
	/**
	 * Get an hash map containing all the steps of the xml map indexed by their id 
	 * @return an hash map containing all the steps of the xml map indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,MapStep> getMapSteps() throws XPathExpressionException;
	/**
	 * Get the location (the path) of the resolver for this map  
	 * @return the location (the path) of the resolver for this map
	 * @throws XPathExpressionException 
	 */
	public String getMapResolver() throws XPathExpressionException;

}
