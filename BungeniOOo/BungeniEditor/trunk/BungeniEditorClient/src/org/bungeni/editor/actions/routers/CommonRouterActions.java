/*
 * CommonRouterActions.java
 *
 * Created on March 12, 2008, 10:27 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.actions.routers;

import javax.swing.JDialog;
import javax.swing.WindowConstants;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.actions.toolbarSubAction;
import org.bungeni.editor.selectors.DialogSelectorFactory;
import org.bungeni.editor.selectors.IDialogSelector;
import org.bungeni.error.BungeniMsg;
import org.bungeni.error.BungeniValidatorState;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public class CommonRouterActions {
       private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(CommonRouterActions.class.getName());
 
    /** Creates a new instance of CommonRouterActions */
    public CommonRouterActions() {
    }
    
        public static BungeniValidatorState displayFilteredDialog(toolbarAction action, toolbarSubAction subAction, OOComponentHelper ooDocument) {
            BungeniValidatorState returnState =  null;
           try {
             log.debug("displayFilteredDialog: subAction name = "+ subAction.sub_action_name());
             // toolbarAction parentAction = getParentAction();
             
             JDialog dlg;
             dlg= new JDialog();
             dlg.setTitle("Enter Settings for Document");
             dlg.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
             //initDebaterecord.setPreferredSize(new Dimension(420, 300));
             IDialogSelector panel = DialogSelectorFactory.getDialogClass(subAction.dialog_class());
             panel.initObject(ooDocument, dlg, action, subAction);
             //panel.setDialogMode(SelectorDialogModes.TEXT_INSERTION);
             //panel.setBackground(new Color(255, 255, 153));
             //initDebaterecord.setTitle("Selection Mode");
             dlg.getContentPane().add(panel.getPanel());
             dlg.pack();
             dlg.setLocationRelativeTo(null);
             dlg.setVisible(true);
             dlg.setAlwaysOnTop(true);   
             returnState = new BungeniValidatorState(true, new BungeniMsg("SUCCESS")); 
             } catch (Exception ex) {
                 log.error("displayFilteredDialog : " + ex.getMessage());
                 log.error("displayFilteredDialog: stack trace :  \n" + org.bungeni.utils.CommonExceptionUtils.getStackTrace(ex));
                 returnState = new BungeniValidatorState(true, new BungeniMsg("EXCEPTION_FAILURE")); 
                 
             } finally {
                   return returnState; 
             }
    }
}
