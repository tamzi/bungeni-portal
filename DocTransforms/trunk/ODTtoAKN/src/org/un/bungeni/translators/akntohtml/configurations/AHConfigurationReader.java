package org.un.bungeni.translators.akntohtml.configurations;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.stream.StreamSource;

import org.un.bungeni.translators.odttoakn.steps.XSLTStep;
import org.un.bungeni.translators.xslttransformer.XSLTTransformer;
import org.xml.sax.SAXException;

/**
 * This is the pipeline reader. It is builded on a pipeline.xsl file and read the pipeline creating the XSLT path
 *
 */
public class AHConfigurationReader 
{
	//the pipeline of this configuration reader
	private StreamSource pipeline;
	
	/**
	 * Create a new AHConfigurationReader based on the given pipeline.
	 * @param aPipelinePath the path of the pipeline to apply to a document in order to translate it
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 */
	public AHConfigurationReader(String aPipelinePath) throws SAXException, IOException, ParserConfigurationException
	{
		//create a stream source by the href of the XSLT
		this.pipeline = new StreamSource(new File(aPipelinePath));
		
		System.out.println(this.pipeline.toString());
	}
	
	public HashMap<Integer,XSLTStep> getStepsForDocumentTranslation(File aDocument) throws TransformerException
	{
		
		//apply the pipeline to the document
		XSLTTransformer.getInstance().transform(new StreamSource(aDocument), this.pipeline);
		
		
		return null;
	}
	
}
