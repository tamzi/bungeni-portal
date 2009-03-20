package org.un.bungeni.translators.utility.exceptionmanager;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.InvalidPropertiesFormatException;
import java.util.Properties;
import java.util.ResourceBundle;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.xml.validation.Validator;
import javax.xml.validation.ValidatorHandler;

import org.apache.xerces.impl.Constants;
import org.apache.xerces.parsers.DOMParser;
import org.un.bungeni.translators.globalconfigurations.GlobalConfigurations;
import org.w3c.dom.Node;
import org.xml.sax.ErrorHandler;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;

/**
 * This object parse a SAXEception understand what type of exception is and throws an 
 * user readable error
 */
public class ExceptionManager implements ErrorHandler
{
	/* The instance of this FileUtility object*/
	private static ExceptionManager instance = null;
		
	/* The resource bundle for the messages */
	private ResourceBundle resourceBundle;
	
	/* This is the DOM parser that will contain the references to the elements in witch errors occur*/
	public DOMParser parser;
	
	/**
	 * Private constructor used to create the ExceptionManager instance
	 * @throws IOException 
	 * @throws InvalidPropertiesFormatException 
	*/
	private ExceptionManager() throws InvalidPropertiesFormatException, IOException 
	{
		//create the Properties object
		Properties properties = new Properties();
		
		//read the properties file
		InputStream propertiesInputStream = new FileInputStream(GlobalConfigurations.getApplicationPathPrefix() + GlobalConfigurations.getConfigurationFilePath());
			
		//load the properties
		properties.loadFromXML(propertiesInputStream);
		
		//create the resource bundle
		this.resourceBundle = ResourceBundle.getBundle(properties.getProperty("resourceBundlePath"));		
	}
		
	/**
	 * Get the current instance of the ExceptionManager class 
	 * @return the ExceptionManager instance
	*/
	public static ExceptionManager getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			try 
			{
				instance = new ExceptionManager();
			} 
			catch (Exception e) 
			{
				e.printStackTrace();
			} 
		}
		//otherwise return the instance
		return instance;
	}
	
	
    /**
     * Report a non-fatal error
     * @param ex the error condition
     */
    public void error(SAXParseException ex)  
    {
    	//the message of the exception
		String exceptionMessage = ex.getMessage();
		
		//check what type of text the exception launch
		if(exceptionMessage.matches("(.*)Attribute '(.*)' must appear on element '(.*)'.")) 
		{
			//compile the regex
			Pattern p = Pattern.compile("(.*)Attribute '(.*)' must appear on element '(.*)'");
        	//set the input
			Matcher m = p.matcher(exceptionMessage);
        	//the attribute name
			String attribute = ""; 
			//the elemet name
			String element = ""; 
        	while (m.find())
        	{
        	    //get the attribute name
        		attribute = m.group(2).toString();
        		//get element name
        	    element = m.group(3).toString();
        	}
        	//create the text of the exception
    		String message = resourceBundle.getString("MISSING_ATTRIBUTE_LEFT_TEXT") +
	  		                 attribute +
	  		                 resourceBundle.getString("MISSING_ATTRIBUTE_CENTER_TEXT") +
	  		                 element +
	  		                 resourceBundle.getString("MISSING_ATTRIBUTE_RIGHT_TEXT");
        	
            System.err.println("At line " + ex.getLineNumber()  + " of " + ex.getSystemId() + ':');
            System.err.println(message);
            
         	       // System.exit(0);
		}
		else
		{
			
			System.err.println("At line " + ex.getLineNumber()  + " of " + ex.getSystemId() + ':');
	        System.err.println(exceptionMessage);
	        Node node = null;

    		try {
    			
    			System.err.println(parser.getProperty("http://apache.org/xml/properties/dom/current-element-node"));
    	        // System.err.println(this.validator.getProperty("http://apache.org/xml/properties/dom/current-element-node"));
    			// System.err.println(this.validator.getFeature("http://apache.org/xml/features/dom/defer-node-expansion"));
     		    node =	(Node)this.parser.getProperty("http://apache.org/xml/properties/dom/current-element-node");
    		}
        	catch (SAXException e)
        	{
        		e.printStackTrace();
        	}
        	if (node != null)
    		{
    			System.err.println("node = " + node.getNodeName() + " id=" );
    		}
        	else
        	{
        		System.err.println("cazzo");
        			
        	}
   //ex.printStackTrace();
	    }
    }

    /**
     * Report a fatal error
     * @param ex the error condition
     */

    public void fatalError(SAXParseException ex) 
    {
		//the message of the exception
		String exceptionMessage = ex.getMessage();
		
		//check what type of text the exception launch
		if(exceptionMessage.matches("(.*)Attribute '(.*)' must appear on element '(.*)'.")) 
		{
			//compile the regex
			Pattern p = Pattern.compile("(.*)Attribute '(.*)' must appear on element '(.*)'");
        	//set the input
			Matcher m = p.matcher(exceptionMessage);
        	//the attribute name
			String attribute = ""; 
			//the elemet name
			String element = ""; 
        	while (m.find())
        	{
        	    //get the attribute name
        		attribute = m.group(2).toString();
        		//get element name
        	    element = m.group(3).toString();
        	}
        	//create the text of the exception
    		String message = resourceBundle.getString("MISSING_ATTRIBUTE_LEFT_TEXT") +
	  		                 attribute +
	  		                 resourceBundle.getString("MISSING_ATTRIBUTE_CENTER_TEXT") +
	  		                 element +
	  		                 resourceBundle.getString("MISSING_ATTRIBUTE_RIGHT_TEXT");
        	
            System.err.println("At line " + ex.getLineNumber()  + " of " + ex.getSystemId() + ':');
            System.err.println(message);
            //System.exit(0);
    	}
    }

    /**
     * Report a warning
     * @param ex the warning condition
     */
    public void warning(org.xml.sax.SAXParseException ex) 
    {
		//the message of the exception
		String exceptionMessage = ex.getMessage();
		
		//check what type of text the exception launch
		if(exceptionMessage.matches("(.*)Attribute '(.*)' must appear on element '(.*)'.")) 
		{
			//compile the regex
			Pattern p = Pattern.compile("(.*)Attribute '(.*)' must appear on element '(.*)'");
        	//set the input
			Matcher m = p.matcher(exceptionMessage);
        	//the attribute name
			String attribute = ""; 
			//the elemet name
			String element = ""; 
        	while (m.find())
        	{
        	    //get the attribute name
        		attribute = m.group(2).toString();
        		//get element name
        	    element = m.group(3).toString();
        	}
        	//create the text of the exception
    		String message = resourceBundle.getString("MISSING_ATTRIBUTE_LEFT_TEXT") +
	  		                 attribute +
	  		                 resourceBundle.getString("MISSING_ATTRIBUTE_CENTER_TEXT") +
	  		                 element +
	  		                 resourceBundle.getString("MISSING_ATTRIBUTE_RIGHT_TEXT");
        	
            System.err.println("At line " + ex.getLineNumber()  + " of " + ex.getSystemId() + ':');
            System.err.println(message);
            //System.exit(0);
           
    	}
    }
    
    /**
     * This element is used to set the DOMParser of this object
     * @param aDOMParser the DOMParser to set for this object
     */
    public void setDOMParser(DOMParser aDOMParser)
    {
    	//set the DOM parser of the object to the given one
    	this.parser = aDOMParser;
    }
}
