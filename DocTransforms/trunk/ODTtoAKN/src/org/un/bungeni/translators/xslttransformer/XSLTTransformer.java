package org.un.bungeni.translators.xslttransformer;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.io.StringWriter;
import javax.xml.transform.TransformerException;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;


/**
 * This is the  XSLT transformer object.
 * It is used to perform an XSLT transformation on a Document
 */
public class XSLTTransformer implements XSLTTransformerInterface 
{

	/* The instance of this XSLTTransformer*/
	private static XSLTTransformer instance = null;
	

	/**
	 * Private constructor used to create the XSLTTransformer instance
	 */
	private XSLTTransformer()
	{
		
	}
	
	/**
	 * Get the current instance of the XSLTTransformer resolver 
	 * @return the XSLTTransformer instance
	 */
	public static XSLTTransformer getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			instance = new XSLTTransformer();
		}
		//otherwise return the instance
		return instance;
	}

	/**
	 * This method applies the given XSLT to the given Document and returns the Document obtained after the transformation
	 * @param aDocumentSource the stream source of the document to transform
	 * @param anXSLTSource the stream source of the XSLT to apply to the document that you want to transform
	 * @return the new StreamSource of the Document resulting applying the given XSLT to the given Document
	 * @throws TransformerException 
	 */
	public StreamSource transform(StreamSource aDocumentSource, StreamSource anXSLTSource) throws TransformerException
	{
		//set the compilator to use SAXON
		System.setProperty("javax.xml.transform.TransformerFactory","net.sf.saxon.TransformerFactoryImpl");
		
	   // create an instance of TransformerFactory
	    TransformerFactory transFact = TransformerFactory.newInstance();
	 
	    //create a new transformer
	    Transformer trans = transFact.newTransformer(anXSLTSource);
	    
	    //create the writer for the transformation
	    StringWriter resultString = new StringWriter();
	    
	    //perform the transformation
	    trans.transform(aDocumentSource, new StreamResult(resultString));
	    
	    //returns the obtained file
	    return new StreamSource(((InputStream)new ByteArrayInputStream(resultString.toString().getBytes())));
	}
}
