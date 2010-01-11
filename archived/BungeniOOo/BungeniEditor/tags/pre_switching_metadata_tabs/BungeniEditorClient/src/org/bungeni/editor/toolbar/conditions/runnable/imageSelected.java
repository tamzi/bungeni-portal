/*
 * imageSelected.java
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
 * Contextual evaluator that checks the condition if an image has been selecte int he document.
 * e.g. imageSelected:true
 * evaluates to true if an image has been selected in the document
 * evaluates to false if an image has not been selected in the document
 * @author Administrator
 */
public class imageSelected implements IBungeniToolbarCondition {
    private OOComponentHelper ooDocument;
    /** Creates a new instance of imageSelected */
    public imageSelected() {
    }

    public void setOOoComponentHelper(OOComponentHelper ooDocument) {
        this.ooDocument = ooDocument;
    }

    boolean check_imageSelected (BungeniToolbarCondition condition) {
        String actionState =  condition.getConditionValue();
        boolean bObjSelected = ooDocument.isTextGraphicObjectSelected();
      return bObjSelected;
    }
    
    public boolean processCondition(BungeniToolbarCondition condition) {
        return check_imageSelected(condition);
    }
        



 }
