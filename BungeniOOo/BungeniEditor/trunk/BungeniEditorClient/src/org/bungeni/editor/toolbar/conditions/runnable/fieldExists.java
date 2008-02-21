/*
 * sectionExists.java
 *
 * Created on January 26, 2008, 10:25 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.toolbar.conditions.runnable;

import com.sun.star.container.XEnumeration;
import com.sun.star.container.XEnumerationAccess;
import org.bungeni.editor.BungeniEditorProperties;
import org.bungeni.editor.toolbar.conditions.BungeniToolbarCondition;
import org.bungeni.editor.toolbar.conditions.IBungeniToolbarCondition;
import org.bungeni.ooo.OOComponentHelper;

/**
 * 
 * Contextual evaluator that checks if a field exists in a document.
 * e.g. fieldExists:field_name
 * will evaluate to true if the field_name exists in the document
 * will evaluate to false if the field_name does not exist in the document
 * @author Administrator
 */
public class fieldExists implements IBungeniToolbarCondition {
    private OOComponentHelper ooDocument;
    /** Creates a new instance of sectionExists */
    public fieldExists() {
    }

    public void setOOoComponentHelper(OOComponentHelper ooDocument) {
        this.ooDocument = ooDocument;
    }

    boolean check_fieldExists (BungeniToolbarCondition condition) {
        String fieldName  =  condition.getConditionValue();
        XEnumerationAccess fieldAccess = ooDocument.getTextFields();
        /*
        if (fieldAccess != null ) {
            
            XEnumeration enumField = fieldAccess.createEnumeration();
            while (enumField.hasMoreElements()) {
                
            }
        }
        */
         return false;
    }
    
    public boolean processCondition(BungeniToolbarCondition condition) {
        return check_fieldExists(condition);
    }
        
    /*
       boolean check_sectionExists(String[] arrCondition) {.
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
