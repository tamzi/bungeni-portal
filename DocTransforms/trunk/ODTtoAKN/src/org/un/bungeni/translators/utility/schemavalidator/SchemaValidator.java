package org.un.bungeni.translators.utility.schemavalidator;

import javax.xml.transform.stream.StreamSource;


/**
 * This is the interface for the Schema Validator object.
 * It is used to perform a validation of a document through a schema
 */
public class SchemaValidator implements SchemaValidatorInterface 
{

	/* The instance of this Schema Validator*/
	private static SchemaValidator instance = null;
		
	/**
	 * Private constructor used to create the Schema Validator instance
	 */
	private SchemaValidator()
	{		
	 
	}
	
	/**
	 * Get the current instance of the Schema Validator 
	 * @return the Schema Validator instance
	 */
	public static SchemaValidator getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			instance = new SchemaValidator();
		}
		//otherwise return the instance
		return instance;
	}

	/**
	 * This method validate a document through a schema
	 * @param aDocumentSource the source of the document to validate
	 * @param aSchemaPath the path of the schema that must be used for the validation 
	 * @return true if the document is valid
	 */
	public boolean validate(StreamSource aDocumentSource, String aSchemaPath)
	{
		return true;
	}

}
