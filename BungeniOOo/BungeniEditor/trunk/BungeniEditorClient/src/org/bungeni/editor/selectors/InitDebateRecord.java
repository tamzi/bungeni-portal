/*
 * InitDebateRecord.java
 *
 * Created on August 27, 2007, 11:39 AM
 */

package org.bungeni.editor.selectors;

import com.sun.star.text.XText;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextCursor;
import com.sun.star.text.XTextViewCursor;
import java.awt.Container;
import java.io.File;
import java.text.DateFormat;
import java.text.Format;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import javax.swing.InputVerifier;
import javax.swing.JComponent;
import javax.swing.JDialog;
import javax.swing.JFileChooser;
import javax.swing.JFormattedTextField;
import javax.swing.JRootPane;
import javax.swing.JSpinner;
import javax.swing.JTextField;
import javax.swing.SpinnerDateModel;
import javax.swing.text.DateFormatter;
import javax.swing.text.DefaultFormatterFactory;
import javax.swing.text.MaskFormatter;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.BungeniEditorProperties;
import org.bungeni.editor.actions.toolbarSubAction;
import org.bungeni.editor.dialogs.*;
import org.bungeni.editor.fragments.FragmentsFactory;
import org.bungeni.editor.macro.ExternalMacro;
import org.bungeni.editor.macro.ExternalMacroFactory;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooDocMetadata;
import org.bungeni.utils.MessageBox;

/**
 *
 * @author  Administrator
 * This class creates the initial MastHead section
 * - creates text section with specific name
 * - allows setting various variables within that section
 * - slaps the text into the created text section
 */
public class InitDebateRecord extends selectorTemplatePanel {
   private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(InitDebateRecord.class.getName());
   private toolbarSubAction theSubAction = null;
   private ArrayList<String> enabledControls = new ArrayList<String>(); 
   private String m_strLogoPath; 
   private String m_strLogoFileName;
   
    /** Creates new form InitDebateRecord */
    public InitDebateRecord() {
        initComponents();
    }
    
    public InitDebateRecord(OOComponentHelper ooDocument, 
            JDialog parentDlg, 
            toolbarAction theAction) {
         super(ooDocument, parentDlg, theAction);
        init();       // initdebate_timeofhansard.setFormatterFactory(new DefaultFormatterFactory(dfTimeOfHansard));
        setControlModes();
        setControlData();
    
    }
    
  
      public InitDebateRecord(OOComponentHelper ooDocument, 
            JDialog parentDlg, 
            toolbarAction theAction, toolbarSubAction subAction) {
         super(ooDocument, parentDlg, theAction);
         this.theSubAction = subAction;
         init();
         setControlModes();
         setControlData();
         selectionControlModes();
      }
    
      String[] controls_ignore_list = {"btn_apply", "btn_cancel" };
      public void selectionControlModes() {
        //set selection mode control modes
         getEnabledControls();
         if (theControlMap.keySet().size() > 0 ) {
             Iterator<String> iterCtlNames = theControlMap.keySet().iterator();
             while (iterCtlNames.hasNext()) {
                 String controlname =   iterCtlNames.next();
                 if (!enabledControls.contains(controlname)) {
                     //disable all these controls
                     if (theControlMap.containsKey(controlname)) {
                         theControlMap.get(controlname).setVisible(false);
                     }
                 }
             }
         } else {
             log.debug("selectionControlModes: no controls with names were found");
         }
      }
      
      private void getEnabledControls() {
         String actionFields = theSubAction.action_fields().trim();
         if (actionFields.indexOf(";") != -1) {
            String[] enabledFields =  actionFields.split(";");
            for (int i=0; i < enabledFields.length; i++ ) {
                enabledControlNameFromAction(enabledFields[i]);
            }
         } else {
            enabledControlNameFromAction(actionFields);
         }
         //add elements from ignore list
         for (int i=0; i < this.controls_ignore_list.length ; i++ ) {
             this.enabledControls.add(controls_ignore_list[i]);
         }
      }
      
      private void enabledControlNameFromAction (String actionField) {
                 String[] control_and_name = actionField.split(":");
                 String controlName = control_and_name[0].trim()+"_"+control_and_name[1].trim();
                 this.enabledControls.add(controlName);
                 String labelName = "lbl_" + control_and_name[1];
                 this.enabledControls.add(labelName);
      }
      
      public void init(){
          
        initComponents();
        //default m_strLogoPath
        String logoPath = BungeniEditorProperties.getEditorProperty("logoPath");
        log.debug("logo path = " + logoPath);
        String strPath = DefaultInstanceFactory.DEFAULT_INSTALLATION_PATH();
        m_strLogoPath = strPath + File.separator + logoPath + File.separator + "default_logo.jpg";
        log.debug("InitDebateRecord:" + m_strLogoPath);
        dt_initdebate_timeofhansard.setModel(new SpinnerDateModel(new Date(), null, null, Calendar.HOUR));
        dt_initdebate_timeofhansard.setEditor(new JSpinner.DateEditor(dt_initdebate_timeofhansard, "HH:mm"));
        ((JSpinner.DefaultEditor)dt_initdebate_timeofhansard.getEditor()).getTextField().setEditable(false);
        this.dt_initdebate_hansarddate.setInputVerifier(new DateVerifier());
        buildComponentsArray();

      }
      
     
      
    public void setControlModes() {
        if (theMode == SelectorDialogModes.TEXT_EDIT) {
            this.lbl_initdebate_selectlogo.setVisible(false);
            this.btn_initdebate_selectlogo.setVisible(false);
        } else if (theMode == SelectorDialogModes.TEXT_INSERTION) {
            this.lbl_initdebate_selectlogo.setVisible(true);
            this.btn_initdebate_selectlogo.setVisible(true);
        } else if (theMode == SelectorDialogModes.TEXT_SELECTED_INSERT) {
            
            
        } else if (theMode == SelectorDialogModes.TEXT_SELECTED_EDIT) {
            
            
        } else {
            this.lbl_initdebate_selectlogo.setVisible(true);
            this.btn_initdebate_selectlogo.setVisible(true);
        }
    }
    
    public void setControlData() {
        try {
        //only in edit mode, only if the metadata properties exist
        if (theMode == SelectorDialogModes.TEXT_EDIT) {
            if (ooDocument.propertyExists("Bungeni_DebateOfficialDate") &&
                    ooDocument.propertyExists("Bungeni_DebateOfficialTime")) {
                ooDocMetadata meta = new ooDocMetadata(ooDocument);
                String strDate = meta.GetProperty("Bungeni_DebateOfficialDate");
                String strTime = meta.GetProperty("Bungeni_DebateOfficialTime");
                SimpleDateFormat formatter = new SimpleDateFormat ("MMMM dd yyyy");
                this.dt_initdebate_hansarddate.setDate(formatter.parse(strDate));
                SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
                this.dt_initdebate_timeofhansard.setValue(timeFormat.parse(strTime));
                }
            }
        } catch (ParseException ex) {
            log.error("SetControlData: "+ ex.getMessage());
        }
    }
    
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    // <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    private void initComponents() {
        dt_initdebate_hansarddate = new org.jdesktop.swingx.JXDatePicker();
        lbl_initdebate_hansarddate = new javax.swing.JLabel();
        lbl_initdebate_selectlogo = new javax.swing.JLabel();
        btn_initdebate_selectlogo = new javax.swing.JButton();
        lbl_initdebate_timeofhansard = new javax.swing.JLabel();
        btnApply = new javax.swing.JButton();
        btnCancel = new javax.swing.JButton();
        lbl_initdebate_setpath = new javax.swing.JLabel();
        dt_initdebate_timeofhansard = new javax.swing.JSpinner();

        dt_initdebate_hansarddate.setName("dt_initdebate_hansarddate");

        lbl_initdebate_hansarddate.setText("Hansard Date");
        lbl_initdebate_hansarddate.setName("lbl_initdebate_hansarddate");

        lbl_initdebate_selectlogo.setText("Masthead Logo");
        lbl_initdebate_selectlogo.setName("lbl_initdebate_selectlogo");

        btn_initdebate_selectlogo.setText("Select Logo...");
        btn_initdebate_selectlogo.setName("btn_initdebate_selectlogo");
        btn_initdebate_selectlogo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btn_initdebate_selectlogoActionPerformed(evt);
            }
        });

        lbl_initdebate_timeofhansard.setText("Hansard Time");
        lbl_initdebate_timeofhansard.setName("lbl_initdebate_hansardtime");

        btnApply.setText("Apply to Document ");
        btnApply.setName("btn_apply");
        btnApply.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnApplyActionPerformed(evt);
            }
        });

        btnCancel.setText("Cancel");
        btnCancel.setName("btn_cancel");
        btnCancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnCancelActionPerformed(evt);
            }
        });

        dt_initdebate_timeofhansard.setName("dt_initdebate_hansardtime");

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(layout.createSequentialGroup()
                        .add(lbl_initdebate_setpath, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 279, Short.MAX_VALUE)
                        .addContainerGap())
                    .add(lbl_initdebate_hansarddate, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 289, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, layout.createSequentialGroup()
                        .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, btn_initdebate_selectlogo, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 133, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, lbl_initdebate_selectlogo, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 163, Short.MAX_VALUE)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, lbl_initdebate_timeofhansard, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 163, Short.MAX_VALUE)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, btnApply, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 138, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(btnCancel, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 112, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addContainerGap())
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, layout.createSequentialGroup()
                        .add(dt_initdebate_hansarddate, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 279, Short.MAX_VALUE)
                        .addContainerGap())
                    .add(layout.createSequentialGroup()
                        .add(dt_initdebate_timeofhansard, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 86, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addContainerGap())))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .add(36, 36, 36)
                .add(lbl_initdebate_hansarddate)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(dt_initdebate_hansarddate, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lbl_initdebate_timeofhansard)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(dt_initdebate_timeofhansard, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lbl_initdebate_selectlogo)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btn_initdebate_selectlogo)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lbl_initdebate_setpath, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 14, Short.MAX_VALUE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(btnApply)
                    .add(btnCancel))
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents

   
    private void enableButtons(boolean state) {
        btnApply.setEnabled(state);
        btnCancel.setEnabled(state);
    }
    
    private boolean actionTypeCheck (toolbarAction action ) {
    if (action.action_type().equals("section") ) {
        if (action.action_numbering_convention().equals("single")) 
           if (ooDocument.hasSection(action.action_naming_convention())) {
                MessageBox.OK(parent, "This document already has a mast head, you cannot add a second one!");
                enableButtons(true);
                return false;
                }
        }
    return true;
    }
    
    private void btnApplyActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnApplyActionPerformed
// TODO add your handling code here:
        //get field values : 
    enableButtons(false);    
    //validate fields
    Date dtDebateDate = this.dt_initdebate_hansarddate.getDate();
   
    //order defines the nth sequence of this section
    int nOrder = theAction.action_order();
    
    //do checks if doc does not have root section, faile
    if (!ooDocument.hasSection("root")){
        MessageBox.OK(parent, "The document does not have a root section, and cannot be used!" );
        enableButtons(true);
        return;
    }
    //if (!actionTypeCheck(theAction)) {
    //    return;
    //}
     
    //adding section
    if (theSubAction == null ) {
           if (theAction.action_type().equals("section")) {
               if (!routeSectionAction()) {
                   enableButtons(true);
                   return;
               }
           }
           else if (theAction.action_type().equals("markup")) 
               markupAction();
    } else {
        processSelectionAction();
    }
    
    
     parent.dispose();
       
      
    }//GEN-LAST:event_btnApplyActionPerformed
    
    private void processSelectionAction() {
        
    }
    
    private boolean routeSectionAction () {
        if (theMode == SelectorDialogModes.TEXT_INSERTION) {
             return sectionInsertionAction();
        } else if (theMode == SelectorDialogModes.TEXT_EDIT) {
             return sectionEditAction();
        } else 
            return false;
    }
    
    private boolean sectionEditAction() {
        //if section exists
        //update fields
        String containerSection = theAction.action_naming_convention();
        if (ooDocument.hasSection(containerSection) && ooDocument.hasSection("int:masthead_datetime")) {
           //now edit the fields and set the new values
            String strDebateDate = "", strTimeOfHansard = "";   
            Date dtDebate = dt_initdebate_hansarddate.getDate();
         
            SimpleDateFormat df = new SimpleDateFormat("HH:mm");
            strTimeOfHansard =  df.format((Date)dt_initdebate_timeofhansard.getValue()); //.getText();

            SimpleDateFormat formatter = new SimpleDateFormat ("MMMM dd yyyy");
            strDebateDate = formatter.format(dtDebate);
            
            ExternalMacro setFieldValue = ExternalMacroFactory.getMacroDefinition("SetReferenceInputFieldValue");
            setFieldValue.addParameter(new String("debaterecord_official_date"));
            setFieldValue.addParameter(strDebateDate);
            setFieldValue.addParameter(new String("int:masthead_datetime"));
            ooDocument.executeMacro( setFieldValue.toString(),  setFieldValue.getParams());
            setFieldValue.clearParams();
            setFieldValue.addParameter(new String("debaterecord_official_time"));
            setFieldValue.addParameter(strTimeOfHansard);
            setFieldValue.addParameter(new String("int:masthead_datetime"));
            ooDocument.executeMacro( setFieldValue.toString(),  setFieldValue.getParams());   
            //set date and time of hansard to document
            ooDocMetadata meta = new ooDocMetadata(ooDocument);
            meta.AddProperty("Bungeni_DebateOfficialDate", strDebateDate);
            meta.AddProperty("Bungeni_DebateOfficialTime", strTimeOfHansard);
            return true;
            
        } else {
            MessageBox.OK(parent, "There is no masthead section available for editing in this document!");
            return false;
        }
    }
    private boolean sectionInsertionAction() {
        String strDebateDate = "", strTimeOfHansard = "", strLogoPath = "";   
        Date dtDebate = dt_initdebate_hansarddate.getDate();
        SimpleDateFormat df= new SimpleDateFormat("HH:mm");
        strTimeOfHansard =  df.format((Date)dt_initdebate_timeofhansard.getValue());
        SimpleDateFormat formatter = new SimpleDateFormat ("MMMM dd yyyy");
        strDebateDate = formatter.format(dtDebate);
        strLogoPath = m_strLogoPath;
        
        long sectionBackColor = 0xffffff;
        float sectionLeftMargin = (float).2;
        log.debug("section left margin : "+ sectionLeftMargin);
        //get the parent section name of this action
        //query action parents to find the parent of this action
       
        //String parentSectionName = 
        
        ExternalMacro AddSectionInsideSection = ExternalMacroFactory.getMacroDefinition("AddSectionInsideSectionWithStyle");
        AddSectionInsideSection.addParameter(ooDocument.getComponent());
        AddSectionInsideSection.addParameter("root");
        AddSectionInsideSection.addParameter(theAction.action_naming_convention());
        AddSectionInsideSection.addParameter(sectionBackColor);
        AddSectionInsideSection.addParameter(sectionLeftMargin);
        
        ooDocument.executeMacro(AddSectionInsideSection.toString(), AddSectionInsideSection.getParams());
        
        this.setSectionMetadataForAction(theAction.action_naming_convention(), theAction);
        //embed logo image
             ExternalMacro addImageIntoSection = ExternalMacroFactory.getMacroDefinition("AddImageIntoSection");
             addImageIntoSection.addParameter(theAction.action_naming_convention());
             addImageIntoSection.addParameter(m_strLogoPath);
             ooDocument.executeMacro(addImageIntoSection.toString(), addImageIntoSection.getParams());
            
        //loading the related document
            ExternalMacro insertDocIntoSection = ExternalMacroFactory.getMacroDefinition("InsertDocumentIntoSection");
            insertDocIntoSection.addParameter(ooDocument.getComponent());
            insertDocIntoSection.addParameter(theAction.action_naming_convention())  ;
            insertDocIntoSection.addParameter(FragmentsFactory.getFragment("hansard_masthead"));
            ooDocument.executeMacro(insertDocIntoSection.toString(), insertDocIntoSection.getParams());
            
            ExternalMacro setFieldValue = ExternalMacroFactory.getMacroDefinition("SetReferenceInputFieldValue");
            setFieldValue.addParameter(new String("debaterecord_official_date"));
            setFieldValue.addParameter(strDebateDate);
            setFieldValue.addParameter(new String("int:masthead_datetime"));
            ooDocument.executeMacro( setFieldValue.toString(),  setFieldValue.getParams());
            
            
            setFieldValue.clearParams();
            setFieldValue.addParameter(new String("debaterecord_official_time"));
            setFieldValue.addParameter(strTimeOfHansard);
            setFieldValue.addParameter(new String("int:masthead_datetime"));
            ooDocument.executeMacro( setFieldValue.toString(),  setFieldValue.getParams());   
        
            ooDocMetadata meta = new ooDocMetadata(ooDocument);
            meta.AddProperty("Bungeni_DebateOfficialDate", strDebateDate);
            meta.AddProperty("Bungeni_DebateOfficialTime", strTimeOfHansard);
            
            enableButtons(true);
            //MessageBox.OK(parent, "Prayers section was successfully added");
            return true;
    }
    
    private void markupAction() {
    }

    private void btn_initdebate_selectlogoActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btn_initdebate_selectlogoActionPerformed
// TODO add your handling code here:
        String logoPath = "";
        logoPath = BungeniEditorProperties.getEditorProperty("logoPath");
        log.debug("logo path = " + logoPath);
        String strPath = DefaultInstanceFactory.DEFAULT_INSTALLATION_PATH();
        logoPath = strPath + File.separator + logoPath;
        log.debug("logo path new = "+ logoPath);
        JFileChooser chooser = new JFileChooser();
        File fLogoPath = new File(logoPath);
        chooser.setCurrentDirectory(fLogoPath);
        int nReturnVal = chooser.showOpenDialog(this);
        if (nReturnVal == JFileChooser.APPROVE_OPTION) {
            File file = chooser.getSelectedFile();
            m_strLogoFileName = file.getName();
            m_strLogoPath = file.getAbsolutePath();
            lbl_initdebate_setpath.setText(m_strLogoFileName);
            //This is where a real application would open the file.
            log.debug("Opening: " + file.getName() + "." + "\n");
        } else {
            log.debug("Open command cancelled by user." + "\n");
        }
    }//GEN-LAST:event_btn_initdebate_selectlogoActionPerformed

    private void btnCancelActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnCancelActionPerformed
// TODO add your handling code here:
        parent.dispose();
    }//GEN-LAST:event_btnCancelActionPerformed


    
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnApply;
    private javax.swing.JButton btnCancel;
    private javax.swing.JButton btn_initdebate_selectlogo;
    private org.jdesktop.swingx.JXDatePicker dt_initdebate_hansarddate;
    private javax.swing.JSpinner dt_initdebate_timeofhansard;
    private javax.swing.JLabel lbl_initdebate_hansarddate;
    private javax.swing.JLabel lbl_initdebate_selectlogo;
    private javax.swing.JLabel lbl_initdebate_setpath;
    private javax.swing.JLabel lbl_initdebate_timeofhansard;
    // End of variables declaration//GEN-END:variables
  
   public class DateVerifier extends InputVerifier {
     public boolean verify(JComponent input) {
         if (input instanceof JFormattedTextField) {
             JFormattedTextField ftf = (JFormattedTextField)input;
             JFormattedTextField.AbstractFormatter formatter = ftf.getFormatter();
             if (formatter != null) {
                 String text = ftf.getText();
                 try {
                      formatter.stringToValue(text);
                      return true;
                  } catch (ParseException pe) {
                      return false;
                  }
              }
          }
          return true;
      }
      public boolean shouldYieldFocus(JComponent input) {
          return verify(input);
      }
  }
}
