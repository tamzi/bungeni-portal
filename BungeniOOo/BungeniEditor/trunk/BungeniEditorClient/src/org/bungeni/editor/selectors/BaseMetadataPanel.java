/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.editor.selectors;

import java.awt.Component;
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
 
    protected OOComponentHelper ooDocument;
    protected JFrame parentFrame;
    protected toolbarAction theAction =null ;
    protected toolbarSubAction theSubAction = null;
    protected SelectorDialogModes dialogMode;
    
    public BaseMetadataPanel(){
        super();
    }
    
    public void initVariables(OOComponentHelper ooDoc, JFrame pFrame, toolbarAction tAction, toolbarSubAction tSubAction, SelectorDialogModes smode) {
        ooDocument = ooDoc;
        parentFrame = pFrame;
        theAction = tAction;
        theSubAction = tSubAction;
        dialogMode = smode;
    }
    abstract public String getPanelName() ;

    abstract public Component getPanelComponent() ;
    
    private SelectorDialogModes getDialogMode(){
        return dialogMode;
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
            
    
    
}
