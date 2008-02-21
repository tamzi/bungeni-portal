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
 * Contextual evaluator that checks if a particular section exists in the document.
 * e.g. sectionsExists:section_name
 * will evaluate to true if a section called section_name exists the document
 * will evaluate to false if a section called section_name does not exist the document
 * @author Administrator
 */
public class sectionExists implements IBungeniToolbarCondition {
    private OOComponentHelper ooDocument;
    /** Creates a new instance of sectionExists */
    public sectionExists() {
    }

    public void setOOoComponentHelper(OOComponentHelper ooDocument) {
        this.ooDocument = ooDocument;
    }

    boolean check_sectionExists (BungeniToolbarCondition condition) {
        String sectionToActUpon =  condition.getConditionValue();
        if (sectionToActUpon.equals("root")) {
           String activeDoc =  BungeniEditorProperties.getEditorProperty("activeDocumentMode");
           sectionToActUpon = BungeniEditorProperties.getEditorProperty("root:"+activeDoc);
        }
        if (ooDocument.hasSection(sectionToActUpon)) {
         return true;
        } else {
         return false;
        }
    }
    
    public boolean processCondition(BungeniToolbarCondition condition) {
        return check_sectionExists(condition);
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
