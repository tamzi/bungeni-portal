package org.un.bungeni.translators.odttoakn.translator;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;

import javax.xml.parsers.DocumentBuilderFactory;

import org.un.bungeni.translators.odf.ODFUtility;
import org.un.bungeni.translators.odttoakn.configurations.Configuration;
import org.un.bungeni.translators.streams.StreamSourceUtility;
import org.w3c.dom.Document;

import javax.xml.transform.*;
import javax.xml.transform.stream.StreamSource;

public class Translator implements TranslatorInterface
{
	
	/* The instance of this Translator*/
	private static Translator instance = null;
	
	/**
	 * Private constructor used to create the Translator instance
	 */
	private Translator()
	{
		
	}
	
	/**
	 * Get the current instance of the Translator 
	 * @return the translator instance
	 */
	public static Translator getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			instance = new Translator();
		}
		//otherwise return the instance
		return instance;
	}

	/**
	 * Transforms the document at the given path using the configuration at the given path 
	 * @param aDocumentPath the path of the document to translate
	 * @param aConfigurationPath the path of the configuration to use for the translation 
	 * @return the translated document
	 * @throws Exception 
	 * @throws TransformerFactoryConfigurationError 
	 */
	public File translate(String aDocumentPath, String aConfigurationPath) throws TransformerFactoryConfigurationError, Exception 
	{
		//get the File of the configuration 
		Document configurationDoc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(aConfigurationPath);
		
		//create the configuration 
		Configuration configuration = new Configuration(configurationDoc);

		//get the document stream obtained after the merge of all the ODF XML contained in the given ODF pack
		//StreamSource iteratedDocument = new StreamSource(ODFUtility.getInstance().mergeODF(aDocumentPath));
		StreamSource ODFDocument = new StreamSource(ODFUtility.getInstance().mergeODF(aDocumentPath));

		//applies the input steps to the StreamSource of the ODF document
		StreamSource iteratedDocument = InputStepsResolver.resolve(ODFDocument, configuration);

		//applies the map steps to the StreamSource of the ODF document
		iteratedDocument = MapStepsResolver.resolve(iteratedDocument, configuration);

		//applies the map steps to the StreamSource of the ODF document
		String iteratedStringDocument = ReplaceStepsResolver.resolve(iteratedDocument, configuration);

	    //create a file for the result  
		File tempFile = File.createTempFile("temp", ".xml");
		
		//delete the temp file on exit
		tempFile.deleteOnExit();

		//write the result on the temporary file
		BufferedWriter out = new BufferedWriter(new FileWriter(tempFile));
	    out.write(iteratedStringDocument);
	    out.close();
		
		//create a new StremSource
		StreamSource tempStreamSource = new StreamSource(tempFile);

		//apply the OUTPUT XSLT to the StreamSource
		StreamSource resultStream = OutputStepsResolver.resolve(tempStreamSource, configuration);
		
		//write the result stream to a string
		String resultDocumentString = StreamSourceUtility.getInstance().writeToString(resultStream);
		
	    //create a file for the result  
		File resultFile = File.createTempFile("result", ".xml");
		
		//delete the temp file on exit
		resultFile.deleteOnExit();

		//write the result on the temporary file
		BufferedWriter outresult = new BufferedWriter(new FileWriter(resultFile));
	    outresult.write(resultDocumentString);
	    outresult.close();
		
		
	    //return the Source of the new document
	    return resultFile;
	}

}
