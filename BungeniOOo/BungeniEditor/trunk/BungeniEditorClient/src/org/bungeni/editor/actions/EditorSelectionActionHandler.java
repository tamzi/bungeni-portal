/*
 * EditorSelectionActionHandler.java
 *
 * Created on December 2, 2007, 10:58 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.actions;

import com.sun.star.text.XText;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextSection;
import com.sun.star.text.XTextViewCursor;
import java.awt.Component;
import java.util.HashMap;
import java.util.Vector;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.WindowConstants;
import org.apache.log4j.Logger;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.db.QueryResults;
import org.bungeni.db.SettingsQueryFactory;
import org.bungeni.editor.selectors.InitDebateRecord;
import org.bungeni.editor.selectors.SelectorDialogModes;
import org.bungeni.error.BungeniError;
import org.bungeni.error.ErrorMessages;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.utils.CommonPropertyFunctions;
import org.bungeni.utils.MessageBox;

/**
 *
 * @author Administrator
 */
public class EditorSelectionActionHandler implements IEditorActionEvent {
   private static org.apache.log4j.Logger log = Logger.getLogger(EditorSelectionActionHandler.class.getName());
   private OOComponentHelper ooDocument;
   private toolbarSubAction m_subAction;   
   private JFrame parentFrame;
   private toolbarAction m_parentAction;
   private BungeniClientDB dbSettings;
   private ErrorMessages errorMsgObj = new ErrorMessages();
    /** Creates a new instance of EditorSelectionActionHandler */
    public EditorSelectionActionHandler() {
           
        dbSettings = new BungeniClientDB (DefaultInstanceFactory.DEFAULT_INSTANCE(), DefaultInstanceFactory.DEFAULT_DB());
      
    }

    public void doCommand(OOComponentHelper ooDocument, toolbarAction action, JFrame c) {
    
    }

    public void doCommand(OOComponentHelper ooDocument, toolbarSubAction action, JFrame c) {
        //the modes available are either text_select_insert or edit
        this.ooDocument = ooDocument;
        this.parentFrame = c;
        this.m_subAction = action;
        this.m_parentAction = getParentAction();
        this.m_parentAction.setSelectorDialogMode(action.getSelectorDialogMode());
        
        int nValid = -1;
        //all error returns < 0 indicate failure and stoppagte
        //all error returns > 0 indicate that processing can go ahead
        if ((nValid = _validateAction()) < 0 ) 
        {
            log.debug("EditorSelectionActionHandler : invalid action in this context");
            switch (nValid) {
                case BungeniError.DOCUMENT_ROOT_DOES_NOT_EXIST :
                    MessageBox.OK(errorMsgObj.toString());
                    return;
                case -1:
                     MessageBox.OK("There was no text selected in the document");
                 break;
                case -2:
                    MessageBox.OK("This selection needs to be enclosed in a system container, \n The system container already exists in the document, please cut and paste the selection within the boudaries of the section called :" + m_subAction.system_container() +" \n This section has been highlighted for your convenience.");
                    selectContainer(m_subAction.system_container());
                break;
                case -3:
                    MessageBox.OK("This selection needs to be enclosed in a system container, \n Please first generate the system container by using the 'Generate system container' option from the context menu");
                 break;   
                case -4:
                     MessageBox.OK("The selection is already in the correct system container!");
                  break;
                case -5:
                     MessageBox.OK("The document has the correct system container: "+ m_subAction.system_container()+ " \n" +
                        "but the selection is not within the system container, please the selection within the boudaries of the section called :" + m_subAction.system_container() +" \n" +
                        " This section has been highlighted for your convenience.");
                  break;
                case -6:
                     MessageBox.OK("The selection is not within the mandatory container - "+ m_parentAction.action_naming_convention());
                  break;   
                case -7:
                     MessageBox.OK("The selection to be marked up is within the wrong container, please cut and paste it within the correct container :"+ m_parentAction.action_numbering_convention());
                  break;   
                case -8:
                     MessageBox.OK("The selection and its system container need to be moved within the correct parent container :" + m_parentAction.action_naming_convention());
                  break;   
                case -9:
                     MessageBox.OK("The selection's system container is not within a valid parent section: "+ m_parentAction.action_naming_convention());
                  break;   
                case -10:
                    MessageBox.OK("This section needs to be created within the root section: " + CommonPropertyFunctions.getDocumentRootSection());
                  break;
            }
            return;
        }
        int nRouteAction = _routeAction(nValid);
    
    }
    
     private int _routeAction(int nValidationErrorCode){
        int nRouteAction = BungeniError.METHOD_NOT_IMPLEMENTED;
         switch (m_subAction.getSelectorDialogMode()) {
             case DOCUMENT_LEVEL_ACTION:
                 nRouteAction = routeAction_DocumentLevelAction(nValidationErrorCode);
                 break;
             case TEXT_SELECTED_EDIT:
                 nRouteAction = routeAction_TextSelectedEditAction(nValidationErrorCode);
                 break;
             case TEXT_SELECTED_INSERT:
                 nRouteAction = routeAction_TextSelectedInsertAction(nValidationErrorCode);
                 break;
             case TEXT_SELECTED_SYSTEM_ACTION:
                 nRouteAction = routeAction_TextSelectedSystemAction(nValidationErrorCode);
                 break;
         
         }
        
        return nRouteAction;
    }
    
     private int routeAction_TextSelectedInsertAction( int nValidationErrorCode) {
         return 0;
     }
    
     private int routeAction_TextSelectedEditAction( int nValidationErrorCode) {
         return 0;
     }
    
     
     private int routeAction_TextSelectedSystemAction( int nValidationErrorCode) {
         return 0;
     }

     private int routeAction_DocumentLevelAction( int nValidationErrorCode) {
          //actions operate on the whole document
        int nActionDocument = -1;
        if (m_subAction.sub_action_name().equals("init_document")) {
            nActionDocument = routeAction_DocumentLevelAction_InitDocument(nValidationErrorCode);
            return nActionDocument;
        } else  {
            log.debug("validateAction_DocumentLevelAction() : method not implemented");
            return BungeniError.METHOD_NOT_IMPLEMENTED;
        }
     
     }
     
     private int routeAction_DocumentLevelAction_InitDocument(int nValidationErrorCode){
         int nRouteActionReturnValue = BungeniError.METHOD_NOT_IMPLEMENTED;
         switch (nValidationErrorCode) {
             case BungeniError.DOCUMENT_LEVEL_ACTION_RO0T_EXISTS:
                 
                //document has root section 
                 break;
             case BungeniError.DOCUMENT_LEVEL_ACTION_ROOT_DOES_NOT_EXIST:
                 //document does not have route section
                 
                 break;
                 
             
         }
         return nRouteActionReturnValue;
     }
     
    
     
    private void selectContainer(String containerName) {
                XTextSection systemContainer = ooDocument.getSection(containerName);
                ooDocument.getViewCursor().gotoRange(systemContainer.getAnchor(), true);
    }
    
    private void routeAction() {
            if (m_subAction.getSelectorDialogMode() == SelectorDialogModes.TEXT_SELECTED_SYSTEM_ACTION) {
                routeAction_SystemAction();
            } else {
                routeAction_Masthead();    
            }
    }

    private void routeAction_SystemAction(){
        String systemContainerName = m_subAction.system_container();
        if (!action_createSystemContainerFromSelection(ooDocument, systemContainerName) ) {
           log.debug("routeAction_SystemAction: creating system container from selection failed!");
        }
    }
    
    private boolean action_createSystemContainerFromSelection(OOComponentHelper ooDoc, String systemContainerName){
        boolean bResult = false; 
        try {
        XTextViewCursor xCursor = ooDocument.getViewCursor();
        XText xText = xCursor.getText();
        XTextContent xSectionContent = ooDocument.createTextSection(systemContainerName, (short)1);
        xText.insertTextContent(xCursor, xSectionContent , true); 
        bResult = true;
        } catch (com.sun.star.lang.IllegalArgumentException ex) {
            bResult = false;
            log.error("in addTextSection : "+ex.getLocalizedMessage(), ex);
        }  finally {
            return bResult;
        }
    }
    
    
    private void routeAction_Masthead(){
            if (m_subAction.sub_action_name().equals("selectlogo")) {
                parentCheck();
                displayFilteredDialog();
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
                displayFilteredDialog();
            }
   
    }
   
    private int parentCheck(){
        if (!ooDocument.hasSection(m_parentAction.action_naming_convention())) {
            log.debug("parentCheck: parent container does not exist");
            return -1;
        } 
       return 1; 
    }
    
    
    /*
     *
     *actions are validated in the following order:
     *validateAction() { 
     *  isTextSelected()
     *  systemContainerCheck()
     *  parentContainerCheck()
     */
    /*
    private int validateAction(){
        //selection check
        boolean bSelected=false;
        bSelected = ooDocument.isTextSelected();
        if (!bSelected )
        {
            log.debug("validateAction: nothing was selected ");
            return -1;
        }
        // this is a system container generation action
            
        int nRet = systemContainerCheck(); 
        if (nRet == -2 ) {
            log.debug("validateAction: system container check failed, but system container exists in document");
            return nRet;
        } else if (nRet == -3) {
            log.debug("validateAction: system container check failed, but system container does not exist in document");
            return nRet;
        } else if (nRet == -4) {
            log.debug("validateAction: already in the corect system container");
            return nRet;
        } else if (nRet == -5 ){
            log.debug("validateAction: not in the system contianer, but the document has a system container");
            return nRet;
        }
        
        //parent container check
       
        nRet =  parentContainerCheck();
        if (nRet == -6) {
            log.debug("validateAction: no parent container");
            return nRet;
        }
        if (nRet == -7) {
            log.debug("validateAction: in the wrong section ");
            return nRet;
        }
        if (nRet == -8) {
            log.debug("validateAction: wrong parent section for system container ");
            return nRet;
        }
        if (nRet == -9) {
            log.debug("validateAction: no parent section for system container");
            return nRet;
        }
        if (nRet == -10) {
            return nRet;
        }       
        return 1;
    }
*/
    /*
    private int systemContainerCheck() {
        if (this.m_subAction.system_container().length() == 0 ) {
            //there is no system container 
            return 0;
        }
        //check if this is the creation action for  asystem container, all other actions default to the else
        if (m_subAction.getSelectorDialogMode() == SelectorDialogModes.TEXT_SELECTED_SYSTEM_ACTION ) {
            //generate system container over selection
            if (ooDocument.hasSection(m_subAction.system_container())) {
                if (ooDocument.currentSectionName().equals(m_subAction.system_container())) {
                    //already in the correct system container
                    return -4;
                }
                //document has system container, but the selection isnt in the system container
                return -5;
            } else 
                //document does not have system container, selection can be placed within system container.
                return 0;
        } else {
        //get the current section name
        String currentSectionname = ooDocument.currentSectionName();
        if (currentSectionname.equals(m_subAction.system_container())) {
            return 0;
        } else {
            if (ooDocument.hasSection(m_subAction.system_container())) 
                return -2;
             else 
                return -3;
        }
        } 
    }
   */
    /*
     *
     *
     *
If documentHasNoRootSection
	error root section
	return

If documentHasRootSection
	if NoSelectedText
	 	error selected text
	 	return
	 if selectedText
	 	markupSelectedText()
	 	

if markupSelectedText():
	if action requires SystemSection:
		lookup full hierarchy for markupAction
		if (actionHierarchy == sectionHierarchy) 
			do markupAction()
			exit
		if (actionHierarchy <> sectionHierarchy)
			error hierarchy
			disply valid hierarchy 
			exit
	if action does not require SystemSection:
		lookup full hierarchy for markupAction
		if (actionHierarchy == sectionHierarchy) 
			do markupAction()
			exit
		if (actionHierarchy <> sectionHierarchy)
			error hierarchy
			disply valid hierarchy 
			exit
			 	
     *			 	
     *
     *
     */
    
     private int _validateAction(){
        int nValidateAction = BungeniError.METHOD_NOT_IMPLEMENTED;
         switch (m_subAction.getSelectorDialogMode()) {
             case DOCUMENT_LEVEL_ACTION:
                 nValidateAction = validateAction_DocumentLevelAction();
                 break;
             case TEXT_SELECTED_EDIT:
                 nValidateAction = validateAction_TextSelectedEditAction();
                 break;
             case TEXT_SELECTED_INSERT:
                 nValidateAction = validateAction_TextSelectedInsertAction();
                 break;
             case TEXT_SELECTED_SYSTEM_ACTION:
                 nValidateAction = validateAction_TextSelectedSystemAction();
                 break;
         
         }
         /*
         if (m_subAction.action_type().equals("document_action")) {
             if (m_subAction.sub_action_name().equals("init_document")) {
                 String rootContainerName = CommonPropertyFunctions.getDocumentRootSection();
                 if (ooDocument.hasSection(rootContainerName)) {
                    return BungeniError.DOCUMENT_ROOT_EXISTS;
                 } else {
                     return BungeniError.DOCUMENT_ROOT_DOES_NOT_EXIST;
                 }
                 
                 if (ooDocument.hasSection(Commp))
                    int nRet = MessageBox.Confirm((Component)parentFrame , "This will initalize the document " +
                            "by create a root container for the content. Are you sure you want to do this ?", "Confirm");
                    if (nRet == JOptionPane.YES_OPTION) {
                        //create root container
                        action_createSpannedRootContainer();
                    }   else if (nRet == JOptionPane.NO_OPTION) {
                        //dont create root container
                        
                    }      
             }
         }
         
         
        int nRootContainerCheck = _rootContainerCheck();
        if (nRootContainerCheck == BungeniError.DOCUMENT_ROOT_DOES_NOT_EXIST) {
            log.debug("validateaction: no root container");
            return nRootContainerCheck;
        }
        
         //selection check
        boolean bSelected=false;
        bSelected = ooDocument.isTextSelected();
        if (!bSelected ) {
            log.debug("validateAction: nothing was selected ");
            return BungeniError.NO_TEXT_SELECTED;
        }
      
        if (m_subAction.system_container().length() == 0 ) {
            //system container not required
            //parentCheckWithSystemContainer();
        } else {
            //system container required
        //    parentCheckWithoutSystemContainer();
        } 
          *
          */
     return nValidateAction
             ;
     }
     
    private int _rootContainerCheck(){
        //check if root container exists
        //if it doesnt exist fail
         String documentRoot = CommonPropertyFunctions.getDocumentRootSection();
         if (ooDocument.hasSection(documentRoot)) {
             return BungeniError.DOCUMENT_ROOT_EXISTS;
         } else {
             this.errorMsgObj.add("The document needs to be initialized correctly with a main container.\n" +
                     "Please initialize the document by using the 'Initialize Document' action");
             return BungeniError.DOCUMENT_ROOT_DOES_NOT_EXIST;
         }
    }
    
    
    private int _systemContainerCheck(){
        String systemContainer = m_subAction.system_container();
        String currentSectionname = ooDocument.currentSectionName();
        if (systemContainer.length() == 0 ) {
            //there is no system container 
            return  BungeniError.SYSTEM_CONTAINER_NOT_REQD;
        } 
        //check if document has section
        boolean bHasSystemContainer = ooDocument.hasSection(systemContainer) ;
        if (bHasSystemContainer) {
            //is the current section == the system container
            if (systemContainer.equals(currentSectionname)) {
               //selection is within the correct system container....
                return BungeniError.SYSTEM_CONTAINER_CHECK_OK;
            } else {
                return BungeniError.SYSTEM_CONTAINER_WRONG_POSITION;
            }
        } else {
            //no system container present...
            //get full container hierarchy
           return BungeniError.SYSTEM_CONTAINER_NOT_PRESENT;
        }
   }

    private int _parentContainerCheck(int systemContainerCheck ) {
        switch (systemContainerCheck) {
            case BungeniError.SYSTEM_CONTAINER_NOT_PRESENT :
                //system container was not present
                _parentContainerCheck_MissingSystemContainer();
                break;
            case BungeniError.SYSTEM_CONTAINER_NOT_REQD:
                _parentContainerCheck_SystemContainerNotReqd();
                break;
            case BungeniError.SYSTEM_CONTAINER_WRONG_POSITION:
                _parentContainerCheck_NotInSystemContainer();
                break;
            case BungeniError.SYSTEM_CONTAINER_CHECK_OK:
                _parentContainerCheck_SystemContainerOK();
                break;
 
        }
        
        return 0;
    }
    
    private int _parentContainerCheck_MissingSystemContainer() {
        //add error message for missing system container
        //then run parentContainerCheckSystemContainerOK
        return 0;
    }
    
    private int _parentContainerCheck_SystemContainerOK() {
        //system container was ok. 
        //we need to check the placement of the system container with respect to the parent action
        //first we determine the correct parent hierarchy for the action.
        
        String qrygetParents = SettingsQueryFactory.Q_FETCH_PARENT_ACTIONS(m_parentAction.action_name());
        Vector<Vector<String>> resultRows = new Vector<Vector<String>>();
        String currentSystemContainer = ooDocument.currentSectionName();
        
        QueryResults qrParents = dbSettings.QueryResults(qrygetParents);
        if (qrParents != null ) {
            if (qrParents.hasResults()) {
                //get all the possible parent names
                String[] theActionNames = qrParents.getSingleColumnResult("ACTION_NAME");
                String[] theActionDisplayText = qrParents.getSingleColumnResult("ACTION_DISPLAY_TEXT");
                String[] theActionSectionType = qrParents.getSingleColumnResult("ACTION_SECTION_TYPE");
                //check if the hierarchy of parents = hierachy of sections in the document.
                XTextSection theSystemSection = ooDocument.getSection(currentSystemContainer);
                this.errorMsgObj.start("You need to create the parent containers before marking up using this action.\n");
                this.errorMsgObj.add("The following actions can be used to create valid parent containers: \n");
                for (int i=0; i < theActionNames.length ; i++ ) {
                    this.errorMsgObj.add(" -- "+ theActionDisplayText[i]);
                }
            }
        }
        return 0;
    }

    private int _parentContainerCheck_NotInSystemContainer() {
        return 0;
    }

    private int _parentContainerCheck_SystemContainerNotReqd() {
        
        return 0;
    }
    
    private int validateSectionHierarchy(){
        return 0;
    }
    
    private int parentContainerCheck() {
        String parentContainer = "";
        String systemContainerName =  m_subAction.system_container();
       
        /*
        if (m_subAction.getSelectorDialogMode() == SelectorDialogModes.TEXT_SELECTED_SYSTEM_ACTION ) {
            return 0;
        }
        */
        
        //ugly check below...make this more modular...
        if (m_subAction.sub_action_order().equals("0")) {
            if (m_subAction.sub_action_name().equals("section_creaton")) {
                String currentSection = ooDocument.currentSectionName();
                String documentRoot = CommonPropertyFunctions.getDocumentRootSection();
                if (currentSection.equals(documentRoot)) {
                    return 0;
                } else 
                    return -10;
            }
        }
        
        if (systemContainerName.length() > 0 ) {
            XTextSection xSysContainer = ooDocument.getSection(systemContainerName);
            XTextSection xSysParent = xSysContainer.getParentSection();
            if (xSysParent == null ) {
                //no parent section for system container
                return -9;
            } else {
                //parent section was not null
                String sectionName = ooQueryInterface.XNamed(xSysParent).getName();
                String parentActionPrefix  = this.m_parentAction.action_naming_convention();
                if (sectionName.startsWith(parentActionPrefix)) {
                    return 0;
                } else
                    return -8; //wrong parent section for system container
            }
        } else {
            //no system container
            //so get current section
            String currentSection = ooDocument.currentSectionName();
            if (currentSection.length() == 0) {
                //not in a section, return error
                return -6;
            } else {
                //current section is a section ...check if it is the right one....
                String parentNamePrefix = this.m_parentAction.action_naming_convention();
                if (parentNamePrefix.startsWith(currentSection)) {
                    return 0;
                } else {
                    //wrongly placed needs to be in correct section
                    return -7;
                }
            }
        }
       
    }
     
    
    private void displayFilteredDialog() {
             try {
             log.debug("displayFilteredDialog: subAction name = "+ this.m_subAction.sub_action_name());
             // toolbarAction parentAction = getParentAction();
             
             JDialog initDebaterecord;
             initDebaterecord = new JDialog();
             initDebaterecord.setTitle("Enter Settings for Document");
             initDebaterecord.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
             //initDebaterecord.setPreferredSize(new Dimension(420, 300));
            
             InitDebateRecord panel = new InitDebateRecord(ooDocument, 
                     initDebaterecord, m_parentAction, m_subAction);
             //panel.setDialogMode(SelectorDialogModes.TEXT_INSERTION);
             //panel.setBackground(new Color(255, 255, 153));
             //initDebaterecord.setTitle("Selection Mode");
             initDebaterecord.getContentPane().add(panel);
             initDebaterecord.pack();
             initDebaterecord.setLocationRelativeTo(null);
             initDebaterecord.setVisible(true);
             initDebaterecord.setAlwaysOnTop(true);   
             } catch (Exception ex) {
                 log.error("displayFilteredDialog : " + ex.getMessage());
                 log.error("displayFilteredDialog: stack trace :  \n" + org.bungeni.utils.CommonExceptionUtils.getStackTrace(ex));
             }
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
            dbSettings.Connect();
            QueryResults qr = dbSettings.QueryResults(SettingsQueryFactory.Q_FETCH_ACTION_BY_NAME(this.m_subAction.parent_action_name()));
            dbSettings.EndConnect();
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

    private int validateAction_DocumentLevelAction() {
        //actions operate on the whole document
        int nActionDocument = -1;
        if (m_subAction.sub_action_name().equals("init_document")) {
            nActionDocument = validateAction_DocumentLevelAction_InitDocument();
            return nActionDocument;
        } else  {
            log.debug("validateAction_DocumentLevelAction() : method not implemented");
            return BungeniError.METHOD_NOT_IMPLEMENTED;
        }
    }
   
    private int validateAction_DocumentLevelAction_InitDocument() {
        String rootSectionname = CommonPropertyFunctions.getDocumentRootSection();
        if (ooDocument.hasSection(rootSectionname)){
            return BungeniError.DOCUMENT_LEVEL_ACTION_RO0T_EXISTS;
        } else {
            return BungeniError.DOCUMENT_LEVEL_ACTION_ROOT_DOES_NOT_EXIST;
        }
    }

    private int validateAction_TextSelectedEditAction() {
        
        return 0;
    }

    private int validateAction_TextSelectedInsertAction() {
        return 0;
    }

    private int validateAction_TextSelectedSystemAction() {
        return 0;
    }

    private int action_initDocument(){
        return 0;
    }

   }
