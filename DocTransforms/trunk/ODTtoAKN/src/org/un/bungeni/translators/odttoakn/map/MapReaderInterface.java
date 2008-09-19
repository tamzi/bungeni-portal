package org.un.bungeni.translators.odttoakn.map;

import java.util.HashMap;

import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.steps.MapStep;

/**
 *  This is the interface for the map reader Object.
 *  A map reader object is used to read a map xml.
 */
public interface MapReaderInterface 
{
	/**
	 * Return the step having the given id
	 * @param anId the id of the step that you want to retrieve 
	 * @return the Step having the given id
	 * @throws XPathExpressionException 
	 */
	public MapStep getMapStepById(Integer anId) throws XPathExpressionException;
	/**
	 * Return the HashMp containing all the step of the the map having the given type
	 * @param aType the type of the steps that you want to retrieve 
	 * @return the HashMap containing all the step of the map having the given type indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapStepsByType(String aType) throws XPathExpressionException;
	/**
	 * Returns all the steps having the given name
	 * @param aName the name of the steps that you want to retrieve  
	 * @return the HashMap containing all the Steps of the map having the given name indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapStepsByName(String aName) throws XPathExpressionException;
	/**
	 * Returns all the steps having the given bungeniSectionType
	 * @param aBungeniSectionType the bungeniSectionType of the Steps of the Map that you want to retrieve
	 * @return the HashMap containing all the steps of the map having the given bungeniSectionType indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapStepsByBungeniSectionType(String aBungeniSectionType) throws XPathExpressionException;
	/**
	 * Returns all the steps having the given result
	 * @param aResult the result of the Steps of the map that you want to retrieve 
	 * @return an HashMap containing all the steps of the map having the given result indexed by their id 
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapStepsByResult(String aResult) throws XPathExpressionException;	
	
	/**
	 * Return an HashMap containing all the step of the map indexed by their id 
	 * @return the HashMap containing all the step of the map indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapSteps() throws XPathExpressionException;
	
	/**
	 * Returns a String containing the path of the map resolver 
	 * @return a String containing the path of the map resolver 
	 * @throws XPathExpressionException
	 */
	public String getMapResolver() throws XPathExpressionException;

}
