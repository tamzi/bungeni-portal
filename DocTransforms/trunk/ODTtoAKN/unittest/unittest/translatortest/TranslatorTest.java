/**
 * 
 */
package unittest.translatortest;

import static org.junit.Assert.*;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.StringWriter;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;
import javax.xml.xpath.XPathExpressionException;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.un.bungeni.translators.odttoakn.translator.Translator;
import org.xml.sax.SAXException;


/**
 * @author lucacervone
 *
 */
public class TranslatorTest 
{
	private Translator myTranslator;
	/**
	 * @throws java.lang.Exception
	 */
	@Before
	public void setUp() throws Exception 
	{
		//get the instance of the translator
		myTranslator = Translator.getInstance();
	}

	/**
	 * @throws java.lang.Exception
	 */
	@After
	public void tearDown() throws Exception {
	}

	/**
	 * Test method for {@link org.un.bungeni.translators.odttoakn.translator.Translator#getInstance()}.
	 */
	@Test
	public final void testGetInstance() 
	{
		//chek if the instance is successful instanced  
		assertNotNull(myTranslator);
	}

	/**
	 * Test method for {@link org.un.bungeni.translators.odttoakn.translator.Translator#translate(java.lang.String, java.lang.String)}.
	 * @throws TransformerException 
	 * @throws ParserConfigurationException 
	 * @throws IOException 
	 * @throws SAXException 
	 * @throws XPathExpressionException 
	 */
	@Test
	public final void testTranslate() throws XPathExpressionException, SAXException, IOException, ParserConfigurationException, TransformerException 
	{
		//perform a translation
		StreamSource translation = (StreamSource)myTranslator.translate("resources/content2.xml", "resources/configurations/debaterecord/common/DebateRecordCommonConfig.xml");
		
		//check if the translation is a Source type
		assertEquals(StreamSource.class, translation.getClass());
		
		//check if the translation is not null
		assertNotNull(translation);
		
		//create an instance of TransformerFactory
		TransformerFactory transFact = TransformerFactory.newInstance();
	 
	    //create a new transformer
	    Transformer trans = transFact.newTransformer();
	    
	    //create the writer for the transformation
	    StringWriter resultString = new StringWriter();
	    
	    //perform the transformation
	    trans.transform(translation, new StreamResult(resultString));

	    //create a file for the result  
	    File aFile = new File("resources/result.xml");
	    
	    //create an output stram on the file 
	    FileOutputStream out = new FileOutputStream(aFile,false);
	    
	    //get the output channel of the file
	    FileChannel outChannel = out.getChannel();
	    
	    //write the document on the file
	    outChannel.write(ByteBuffer.wrap(resultString.toString().getBytes()));
	    
	    //close the output stream
	    out.close();
	    
	}

}
