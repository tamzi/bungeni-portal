package org.un.bungeni.translators.odf;

import java.io.File;

import javax.xml.transform.Result;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.openoffice.odf.doc.OdfDocument;
import org.w3c.dom.Document;
import org.w3c.dom.Node;

/**
 * This class supplies several methods useful for the management of the ODF documents. 
 *
 */
public class ODFUtility 
{
	/* The instance of this ODFUtility object*/
	private static ODFUtility instance = null;
	

	/**
	 * Private constructor used to create the ODFUtility instance
	 */
	private ODFUtility()
	{
		
	}
	
	/**
	 * Get the current instance of the ODFUtility class 
	 * @return the Utility instance
	 */
	public static ODFUtility getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			instance = new ODFUtility();
		}
		//otherwise return the instance
		return instance;
	}

	
	/**
	 * This method returns a File that is formed merging in a single file the "content.xlm"
	 * "meta.xml" and "style.xml" files of the given ODF package
	 * @param anODFPath the path of the ODF package to merge 
	 * @return
	 * @throws TransformerFactoryConfigurationError 
	 * @throws Exception 
	 */
	public File mergeODF(String anODFPath) throws TransformerFactoryConfigurationError, Exception
	{
		//get the ODF package
		OdfDocument odf = OdfDocument.loadDocument(anODFPath);
		
	
		//get the DOM of the content.xml file
		Document odfDom = odf.getContentDom();
		
		//get the content of the style.xml file
		Document odfStyle = odf.getStylesDom();
	
		//get all the style nodes contained in the in the style.xml file
		Node prova = odfStyle.getElementsByTagName("office:styles").item(0);
		
		//appends the style nodes to the content.xml node 
		odfDom.getElementsByTagName("office:document-content").item(0).appendChild(odfDom.adoptNode(prova));	
	
		 // Prepare the DOM document for writing
        Source source = new DOMSource(odfDom);

		//create a temp file for   
		File returnFile = File.createTempFile("temp",".xml");
		
		//create the result on the temp file
		Result result = new StreamResult(returnFile);

        // get the instance of the transformer
        Transformer xformer = TransformerFactory.newInstance().newTransformer();
        
        //Write the DOM document to the file
        xformer.transform(source, result);
        
        //return the file
        return returnFile;
	}
}
