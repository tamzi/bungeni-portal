package org.un.bungeni.translators.utility.schemavalidator;

import java.io.File;
import java.io.IOException;

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.ValidatorHandler;

import org.un.bungeni.translators.exceptions.MissingAttributeException;
import org.un.bungeni.translators.utility.exceptionmanager.ExceptionManager;
import org.un.bungeni.translators.utility.exceptionmanager.LocalContentHandler;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.XMLReader;


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
	 * @param aDocument the document to validate
	 * @param aSchemaPath the path of the schema that must be used for the validation 
	 * @throws SAXException 
	 * @throws IOException 
	 * @throws MissingAttributeException 
	 */
	public void validate(File aDocument, String aSchemaPath) throws SAXException, IOException, MissingAttributeException
	{
		try
		{
			//create the stream source of the schema 
			StreamSource schemaSource = new StreamSource(new File(aSchemaPath));
			
	        //set the exception manager of the schema factory
			this.schemaFactory.setErrorHandler(ExceptionManager.getInstance());
			
			//create the Schema
			Schema schemaGrammar = this.schemaFactory.newSchema(schemaSource);
			
			//create a validator to validate against the schema.
			ValidatorHandler schemaValidator = schemaGrammar.newValidatorHandler();
			
			//set the error handler of the schema
			schemaValidator.setErrorHandler(ExceptionManager.getInstance());
	
			//set the content handler of the schema
	        schemaValidator.setContentHandler(new LocalContentHandler(schemaValidator.getTypeInfoProvider()));
	
	        //create a new sax parser factory
	        SAXParserFactory parserFactory = SAXParserFactory.newInstance();
	        parserFactory.setNamespaceAware(true);
	
	        //create a new sax parser
	        SAXParser parser = parserFactory.newSAXParser();
	
	        //create a  new XML Reader
	        XMLReader reader = parser.getXMLReader();
	        reader.setContentHandler(schemaValidator);
	        reader.parse(new InputSource(aDocument.toURI().toString()));
		}
		catch (SAXException saxe) 
		{
        } 
		catch (Exception e) 
		{
            e.printStackTrace();
        }
        //create a validator
		/*Validator validator = schema.newValidator();
		
		//set the exception manager of the validator
		validator.setErrorHandler(ExceptionManager.getInstance());

		
		//try to validate the document
		try
		{
			//validate the document
			validator.validate(aDocumentSource);
		}
		//if the validation fails send the exception to the exception manager
		catch(SAXException ex)
		{

            //e.printStackTrace();
			//send the exception to the exception manager
			//ExceptionManager.getInstance().parseException(e);
		}*/
	}

}

