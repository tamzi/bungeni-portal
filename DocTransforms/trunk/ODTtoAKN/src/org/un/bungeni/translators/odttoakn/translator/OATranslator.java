package org.un.bungeni.translators.odttoakn.translator;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.InvalidPropertiesFormatException;
import java.util.Properties;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.un.bungeni.translators.globalconfigurations.GlobalConfigurations;
import org.un.bungeni.translators.odttoakn.configurations.OAConfiguration;
import org.un.bungeni.translators.utility.dom.DOMUtility;
import org.un.bungeni.translators.utility.odf.ODFUtility;
import org.un.bungeni.translators.utility.schemavalidator.SchemaValidator;
import org.un.bungeni.translators.utility.streams.StreamSourceUtility;
import org.un.bungeni.translators.utility.xslttransformer.XSLTTransformer;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;

import javax.xml.transform.*;
import javax.xml.transform.stream.StreamSource;
import javax.xml.xpath.XPathExpressionException;

public class OATranslator implements org.un.bungeni.translators.interfaces.Translator
{
	
	/* The instance of this Translator*/
	private static OATranslator instance = null;
	
	/* The configuration for the metalex translation*/
	private String metalexConfigPath;
	
	/* The path of the AKOMA NTOSO schema*/
	private String akomantosoAddNamespaceXSLTPath;

	/* The path of the AKOMA NTOSO schema*/
	private String akomantosoSchemaPath;

	/**
	 * Private constructor used to create the Translator instance
	 * @throws IOException 
	 * @throws InvalidPropertiesFormatException 
	 */
	private OATranslator() throws InvalidPropertiesFormatException, IOException
	{
		//create the Properties object
		Properties properties = new Properties();
	
		//read the properties file
		InputStream propertiesInputStream = new FileInputStream(GlobalConfigurations.getApplicationPathPrefix() + "configfiles/odttoakn/TranslatorConfig.xml");
	
		//load the properties
		properties.loadFromXML(propertiesInputStream);
		
		//get the metalex configuration path
		this.metalexConfigPath = properties.getProperty("metalexConfigPath");

		//get the path of the AKOMA NTOSO schema
		this.akomantosoSchemaPath = properties.getProperty("akomantosoSchemaPath");
		
		//get the path of the XSLT that add the namespace to AKOMA NTOSO produced files
		this.akomantosoAddNamespaceXSLTPath = properties.getProperty("akomantosoAddNamespaceXSLTPath");
	}

	/**
	 * Get the current instance of the Translator 
	 * @return the translator instance
	 */
	public static OATranslator getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			try 
			{
				instance = new OATranslator();
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
	 * Transforms the document at the given path using the pipeline at the given path 
	 * @param aDocumentPath the path of the document to translate
	 * @param aPipelinePath the path of the pipeline to use for the translation 
	 * @return the translated document
	 * @throws Exception 
	 * @throws TransformerFactoryConfigurationError 
	 */
	public File translate(String aDocumentPath, String aPipelinePath) throws TransformerFactoryConfigurationError, Exception 
	{
		//get the document stream obtained after the merge of all the ODF XML contained in the given ODF pack
		StreamSource ODFDocument = new StreamSource(ODFUtility.getInstance().mergeODF(aDocumentPath));

		//translate the document to METALEX
		File metalexFile = translateToMetalex(ODFDocument, this.metalexConfigPath);
		
		//create the XSLT that transforms the metalex
		File xslt = this.buildXSLT(aPipelinePath);
		
		//apply the XSLT to the document 
		StreamSource result = XSLTTransformer.getInstance().transform(new StreamSource(metalexFile), new StreamSource(xslt));
		
		//apply to the result the XSLT that insert the namespace
		StreamSource resultWithNamespace = XSLTTransformer.getInstance().transform(result, new StreamSource(new File(this.akomantosoAddNamespaceXSLTPath)));

		//create the file that will be returned in case the validation do not fail
		File fileToReturn = StreamSourceUtility.getInstance().writeToFile(resultWithNamespace);
		
		//validate the produced document
		//SchemaValidator.getInstance().validate(new StreamSource(fileToReturn), this.akomantosoSchemaPath);
		
		//write the stream to a File and return it
		return fileToReturn;
	}

	/**
	 * Transforms the document at the given path using the pipeline at the given path 
	 * @param aDocumentPath the path of the document to translate
	 * @param aPipelinePath the path of the pipeline to use for the translation 
	 * @return the translated document
	 * @throws Exception 
	 * @throws TransformerFactoryConfigurationError 
	 */
	public File translate(File aDocumentHandle, String aPipelinePath) throws TransformerFactoryConfigurationError, Exception 
	{
		//get the document stream obtained after the merge of all the ODF XML contained in the given ODF pack
		StreamSource ODFDocument = new StreamSource(ODFUtility.getInstance().mergeODF(aDocumentHandle));

		//translate the document to METALEX
	    File metalexFile = translateToMetalex(ODFDocument, this.metalexConfigPath);
		
		//create the XSLT that transforms the metalex
		File xslt = this.buildXSLT(aPipelinePath);
		
		//apply the XSLT to the document 
		StreamSource result = XSLTTransformer.getInstance().transform(new StreamSource(metalexFile), new StreamSource(xslt));
		
		//apply to the result the XSLT that insert the namespace
		StreamSource resultWithNamespace = XSLTTransformer.getInstance().transform(result, new StreamSource(new File(this.akomantosoAddNamespaceXSLTPath)));
		
		//create the file that will be returned in case the validation do not fail
		File fileToReturn = StreamSourceUtility.getInstance().writeToFile(resultWithNamespace);
		
		//validate the produced document
		SchemaValidator.getInstance().validate(new StreamSource(fileToReturn), this.akomantosoSchemaPath);
		
		//write the stream to a File and return it
		return fileToReturn;
	}

	/**
	 * Translate an ODF stream source to the METALEX format
	 * @param ODFDocument the ODFStreamSource to translate
	 * @param aConfigurationPath the path of the configuration file used for the translation
	 * @return a File containing the document into the METALEX format
	 * @throws TransformerFactoryConfigurationError
	 * @throws Exception
	 */
	public File translateToMetalex(StreamSource ODFDocument, String aConfigurationPath) throws TransformerFactoryConfigurationError, Exception 
	{
		//get the File of the configuration 
		Document configurationDoc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(aConfigurationPath);
		
		//create the configuration 
		OAConfiguration configuration = new OAConfiguration(configurationDoc);

		//applies the input steps to the StreamSource of the ODF document
		StreamSource iteratedDocument = OAInputStepsResolver.resolve(ODFDocument, configuration);

		//applies the map steps to the StreamSource of the ODF document
		iteratedDocument = OAReplaceStepsResolver.resolve(iteratedDocument, configuration);

		//apply the OUTPUT XSLT to the StreamSource
		StreamSource resultStream = OAOutputStepsResolver.resolve(iteratedDocument, configuration);
		
		//write the source to a File
		File resultFile = StreamSourceUtility.getInstance().writeToFile(resultStream);
		
		/***
		 * TO BE DELETED
		 */
		//input stream
		FileInputStream fis  = new FileInputStream(resultFile);
		
		//output stream 
		FileOutputStream fos = new FileOutputStream("resources/result_bill.xml");
		
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
		
		//return the Source of the new document
	    return resultFile;	
	}
	
	/**
	 * Create and return an XSLT builded upon the instructions of the given pipeline. 
	 * @param aPipelinePath the pipeline upon which the XSLT will be created
	 * @return a File containing the created XSLT
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws XPathExpressionException 
	 * @throws TransformerException 
	 * @throws TransformerFactoryConfigurationError 
	 */
	public File buildXSLT(String aPipelinePath) throws XPathExpressionException, SAXException, IOException, ParserConfigurationException, TransformerFactoryConfigurationError, TransformerException
	{
		//create the XSLT document starting from the pipeline
		Document pipeline = OAPipelineResolver.getInstance().resolve(aPipelinePath);
				
		//write the document to a File
		File resultFile = DOMUtility.getInstance().writeToFile(pipeline);
		
		//return the file
		return resultFile;
	}
	
}
