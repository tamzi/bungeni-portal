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
 * Contextual evauluator that checks if the cursor is in a particular section in the document.
 * e.g. cursorInSection:section_name
 * will evaluate to true if the cursor is placed in section called section_name
 * will evaluate to false if the cursor is placed in section not called section_name
 * will evaluate to false if the cursor is not placed in a section.
 * @author Administrator
 */
public class cursorInSection implements IBungeniToolbarCondition {
    private OOComponentHelper ooDocument;
    /** Creates a new instance of sectionExists */
    public cursorInSection() {
    }

    public void setOOoComponentHelper(OOComponentHelper ooDocument) {
        this.ooDocument = ooDocument;
    }

    boolean check_cursorInSection (BungeniToolbarCondition condition) {
        String sectionToActUpon =  condition.getConditionValue();
        if (sectionToActUpon.equals("root")) {
           String activeDoc =  BungeniEditorProperties.getEditorProperty("activeDocumentMode");
           sectionToActUpon = BungeniEditorProperties.getEditorProperty("root:"+activeDoc);
        }
        if (ooDocument.currentSectionName().equalsIgnoreCase(sectionToActUpon)) {
         return true;
        } else {
         return false;
        }
    }
    
    public boolean processCondition(BungeniToolbarCondition condition) {
        return check_cursorInSection(condition);
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
