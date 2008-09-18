package org.un.bungeni.translators.odttoakn.translator;

import java.io.IOException;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Source;
import javax.xml.transform.TransformerException;
import javax.xml.xpath.XPathExpressionException;

import org.xml.sax.SAXException;

/**
 * This is the interface for the ODTtoAKN translator.
 * It has only a method that simply takes the path of the configuration and the path of the document to translate and translate 
 * the document. 
 */
public interface TranslatorInterface 
{
	/**
	 * Transforms the document at the given path using the configuration at the given path 
	 * @param aDocumentPath the path of the document to translate
	 * @param aConfigurationPath the path of the configuration to use for the translation 
	 * @return the translated document
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws XPathExpressionException 
	 * @throws TransformerException 
	 */
	public Source translate(String aDocumentPath, String aConfigurationPath) throws SAXException, IOException, ParserConfigurationException, XPathExpressionException, TransformerException;
}
