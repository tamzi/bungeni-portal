/*
 * ExternalMacro.java
 *
 * Created on August 28, 2007, 4:31 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.macro;

import java.util.Vector;

/**
 *
 * @author Administrator
 */
public class ExternalMacro {
    
    private String name;
    private int param_count = 0;
    private String library_name = "BungeniLibs.Common";
    
    private String programming_language = "Basic";
    private Vector<Object> params = null ;
    
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(ExternalMacro.class.getName());
  
    /** Creates a new instance of ExternalMacro */
    public ExternalMacro(String macroName, int no_of_params) {
        this.name = macroName;
        param_count = no_of_params;
        params = new Vector<Object>();
    }
    public ExternalMacro(String programLang, String libraryName, String macroName,  int no_of_params) {
        this.name = macroName;
        this.programming_language = programLang;
        this.param_count = no_of_params;
        params = new Vector<Object>();
    }
        
    public void setMacroLanguage (String language ) {
        this.programming_language = language;
    }
    
    
    public void addParameter (Object parameterValue) {
        params.add(parameterValue);
    }
    
    public void clearParams() {
        params.removeAllElements();
    }
    
    public void resetParamAtIndex (Object value, int index) {
        if ( (params.size() - 1 ) >= index ) {
            params.set(index, value);
            log.debug("resetParamAtIndex done");
        }
                
    }
    
    public String toString() {
        return this.name;
    }
    public String getExecutionString() {
        String strScriptTemplate = "vnd.sun.star.script:"+ 
                this.library_name+"."+ this.name + 
                "?language="+this.programming_language+"&location=application"   ; 
        log.debug("getExecutionString: "+ strScriptTemplate);
        return strScriptTemplate;
    }
    
    public Object[] getParams() { 
        if (params.size() > 0 ) {
            log.debug("getParams : params > 0, size = "+ params.size());
            Object[] paramArray = (Object[])params.toArray(new Object[params.size()]);
            return paramArray;
        } else {
            return null;
        }
     }
    }

