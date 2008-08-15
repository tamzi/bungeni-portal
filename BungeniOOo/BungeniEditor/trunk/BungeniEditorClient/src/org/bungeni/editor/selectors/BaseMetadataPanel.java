/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.editor.selectors;

import java.awt.Component;
import java.util.HashMap;
import javax.swing.JFrame;
import javax.swing.JPanel;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.actions.toolbarSubAction;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author undesa
 */
public abstract class BaseMetadataPanel extends JPanel implements IMetadataPanel {
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(BaseMetadataPanel.class.getName());
    private BaseMetadataContainerPanel containerPanel ;
    private BungeniFormContext formContext;
    private HashMap<String,Object> thePreInsertMap = new HashMap<String,Object>();
    
    public BaseMetadataPanel(){
        super();
    }
    /*
    public void initVariables(OOComponentHelper ooDoc, JFrame pFrame, toolbarAction tAction, toolbarSubAction tSubAction, SelectorDialogModes smode) {
        ooDocument = ooDoc;
        parentFrame = pFrame;
        theAction = tAction;
        theSubAction = tSubAction;
        dialogMode = smode;
    }*/
    public void initVariables(BaseMetadataContainerPanel panel) {
        this.containerPanel = panel;
        createContext();
        initFields();
    }
    
     private void createContext(){
        formContext = new BungeniFormContext();
        getFormContext().setTheAction(getTheAction());
        getFormContext().setTheSubAction(getTheSubAction());
        getFormContext().setOoDocument(getOoDocument());
        getFormContext().setPreInsertMap(getThePreInsertMap());
    }
     
    private void initFields(){
        switch (getDialogMode()) {
            case TEXT_SELECTED_EDIT:
                initFieldsSelectedEdit();
                return;
            case TEXT_SELECTED_INSERT:
                initFieldsSelectedInsert();
                return;
            case TEXT_INSERTION:
                initFieldsInsert();
                return;
            case TEXT_EDIT:  
                initFieldsEdit();
                return;
            default:
                return;
        }
    }

    /**
     * The following functions are called upon initalization of the panel, depening on the current mode,
     * the appropriate function is called.
     */
    abstract protected void initFieldsSelectedEdit();
    abstract protected void initFieldsSelectedInsert();
    abstract protected void initFieldsInsert();
    abstract protected void initFieldsEdit();
    
    abstract public String getPanelName() ;

    abstract public Component getPanelComponent() ;
    
    /** helper functions to get variables from parent container **/
    public BaseMetadataContainerPanel getContainerPanel(){
        return containerPanel;
    }
    
    public OOComponentHelper getOoDocument(){
        return getContainerPanel().getOoDocument();
    }
    
    public JFrame getParentFrame(){
        return getContainerPanel().getParentFrame();
    }
    
    public toolbarAction getTheAction(){
        return getContainerPanel().getTheAction();
    }
    
    public toolbarSubAction getTheSubAction(){
        return getContainerPanel().getTheSubAction();
    }
    
    public SelectorDialogModes getDialogMode(){
        return getContainerPanel().getDialogMode();
    }

    public void addErrorMessage(java.awt.Component p, String msg) {
        getContainerPanel().addErrorMessage(p, msg);
    }
    
    public String ErrorMessagesAsString(){
        return getContainerPanel().ErrorMessagesAsString();
    }

    public boolean doApply(){
         switch (getDialogMode()) {
            case TEXT_SELECTED_EDIT :
                return applySelectEdit();
            case TEXT_SELECTED_INSERT :
                return applySelectInsert();
            case TEXT_EDIT:
                return applyFullEdit();
            case TEXT_INSERTION:
                return applyFullInsert();
            default:
                return true;
         }
    }
    
    public boolean applyFullEdit(){    
       
        if (validateFields() == false) {
                return false;
        }
       
        if (preFullEdit() == false) {
            return false;
        }   
       
        if (processFullEdit() == false) {
                return false;
       }   
       
        if (postFullEdit() == false) {
                return false;
       }
        
        return true;
    }

    abstract public boolean preFullEdit();
    abstract public boolean processFullEdit();
    abstract public boolean postFullEdit();
    
    
    public boolean applyFullInsert(){    
       
        if (validateFields() == false) {
                return false;
        }
       
        if (preFullInsert() == false) {
            return false;
       }   
       
        if (processFullInsert() == false) {
                return false;
       }   
       
        if (postFullInsert() == false) {
                return false;
       }
        
        return true;
}

    abstract public boolean preFullInsert();
    abstract public boolean processFullInsert();
    abstract public boolean postFullInsert();
    
    public boolean applySelectEdit(){    
       
        if (validateFields() == false) {
             return false;
        }
       
        if (preSelectEdit() == false) {
            return false;
       }   
       
        if (processSelectEdit() == false) {
           return false;
       }   
       
        if (postSelectEdit() == false) {
           return false;
       }
        return true;
}
    
    abstract public boolean preSelectEdit();
    abstract public boolean processSelectEdit();
    abstract public boolean postSelectEdit();

    
        public boolean applySelectInsert(){    
       
        if (validateFields() == false) {
             return false;
        }
       
        if (preSelectInsert() == false) {
            return false;
        }   
       
        if (processSelectInsert() == false) {
            return false;
       }   
       
        if (postSelectInsert() == false) {
            return false;
       }
       
        return true;
}
    
    abstract public boolean preSelectInsert();
    abstract public boolean processSelectInsert();
    abstract public boolean postSelectInsert();
    
    
    public boolean validateFields(){
           switch (getDialogMode()) {
                case TEXT_SELECTED_EDIT :
                    return validateSelectedEdit();
                case TEXT_SELECTED_INSERT :
                    return validateSelectedInsert();
                case TEXT_EDIT:
                    return validateFullEdit();
                case TEXT_INSERTION:
                    return validateFullInsert();
                default:
                    return true;
            }
    }

    abstract public boolean validateSelectedEdit();
    
    abstract public boolean validateSelectedInsert();
    
    abstract public boolean validateFullInsert();
    
    abstract public boolean validateFullEdit();
    
    abstract public boolean doCancel();
    
    abstract public boolean doReset();

    public BungeniFormContext getFormContext() {
        return formContext;
    }

    public HashMap<String, Object> getThePreInsertMap() {
        return thePreInsertMap;
    }
            
    
    
}
