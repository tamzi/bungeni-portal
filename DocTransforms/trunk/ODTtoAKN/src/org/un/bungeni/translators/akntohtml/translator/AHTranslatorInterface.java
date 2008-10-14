package org.un.bungeni.translators.akntohtml.translator;

import java.io.File;
import java.io.IOException;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.xpath.XPathExpressionException;

import org.xml.sax.SAXException;

/**
 * This is the interface for the AKN->HTML translator object. 
 * It defines the translate method that is used to translate a AKN document into HTML
 */
public interface AHTranslatorInterface 
{
	/**
	 * Translate the given document into HTML according to the given pipeline
	 * @param aDocumentPath the path of the document to translate 
	 * @param aPipelinePath the path of the pipeline to apply to the document in order to translate it into HTML
	 * @return a File containing the translated document
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws TransformerException 
	 * @throws XPathExpressionException 
	 */
	public File translate(String aDocumentPath, String aPipelinePath) throws SAXException, IOException, ParserConfigurationException, XPathExpressionException, TransformerException;
}
