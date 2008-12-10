package org.un.bungeni.translators.utility.schemavalidator;


import javax.xml.transform.stream.StreamSource;

/**
 * This is the interface for the Schema Validator object.
 * It is used to perform a validation of a document through a schema
 */
public interface SchemaValidatorInterface 
{
	/**
	 * This method validate a document through a schema
	 * @param aDocumentSource the source of the document to validate
	 * @param aSchemaPath the path of the schema that must be used for the validation 
	 * @return true if the document is valid
	 */
	public boolean validate(StreamSource aDocumentSource, String aSchemaPath);
	
}
