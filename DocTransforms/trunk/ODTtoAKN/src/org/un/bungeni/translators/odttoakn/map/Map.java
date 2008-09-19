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
	
	//the map writer
	private MapWriter writer;
	
	/**
	 * Create a new map based on a given map XML file
	 * @param aMapXML the XML Document in witch the map is written 
	 */
	public Map(Document aMapXML)
	{
		//create the writer
		this.writer = new MapWriter(aMapXML);
		
		//create the reader
		this.reader = new MapReader(aMapXML);
	}
	/**
	 * Get the Step of the map with the given id
	 * @param anId the id of the step that you want to retrieve  
	 * @return the step with the given ID
	 * @throws XPathExpressionException 
	 */
	public MapStep getMapStepById(Integer anId) throws XPathExpressionException
	{
		//ask the reader to get the map step with the given id
		MapStep resultStep = this.reader.getMapStepById(anId);
		
		//return the gotten step 
		return resultStep;
	}
	/**
	 * Get the Steps of the map with the given type
	 * @param aType the type of the steps that you want to retrieve 
	 * @return an hash map containing all  the step with the given type indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,MapStep> getMapStepsByType(String aType) throws XPathExpressionException
	{
		//ask the reader to get the map step with the given type
		HashMap<Integer,MapStep> resultStep = this.reader.getMapStepsByType(aType);
		
		//return the gotten step 
		return resultStep;
	}
	/**
	 * Get the Step of the map with the given name
	 * @param aName the id of the steps that you want to retrieve 
	 * @return an hash map containing all  the step with the given name indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,MapStep> getMapStepsByName(String aName) throws XPathExpressionException
	{
		//ask the reader to get the map step with the given name
		HashMap<Integer,MapStep> resultStep = this.reader.getMapStepsByName(aName);
		
		//return the gotten step 
		return resultStep;
	}
	/**
	 * Get the Step of the map with the given bungeniSectionType
	 * @param aBungeniSectionType the bungeniSectionType of the steps that you want to retrieve 
	 * @return an hash map containing all  the step with the given bungeniSectionType indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,MapStep> getMapStepsByBungeniSectionType(String aBungeniSectionType) throws XPathExpressionException
	{
		//ask the reader to get the map step with the given bungeniSectionType
		HashMap<Integer,MapStep> resultStep = this.reader.getMapStepsByBungeniSectionType(aBungeniSectionType);
		
		//return the gotten step 
		return resultStep;
	}
	/**
	 * Get the Step of the map with the given result
	 * @param aResult the id of the steps that you want to retrieve 
	 * @return an hash map containing all  the step with the given result indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer,MapStep> getMapStepsByResult(String aResult) throws XPathExpressionException
	{
		//ask the reader to get the map step with the given result
		HashMap<Integer,MapStep> resultStep = this.reader.getMapStepsByResult(aResult);
		
		//return the gotten step 
		return resultStep;
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

	/**
	 * Get the location (the path) of the resolver for this map  
	 * @return the location (the path) of the resolver for this map
	 * @throws XPathExpressionException 
	 */
	public String getMapResolver() throws XPathExpressionException
	{
		//ask the reader to get all location of the resolver
		String resolverLocation = this.reader.getMapResolver();
		
		//return the gotten location of the resolver
		return resolverLocation;
	}
	
	/**
	 * Add a step to the map file 
	 * @param aMapStep the map step that you want to add to the configuration object
	*/
	public void writeMapStep(MapStep aStep)
	{
		System.out.println(this.writer.toString());
	}

}
