package org.un.bungeni.translators.localization;

import java.util.ListResourceBundle;

/**
 * This class is used to set all the messages in English for Kenya
 */
public class Messages_en_US extends ListResourceBundle {

	//The List that contains the messages for kenya
	static Object[][] contents = 
	{
	    { "MISSING_ATTRIBUTE_LEFT_TEXT",
	      "The additional info '" },
	    { "MISSING_ATTRIBUTE_CENTER_TEXT",
	      "' is mandatory for the section '" },
		{ "MISSING_ATTRIBUTE_RIGHT_TEXT",
		  "'" },
		{ "TRANSLATION_TO_METALEX_FAILED_TEXT",
		  "There was a problem during the translation to the METALEX metaformat" },
		{ "TRANSLATION_FAILED_TEXT",
		  "There was a problem during the translation" },
		{ "VALIDATION_FAILED_TEXT",
	      "There was a problem during the validation of the document" },
		{ "XSLT_BUILDING_FAILED_TEXT",
		  "There was a problem during the building of the XSLT starting from the pipeline" },
		{ "IOEXCEPTION_TEXT",
		  "Some of the needed document was not found or was not produced correctly" },
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
