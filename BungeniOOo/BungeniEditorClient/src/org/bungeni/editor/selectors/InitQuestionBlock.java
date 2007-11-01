/*
 * InitQuestionBlock.java
 *
 * Created on August 31, 2007, 4:01 PM
 */

package org.bungeni.editor.selectors;

import com.sun.star.beans.XPropertySet;
import com.sun.star.text.XTextSection;
import com.sun.star.uno.AnyConverter;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.ParseException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;
import java.util.Vector;
import javax.swing.JComponent;
import javax.swing.JDialog;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.BungeniRegistryFactory;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.db.GeneralQueryFactory;
import org.bungeni.db.QueryResults;
import org.bungeni.db.SettingsQueryFactory;
import org.bungeni.db.registryQueryDialog;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.fragments.FragmentsFactory;
import org.bungeni.editor.macro.ExternalMacro;
import org.bungeni.editor.macro.ExternalMacroFactory;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooDocMetadata;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.utils.MessageBox;
import org.safehaus.uuid.UUID;
import org.safehaus.uuid.UUIDGenerator;

/**
 *
 * @author  Administrator
 */
public class InitQuestionBlock extends selectorTemplatePanel  {
  
    registryQueryDialog rqs;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(InitQuestionBlock.class.getName());
 
    HashMap<String, String> selectionData = new HashMap<String,String>();
    String txtURI = "";
    
    String[] fldsSerialized = {"txtQuestionTitle", "txtQuestionName", "txtPersonURI", "txtAddressedTo", "txtQuestionText" };
    
    private String sourceSectionName;
    /** Creates new form InitQuestionBlock */
    public InitQuestionBlock() {
        initComponents();
    }
    public InitQuestionBlock(OOComponentHelper ooDocument, JDialog parentDlg, toolbarAction theAction) {
        super(ooDocument, parentDlg, theAction);
        initComponents();
        //above is required code....
        init();

    }
   
    
    private void init() {
        txtQuestionText.setContentType("text/html");
        setControlModes();
        setControlData();
        
    }
    
    private void initSerializationMap() {
        for (int i=0; i < fldsSerialized.length; i++) {
            theSerializationMap.put(fldsSerialized[i], "");
        }
    }
    
   
    
    
    private void setControlModes() {

        if (theMode == SelectorDialogModes.TEXT_INSERTION) {
            txtAddressedTo.setEditable(false);
            txtPersonName.setEditable(true);
            txtQuestionText.setEditable(false);
            txtQuestionTitle.setEditable(false);
            txtPersonURI.setVisible(false); lblPersonURI.setVisible(false);
            txtQuestionText.setVisible(true);
            lblQuestionText.setVisible(true);
 
            txtMessageArea.setText("You are attempting to insert a new Question, " +
                    "please select a question, and edit the name if neccessary, the " +
                    "text of the question and the metadata will be inserted into the " +
                    "document");
        } else if (theMode == SelectorDialogModes.TEXT_EDIT) {
            log.debug("InitQuestionBlock: In selectorDialogMode TEXT_EIDT ");
            txtAddressedTo.setEditable(false);
            txtPersonName.setEditable(true);
            txtQuestionText.setEditable(false);
            txtQuestionTitle.setEditable(false);
            txtPersonURI.setEditable(false);
            txtPersonURI.setVisible(true); 
            lblPersonURI.setVisible(true);
            txtQuestionText.setVisible(false);
            lblQuestionText.setVisible(false);
            scrollQuestionText.setVisible(false);
            this.btnSelectQuestion.setVisible(false);
            txtMessageArea.setText("You are attempting to Edit metadata for a question");
            
        } else if (theMode == SelectorDialogModes.TEXT_SELECTED) {
            txtAddressedTo.setEditable(false);
            lblNameOfPersonFrom.setVisible(false);
            txtPersonName.setVisible(false); //setEditable(false);
            txtQuestionText.setEditable(false);
            txtQuestionTitle.setEditable(false);    
            txtPersonURI.setVisible(false); lblPersonURI.setVisible(false);
            txtQuestionText.setVisible(true);
            lblQuestionText.setVisible(true);
            
            txtMessageArea.setText("You are in Select mode. Your hightlighted block of text will be marked up as a Question using this interface ");
                   
        }
    }
    
    public void setControlData(){
           try {
        //only in edit mode, only if the metadata properties exist
        if (theMode == SelectorDialogModes.TEXT_EDIT) {
                goEditMode();
                btnApply.setEnabled(true);
                btnCancel.setEnabled(true);
                
            }
        } catch (Exception ex) {
            log.error("SetControlData: "+ ex.getMessage());
        }
    }
    
    private boolean goEditMode() {
          String currentSectionName = "";
            currentSectionName = ooDocument.currentSectionName();
            ///do stuff for speech sections retrieve from section metadata////
            ///we probably need a associative metadata attribute factory that
            ///retrieves valid metadata elements for specific seciton types.
            ///how do you identify section types ? probably by naming convention....
            if (currentSectionName.startsWith(theAction.action_naming_convention())) {
                //this section stores MP specific metadata
                //get attribute names for mp specific metadata
                //Bungeni_SpeechMemberName
                //Bungeni_SpeechMemberURI
                //the basic macro for adding attributes takes two arrays as a parameter
                //one fr attribute names , one for attribute values
                HashMap<String,String> attribMap = ooDocument.getSectionMetadataAttributes(currentSectionName);
                this.sourceSectionName = currentSectionName;
                if (attribMap.size() > 0 ) {
                  
                    this.txtAddressedTo.setText(attribMap.get("Bungeni_QuestionAddressedTo"));
                    this.txtQuestionTitle.setText(attribMap.get("Bungeni_QuestionTitle"));
                    this.txtPersonName.setText(attribMap.get("Bungeni_QuestionMemberFrom"));
                    this.txtPersonURI.setText(attribMap.get("Bungeni_QuestionMemberFromURI"));
                 
                  return true;
                } else {
                    MessageBox.OK(parent, "No metadata has been set for this section!");
                    return false;
                }
            } else {
                MessageBox.OK(this.parent, "The Current section, "+currentSectionName + ", does not have any Speech related metadata !");
                parent.dispose();
                return false;
            }
    }
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    // <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    private void initComponents() {
        lblQuestionText = new javax.swing.JLabel();
        btnSelectQuestion = new javax.swing.JButton();
        txtQuestionTitle = new javax.swing.JTextField();
        lblQuestionTitle = new javax.swing.JLabel();
        txtPersonName = new javax.swing.JTextField();
        lblNameOfPersonFrom = new javax.swing.JLabel();
        btnApply = new javax.swing.JButton();
        btnCancel = new javax.swing.JButton();
        txtAddressedTo = new javax.swing.JTextField();
        lblQuestionAddressedTo = new javax.swing.JLabel();
        separatorLine1 = new javax.swing.JSeparator();
        scrollMessageArea = new javax.swing.JScrollPane();
        txtMessageArea = new javax.swing.JTextArea();
        lblPersonURI = new javax.swing.JLabel();
        txtPersonURI = new javax.swing.JTextField();
        scrollQuestionText = new javax.swing.JScrollPane();
        txtQuestionText = new javax.swing.JTextPane();

        lblQuestionText.setText("Question Text");

        btnSelectQuestion.setText("Select a Question...");
        btnSelectQuestion.setActionCommand("Select a Question");
        btnSelectQuestion.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnSelectQuestionActionPerformed(evt);
            }
        });

        lblQuestionTitle.setText("Question Title ");

        lblNameOfPersonFrom.setText("Edit name of Person asking Question");

        btnApply.setText("Apply");
        btnApply.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnApplyActionPerformed(evt);
            }
        });

        btnCancel.setText("Close");
        btnCancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnCancelActionPerformed(evt);
            }
        });

        lblQuestionAddressedTo.setText("Question Addressed To :");

        txtMessageArea.setBackground(new java.awt.Color(204, 204, 204));
        txtMessageArea.setColumns(20);
        txtMessageArea.setEditable(false);
        txtMessageArea.setFont(new java.awt.Font("Tahoma", 0, 11));
        txtMessageArea.setLineWrap(true);
        txtMessageArea.setRows(5);
        txtMessageArea.setWrapStyleWord(true);
        scrollMessageArea.setViewportView(txtMessageArea);

        lblPersonURI.setText("URI of Person");

        scrollQuestionText.setViewportView(txtQuestionText);

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(scrollQuestionText, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 279, Short.MAX_VALUE)
                    .add(scrollMessageArea, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 279, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, separatorLine1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 279, Short.MAX_VALUE)
                    .add(btnSelectQuestion)
                    .add(lblQuestionTitle, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 190, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(txtQuestionTitle, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 279, Short.MAX_VALUE)
                    .add(lblNameOfPersonFrom, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 264, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(txtPersonName, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 279, Short.MAX_VALUE)
                    .add(layout.createSequentialGroup()
                        .add(btnApply, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 117, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 43, Short.MAX_VALUE)
                        .add(btnCancel, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 119, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                    .add(lblPersonURI, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 138, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(txtPersonURI, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 279, Short.MAX_VALUE)
                    .add(lblQuestionAddressedTo, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 265, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(txtAddressedTo, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 279, Short.MAX_VALUE)
                    .add(lblQuestionText))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(org.jdesktop.layout.GroupLayout.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .add(scrollMessageArea, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 73, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(separatorLine1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 10, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btnSelectQuestion)
                .add(14, 14, 14)
                .add(lblQuestionTitle)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(txtQuestionTitle, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lblNameOfPersonFrom)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(txtPersonName, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lblPersonURI)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(txtPersonURI, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lblQuestionAddressedTo)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(txtAddressedTo, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lblQuestionText)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(scrollQuestionText, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 112, Short.MAX_VALUE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(btnApply)
                    .add(btnCancel))
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents

    private void btnCancelActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnCancelActionPerformed
// TODO add your handling code here:
        parent.dispose();
    }//GEN-LAST:event_btnCancelActionPerformed

    private void returnError (boolean state) {
        btnApply.setEnabled(state);
        btnCancel.setEnabled(state);
        btnSelectQuestion.setEnabled(state);
        return;
    }
    
    private void btnApplyActionPerformed(java.awt.event.ActionEvent evt)  {//GEN-FIRST:event_btnApplyActionPerformed
// TODO add your handling code here:
        returnError(false);
        
        String AddressedTo = txtAddressedTo.getText();
        String PersonName = txtPersonName.getText();
        String QuestionText = txtQuestionText.getText();
        String QuestionTitle = txtQuestionTitle.getText();
        String URI = selectionData.get("QUESTION_FROM");
        
        String QuestionId = theAction.action_naming_convention() +  selectionData.get("ID");
        log.debug("In Current Mode = " + theMode);
        //if (URI == null) URI = "";
        if (selectionData.size() == 0 ) {
            if ((theMode == SelectorDialogModes.TEXT_INSERTION)|| (theMode == SelectorDialogModes.TEXT_SELECTED)) {
            MessageBox.OK(parent, "Please select a question first!");
             returnError(true);
            return;
            }
        }
       // if (URI.length() == 0 ) {
        //    MessageBox.OK(parent, "Please select a question first !");
         //   return;
       // }
        
        try {
        if (this.theMode == SelectorDialogModes.TEXT_SELECTED) {
            //insert mode
            log.debug("in selection mode");
            //check if section by that name exists, fail immediately if true
            if (ooDocument.getTextSections().hasByName(QuestionId)) {
                MessageBox.OK(parent, "The Question: " + QuestionId+" already exists in the document !");
                returnError(true);
                return;
            }
            //now check if inside a question-section, if so fail immediately
            ExternalMacro cursorInSection = ExternalMacroFactory.getMacroDefinition("CursorInSection");
            Object retValue = ooDocument.executeMacro(cursorInSection.toString(), cursorInSection.getParams());
            String sectionNameExists = (String)retValue;
            
            dbSettings.Connect();
            QueryResults qr = dbSettings.QueryResults(SettingsQueryFactory.Q_GET_SECTION_PARENT(theAction.action_name()));
            dbSettings.EndConnect();
            String[] validParentSections = qr.getSingleColumnResult("ACTION_NAMING_CONVENTION");
            
            boolean wrongSection = true;
            int validCounter = 0;
            for ( ; validCounter < validParentSections.length; validCounter++ ) {
                if (sectionNameExists.equals(validParentSections[validCounter])) {
                    wrongSection = false;
                    break;
                }
            }
        
            
            if (wrongSection) {
                String message = "You cannot insert a question in this section, \n Please place the cursor in a different part of the document, valid sections are: ";
                for (int i=0; i < validParentSections.length; i++) {
                    message+=validParentSections[i]+ ", ";
                }
                MessageBox.OK(parent, message);
                returnError(true);
                return;
            }
            //now add the section
            ooDocument.addViewSection(QuestionId, new Integer(0xffffff));
            //now add the section Content
            MessageBox.OK(parent, "The selected text was placed in a section , and marked up " +
                    "as: " + QuestionId + "\n Please highlight the name of the person making the speech to assigne their metadata");
            returnError(true);
            
        } else if (this.theMode == SelectorDialogModes.TEXT_EDIT) {
            
            //only name can be edited nothing else....
            String sectionName = ooDocument.currentSectionName();
            //unprotect any child sections if neccessary, and reprotect them at the end
            //1 change the metadata in the parent section
            //2 change he display text in the inner section
            String childSection = ooDocument.getMatchingChildSection(sectionName, "meta-mp-");
            boolean wasProtected = false;
            if (ooDocument.isSectionProtected(childSection))
                wasProtected = true;
                
            ExternalMacro ReplaceLinkInSectionByName = ExternalMacroFactory.getMacroDefinition("ReplaceLinkInSectionByName");
            ReplaceLinkInSectionByName.addParameter(ooDocument.getComponent());
            ReplaceLinkInSectionByName.addParameter(childSection);
            ReplaceLinkInSectionByName.addParameter(new String("member_url"));
            ReplaceLinkInSectionByName.addParameter(PersonName);
            ReplaceLinkInSectionByName.addParameter( "Name: "+PersonName+ ";URI: "+this.txtPersonURI.getText());
            ReplaceLinkInSectionByName.addParameter(wasProtected);
            
            ooDocument.executeMacro(ReplaceLinkInSectionByName.toString(), ReplaceLinkInSectionByName.getParams());

            
            /////now set the section metadata///
            
            String[] attrNames = new String[1];
            String[] attrValues = new String[1];
            attrNames[0] = "Bungeni_QuestionMemberFrom";
            
            attrValues[0] = PersonName;
            log.debug("Updating person name = " + PersonName);
            /*
             *Set metadata into section
             */
            ExternalMacro SetSectionMetadata = ExternalMacroFactory.getMacroDefinition("SetSectionMetadata");
            SetSectionMetadata.addParameter(ooDocument.getComponent());
            SetSectionMetadata.addParameter(sectionName );
            SetSectionMetadata.addParameter(attrNames);
            SetSectionMetadata.addParameter(attrValues);
            ooDocument.executeMacro(SetSectionMetadata.toString(), SetSectionMetadata.getParams());
            
           
            MessageBox.OK(parent, "Metadata for the section was updated");
            returnError(true);
            parent.dispose();
            
        } else if (this.theMode == SelectorDialogModes.TEXT_INSERTION) {
            log.debug("in insert mode");
             if (ooDocument.getTextSections().hasByName(QuestionId)) {
                MessageBox.OK(parent, "The Question: " + QuestionId+" already exists in the document !");
                returnError(true);
                return;
            }
          
         
            /* 
            ExternalMacro cursorInSection = ExternalMacroFactory.getMacroDefinition("CursorInSection");
            Object retValue = ooDocument.executeMacro(cursorInSection.toString(), cursorInSection.getParams());
            String sectionNameExists = (String)retValue;
            if (sectionNameExists.startsWith("question")) {
                MessageBox.OK(parent, "You cannot insert a question inisde another, \n Please place the cursor in a different part of the document");
                returnError(true);
                return;
            }
            */
            
            /*
             *Import of Question in XHTML Format is done in the following way..
             *Question text is dumped into a temporary html file
             *the temporary html file is loaded (using loadComponentFromFile() ) into
             *the section, the OOo html importer takes care of formatting the html.
             */
             
            UUIDGenerator gen = UUIDGenerator.getInstance();
            UUID uuid = gen.generateTimeBasedUUID();
            String tmpFileName = uuid.toString().replaceAll("-", "")+".html";
            String pathToFile = DefaultInstanceFactory.DEFAULT_INSTALLATION_PATH() + File.separator+ "tmp" + File.separator;
                BufferedWriter out;
                    out = new BufferedWriter(new FileWriter(new File(pathToFile + tmpFileName)));
            out.write(QuestionText);
            out.close();
            log.debug("tmpFile Name = " + pathToFile+tmpFileName);
            //selection mode
            //insert mode
       
            //now add the section
            // commented on 13 Sep 2007
            //ooDocument.addViewSection(QuestionId, new Integer(0xffffe1));
            /*
             *Add question section into the QA section
             */
            log.debug("adding section inside section");
            long sectionBackColor = 0xffffff;
            float sectionLeftMargin = (float).2;
            log.debug("section left margin : "+ sectionLeftMargin);
            ExternalMacro AddSectionInsideSection = ExternalMacroFactory.getMacroDefinition("AddSectionInsideSectionWithStyle");
            AddSectionInsideSection.addParameter(ooDocument.getComponent());
            AddSectionInsideSection.addParameter("qa");
            AddSectionInsideSection.addParameter(QuestionId);
            AddSectionInsideSection.addParameter(sectionBackColor);
            AddSectionInsideSection.addParameter(sectionLeftMargin);
            ooDocument.executeMacro(AddSectionInsideSection.toString(), AddSectionInsideSection.getParams());
            
            //now add the section Content
            //add question title into section
            /*
             *Add hansard_question document fragment to import the question header into the 
             *document, question header - which sets question title and brief writeup about question
             */
            ExternalMacro insertDocIntoSection = ExternalMacroFactory.getMacroDefinition("InsertDocumentIntoSection");
            insertDocIntoSection.addParameter(ooDocument.getComponent());
            insertDocIntoSection.addParameter(QuestionId)   ;
            insertDocIntoSection.addParameter(FragmentsFactory.getFragment("hansard_question"));
            ooDocument.executeMacro(insertDocIntoSection.toString(), insertDocIntoSection.getParams());
            //search replace title into question title marker
            /*
             *SearchAndReplace question_title with actual question title from the swing dialog
             */
            ExternalMacro SearchAndReplace = ExternalMacroFactory.getMacroDefinition("SearchAndReplace");
            SearchAndReplace.addParameter(ooDocument.getComponent());
            SearchAndReplace.addParameter("[[QUESTION_TITLE]]");
            SearchAndReplace.addParameter(QuestionTitle);
            ooDocument.executeMacro(SearchAndReplace.toString(), SearchAndReplace.getParams());
            //add sub section (numbered serially) and 
            /*
             *Generate incrementally numbered question section, generate it based on 
             *current maximum question no. in document + 1
             */
            String newSectionName = QuestionId + "-que1" ;
            int nCounter = 1;
            while (ooDocument.getTextSections().hasByName(newSectionName) ) {
                nCounter++;
                newSectionName = QuestionId+"-que"+nCounter;
            }
            
            log.debug("addingSectionInsideSection : queston id="+QuestionId+" , new section name="+newSectionName+" , sectionBackColor="+sectionBackColor+", "+sectionLeftMargin);
            /*
             *add a question section named based on the generated name above
             *add it inside the qa section
             */
            AddSectionInsideSection.clearParams();
            sectionBackColor = 0xffffff;
            sectionLeftMargin = (float).4;
            AddSectionInsideSection.addParameter(ooDocument.getComponent());
            AddSectionInsideSection.addParameter(QuestionId);
            AddSectionInsideSection.addParameter(newSectionName);
            AddSectionInsideSection.addParameter(sectionBackColor);
            AddSectionInsideSection.addParameter(sectionLeftMargin);
            ooDocument.executeMacro(AddSectionInsideSection.toString(), AddSectionInsideSection.getParams());
            //import sub section fragment
            /*
             *Import hansard_question_text fragment into newly created section
             */
            insertDocIntoSection.clearParams();
            insertDocIntoSection.addParameter(ooDocument.getComponent());
            insertDocIntoSection.addParameter(newSectionName);
            insertDocIntoSection.addParameter(FragmentsFactory.getFragment("hansard_question_text"));
            ooDocument.executeMacro(insertDocIntoSection.toString(), insertDocIntoSection.getParams());
            //search and replace into fragment
            /*
             *Search and replace "question by" from between the beginnign and ending bookmarks
             */
            String[] arrBookmarkRanges = { "begin-question_from", "end-question_from" };
            ExternalMacro SearchAndReplace2 = ExternalMacroFactory.getMacroDefinition("SearchAndReplace2");
            SearchAndReplace2.addParameter(ooDocument.getComponent());
            SearchAndReplace2.addParameter("[[QUESTION_FROM]]");
            SearchAndReplace2.addParameter(PersonName);
            SearchAndReplace2.addParameter(arrBookmarkRanges);
            SearchAndReplace2.addParameter("Name: "+PersonName+ ";URI: "+selectionData.get("QUESTION_FROM"));
            SearchAndReplace2.addParameter("member_url");
            ooDocument.executeMacro(SearchAndReplace2.toString(), SearchAndReplace2.getParams());
            /*
             *Imported section has section called mp_name that contains the default name "mp_name"
             *rename it to the UUID based name
             */
            ExternalMacro RenameSection = ExternalMacroFactory.getMacroDefinition("RenameSection");
            RenameSection.addParameter("mp_name");
            String renamedSectionName = "meta-mp-"+uuid.toString();
            RenameSection.addParameter(renamedSectionName);
            ooDocument.executeMacro(RenameSection.toString(), RenameSection.getParams());
            
            String[] attrNames = new String[5];
            String[] attrValues = new String[5];
            attrNames[0] = "Bungeni_QuestionMemberFrom";
            attrNames[1] = "Bungeni_QuestionMemberFromURI" ;
            attrNames[2] = "Bungeni_QuestionID";
            attrNames[3] = "Bungeni_QuestionAddressedTo";
            attrNames[4] = "Bungeni_QuestionTitle";
            
            attrValues[0] = PersonName;
            attrValues[1] = URI;
            attrValues[2] = QuestionId;
            attrValues[3] = AddressedTo;
            attrValues[4] = QuestionTitle;
            /*
             *Set metadata into section
             */
            ExternalMacro SetSectionMetadata = ExternalMacroFactory.getMacroDefinition("SetSectionMetadata");
            SetSectionMetadata.addParameter(ooDocument.getComponent());
            SetSectionMetadata.addParameter(newSectionName );
            SetSectionMetadata.addParameter(attrNames);
            SetSectionMetadata.addParameter(attrValues);
            ooDocument.executeMacro(SetSectionMetadata.toString(), SetSectionMetadata.getParams());
            
            /*
             *Import html document framgment 
             */
            ExternalMacro insertHtmlDocumentIntoSection = ExternalMacroFactory.getMacroDefinition("InsertHTMLDocumentIntoSection");
            insertHtmlDocumentIntoSection.addParameter(newSectionName);
            insertHtmlDocumentIntoSection.addParameter(pathToFile+tmpFileName);
            insertHtmlDocumentIntoSection.addParameter(new String("question-text"));
            ooDocument.executeMacro(insertHtmlDocumentIntoSection.toString(), insertHtmlDocumentIntoSection.getParams() );
            
            //MessageBox.OK(parent, "Finished Importing !");
            returnError(true);
            parent.dispose();
        }   
        
    // End of variables declaration                      
            } catch (IOException ex) {
                    log.error("InitQuestionBlock: " +ex.getMessage());
                 returnError(true);
            }
           
    }//GEN-LAST:event_btnApplyActionPerformed

    private void btnSelectQuestionActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnSelectQuestionActionPerformed
// TODO add your handling code here:
        rqs = new registryQueryDialog("Select A Question", "Select * from questions", parent);
        rqs.show();
        log.debug("Moved on before closing child dialog");
        selectionData = rqs.getData();
        if (selectionData.size() > 0 ) {
            Set keyset = selectionData.keySet();
            log.debug("selected keyset size = " + keyset.size());
            txtQuestionTitle.setText(selectionData.get("QUESTION_TITLE"));
            txtAddressedTo.setText(selectionData.get("QUESTION_TO"));
            //resolve person name URI to registry entry
            dbInstance.Connect();
            QueryResults rs = dbInstance.QueryResults(GeneralQueryFactory.Q_FETCH_PERSON_BY_URI(selectionData.get("QUESTION_FROM")));
            dbInstance.EndConnect();
            String fullName = "";
            if (rs.hasResults()) {
                
                String[] firstName = rs.getSingleColumnResult("FIRST_NAME");
                String[] lastName = rs.getSingleColumnResult("LAST_NAME");
                if (firstName != null )
                    fullName = firstName[0];
                if (lastName != null ) 
                    fullName += " " + lastName[0];
                
            }
            txtPersonName.setText(fullName);
            
            //
            txtQuestionText.setText(selectionData.get("QUESTON_TEXT"));
            //fillDocument();
        } else {
            log.debug("selected keyset empty");
        }
    }//GEN-LAST:event_btnSelectQuestionActionPerformed

    private void fillDocument(){
           //check if section exists
           //if already exists, bail out with error message
           //else
           //create section with appropriate name
           //set section metadata
           //fill up respetive information on the document.
           String newSectionName = "";
           //must check for action type too, but for testing purposes ignored...
           newSectionName = theAction.action_naming_convention()+"-"+selectionData.get("ID");
           if (ooDocument.getTextSections().hasByName(newSectionName)) {
               MessageBox.OK("There is Question : " + selectionData.get("ID")+" has already been imported into the document!" );
               return;
           }
           //now create section
          ooDocument.addViewSection(newSectionName); 
        
    }
   

   
    
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnApply;
    private javax.swing.JButton btnCancel;
    private javax.swing.JButton btnSelectQuestion;
    private javax.swing.JLabel lblNameOfPersonFrom;
    private javax.swing.JLabel lblPersonURI;
    private javax.swing.JLabel lblQuestionAddressedTo;
    private javax.swing.JLabel lblQuestionText;
    private javax.swing.JLabel lblQuestionTitle;
    private javax.swing.JScrollPane scrollMessageArea;
    private javax.swing.JScrollPane scrollQuestionText;
    private javax.swing.JSeparator separatorLine1;
    private javax.swing.JTextField txtAddressedTo;
    private javax.swing.JTextArea txtMessageArea;
    private javax.swing.JTextField txtPersonName;
    private javax.swing.JTextField txtPersonURI;
    private javax.swing.JTextPane txtQuestionText;
    private javax.swing.JTextField txtQuestionTitle;
    // End of variables declaration//GEN-END:variables
    
}
