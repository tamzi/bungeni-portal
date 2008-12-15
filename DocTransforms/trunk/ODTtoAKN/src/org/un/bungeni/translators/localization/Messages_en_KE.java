package org.un.bungeni.translators.localization;

import java.util.ListResourceBundle;

/**
 * This class is used to set all the messages in English for Kenya
 */
public class Messages_en_KE extends ListResourceBundle {

	//The List that contains the messages for kenya
	static Object[][] contents = 
	{
	    { "HELLO_TEXT",
	      "Hello, world!" },
	    { "GOODBYE_TEXT",
	      "Goodbye everyone!" },
	};
	
	
	/**
	 * Return the list of the messages
	 * @Override
	 */
	protected Object[][] getContents() 
	{
		//return the list of the messages
		return contents;
	}

}
