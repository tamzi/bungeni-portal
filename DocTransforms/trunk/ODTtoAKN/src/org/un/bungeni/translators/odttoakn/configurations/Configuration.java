package org.un.bungeni.translators.odttoakn.configurations;

import java.util.HashMap;

import org.un.bungeni.translators.odttoakn.steps.Step;
import org.w3c.dom.Document;

public class Configuration implements ConfigurationInterface 
{
	//the configuration reader
	private ConfigurationReader reader;
	
	//the configuration writer
	private ConfigurationWriter writer;
	
	/**
	 * Create a new configuration based on a given Configuration XML file
	 * @param aConfigXML the XML Document in witch the configuration is written 
	 */
	public Configuration(Document aConfigXML)
	{
		//create the writer
		this.writer = new ConfigurationWriter(aConfigXML);
		
		//create the reader
		this.reader = new ConfigurationReader(aConfigXML);
	}

	public Step getStepByHref(String auri) {
		// TODO Auto-generated method stub
		return null;
	}

	public Step getStepByName(String name) {
		// TODO Auto-generated method stub
		return null;
	}

	public Step getStepByPosition(Integer position) {
		// TODO Auto-generated method stub
		return null;
	}

	public HashMap<Integer, Step> getSteps() {
		// TODO Auto-generated method stub
		return null;
	}

	public void writeStep(Step step) {
		// TODO Auto-generated method stub

	}

}
