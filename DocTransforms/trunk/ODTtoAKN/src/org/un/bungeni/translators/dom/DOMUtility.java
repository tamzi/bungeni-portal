package org.un.bungeni.translators.dom;

import org.w3c.dom.Document;

/**
 * This class supplies several method useful for the management of the DOM documents
 *
 */
public class DOMUtility 
{
	/* The instance of this DOMUtility object*/
	private static DOMUtility instance = null;
	

	/**
	 * Private constructor used to create the DOMUtility instance
	 */
	private DOMUtility()
	{
		
	}
	
	/**
	 * Get the current instance of the DOMUtility class 
	 * @return the Utility instance
	 */
	public static DOMUtility getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			instance = new DOMUtility();
		}
		//otherwise return the instance
		return instance;
	}
	
	public String DOMToString(Document aDOMDocument)
	{
		return null;
	}

}
