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
import org.un.bungeni.translators.odttoakn.translator.Translator;


/**
 * @author lucacervone
 *
 */
public class OATranslatorTest 
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
	 * @throws Exception 
	 */
	@Test
	public final void testTranslate() throws Exception 
	{
		//perform a translation
		File translation = myTranslator.translate("resources/debate_file_01.odt", "resources/configurations/debaterecord/common/DebateRecordCommonConfig.xml");
	
		//input stream
		FileInputStream fis  = new FileInputStream(translation);
		
		//output stream 
		FileOutputStream fos = new FileOutputStream("resources/result.xml");
		
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
		
	}

}
