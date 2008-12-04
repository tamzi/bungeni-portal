package org.un.bungeni.translators.utility.odf;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.Result;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.openoffice.odf.doc.OdfDocument;
import org.un.bungeni.translators.utility.dom.DOMUtility;
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
		File returnFile = commonMergeODF (odf);
		return returnFile;
	}
	
	public File mergeODF(File aDocumentHandle ) throws TransformerFactoryConfigurationError, Exception {
		OdfDocument odf = OdfDocument.loadDocument(aDocumentHandle);
		File returnFile = commonMergeODF (odf);
		return returnFile;
	}
	
	private File commonMergeODF (OdfDocument odf)  throws TransformerFactoryConfigurationError, Exception 
	{
		
		//get the DOM of the content.xml file
		Document odfDom = odf.getContentDom();
		
		//get the content of the style.xml file
		Document odfStyle = odf.getStylesDom();
		
		//get the content of the meta.xml file
		InputStream odfMetaStream = odf.getMetaStream();
		
		//create the dom of the metadata from the stream 
		Document odfMeta = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(odfMetaStream);
	
		/**
		 * TO BE DELETED
		 */
		File metaf = DOMUtility.getInstance().writeToFile(odfMeta);
		//input stream
		FileInputStream fis  = new FileInputStream(metaf);
		
		//output stream 
		FileOutputStream fos = new FileOutputStream("resources/meta.xml");
		
		//copy the file
		try 
		{
			byte[] buf = new byte[1024];
		    int i = 0;
		    while ((i = fis.read(buf)) != -1) 
		    {
		            fos.write(buf, 0, i);
		    }
		} 
		catch (Exception e) 
		{
		}
		finally 
		{
		        if (fis != null) fis.close();
		        if (fos != null) fos.close();
		}	

		/**
		 * END TO BE DELETED
		 */
		//get all the style nodes contained in the in the style.xml file
		Node stylesNodes = odfStyle.getElementsByTagName("office:styles").item(0);

		//get all the meta nodes contained in the in the meta.xml file
		Node metaNodes = odfMeta.getElementsByTagName("office:meta").item(0);

		//appends the style nodes to the content.xml document 
		odfDom.getElementsByTagName("office:document-content").item(0).appendChild(odfDom.adoptNode(stylesNodes));	

		//appends the meta nodes to the content.xml document 
		odfDom.getElementsByTagName("office:document-content").item(0).appendChild(odfDom.adoptNode(metaNodes));	

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
