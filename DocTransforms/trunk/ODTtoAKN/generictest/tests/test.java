package tests;

import org.un.bungeni.translators.odttoakn.translator.Translator;


public class test {

	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception 
	{
		Translator trans = Translator.getInstance();
		trans.translate("resources/content.xml", "resources/configurations/debaterecord/common/DebateRecordCommonConfig.xml");
		System.out.println("great!");
		
		//OdfDocument odf = OdfDocument.load("resources/ken_pdr_02052000p_en.odt");
		//Document odfDoc = odf.getContentDom();
	}

}
