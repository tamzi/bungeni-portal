package org.un.bungeni.translators.akntohtml.configurations;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;

import javax.xml.parsers.ParserConfigurationException;

import org.un.bungeni.translators.odttoakn.steps.XSLTStep;
import org.xml.sax.SAXException;


/**
 * This Object is a AKN->HTML configuration. It is used to create a new configuration for the translation to HTML based on a
 * pipeline.xsl file
 *
 */
public class AHConfiguration 
{
	//the pipeline document
	private AHConfigurationReader reader;
	
	/**
	 * Create a new AHConfiguration file based on the given pipeline and the given document (the document to translate)
	 * @param aPipelinePath the path of the pipeline for that will be applied to transform the document 
	 * @param aDocument the Document to translate
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 */
	public AHConfiguration(String aPipelinePath, File aDocument) throws SAXException, IOException, ParserConfigurationException
	{
		//create the new configuration reader
		this.reader = new AHConfigurationReader(aPipelinePath);
	}
	
	public HashMap<Integer,XSLTStep> getXSLTSteps()
	{
		System.out.println(this.reader.toString());
		return null;
	}
}
