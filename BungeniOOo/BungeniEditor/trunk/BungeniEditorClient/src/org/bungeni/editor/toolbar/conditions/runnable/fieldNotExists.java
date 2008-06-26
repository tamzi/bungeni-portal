/*
 * sectionExists.java
 *
 * Created on January 26, 2008, 10:25 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.toolbar.conditions.runnable;

import com.sun.star.beans.XPropertySet;
import com.sun.star.container.NoSuchElementException;
import com.sun.star.container.XEnumeration;
import com.sun.star.container.XEnumerationAccess;
import com.sun.star.lang.XServiceInfo;
import com.sun.star.text.XTextField;
import org.bungeni.editor.BungeniEditorProperties;
import org.bungeni.editor.toolbar.conditions.BungeniToolbarCondition;
import org.bungeni.editor.toolbar.conditions.IBungeniToolbarCondition;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooQueryInterface;

/**
 * 
 * Contextual evaluator that checks if a field exists in a document.
 * e.g. fieldExists:field_name
 * will evaluate to true if the field_name exists in the document
 * will evaluate to false if the field_name does not exist in the document
 * @author Administrator
 */
public class fieldNotExists implements IBungeniToolbarCondition {
    private OOComponentHelper ooDocument;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(fieldExists.class.getName());
    /** Creates a new instance of sectionExists */
    public fieldNotExists() {
    }

    public void setOOoComponentHelper(OOComponentHelper ooDocument) {
        this.ooDocument = ooDocument;
    }

    boolean check_fieldNotExists (BungeniToolbarCondition condition) {
        fieldExists fldExists = new fieldExists();
        fldExists.setOOoComponentHelper(ooDocument);
        if (fldExists.processCondition(condition)) {
            log.debug("fieldNotExists = false");
            return false;
        } else {
            log.debug("fieldNotExists = true");
            return true;
        }
    }
    
    public boolean processCondition(BungeniToolbarCondition condition) {
        log.debug("processing fieldNotExists");
        return check_fieldNotExists(condition);
    }
        




 }
