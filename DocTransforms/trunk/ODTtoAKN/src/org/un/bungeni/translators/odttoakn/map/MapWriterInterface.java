package org.un.bungeni.translators.odttoakn.map;

import org.un.bungeni.translators.odttoakn.steps.MapStep;

/**
 * This is the interface for the map writer object
 * A map writer is used to configure a new map xlm.
 */
public interface MapWriterInterface 
{
	/**
	 * Add a step to the map file 
	 * @param aMapStep the step that you want to add to the configuration object
	*/
	public void writeStep(MapStep aStep);
}
