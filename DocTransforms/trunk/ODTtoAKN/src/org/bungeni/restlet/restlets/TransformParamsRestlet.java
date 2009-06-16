package org.bungeni.restlet.restlets;

import java.util.HashMap;

import org.bungeni.plugins.translator.OdtTranslate;
import org.restlet.Restlet;
import org.restlet.data.Form;
import org.restlet.data.Method;
import org.restlet.data.Request;
import org.restlet.data.Response;
import org.restlet.data.Status;

/**
 * Sets the dynamic parameters for the Odt Transformer.
 * Currently the only dynamic parameter is the document type
 * @author Ashok Hariharan
 */
public class TransformParamsRestlet extends Restlet {
    private String documentType ;
    private String pluginMode;
    
    
private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(TransformParamsRestlet.class.getName());

	private void setTranslatorParams() {
		OdtTranslate translator = OdtTranslate.getInstance();
		//set the parameters for the server
		//get the default parameters
		String currentDirectory = System.getProperty("user.dir");
		// this parameter is set at runtime before calling exec
		//paramMap.put("OdfFileURL", currentDirectory + "/bin/debaterecord_ken_eng_2008_12_17_main.odt");
		//this parameter is set at runtime before calling exec
		//paramMap.put("OutputFilePath", currentDirectory + "/bin/debaterecord_ken_eng_2008_12_17_main.xml");
		HashMap<String, Object> translatorParameterMap = new HashMap<String, Object>();
		//set the root directory / path prefix for the translator
		translatorParameterMap.put("TranslatorRootFolder", currentDirectory);
		if (this.pluginMode.equals("odt2akn")) {
			
		} else if (this.pluginMode.equals("akn2html")) {
			//do this later
		}
		
		if (this.documentType.equals("debaterecord")) {
			paramMap.put("TranslatorConfigFile", "configfiles/odttoakn/TranslatorConfig_debaterecord.xml");
			paramMap.put("TranslatorPipeline","odttoakn/minixslt/debaterecord/pipeline.xsl" );
			paramMap.put("CurrentDocType", documentType);
		}
		paramMap.put("CallerPanel", null);
		paramMap.put("PluginMode", "odt2akn");
		//set the dynamic parameters
		translator.setParams(inputParams)
	}
	
	
   @Override
    public void handle(Request request, Response response) {
       log.debug("handling method : "+ request.getMethod().getName());
       try {
        if(request.getMethod().equals(Method.POST)) {
            Form postedForm = request.getEntityAsForm();
            this.documentType = (String) postedForm.getFirstValue("DocumentType");
            this.pluginMode = (String) postedForm.getFirstValue("PluginMode");
            System.out.println("doc type = "+ this.documentType);
            response.setStatus(Status.SUCCESS_NO_CONTENT);
        } else {
            response.setStatus(Status.CLIENT_ERROR_BAD_REQUEST);
        }
       } catch (Exception ex) {
           log.error("handle : " , ex);
       }
   }

}
