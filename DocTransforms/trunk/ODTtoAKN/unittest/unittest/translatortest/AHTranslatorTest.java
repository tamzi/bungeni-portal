package unittest.translatortest;


import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.un.bungeni.translators.akntohtml.configurations.AHConfigurationBuilder;

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
		AHConfigurationBuilder.newInstance().createConfiguration("resources/akntohtml/minixslt/");
	}	
}
