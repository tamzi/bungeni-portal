/*
 * DebateRecordMetadata.java
 *
 * Created on November 4, 2008, 1:43 PM
 */

package org.bungeni.editor.dialogs.debaterecord;

import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.Dimension;
import java.io.File;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JRootPane;
import javax.swing.JSpinner;
import javax.swing.SpinnerDateModel;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.editor.BungeniEditorProperties;
import org.bungeni.editor.BungeniEditorPropertiesHelper;
import org.bungeni.editor.selectors.SelectorDialogModes;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooDocMetadata;
import org.bungeni.ooo.transforms.impl.BungeniTransformationTargetFactory;
import org.bungeni.ooo.transforms.impl.IBungeniDocTransform;
import org.bungeni.utils.BungeniFileSavePathFormat;
import org.bungeni.utils.MessageBox;

/**
 *
 * @author  undesa
 */
public class DebateRecordMetadata extends javax.swing.JPanel {

    
    OOComponentHelper ooDocument  = null;
    JFrame parentFrame = null;
    SelectorDialogModes dlgMode = null;
    
    class CountryCode {
        String countryCode;
        String countryName;
        
        CountryCode(String countryC, String countryN) {
            countryCode = countryC;
            countryName = countryN;
        }
        
        @Override
        public String toString(){
            return countryName;
        }
        
    }
    
    ArrayList<CountryCode> countryCodes = new ArrayList<CountryCode>(0);

    class LanguageCode {
        String languageCode;
        String languageName;
        
        LanguageCode(String langC, String langN) {
            languageCode = langC;
            languageName = langN;
        }
        
        @Override
        public String toString(){
            return languageName;
        }
    }

        ArrayList<LanguageCode> languageCodes = new ArrayList<LanguageCode>(0);

    private void initMetadata(){
        countryCodes.add(new CountryCode("ken", "Kenya"));
        countryCodes.add(new CountryCode("uga", "Uganda"));
        countryCodes.add(new CountryCode("tza", "Tanzania"));
        
        languageCodes.add(new LanguageCode("eng", "English"));
        languageCodes.add(new LanguageCode("fra", "French"));
        
    }
    
    private CountryCode findCountryCode (String countryCode) {
        for (CountryCode c : countryCodes) {
            if (c.countryCode.equals(countryCode)) {
                return c;
            }
        }
        return null;
    }
    
    private LanguageCode findLanguageCode(String langCode) {
        for (LanguageCode lc : languageCodes){
            if (lc.languageCode.equals(langCode)){
                return lc;
            }
        }
        return null;
    }
    private void initControls(){
        String popupDlgBackColor = BungeniEditorProperties.getEditorProperty("popupDialogBackColor");
        this.setBackground(Color.decode(popupDlgBackColor));
        cboCountry.setModel(new DefaultComboBoxModel(countryCodes.toArray()));
        cboLanguage.setModel(new DefaultComboBoxModel(languageCodes.toArray()));
         dt_initdebate_timeofhansard.setModel(new SpinnerDateModel(new Date(), null, null, Calendar.HOUR));
        dt_initdebate_timeofhansard.setEditor(new JSpinner.DateEditor(dt_initdebate_timeofhansard, BungeniEditorProperties.getEditorProperty("metadataTimeFormat")));
        ((JSpinner.DefaultEditor)dt_initdebate_timeofhansard.getEditor()).getTextField().setEditable(false);
 
    }
    
    public Component findComponentByName(Container container, String componentName) {
  for (Component component: container.getComponents()) {
    if (componentName.equals(component.getName())) {
      return component;
    }
    if (component instanceof JRootPane) {
      // According to the JavaDoc for JRootPane, JRootPane is
      // "A lightweight container used behind the scenes by JFrame,
      // JDialog, JWindow, JApplet, and JInternalFrame.". The reference
      // to the RootPane is set up by implementing the RootPaneContainer
      // interface by the JFrame, JDialog, JWindow, JApplet and
      // JInternalFrame. See also the JavaDoc for RootPaneContainer.
      // When a JRootPane is found, recurse into it and continue searching.
      JRootPane nestedJRootPane = (JRootPane)component;
      return findComponentByName(nestedJRootPane.getContentPane(), componentName);
    }
    if (component instanceof JPanel) {
      // JPanel found. Recursing into this panel.
      JPanel nestedJPanel = (JPanel)component;
      return findComponentByName(nestedJPanel, componentName);
    }
  }
  return null;
}

private void applySelectedMetadata(BungeniFileSavePathFormat spf){
    
    String sParliamentID = this.BungeniParliamentID.getText();
    String sParliamentSitting = this.txtParliamentSitting.getText();
    String sParliamentSession = this.txtParliamentSession.getText();
    CountryCode selCountry = (CountryCode)this.cboCountry.getSelectedItem();
    LanguageCode selLanguage = (LanguageCode) this.cboLanguage.getSelectedItem();
    ooDocMetadata docMeta = new ooDocMetadata(ooDocument);
    //get the official time
        SimpleDateFormat tformatter = new SimpleDateFormat (BungeniEditorProperties.getEditorProperty("metadataTimeFormat"));
       Object timeValue = this.dt_initdebate_timeofhansard.getValue();
       Date hansardTime = (Date) timeValue;
    final String strTimeOfHansard = tformatter.format(hansardTime);
    //get the offical date
       SimpleDateFormat dformatter = new SimpleDateFormat (BungeniEditorProperties.getEditorProperty("metadataDateFormat"));
       final String strDebateDate = dformatter.format( dt_initdebate_hansarddate.getDate());
    
    
    docMeta.AddProperty("BungeniParliamentID", sParliamentID);
    docMeta.AddProperty("BungeniParliamentSitting", sParliamentSitting);
    docMeta.AddProperty("BungeniParliamentSession", sParliamentSession);
    docMeta.AddProperty("BungeniCountryCode", selCountry.countryCode);
    docMeta.AddProperty("BungeniLanguageCode", selLanguage.languageCode);
    docMeta.AddProperty("BungeniDebateOfficialDate", strDebateDate);
    docMeta.AddProperty("BungeniDebateOfficialTime", strTimeOfHansard);

    spf.setSaveComponent("DocumentType", BungeniEditorPropertiesHelper.getCurrentDocType());
    spf.setSaveComponent("CountryCode", selCountry.countryCode);
    spf.setSaveComponent("LanguageCode", selLanguage.languageCode);
    Date dtHansardDate = dt_initdebate_hansarddate.getDate();
    GregorianCalendar debateCal = new GregorianCalendar();
    debateCal.setTime(dtHansardDate);
    spf.setSaveComponent("Year", debateCal.get(Calendar.YEAR));
    spf.setSaveComponent("Month", debateCal.get(Calendar.MONTH));
    spf.setSaveComponent("Day", debateCal.get(Calendar.DAY_OF_MONTH));
    spf.setSaveComponent("FileName", spf.getFileName());
}    

private void saveDocumentToDisk(BungeniFileSavePathFormat spf){
            
        String exportPath = BungeniEditorProperties.getEditorProperty("defaultSavePath");
        exportPath = exportPath.replace('/', File.separatorChar);
        exportPath = DefaultInstanceFactory.DEFAULT_INSTALLATION_PATH() + File.separator + exportPath + File.separator + spf.getSavePath();
        File fDir = new File(exportPath);
        if (!fDir.exists()) {
            //if path does not exist, create it
            fDir.mkdirs();
        }
        
        
        String fileFullPath = "";
        fileFullPath = exportPath + File.separator + spf.getFileName();
        File fFile = new File(fileFullPath);
        //MessageBox.OK(parentFrame, exportPath);
        String exportPathURL = "";
            exportPathURL = fFile.toURI().toString();
        HashMap<String,Object> params = new HashMap<String,Object>();
        params.put("StoreToUrl", exportPathURL);
        IBungeniDocTransform idocTrans = BungeniTransformationTargetFactory.getDocTransform("ODT");
        idocTrans.setParams(params);
        boolean bState= idocTrans.transform(ooDocument);
        if (bState) 
            MessageBox.OK(parentFrame, "Document was Saved!");
        else
            MessageBox.OK(parentFrame, "The Document could not be saved!");
   
}
    

class FieldAssociation {
        String mapKey;
        String fieldName;
        String labelName;
    }
    
    /** Creates new form DebateRecordMetadata */
    public DebateRecordMetadata(OOComponentHelper ooDoc, JFrame parentFrame, SelectorDialogModes aMode) {
        this.parentFrame = parentFrame;
        this.ooDocument = ooDoc;
        initComponents();
        
        dlgMode = aMode;
   
        initMetadata();
        initControls();
        
        if (aMode == SelectorDialogModes.TEXT_EDIT) {
            try {
                //retrieve metadata... and set in controls....
                ooDocMetadata docMeta = new ooDocMetadata(ooDocument);
                String sParlId = docMeta.GetProperty("BungeniParliamentID");
                String sParlSitting = docMeta.GetProperty("BungeniParliamentSitting");
                String sParlSession = docMeta.GetProperty("BungeniParliamentSession");
                String sCountryCode = docMeta.GetProperty("BungeniCountryCode");
                String sLanguageCode = docMeta.GetProperty("BungeniLanguageCode");
                String sOfficDate = docMeta.GetProperty("BungeniDebateOfficialDate");
                String sOfficTime = docMeta.GetProperty("BungeniDebateOfficialTime");

                //official date
                SimpleDateFormat formatter = new SimpleDateFormat(BungeniEditorProperties.getEditorProperty("metadataDateFormat"));
                this.dt_initdebate_hansarddate.setDate(formatter.parse(sOfficDate));
                //official time
                SimpleDateFormat timeFormat = new SimpleDateFormat(BungeniEditorProperties.getEditorProperty("metadataTimeFormat"));
                dt_initdebate_timeofhansard.setValue(timeFormat.parse(sOfficTime));
                this.BungeniParliamentID.setText(sParlId);
                this.txtParliamentSession.setText(sParlSession);
                this.txtParliamentSitting.setText(sParlSitting);
                this.cboCountry.setSelectedItem(findCountryCode(sCountryCode));
                this.cboLanguage.setSelectedItem(findLanguageCode(sLanguageCode));
                
            } catch (ParseException ex) {
                Logger.getLogger(DebateRecordMetadata.class.getName()).log(Level.SEVERE, null, ex);
            }
         
        }
       // getComponentWithNames(this);
    }

    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        cboCountry = new javax.swing.JComboBox();
        cboLanguage = new javax.swing.JComboBox();
        jLabel1 = new javax.swing.JLabel();
        jLabel2 = new javax.swing.JLabel();
        jLabel3 = new javax.swing.JLabel();
        jLabel4 = new javax.swing.JLabel();
        jLabel5 = new javax.swing.JLabel();
        btnSave = new javax.swing.JButton();
        btnCancel = new javax.swing.JButton();
        BungeniParliamentID = new javax.swing.JTextField();
        txtParliamentSession = new javax.swing.JTextField();
        txtParliamentSitting = new javax.swing.JTextField();
        jScrollPane1 = new javax.swing.JScrollPane();
        jTextArea1 = new javax.swing.JTextArea();
        dt_initdebate_hansarddate = new org.jdesktop.swingx.JXDatePicker();
        jLabel6 = new javax.swing.JLabel();
        dt_initdebate_timeofhansard = new javax.swing.JSpinner();
        jLabel7 = new javax.swing.JLabel();

        setBackground(java.awt.Color.lightGray);

        cboCountry.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        cboCountry.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        cboCountry.setName("fld.BungeniCountryCode"); // NOI18N
        cboCountry.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                cboCountryActionPerformed(evt);
            }
        });

        cboLanguage.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        cboLanguage.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        cboLanguage.setName("fld.BungeniLanguageID"); // NOI18N

        jLabel1.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        jLabel1.setText("Country");
        jLabel1.setName("lbl.BungeniCountryCode"); // NOI18N

        jLabel2.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        jLabel2.setText("Language");
        jLabel2.setName("lbl.BungeniLanguageID"); // NOI18N

        jLabel3.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        jLabel3.setText("Parliament ID");
        jLabel3.setName("lbl.BungeniParliamentID"); // NOI18N

        jLabel4.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        jLabel4.setText("Parliament Session");
        jLabel4.setName("lbl.BungeniParliamentSession"); // NOI18N

        jLabel5.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        jLabel5.setText("Parliament Sitting");
        jLabel5.setName("lbl.BungeniParliamentSitting"); // NOI18N

        btnSave.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        btnSave.setText("Save");
        btnSave.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnSaveActionPerformed(evt);
            }
        });

        btnCancel.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        btnCancel.setText("Cancel");

        BungeniParliamentID.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        BungeniParliamentID.setName("fld.BungeniParliamentID"); // NOI18N
        BungeniParliamentID.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                BungeniParliamentIDActionPerformed(evt);
            }
        });

        txtParliamentSession.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        txtParliamentSession.setName("fld.BungeniParliamentSession"); // NOI18N

        txtParliamentSitting.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        txtParliamentSitting.setName("BungeniParliamentSitting"); // NOI18N

        jTextArea1.setBackground(java.awt.Color.lightGray);
        jTextArea1.setColumns(20);
        jTextArea1.setEditable(false);
        jTextArea1.setLineWrap(true);
        jTextArea1.setRows(5);
        jTextArea1.setText("This is a new document, Please select and enter required metadata to initialize the document");
        jTextArea1.setWrapStyleWord(true);
        jTextArea1.setBorder(null);
        jScrollPane1.setViewportView(jTextArea1);

        dt_initdebate_hansarddate.setFont(new java.awt.Font("DejaVu Sans", 0, 10));

        jLabel6.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        jLabel6.setText("Date");
        jLabel6.setName("lbl.BungeniParliamentSitting"); // NOI18N

        dt_initdebate_timeofhansard.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        dt_initdebate_timeofhansard.setName("dt_initdebate_timeofhansard"); // NOI18N

        jLabel7.setFont(new java.awt.Font("DejaVu Sans", 0, 10));
        jLabel7.setText("TIme");
        jLabel7.setName("lbl.BungeniParliamentSitting"); // NOI18N

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 381, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel2, javax.swing.GroupLayout.PREFERRED_SIZE, 185, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(cboLanguage, 0, 381, Short.MAX_VALUE)
                    .addComponent(cboCountry, 0, 381, Short.MAX_VALUE)
                    .addComponent(jLabel1, javax.swing.GroupLayout.PREFERRED_SIZE, 150, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                                        .addComponent(txtParliamentSitting)
                                        .addComponent(BungeniParliamentID, javax.swing.GroupLayout.DEFAULT_SIZE, 155, Short.MAX_VALUE)
                                        .addComponent(jLabel3, javax.swing.GroupLayout.PREFERRED_SIZE, 111, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addComponent(jLabel5, javax.swing.GroupLayout.PREFERRED_SIZE, 110, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addComponent(dt_initdebate_hansarddate, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                                    .addComponent(jLabel6, javax.swing.GroupLayout.PREFERRED_SIZE, 110, javax.swing.GroupLayout.PREFERRED_SIZE))
                                .addGap(44, 44, 44))
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                                .addComponent(btnSave, javax.swing.GroupLayout.PREFERRED_SIZE, 84, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addGap(15, 15, 15)))
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(dt_initdebate_timeofhansard, javax.swing.GroupLayout.PREFERRED_SIZE, 86, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(jLabel4)
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                                .addComponent(txtParliamentSession, javax.swing.GroupLayout.DEFAULT_SIZE, 155, Short.MAX_VALUE)
                                .addGap(27, 27, 27))
                            .addComponent(jLabel7, javax.swing.GroupLayout.PREFERRED_SIZE, 110, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addGroup(layout.createSequentialGroup()
                                .addGap(23, 23, 23)
                                .addComponent(btnCancel, javax.swing.GroupLayout.PREFERRED_SIZE, 77, javax.swing.GroupLayout.PREFERRED_SIZE)))))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 49, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel1)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(cboCountry, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel2, javax.swing.GroupLayout.PREFERRED_SIZE, 15, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(cboLanguage, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel3)
                    .addComponent(jLabel4, javax.swing.GroupLayout.PREFERRED_SIZE, 13, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(1, 1, 1)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(BungeniParliamentID, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(txtParliamentSession, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel5)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(txtParliamentSitting, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(7, 7, 7)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel6)
                    .addComponent(jLabel7))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(dt_initdebate_hansarddate, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(dt_initdebate_timeofhansard, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(btnSave)
                    .addComponent(btnCancel))
                .addGap(4, 4, 4))
        );
    }// </editor-fold>//GEN-END:initComponents

private void cboCountryActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_cboCountryActionPerformed
// TODO add your handling code here:
}//GEN-LAST:event_cboCountryActionPerformed

private void BungeniParliamentIDActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_BungeniParliamentIDActionPerformed
// TODO add your handling code here:
}//GEN-LAST:event_BungeniParliamentIDActionPerformed

private void btnSaveActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnSaveActionPerformed
// TODO add your handling code here:
   //APPLY SELECTED METADATA... 
    BungeniFileSavePathFormat spf = new BungeniFileSavePathFormat();
    applySelectedMetadata(spf);
    saveDocumentToDisk(spf);
    parentFrame.dispose();
}//GEN-LAST:event_btnSaveActionPerformed


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JTextField BungeniParliamentID;
    private javax.swing.JButton btnCancel;
    private javax.swing.JButton btnSave;
    private javax.swing.JComboBox cboCountry;
    private javax.swing.JComboBox cboLanguage;
    private org.jdesktop.swingx.JXDatePicker dt_initdebate_hansarddate;
    private javax.swing.JSpinner dt_initdebate_timeofhansard;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JLabel jLabel6;
    private javax.swing.JLabel jLabel7;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JTextArea jTextArea1;
    private javax.swing.JTextField txtParliamentSession;
    private javax.swing.JTextField txtParliamentSitting;
    // End of variables declaration//GEN-END:variables

    public static void main (String[] args) {
      //  DebateRecordMetadata metaPanel = new DebateRecordMetadata();
       // JFrame f = new JFrame("DebateRecord metadata");
      //  f.setSize(new Dimension(234, 286));
      //  f.add(metaPanel);
     //   f.setVisible(true);
     //   f.setAlwaysOnTop(true);
    }
}
