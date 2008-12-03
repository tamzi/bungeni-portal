/**
 * 
 */
package unittest.translatortest;

import static org.junit.Assert.*;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
//import org.un.bungeni.translators.akntohtml.translator.AHTranslator;
import org.un.bungeni.translators.odttoakn.translator.OATranslator;
import org.un.bungeni.translators.odttoakn.xslprocbuilder.OAXSLProcBuilder;


/**
 * @author lucacervone
 *
 */
public class OATranslatorTest 
{
	private OATranslator myTranslator;
	/**
	 * @throws java.lang.Exception
	 */
	@Before
	public void setUp() throws Exception 
	{
		//get the instance of the translator
		myTranslator = OATranslator.getInstance();
	}

	/**
	 * @throws java.lang.Exception
	 */
	@After
	public void tearDown() throws Exception {
	}

	/**
	 * Test method for {@link org.un.bungeni.translators.odttoakn.translator.OATranslator#getInstance()}.
	 */
	@Test
	public final void testGetInstance() 
	{
		//chek if the instance is successful instanced  
		assertNotNull(myTranslator);
	}

	/**
	 * Test method for {@link org.un.bungeni.translators.odttoakn.translator.OATranslator#translate(java.lang.String, java.lang.String)}.
	 * @throws Exception 
	 */
	@Test
	public final void testTranslate() throws Exception 
	{
		
		OAXSLProcBuilder.newInstance().createXSLProc("resources/odttoakn/minixslt/debaterecord/");
		File xslt = OATranslator.getInstance().buildXSLT("resources/odttoakn/minixslt/debaterecord/pipeline.xsl");
		
		//input stream
		FileInputStream fis  = new FileInputStream(xslt);
		
		//output stream 
		FileOutputStream fos = new FileOutputStream("resources/OAXSLTResult.xsl");
		
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
		
		//perform a translation
		/*File translation = myTranslator.translate("resources/debate_file_01.odt", "resources/odttometalex/debaterecord/config.xml");
	
		//input stream
		FileInputStream fis  = new FileInputStream(translation);
		
		//output stream 
		FileOutputStream fos = new FileOutputStream("resources/resultAKN.xml");
		
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
		}	*/
		
	}

}
