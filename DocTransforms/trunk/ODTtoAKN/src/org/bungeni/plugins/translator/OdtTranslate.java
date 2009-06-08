/**
 * 
 */
package org.bungeni.plugins.translator;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.HashMap;
import org.apache.log4j.Logger;
import org.bungeni.plugins.IEditorPlugin;
import org.un.bungeni.translators.globalconfigurations.GlobalConfigurations;
import org.un.bungeni.translators.odttoakn.translator.OATranslator;

/**
 * Bridging class that implements the IEditorPlugin interface for interacting with the bungeni editor.
 * The IEditorPlugin interface is described here :
 * http://code.google.com/p/bungeni-editor/
 * @author Ashok Hariharan
 *
 */
public class OdtTranslate implements IEditorPlugin {

    private static org.apache.log4j.Logger log            =
        Logger.getLogger(OdtTranslate.class.getName());

    private HashMap                      editorParams    = null;
    private String                       odfFileUrl      = null;
    private String 					 	 outputFilePath = null;
    private String                       translatorRootFolder = null;
    private String						 translatorConfigFile = null;
    private String						 currentDocType = null;
	private Object					     callerPanel = null;
	private javax.swing.JFrame			 callerFrame = null;
	private String 						 pluginMode = null;
	
	public OdtTranslate(){
		//for call by reflection
	}
	
	public String exec() {
		FileInputStream fis = null;
		FileOutputStream fos = null;
		String retvalue = "";
		try 
		{
			OATranslator myTranslator = OATranslator.getInstance();
			
			File translation = myTranslator.translate(this.odfFileUrl,GlobalConfigurations.getApplicationPathPrefix() + "odttoakn/minixslt/debaterecord/pipeline.xsl");
			//File translation = myTranslator.translate("resources/debaterecord_ken_eng_2008_12_17_main.odt", GlobalConfigurations.getApplicationPathPrefix() + "odttoakn/minixslt/debaterecord/pipeline.xsl");
			
			//input stream
			fis  = new FileInputStream(translation);
			
			//output stream 
			fos = new FileOutputStream(getOutputFileName());
			
			//copy the file
	
				byte[] buf = new byte[1024];
			    int i = 0;
			    while ((i = fis.read(buf)) != -1) 
			    {
			            fos.write(buf, 0, i);
			    }
			 fis.close();
			 fos.close();
		} 
		catch (IOException e) 
		{
			log.error("exec()", e);
		}  
		finally{
		    return retvalue;
		}	
	}

	public Object exec2(Object[] arg0) {
		// TODO Auto-generated method stub
		return null;
	}

	/**
	 * The following parameters are supported and mandatory:
	 * OdfFileURL - full path to the Odf file being translated
	 * OutputFilePath - full path to the output Xml file to be generated
	 * TranslatorRootFolder - root folder for the translator usually the folder containing the main directories used by the translator. Path must end in a "/"
	 * TranslatorConfigFile - the configuration file for the document type being transformed (this is a relative path - relative to the translator root folder)
	 * CurrentDocType - the document type being translated
	 * CallerPanel  - the UI JPanel invoking the translator
	 * PluginMode - 2 modes are supported odt2akn and akn2html.
	 * ParentFrame - the JFrame object to use as the parent frame for any UI interactions
	 */
	public void setParams(HashMap inputParams) {
        try {
            log.debug("setting inputparams");
            
            //first recieve the input parameters for the plugin from the parameter map
            this.editorParams    = inputParams;
            this.odfFileUrl      = (String) this.editorParams.get("OdfFileURL");
            this.outputFilePath = (String) this.editorParams.get("OutputFilePath");
            this.translatorRootFolder = (String) this.editorParams.get("TranslatorRootFolder");
            this.translatorConfigFile = (String)  this.editorParams.get("TranslatorConfigFile");
            this.currentDocType  = (String) this.editorParams.get("CurrentDocType");
            this.pluginMode = (String) this.editorParams.get("PluginMode");
            if (this.editorParams.containsKey("ParentFrame")) {
                this.callerFrame = (javax.swing.JFrame) this.editorParams.get("ParentFrame");
            }
            if (this.editorParams.containsKey("CallerPanel")) {
            	this.callerPanel = this.editorParams.get("CallerPanel");
            }
            
            //set the parameters for the translator now
            appInit();
            
            } catch (Exception ex) {
                log.error("setParams : " + ex.getMessage());
                log.error("setParams : stacktrace : ", ex);
                ex.printStackTrace(System.out);
            }
	}

	/*** Application code **/
	private void appInit(){
		//Do application initialization here
		//setting application prefixes etc..
		GlobalConfigurations.setApplicationPathPrefix(this.translatorRootFolder);
		//GlobalConfigurations.setConfigurationFilePath("configfiles/odttoakn/TranslatorConfig_debaterecord.xml");
		GlobalConfigurations.setConfigurationFilePath(this.translatorConfigFile);

	}
	
	private String getOutputFileName() {
		return this.outputFilePath;
	}
}
