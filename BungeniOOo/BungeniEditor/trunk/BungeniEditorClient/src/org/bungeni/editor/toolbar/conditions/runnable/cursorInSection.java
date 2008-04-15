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
import org.bungeni.utils.CommonExceptionUtils;

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
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(cursorInSection.class.getName());
 
    /** Creates a new instance of sectionExists */
    public cursorInSection() {
    }

    public void setOOoComponentHelper(OOComponentHelper ooDocument) {
        this.ooDocument = ooDocument;
    }

    boolean check_cursorInSection (BungeniToolbarCondition condition) {
        boolean bReturn = true;
        try {
        String sectionToActUpon =  condition.getConditionValue();
        if (sectionToActUpon.equals("root")) {
           String activeDoc =  BungeniEditorProperties.getEditorProperty("activeDocumentMode");
           sectionToActUpon = BungeniEditorProperties.getEditorProperty("root:"+activeDoc);
        }
        if (ooDocument.currentSectionName().matches(sectionToActUpon)) {
         bReturn = true;
        } else {
         bReturn = false;
        }
        } catch (Exception ex) {
            log.error("cursorInSection :" + ex.getMessage());
            log.error("cursorInSection, stack =" + CommonExceptionUtils.getStackTrace(ex));
        } finally {
            return bReturn;
        }
    }
    
    public boolean processCondition(BungeniToolbarCondition condition) {
       // System.out.println("processing condition: "+ ooDocument.getDocumentTitle());
        return check_cursorInSection(condition);
    }
        
 


 }
