package org.un.bungeni.translators.utility.exceptionmanager;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.InvalidPropertiesFormatException;
import java.util.Properties;
import java.util.ResourceBundle;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.log4j.Logger;
import org.apache.xerces.parsers.DOMParser;
import org.un.bungeni.translators.globalconfigurations.GlobalConfigurations;
import org.un.bungeni.translators.utility.odf.ODFUtility;
import org.w3c.dom.Node;
import org.xml.sax.Attributes;
import org.xml.sax.ErrorHandler;
import org.xml.sax.Locator;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;
import org.xml.sax.helpers.DefaultHandler;

/**
 * This object parse a SAXEception understand what type of exception is and throws an 
 * user readable error
 */
public class LocationHandler extends DefaultHandler 
{
	Locator locator; 
		
	/* The instance of this FileUtility object*/
	private static LocationHandler instance = null;
		
	/* The resource bundle for the messages */
	private ResourceBundle resourceBundle;
	
	/* This is the DOM parser that will contain the references to the elements in witch errors occur*/
	public DOMParser parser;
	
	/* This is the string that will contain the path to the original ODF document*/
	public String ODFDocument;
	
	/* This is the ODF string that contains all the section names and infos of the original document */
	public String ODFSectionString; 
	
	/**
	 * Private constructor used to create the ExceptionManager instance
	 * @throws IOException 
	 * @throws InvalidPropertiesFormatException 
	*/
	private LocationHandler() throws InvalidPropertiesFormatException, IOException 
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
	public static LocationHandler getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			try 
			{
				instance = new LocationHandler();
			} 
			catch (Exception e) 
			{
				e.printStackTrace();
			} 
		}
		//otherwise return the instance
		return instance;
	}
	
	public void setDocumentLocator(Locator aLocator)
	{
		this.locator = aLocator;
	}
	
	//for testing we allow only 'clause'
	//ideally we should be trapping saxexception and doing the source
	//location stuff there
	public void startElement(String uri, String localName, String qName, Attributes at) throws SAXException 
	{
		try
		{
			System.out.println(qName);
			//for every other element raise an exception and identify
			//the source of the error
			//do mapping staff between AN xml error and ODF error
	        String location = "";
	        // if (locator != null) 
	        // {
	        	location = locator.getSystemId(); //name of xml doc
	            location += " line " + locator.getLineNumber();
	            location += ", column " + locator.getColumnNumber();
	            location += ": ";
	            
	            System.out.println(location);
	        // }
	        //throw new SAXException(location + "Illegal element");
	     }
		catch(Exception e)
		{
			e.printStackTrace();
		}
	}



	/**
     * Report a non-fatal error
     * @param ex the error condition
     */
    public void error(SAXParseException ex)  
    {
    	//the message of the exception
		String exceptionMessage = ex.getMessage();
		
		System.err.println("At line " + ex.getLineNumber()  + " of " + ex.getSystemId() + ':');
		System.err.println(exceptionMessage);
	        
		//check what type of text the exception launch
		if(exceptionMessage.matches("(.*)Attribute '(.*)' must appear on element '(.*)'.")) 
		{
			/*//compile the regex
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
            //System.err.println(message);
            
            try
            {
            	//this will store the section id
            	String sectionId = "";
            	
            	//this will store the section name
            	String sectionName = ""; 
            	
            	//this is the message that shows the id the name and the starting words of the found problem
            	String messageId = resourceBundle.getString("VALIDATION_FAILED_TEXT") + "\n";
            	
            	//get the current visited node
                Node node =	(Node)this.parser.getProperty("http://apache.org/xml/properties/dom/current-element-node");
                
                //get the name of the node
                sectionName = node.getLocalName();
                
                if (node.getAttributes().getNamedItem("id") != null)
                {
                	 //get the section id 
                	 sectionId = node.getAttributes().getNamedItem("id").getNodeValue();
                	 //System.err.println(node.getAttributes().getNamedItem("id").getNodeValue());
                	 //System.err.println("Starting with the words: " + getStartingWords(node.getAttributes().getNamedItem("id").getNodeValue()));
                }
                if (node.getAttributes().getNamedItem("name") != null)
                {
                	//get the section name
                	sectionName = node.getAttributes().getNamedItem("name").getNodeValue();
               	    //System.err.println(node.getAttributes().getNamedItem("name").getNodeValue());
                }
                
                //complete the message to show 
                messageId = messageId + 
                			resourceBundle.getString("SECTION_TYPE_LEFT") +
                			sectionName +
                			"\n" +
                			resourceBundle.getString("SECTION_ID_LEFT") +
                			sectionId +
                			"\n" +
                			resourceBundle.getString("STARTING_WORD_TEXT_LEFT") +
                			getStartingWords(node.getAttributes().getNamedItem("id").getNodeValue());
    			
                //print the messages 
                System.err.println(messageId);
                System.err.println(message);
                  
            }
            catch (SAXException e)
        	{
            	//print the stack trace 
        		e.printStackTrace();
        	} */
        }
		else if (exceptionMessage.matches("(.*)The content of element '(.*)' is not complete(.*)"))
		{
			
			System.err.println("At line " + ex.getLineNumber()  + " of " + ex.getSystemId() + ':');
	        System.err.println(exceptionMessage);
	        /*Node node = null;

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
        		System.err.println("");
        			
        	}*/
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
       }
    }
    
	/**
	 * Set the path of the original ODF document
	 * @param aPathToODFDocument the path of the original ODF document
	 */
    public void setODFDocument(String aPathToODFDocument)
	{
		//set the ODFDocument for the exception manager
		this.ODFDocument = aPathToODFDocument;
		
		//Create the Section Info String 
    	this.ODFSectionString = ODFUtility.getInstance().ExtractSection(this.ODFDocument);
    
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
    
    private String getStartingWords(String anId)
    {
    	//the result that will contain the first words of the section 
    	String result = null; 
    	
    	//get the the lines of the sections string into an array
    	String[] sections = this.ODFSectionString.split("\n");
    	   	
    	//iterate all the line of the sections string
    	for (int i = 0; i < sections.length; i++)
    	{
    		//split the line at the colons 
    		String[] idAndName = sections[i].split(":");
    		
    		//check if the id of the section is equal to the given one
    		if(idAndName[0].compareTo(anId) == 0)
    		{
    			//assign the first words of the section to the result 
    			result = idAndName[1];
    		}
    	}
    	
    	return result;
    }
}
