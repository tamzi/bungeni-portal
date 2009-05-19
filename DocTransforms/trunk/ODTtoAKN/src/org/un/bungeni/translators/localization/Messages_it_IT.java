package org.un.bungeni.translators.localization;

import java.util.ListResourceBundle;

/**
 * This class is used to set all the messages in English for Kenya
 */
public class Messages_it_IT extends ListResourceBundle {

	//The List that contains the messages for kenya
	static Object[][] contents = 
	{
	    { "MISSING_ATTRIBUTE_LEFT_TEXT",
	      "L'informazione addizionale '" },
	    { "MISSING_ATTRIBUTE_CENTER_TEXT",
	      "' è obbligatoria per l'elemento '" },
		{ "MISSING_ATTRIBUTE_RIGHT_TEXT",
		  "'" },
		{ "TRANSLATION_TO_METALEX_FAILED_TEXT",
		  "C'è stato un problema durante la traduzione del documento verso il metaformato METALEX" },
		{ "TRANSLATION_FAILED_TEXT",
		  "C'è stato un problema durante la traduzione" },
		{ "VALIDATION_FAILED_TEXT",
	      "C'è stato un problema durante la validazione del documento" },
		{ "XSLT_BUILDING_FAILED_TEXT",
		  "C'è stato un problema durante la creazione dell'XSLT a partire dalla pipeline" },
		{ "IOEXCEPTION_TEXT",
		  "Uno dei documenti non è stato trovato o non è stato prodotto correttamente" },
		{ "STARTING_WORD_TEXT_LEFT",
		  "Che inizia con le parole: "},
		{ "SECTION_TYPE_LEFT",
		  "Nella sezione di tipo: "},
		{ "SECTION_ID_LEFT",
		  "Con id: "},

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
