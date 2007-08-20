/*
 * IEditorActionEvent.java
 *
 * Created on August 20, 2007, 4:35 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.actions;

import org.bungeni.db.toolbarAction;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public interface IEditorActionEvent {
       public void doCommand(OOComponentHelper ooDocument, toolbarAction action);
}
