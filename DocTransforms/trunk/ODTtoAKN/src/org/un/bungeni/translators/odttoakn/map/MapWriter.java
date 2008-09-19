package org.un.bungeni.translators.odttoakn.map;

import org.un.bungeni.translators.odttoakn.steps.MapStep;
import org.w3c.dom.Document;

/**
 * This is the map writer object
 * A map writer is used to write map xlm or to create a new map XML.
 */
public class MapWriter 
{
	//the XML that contains the map
	private Document mapXML; 

	/**
	 * Create a new Map Object builded on the given map XML file 
	 * @param aMapXML the XML file in witch that contains the configuration
	 */
	public MapWriter(Document aMapXML)
	{
		//save the map XML file 
		this.mapXML = aMapXML;
	}
	
	/**
	 * Add a step to the map file 
	 * @param aMapStep the step that you want to add to the configuration object
	*/
	public void writeStep(MapStep aStep)
	{
		System.out.println(this.mapXML.toString());
	}
}
