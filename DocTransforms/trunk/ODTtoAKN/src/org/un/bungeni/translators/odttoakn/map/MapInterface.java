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
	 * Get the Step of the map with the given id
	 * @param anId the id of the step that you want to retrieve  
	 * @return the step with the given ID
	 * @throws XPathExpressionException 
	 */
	public MapStep getMapStepById(Integer anId) throws XPathExpressionException;
	/**
	 * Get the Steps of the map with the given type
	 * @param aType the type of the steps that you want to retrieve 
	 * @return an hash map containing all  the step with the given type indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,MapStep> getMapStepsByType(String aType) throws XPathExpressionException;
	/**
	 * Get the Step of the map with the given name
	 * @param aName the id of the steps that you want to retrieve 
	 * @return an hash map containing all  the step with the given name indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,MapStep> getMapStepsByName(String aName) throws XPathExpressionException;
	/**
	 * Get the Step of the map with the given bungeniSectionType
	 * @param aBungeniSectionType the bungeniSectionType of the steps that you want to retrieve 
	 * @return an hash map containing all  the step with the given bungeniSectionType indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,MapStep> getMapStepsByBungeniSectionType(String aBungeniSectionType) throws XPathExpressionException;
	/**
	 * Get the Step of the map with the given result
	 * @param aResult the id of the steps that you want to retrieve 
	 * @return an hash map containing all  the step with the given result indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,MapStep> getMapStepsByResult(String aResult) throws XPathExpressionException;
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
	public String getMapMap() throws XPathExpressionException;

}
