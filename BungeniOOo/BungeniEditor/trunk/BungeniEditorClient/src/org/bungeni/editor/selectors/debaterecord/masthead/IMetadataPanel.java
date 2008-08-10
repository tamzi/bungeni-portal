/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.editor.selectors.debaterecord.masthead;

import java.awt.Component;
import javax.swing.JFrame;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.actions.toolbarSubAction;
import org.bungeni.editor.selectors.SelectorDialogModes;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author undesa
 */
public interface IMetadataPanel {
    public String getPanelName();
    public Component getPanelComponent();
    public void initVariables(OOComponentHelper ooDoc, JFrame pFrame, toolbarAction tAction, toolbarSubAction tSubAction, SelectorDialogModes smode) ;

}
