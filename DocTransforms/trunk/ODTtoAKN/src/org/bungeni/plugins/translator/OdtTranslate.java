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
 * @author ashok
 *
 */
public class OdtTranslate implements IEditorPlugin {

    private static org.apache.log4j.Logger log            =
        Logger.getLogger(OdtTranslate.class.getName());

	 /**
     * Supported Params :
     * OdfFileURL = url to odf file
     * SettingsFolder = path to settings folder
     * CurrentDocType = current document type
     */
    private HashMap                      editorParams    = null;
    private String                       odfFileUrl      = null;
    private String                       translatorRootFolder = null;
    private String						 translatorConfigFile = null;
    private String						 currentDocType = null;
	private Object					     callerPanel = null;
	private javax.swing.JFrame			 callerFrame = null;
	private String 						 pluginMode = null;
	
	
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

	public void setParams(HashMap inputParams) {
        try {
            log.debug("setting inputparams");
            this.editorParams    = inputParams;
            this.odfFileUrl      = (String) this.editorParams.get("OdfFileURL");
            this.translatorRootFolder = (String) this.editorParams.get("TranslatorRootFolder");
            this.translatorConfigFile = (String)  this.editorParams.get("TranslatorConfigFile");
            this.currentDocType  = (String) this.editorParams.get("CurrentDocType");
            this.callerPanel = this.editorParams.get("CallerPanel");
            this.pluginMode = (String) this.editorParams.get("PluginMode");
            if (this.editorParams.containsKey("ParentFrame")) {
                    this.callerFrame = (javax.swing.JFrame) this.editorParams.get("ParentFrame");
            }
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
		return new String(); // generate output file name here 
	}
}
