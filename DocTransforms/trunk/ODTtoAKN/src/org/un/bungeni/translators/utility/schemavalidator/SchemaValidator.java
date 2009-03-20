package org.un.bungeni.translators.utility.schemavalidator;

import java.io.File;
import java.io.IOException;
import javax.xml.parsers.ParserConfigurationException;
import org.apache.xerces.parsers.DOMParser;
import org.un.bungeni.translators.exceptions.MissingAttributeException;
import org.un.bungeni.translators.utility.exceptionmanager.ExceptionManager;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;


/**
 * This is the interface for the Schema Validator object.
 * It is used to perform a validation of a document through a schema
 */
public class SchemaValidator implements SchemaValidatorInterface 
{

	/* The instance of this Schema Validator*/
	private static SchemaValidator instance = null;
	
	//the counter of the error founded in a document
	private int errorCount = 0;

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
     * Get the error count
     * @return the number of errors reported, that is, the number of calls on error() or fatalError()
     */
	public int getErrorCount() 
	{
		//return the number of the errors 
        return errorCount;
	}

	/**
	 * This method validate a document through a schema
	 * @param aDocument the document to validate
	 * @param aSchemaPath the path of the schema that must be used for the validation 
	 * @throws SAXException 
	 * @throws IOException 
	 * @throws MissingAttributeException 
	 */
	public void validate(File aDocument, String aSchemaPath) throws SAXException, IOException, ParserConfigurationException
	{
		try
		{
			 //create a dom parser
			 DOMParser domParser = new DOMParser();
			 
			 //set the features of the parser that specifies that the document must be validated 
			 domParser.setFeature("http://xml.org/sax/features/validation",true);
			 domParser.setFeature("http://apache.org/xml/features/validation/schema",true);
			 domParser.setFeature("http://apache.org/xml/features/dom/defer-node-expansion",false);
		     domParser.setFeature("http://apache.org/xml/features/validation/schema-full-checking",true);
			 domParser.setFeature("http://apache.org/xml/features/honour-all-schemaLocations", true);
			 domParser.setProperty("http://apache.org/xml/properties/schema/external-schemaLocation","http://www.akomantoso.org/1.0 " + new File(aSchemaPath).toURI().toURL().toExternalForm());
			
			 //get the exception manager and set the dom parser as parser
			 ExceptionManager.getInstance().setDOMParser(domParser);
			 
			 //set the error handler of the parser to the ExceptionManager
			 domParser.setErrorHandler(ExceptionManager.getInstance()); 
			 
			 //parse the document and validate it
			 domParser.parse(new InputSource(aDocument.toURI().toString()));
			 
		}
		catch (SAXException saxe) 
	    {
			exit(1, "Error: " + saxe.getMessage());
	    } 
		catch (Exception e) 
		{
			e.printStackTrace();
	        exit(2, "Fatal Error: " + e);
		}

	}
	
	private static void exit(int errCode, String msg) 
	{
		System.err.println(msg);
		System.exit(errCode);
	}
}

