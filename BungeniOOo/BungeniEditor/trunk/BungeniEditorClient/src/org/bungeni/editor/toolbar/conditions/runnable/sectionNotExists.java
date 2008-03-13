/*
 * sectionExists.java
 *
 * Created on January 26, 2008, 10:25 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.toolbar.conditions.runnable;

import org.bungeni.editor.BungeniEditorProperties;
import org.bungeni.editor.toolbar.conditions.BungeniToolbarCondition;
import org.bungeni.editor.toolbar.conditions.IBungeniToolbarCondition;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public class sectionNotExists implements IBungeniToolbarCondition {
    private OOComponentHelper ooDocument;
      private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(sectionNotExists.class.getName());
        
    /** Creates a new instance of sectionExists */
    public sectionNotExists() {
    }

    public void setOOoComponentHelper(OOComponentHelper ooDocument) {
        this.ooDocument = ooDocument;
    }

    boolean check_sectionNotExists (BungeniToolbarCondition condition) {
        
        log.debug("sectionNotExists: value "+ condition.getConditionValue());
        log.debug("sectionNotExists: name "+ condition.getConditionName());
        
        String sectionToActUpon =  condition.getConditionValue();
        if (sectionToActUpon.equals("root")) {
           String activeDoc =  BungeniEditorProperties.getEditorProperty("activeDocumentMode");
           sectionToActUpon = BungeniEditorProperties.getEditorProperty("root:"+activeDoc);
        }
        if (ooDocument.hasSection(sectionToActUpon)) {
            log.debug("section :  "+sectionToActUpon + " does not exist" );
            return false;
        } else {
            log.debug("section :  "+sectionToActUpon + " exists" );
            return true;
        }
    }
    
    public boolean processCondition(BungeniToolbarCondition condition) {
        return check_sectionNotExists(condition);
    }
        
    /*
       boolean check_sectionExists(String[] arrCondition) {
             boolean bReturn = false;
          try {
             String sectionToActUpon = arrCondition[1];

             if (sectionToActUpon.equals("root")) {
                String activeDoc =  BungeniEditorProperties.getEditorProperty("activeDocumentMode");
                sectionToActUpon = BungeniEditorProperties.getEditorProperty("root:"+activeDoc);
             }

             if (ooDocument.hasSection(sectionToActUpon)) {
                 bReturn =  true;
             } else {
                 bReturn = false;
             }
         } catch (Exception ex) {
             log.error("check_sectionNotExists:"+ex.getMessage());
             log.error("check_sectionNotExists:"+ CommonExceptionUtils.getStackTrace(ex));
             bReturn = false;
         } finally {
             return bReturn;
         }
     }    
       
    if (arrCondition[0].equals("sectionExists")) {
                    log.debug("processActionCondition:sectionExists");
                    bAction  = check_sectionExists(arrCondition);
                    log.debug("processActionCondition:"+bAction);
                }
*/



 }
