package org.un.bungeni.translators.utility.schemavalidator;

import java.io.File;
import java.io.IOException;

import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.Validator;

import org.un.bungeni.translators.exceptions.MissingAttributeException;
import org.un.bungeni.translators.utility.exceptionmanager.ExceptionManager;
import org.xml.sax.SAXException;


/**
 * This is the interface for the Schema Validator object.
 * It is used to perform a validation of a document through a schema
 */
public class SchemaValidator implements SchemaValidatorInterface 
{

	/* The instance of this Schema Validator*/
	private static SchemaValidator instance = null;
	
	/* The schema manager of this Validator*/
	private SchemaFactory schemaFactory; 
	
	/**
	 * Private constructor used to create the Schema Validator instance
	 */
	private SchemaValidator()
	{		
	    //set the system to use saxon 
		System.setProperty("javax.xml.validation.SchemaFactory:http://www.w3.org/2001/XMLSchema","com.saxonica.jaxp.SchemaFactoryImpl");

		//create the schema factory
		this.schemaFactory = SchemaFactory.newInstance("http://www.w3.org/2001/XMLSchema");
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
	 * @throws SAXException 
	 * @throws IOException 
	 * @throws MissingAttributeException 
	 */
	public void validate(StreamSource aDocumentSource, String aSchemaPath) throws SAXException, IOException, MissingAttributeException
	{
		//create the stream source of the schema 
		StreamSource schemaSource = new StreamSource(new File(aSchemaPath));

		//create the Schema
		Schema schema = this.schemaFactory.newSchema(schemaSource);
		
		//create a validator
		Validator validator = schema.newValidator();
		
		//try to validate the document
		try
		{
			//validate the document
			validator.validate(aDocumentSource);
		}
		//if the validation fails send the exception to the exception manager
		catch(SAXException e)
		{
			//send the exception to the exception manager
			ExceptionManager.getInstance().parseException(e);
		}
	}

}
