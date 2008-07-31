/*
 * baseRunnableCondition.java
 *
 * Created on May 30, 2008, 5:28 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.toolbar.conditions.runnable;

import org.bungeni.editor.toolbar.conditions.BungeniToolbarCondition;
import org.bungeni.editor.toolbar.conditions.IBungeniToolbarCondition;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public abstract class baseRunnableCondition implements IBungeniToolbarCondition {
    protected OOComponentHelper ooDocument;
    /** Creates a new instance of baseRunnableCondition */
    public baseRunnableCondition() {
    }

    public void setOOoComponentHelper(OOComponentHelper ooDocument) {
        this.ooDocument = ooDocument;
    }

    public abstract boolean runCondition(BungeniToolbarCondition condition);
    
    public boolean processCondition(BungeniToolbarCondition condition) {
        boolean bResult = false;
        try {
        if (condition.hasNegationCondition())
            bResult =  !runCondition(condition);
        else
            bResult = runCondition(condition);
        } catch (Exception ex) {
            
        } finally {
            return bResult;
        }
    }
    
}
