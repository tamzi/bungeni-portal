package org.un.bungeni.translators.odttoakn.translator;

import java.io.File;

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
		//get the document stream obtained after the merge of all the ODF XML contained in the given ODF pack
		StreamSource ODFDocument = new StreamSource(ODFUtility.getInstance().mergeODF(aDocumentPath));

		File resultFile = commonTranslate(ODFDocument, aConfigurationPath);
		
		//return the Source of the new document
	    return resultFile;
	}

	/**
	 * Transforms the document at the given path using the configuration at the given path 
	 * @param aDocumentPath the path of the document to translate
	 * @param aConfigurationPath the path of the configuration to use for the translation 
	 * @return the translated document
	 * @throws Exception 
	 * @throws TransformerFactoryConfigurationError 
	 */
	public File translate(File aDocumentHandle, String aConfigurationPath) throws TransformerFactoryConfigurationError, Exception 
	{
		//get the document stream obtained after the merge of all the ODF XML contained in the given ODF pack
		StreamSource ODFDocument = new StreamSource(ODFUtility.getInstance().mergeODF(aDocumentHandle));

	    File resultFile = commonTranslate(ODFDocument, aConfigurationPath);
		//return the Source of the new document
	    return resultFile;
	}


	private File commonTranslate(StreamSource ODFDocument, String aConfigurationPath) throws TransformerFactoryConfigurationError, Exception {
		//get the File of the configuration 
		Document configurationDoc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(aConfigurationPath);
		
		//create the configuration 
		Configuration configuration = new Configuration(configurationDoc);

		//applies the input steps to the StreamSource of the ODF document
		StreamSource iteratedDocument = InputStepsResolver.resolve(ODFDocument, configuration);

		//applies the map steps to the StreamSource of the ODF document
		iteratedDocument = MapStepsResolver.resolve(iteratedDocument, configuration);

		//applies the map steps to the StreamSource of the ODF document
		iteratedDocument = ReplaceStepsResolver.resolve(iteratedDocument, configuration);

		//apply the OUTPUT XSLT to the StreamSource
		StreamSource resultStream = OutputStepsResolver.resolve(iteratedDocument, configuration);
		
		//write the source to a File
		File resultFile = StreamSourceUtility.getInstance().writeToFile(resultStream);
		
		//return the Source of the new document
	    return resultFile;	
	}
}
