/*
 * defaultRouter.java
 *
 * Created on March 10, 2008, 12:26 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.actions.routers;

import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.actions.toolbarSubAction;
import org.bungeni.error.BungeniMsg;
import org.bungeni.error.BungeniValidatorState;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public class defaultRouter implements IBungeniActionRouter {
    protected BungeniClientDB dbSettings;
    /** Creates a new instance of defaultRouter */
    public defaultRouter() {
          dbSettings = new BungeniClientDB (DefaultInstanceFactory.DEFAULT_INSTANCE(), DefaultInstanceFactory.DEFAULT_DB());
    }

    public BungeniValidatorState route(toolbarAction action, toolbarSubAction subAction, javax.swing.JFrame pFrame, OOComponentHelper ooDoc) {
      switch(subAction.getSelectorDialogMode()) {
            case TEXT_INSERTION:
                return route_FullInsert(action, subAction, pFrame, ooDoc);
            case DOCUMENT_LEVEL_ACTION:
                return route_DocumentLevelAction(action, subAction, pFrame,  ooDoc);
            case TEXT_EDIT:
                return route_FullEdit(action, subAction, pFrame,  ooDoc);
            case TEXT_SELECTED_EDIT:
                return route_TextSelectedEdit(action, subAction, pFrame,  ooDoc);
            case TEXT_SELECTED_INSERT:
                return route_TextSelectedInsert(action, subAction,  pFrame, ooDoc);
            default:
                return new BungeniValidatorState(false, new BungeniMsg("DIALOG_MODE_MISSING"));
        }
    }

    public BungeniValidatorState route_DocumentLevelAction(toolbarAction action, toolbarSubAction subAction, javax.swing.JFrame pFrame,  OOComponentHelper ooDocument) {
       return new BungeniValidatorState(true, new BungeniMsg("SUCCESS")); 
    }

    public BungeniValidatorState route_TextSelectedInsert(toolbarAction action, toolbarSubAction subAction, javax.swing.JFrame pFrame,OOComponentHelper ooDocument) {
       return new BungeniValidatorState(true, new BungeniMsg("SUCCESS")); 
    }

    public BungeniValidatorState route_TextSelectedEdit(toolbarAction action, toolbarSubAction subAction,javax.swing.JFrame pFrame, OOComponentHelper ooDocument) {
       return new BungeniValidatorState(true, new BungeniMsg("SUCCESS")); 
    }

    public BungeniValidatorState route_FullInsert(toolbarAction action, toolbarSubAction subAction,javax.swing.JFrame pFrame, OOComponentHelper ooDocument) {
       return new BungeniValidatorState(true, new BungeniMsg("SUCCESS")); 
    }

    public BungeniValidatorState route_FullEdit(toolbarAction action, toolbarSubAction subAction,javax.swing.JFrame pFrame, OOComponentHelper ooDocument) {
       return new BungeniValidatorState(true, new BungeniMsg("SUCCESS")); 
    }
    
}
