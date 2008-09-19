package tests;
import java.io.IOException;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.xpath.XPathExpressionException;

import org.un.bungeni.translators.odttoakn.translator.Translator;
import org.xml.sax.SAXException;


public class test {

	/**
	 * @param args
	 * @throws TransformerException 
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws XPathExpressionException 
	 */
	public static void main(String[] args) throws XPathExpressionException, SAXException, IOException, ParserConfigurationException, TransformerException 
	{
		Translator trans = Translator.getInstance();
		trans.translate("resources/content.xml", "resources/configurations/debaterecord/common/DebateRecordCommonConfig.xml");
		System.out.println("great!");
	}

}
