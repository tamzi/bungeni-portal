package org.un.bungeni.translators.utility.schemavalidator;

import java.util.ResourceBundle;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.xerces.parsers.DOMParser;
import org.w3c.dom.Node;
import org.xml.sax.ErrorHandler;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;
import org.xml.sax.helpers.DefaultHandler;

public class ValidatorErrorHandler implements ErrorHandler 
{
    public String elementName = "";
    public String elementId = "";

	
	/* This is the DOM parser that will contain the references to the elements in witch errors occur*/
	public DOMParser parser;

	public ValidatorErrorHandler() 
    {
		//create the resource bundle
		this.resourceBundle = ResourceBundle.getBundle(properties.getProperty("resourceBundlePath"));		
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
