package org.un.bungeni.translators.odttoakn.configurations;

import org.un.bungeni.translator.odttoakn.steps.Step;

/**
* This is the interface for the configuration reader. A configuration reader has a singleton
* pattern and is used to write the properties of a specific configuration 
*/
public interface ConfigurationWriterInterface 
{
	/**
	 * Add a step to the configuration file 
	 * @param aStep the step that you want to add to the configuration object
	*/
	public void writeStep(Step aStep);
}
