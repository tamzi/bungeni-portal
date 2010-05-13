package plugintest;

import static org.junit.Assert.*;

import java.io.File;
import java.util.HashMap;

import org.bungeni.plugins.translator.OdtTranslate;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class OdtTranslateTest {
	OdtTranslate testObject = null;
	HashMap paramMap = null;
	String currentDirectory = "";
	String currentDocType = "";
	
	@Before
	public void setUp() throws Exception {
		testObject = new OdtTranslate();
		paramMap = new HashMap();
		currentDirectory = System.getProperty("user.dir");
		currentDocType = "debaterecord";
		paramMap.put("OdfFileURL", currentDirectory + "/bin/debaterecord_ken_eng_2008_12_17_main.odt");
		paramMap.put("OutputFilePath", currentDirectory + "/bin/debaterecord_ken_eng_2008_12_17_main.xml");
		paramMap.put("OutputMetalexFilePath", currentDirectory + "/bin/debaterecord_ken_eng_2008_12_17_main_metalex.xml");
		paramMap.put("TranslatorRootFolder", currentDirectory + "/bin/");
		paramMap.put("TranslatorConfigFile", "configfiles/odttoakn/TranslatorConfig_debaterecord.xml");
		paramMap.put("TranslatorPipeline","odttoakn/minixslt/debaterecord/pipeline.xsl" );
		paramMap.put("CurrentDocType", currentDocType);
		paramMap.put("CallerPanel", null);
		paramMap.put("PluginMode", "odt2akn");
	}

	@After
	public void tearDown() throws Exception {
	}

	@Test
	public final void testExec() {
		File foutput  = new File((String) paramMap.get("OutputFilePath"));
		if (foutput.exists()) {
			foutput.delete();
		}
		testObject.setParams(paramMap);
		String sErrors = testObject.exec();
		System.out.println("Translation Errors = \n\n" + sErrors);
		File fnewout =  new File((String) paramMap.get("OutputFilePath"));
		assertTrue("Ooutput file was not created", fnewout.exists() == true);
	}

	@Test
	public final void testExec2() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testSetParams() {
		testObject.setParams(paramMap);
	}

}
