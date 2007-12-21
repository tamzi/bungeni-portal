/*
 * IDialogSelector.java
 *
 * Created on September 2, 2007, 4:56 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.selectors;

import javax.swing.JDialog;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public interface IDialogSelector {
    public void setDialogMode(SelectorDialogModes mode );
    public SelectorDialogModes getDialogMode();
    public void setOOComponentHelper(OOComponentHelper ooComp);
    public void setToolbarAction(toolbarAction action);
    public void setParentDialog(JDialog dlg);
    
}
