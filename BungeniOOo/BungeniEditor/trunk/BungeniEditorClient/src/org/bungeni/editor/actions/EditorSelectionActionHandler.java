/*
 * EditorSelectionActionHandler.java
 *
 * Created on December 2, 2007, 10:58 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.actions;

import com.sun.star.text.XTextContent;
import java.util.HashMap;
import java.util.Vector;
import javax.swing.JDialog;
import javax.swing.WindowConstants;
import org.apache.log4j.Logger;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.db.QueryResults;
import org.bungeni.db.SettingsQueryFactory;
import org.bungeni.editor.selectors.InitDebateRecord;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.utils.MessageBox;

/**
 *
 * @author Administrator
 */
public class EditorSelectionActionHandler implements IEditorActionEvent {
   private static org.apache.log4j.Logger log = Logger.getLogger(EditorSelectionActionHandler.class.getName());
   private OOComponentHelper ooDocument;
   private toolbarSubAction m_subAction;   
   private BungeniClientDB instance;
    /** Creates a new instance of EditorSelectionActionHandler */
    public EditorSelectionActionHandler() {
           
        instance = new BungeniClientDB (DefaultInstanceFactory.DEFAULT_INSTANCE(), DefaultInstanceFactory.DEFAULT_DB());
      
    }

    public void doCommand(OOComponentHelper ooDocument, toolbarAction action) {
    
    }

    public void doCommand(OOComponentHelper ooDocument, toolbarSubAction action) {
        this.ooDocument = ooDocument;
        this.m_subAction = action;
        int nValid = -1;
        if ((nValid = validateAction()) < 0 ) 
        {
            log.debug("EditorSelectionActionHandler : invalid action in this context");
            return;
        }
        routeAction();
    
    }
    
    private void routeAction() {
        if (m_subAction.parent_action_name().equals("makePrayerSection")) {
            routeAction_Masthead();
        }
    }

    private void routeAction_Masthead(){
            if (m_subAction.sub_action_name().equals("selectlogo")) {
                
            }
            if (m_subAction.sub_action_name().equals("section_creation")) {
                //get the parent section name and create it over the selected text
                
                int nSectionRet ;
                nSectionRet = createSection();
                if (nSectionRet < 0 ) {
                    if (nSectionRet == -2) {
                        MessageBox.OK("The section already exists" );
                    }
                } else {
                    MessageBox.OK("Section was successfully created");
                }
                return;
            }
            if (m_subAction.sub_action_name().equals("debatedate_entry")) {
                displayFilteredDialog();
            }
            if (m_subAction.sub_action_name().equals("debatetime_entry")) {
                
            }
            if (m_subAction.sub_action_name().equals("selectlogo")) {
                
            }
    }
    
    private int validateAction(){
        Object selectionObj = null;
        selectionObj = ooDocument.getCurrentSelection();
        if (selectionObj == null )
        {
            log.debug("validateAction: nothing was selected ");
            return -1;
        }
        
        return 1;
    }
    
    private void displayFilteredDialog() {
             toolbarAction parentAction = getParentAction();
             
             JDialog initDebaterecord;
             initDebaterecord = new JDialog();
             initDebaterecord.setTitle("Enter Settings for Document");
             initDebaterecord.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
             //initDebaterecord.setPreferredSize(new Dimension(420, 300));
            
             InitDebateRecord panel = new InitDebateRecord(ooDocument, 
                     initDebaterecord, parentAction, m_subAction);
             //panel.setDialogMode(SelectorDialogModes.TEXT_INSERTION);
             //panel.setBackground(new Color(255, 255, 153));
             //initDebaterecord.setTitle("Selection Mode");
             initDebaterecord.getContentPane().add(panel);
             initDebaterecord.pack();
             initDebaterecord.setLocationRelativeTo(null);
             initDebaterecord.setVisible(true);
             initDebaterecord.setAlwaysOnTop(true);   
         
    }
    
    
    private int createSection() {
        toolbarAction parentAction;
        parentAction = getParentAction();
        if (parentAction == null ) 
            return -1;
        String sectionName = parentAction.action_naming_convention();
        if (ooDocument.hasSection(sectionName)) {
            log.debug("createSection: section already exists");
            return -2;
        } else {
            XTextContent xContent = ooDocument.addViewSection(sectionName);
            if (xContent != null)
                return 1;
        }   
        return 1;
    }

    private toolbarAction getParentAction(){
        Vector<Vector<String>> resultRows = new Vector<Vector<String>>();
        toolbarAction action = null;
        try {
            instance.Connect();
            QueryResults qr = instance.QueryResults(SettingsQueryFactory.Q_FETCH_ACTION_BY_NAME(this.m_subAction.parent_action_name()));
            instance.EndConnect();
            if (qr == null ) {
                throw new Exception ("QueryResults returned null");
            }
            if (qr.hasResults()) {
                 HashMap columns = qr.columnNameMap();
                 //child actions are present
                 //call the result nodes recursively...
                 resultRows = qr.theResults();
                 //should alwayrs return a single result
                 Vector<java.lang.String> tableRow = new Vector<java.lang.String>();
                 tableRow = resultRows.elementAt(0);
                 action = new toolbarAction(tableRow, columns );
            }
        } catch (Exception ex) {
            log.error("getParentSection: "+ ex.getMessage());
        } finally {
            return action;
        }
    }  
   }
