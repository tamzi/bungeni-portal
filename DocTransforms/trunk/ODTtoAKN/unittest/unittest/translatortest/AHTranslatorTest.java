package unittest.translatortest;


import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
//import org.un.bungeni.translators.akntohtml.configurations.AHConfigurationBuilder;
import org.un.bungeni.translators.akntohtml.translator.AHTranslator;

public class AHTranslatorTest {

	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
	}

	@AfterClass
	public static void tearDownAfterClass() throws Exception {
	}

	@Before
	public void setUp() throws Exception {
	}

	@After
	public void tearDown() throws Exception {
	}

	/**
	 * Test method for {@link org.un.bungeni.translators.odttoakn.translator.Translator#translate(java.lang.String, java.lang.String)}.
	 * @throws Exception 
	 */
	@Test
	public final void testTranslate() throws Exception 
	{
		//perform a translation
		//AHConfigurationBuilder.newInstance().createConfiguration("resources/akntohtml/minixslt/");
		File translation = AHTranslator.getInstance().translate("resources/6th March, 2008.xml", "resources/akntohtml/minixslt/pipeline.xsl");
	
		//input stream
		FileInputStream fis  = new FileInputStream(translation);
		
		//output stream 
		FileOutputStream fos = new FileOutputStream("resources/AHresult.html");
		
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
		/*File translation = AHTranslator.getInstance().buildXSLT("resources/akntohtml/minixslt/pipeline.xsl");
		FileInputStream fis  = new FileInputStream(translation);
		
		//output stream 
		FileOutputStream fos = new FileOutputStream("resources/XSLTResult.xsl");
		
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
		}*/		
	}
}
