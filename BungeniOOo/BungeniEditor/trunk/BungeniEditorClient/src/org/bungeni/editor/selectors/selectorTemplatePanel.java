/*
 * selectorTemplatePanel.java
 *
 * Created on September 19, 2007, 11:34 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.selectors;

import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.util.HashMap;
import javax.swing.JDialog;
import javax.swing.JPanel;
import javax.swing.JRootPane;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.BungeniRegistryFactory;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public class selectorTemplatePanel extends javax.swing.JPanel 
                implements IDialogSelector {
    protected OOComponentHelper ooDocument;
    protected JDialog parent;
    protected toolbarAction theAction;
    protected SelectorDialogModes theMode;
    protected BungeniClientDB dbInstance=null;
    protected BungeniClientDB dbSettings = null;
    protected HashMap<String,String> theSerializationMap = new HashMap<String,String>();
    protected HashMap<String,String> theMetadataMap = new HashMap<String,String>();
    protected HashMap<String,Component> theControlMap = new HashMap<String,Component>();
    protected String windowTitle;
    class dlgBackgrounds {
        Color background;
        String windowTitle = "";
        dlgBackgrounds(SelectorDialogModes mode) {
            if (mode == SelectorDialogModes.TEXT_SELECTED_INSERT) {
                  background = new Color(255, 255, 153);
                  windowTitle = "Selection Mode Insert";
              } else 
            if (mode == SelectorDialogModes.TEXT_SELECTED_EDIT) {
                  background = new Color(255, 255, 153);
                  windowTitle = "Selection Mode Edit";
              } else 
            if (mode == SelectorDialogModes.TEXT_INSERTION){
                  background = new Color(204, 255, 153);
                  windowTitle = "Insertion Mode";
            } else 
            if (mode == SelectorDialogModes.TEXT_EDIT){
                  background = new Color(150, 255, 153);
                  windowTitle = "Edit Mode";
            } else {
                background = new Color (100, 255, 153);
                windowTitle = "Mode not Selected";
            }
        }
        
        Color getBackground() {
            return background;
        }
        String getTitle() {
            return windowTitle;
        }
        }
    
    
    /** Creates a new instance of selectorTemplatePanel */
    public selectorTemplatePanel() {
    }
    
    public selectorTemplatePanel (OOComponentHelper ooDocument, 
            JDialog parentDlg, 
            toolbarAction theAction) {
        this.ooDocument = ooDocument;
        this.parent = parentDlg;
        this.theAction = theAction;
        this.theMode = theAction.getSelectorDialogMode();
        dlgBackgrounds bg = new dlgBackgrounds(theMode);
        this.setBackground(bg.getBackground());
        this.windowTitle = bg.getTitle(); 
        HashMap<String,String> registryMap = BungeniRegistryFactory.fullConnectionString();  
        dbInstance = new BungeniClientDB(registryMap);
        dbSettings = new BungeniClientDB(DefaultInstanceFactory.DEFAULT_INSTANCE(), DefaultInstanceFactory.DEFAULT_DB());
    }

    public void setDialogMode(SelectorDialogModes mode) {
        this.theMode = mode;
    }

    public SelectorDialogModes getDialogMode() {
        return this.theMode;
    }

    public String getWindowTitle() {
        return windowTitle;
    }
    public void setOOComponentHelper(OOComponentHelper ooComp) {
        this.ooDocument=ooComp;
    }

    public void setToolbarAction(toolbarAction action) {
        this.theAction = action;
    }

    public void setParentDialog(JDialog dlg) {
        this.parent = dlg;
    }
    
    public void setSectionMetadataForAction(String sectionName, toolbarAction action) {
      
        HashMap<String,String> sectionMeta = new HashMap<String,String>();
        sectionMeta.put("BungeniSectionType", theAction.action_section_type());
        ooDocument.setSectionMetadataAttributes(sectionName, sectionMeta);
      
    }
    
    public void setSectionMetadataSectionType (String sectionName, String sectionType) {
      
        HashMap<String,String> sectionMeta = new HashMap<String,String>();
        sectionMeta.put("BungeniSectionType",sectionType);
        ooDocument.setSectionMetadataAttributes(sectionName, sectionMeta);
        
    }
       
    public HashMap<String,String> getSectionMetadataForAction(String sectionName) {
        HashMap<String,String> sectionMeta = new HashMap<String,String>();
        return ooDocument.getSectionMetadataAttributes(sectionName);
    }    
 
    public void buildComponentsArray() {
        getComponentsWithNames(this);
    }
    
   private void getComponentsWithNames(Container container) {
        
        for (Component component: container.getComponents()){
           String strName = null;
           if (component.getClass() == javax.swing.JList.class) {
               System.out.println("this is a jlist");
           }
           strName = component.getName();
           if (strName != null) {
               theControlMap.put(strName.trim(), component);
           }
     
           if (component instanceof JRootPane) {    
              JRootPane nestedJRootPane = (JRootPane)component;
              getComponentsWithNames(nestedJRootPane.getContentPane());
            }

           if (component instanceof JPanel) {
              // JPanel found. Recursing into this panel.
              JPanel nestedJPanel = (JPanel)component;
              getComponentsWithNames(nestedJPanel);
            }
   
        }
        
    }
}
