/*
 * browseReferences.java
 *
 * Created on July 14, 2008, 3:43 PM
 */

package org.bungeni.editor.panels.loadable.refmgr;

import com.sun.star.container.NoSuchElementException;
import com.sun.star.container.XNameAccess;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextRange;
import java.awt.Component;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.ArrayList;
import java.util.Date;
import java.util.concurrent.ExecutionException;
import javax.swing.JTable;
import javax.swing.SwingWorker;
import javax.swing.table.AbstractTableModel;
import org.bungeni.editor.numbering.ooo.OOoNumberingHelper;
import org.bungeni.editor.panels.impl.BaseLaunchablePanel;
import org.bungeni.ooo.ooDocMetadata;
import org.bungeni.ooo.ooDocMetadataFieldSet;
import org.bungeni.ooo.ooQueryInterface;

/**
 *
 * @author  undesa
 */
public class externalReferences extends BaseLaunchablePanel {
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(externalReferences.class.getName());
    private final static String __TITLE__ = "External References";      
    
    
    /** Creates new form browseReferences */
    public externalReferences() {
       // initComponents();
    }


    private void init(){
        initTableModel();
    }
    
    private void initTableModel(){
        //lazy load of tree....
        ExtReferencesTableModelAgent rtmAgent = new ExtReferencesTableModelAgent(this.tblExternalReferences);
        rtmAgent.execute();
        tblExternalReferences.addMouseListener(new MouseAdapter(){
            @Override
            public void mouseClicked(MouseEvent evt) {
                if (evt.getClickCount() == 2) {
                    //doublic clicked
                    int nRow = tblExternalReferences.getSelectedRow();
                    if (nRow != -1) {
                        /*
                        ExtReferencesTableModel model = (ExtReferencesTableModel)tblExternalReferences.getModel();
                        DocumentInternalReference ref = model.getRowData(nRow);
                        String refName = ref.getActualReferenceName();
                        //move the cursor lazily
                        //MoveCursorToRefRangeAgent moveAgent = new MoveCursorToRefRangeAgent(refName);
                        //moveAgent.execute();
                        */
                    }
                }
            }
        });
    }
    
    
    class MoveCursorToRefRangeAgent extends SwingWorker<Boolean, Void>{
        String thisRange ;
        MoveCursorToRefRangeAgent (String refname) {
            thisRange = refname;
        }
        @Override
        protected Boolean doInBackground() throws Exception{
              XNameAccess refMarks = ooDocument.getReferenceMarks();
              if (refMarks.hasByName(thisRange)){
                  try {
                    Object oRefMark = refMarks.getByName(thisRange);
                    XTextContent xRefContent = ooQueryInterface.XTextContent(oRefMark);
                    XTextRange refMarkRange = xRefContent.getAnchor();
                    ooDocument.getViewCursor().gotoRange(refMarkRange, false);
                  } catch (NoSuchElementException ex) {
                     log.error("tblAllReferences:double_click : " + ex.getMessage());
                  } catch (WrappedTargetException ex) {
                     log.error("tblAllReferences:double_click : " + ex.getMessage());
                  } 
           }
           return true;
        }
        
    }
    
    class FilterSettings {
        String Name;
        String DisplayText;
        
        FilterSettings(String n, String d) {
            Name = n;
            DisplayText = d;
        }
        
        @Override
        public String toString(){
            return DisplayText;
        }
    }
    
    
    private void applyInsertCrossReference() {
        final int nSelectedRow = this.tblExternalReferences.getSelectedRow();
        if (nSelectedRow !=  -1) { //nothing was selected
            int nRow = tblExternalReferences.getSelectedRow();
        }
    }
    
    /**
     * SwingWorker agent to do a lazy load of the references tree...
     * The document references are gathered using threaded agent
     * and the tree is loaded once all the references have been gathered.
     */
    class ExtReferencesTableModelAgent extends SwingWorker<ExtReferencesTableModel, Void>{
        JTable updateThisTable = null;
        ExtReferencesTableModelAgent(JTable inputTable){
           // tableModel = model;
            updateThisTable = inputTable;
        }
        @Override
        protected ExtReferencesTableModel doInBackground() throws Exception {
            ExtReferencesTableModel rtm = buildExtReferencesTableModel();
            return rtm;
        }
        
        @Override
        protected void done(){
            try {
                ExtReferencesTableModel rtm = get();
                if (rtm != null) {
                    updateThisTable.setModel(rtm);
                }
            } catch (InterruptedException ex) {
                log.error("ReferencesTableModelAgent : " + ex.getMessage());
            } catch (ExecutionException ex) {
                log.error("ReferencesTableModelAgent : " + ex.getMessage());
            }
            
        }
        
    }
    
    
     private ExtReferencesTableModel buildExtReferencesTableModel(){
        //we can get all the references from the document properties
         ArrayList<ooDocMetadataFieldSet> metadataFieldSets = ooDocMetadata.getMetadataObjectsByType(ooDocument, OOoNumberingHelper.INTERNAL_REF_PREFIX);
        //but they are not in document sequential order
         //add them sequentially to our table with their contained text
        //the contained text can be retrieved form the cached document metadata
         ArrayList<DocumentExternalReference> docExtRefs = new ArrayList<DocumentExternalReference>(0);
         ExtReferencesTableModel rtm = new ExtReferencesTableModel(docExtRefs);
         return rtm;
    }
     
     class ExtReferencesTableModel extends AbstractTableModel {
         
         ArrayList<DocumentExternalReference> documentReferences = new ArrayList<DocumentExternalReference>();
         ArrayList<DocumentExternalReference> filteredDocumentReferences = new ArrayList<DocumentExternalReference>();
         
         public ExtReferencesTableModel (ArrayList<DocumentExternalReference> dref) {
            super();
            documentReferences = dref;
            //make a memcopy of the dref variable since refArr will be changing
           filteredDocumentReferences = (ArrayList<DocumentExternalReference>) dref.clone();
         }
        
         public void resetModel() {
            synchronized(filteredDocumentReferences) {
                filteredDocumentReferences = (ArrayList<DocumentExternalReference>) documentReferences.clone();
            }
            fireTableDataChanged();
         }
         
         public DocumentExternalReference findMatchingRef(String refName) {
             refName = OOoNumberingHelper.INTERNAL_REF_PREFIX + refName;
             DocumentExternalReference foundRef = null;
             for (DocumentExternalReference dref : documentReferences) {
                 if (dref.Name.toLowerCase().equals(refName.toLowerCase())) {
                     //matched 
                     foundRef = dref;
                     break;
                 }
             }
             return foundRef;
         }
         
         public void filterByType(String filterRefTo) {
             
             filterRefTo = filterRefTo.toLowerCase();
             log.debug("filterByType : filter for : " + filterRefTo);
             /*
             FilterSettings filterBy = (FilterSettings) cboFilterSettings.getSelectedItem();
             synchronized(filteredDocumentReferences) {
                 filteredDocumentReferences.clear();
                 for (DocumentInternalReference dref : documentReferences) {
                     String matchWithThis = "";
                      if (filterBy.Name.equals("by-container")) {
                         matchWithThis = dref.ParentType.toLowerCase();
                      } else if (filterBy.Name.equals("by-type")) {
                         matchWithThis = dref.ReferenceType.toLowerCase();  
                      } else if (filterBy.Name.equals("by-reftext")) {
                         matchWithThis = dref.ReferenceText.toLowerCase();
                      }
                    log.debug("filterByType : filter by : " + matchWithThis);
                    if (matchWithThis.contains(filterRefTo)) {
                        //matching table model
                        filteredDocumentReferences.add(dref);
                    }
                }
             }*/
             fireTableDataChanged();
         }
         
        private String[] columns = {"Ref Name", "Reference To", "Reference Type", "Reference Text" };
        private Class[] column_class = {String.class, String.class, String.class, String.class };
        
        @Override
        public String getColumnName(int col) {
            return columns[col];
        }
        
        @Override
        public Class getColumnClass(int col) {
            return column_class[col];
        }
        
        public int getRowCount() {
            return filteredDocumentReferences.size();
        }

        public int getColumnCount() {
            return columns.length;
        }

        public Object getValueAt(int row, int col) {
           DocumentExternalReference rfObj = filteredDocumentReferences.get(row);
           //DocumentInternalReference rfObj = documentReferences.get(keys[row]);
           return rfObj.Name;
        }
         
        public DocumentExternalReference getRowData (int row) {
            return this.filteredDocumentReferences.get(row);
        } 
        
 
     }

     class DocumentExternalReference implements Cloneable {
         //name of the reference preceded by rf:
         String Name;
         String Href;
         String DisplayText;
         String ReferenceType; //external, uri
         String URItext;
         
         
         DocumentExternalReference(String name, String refText, String displayText) {
             Name = name;
             Href = refText;
             DisplayText = displayText;
             ReferenceType =  "external";
             URItext="";
             // ParentType = parentType;
         }


         DocumentExternalReference(String  name, Date dt, String docType, String docIdentifier, String displayText) {
             Name = name;
             Href = "";
             DisplayText = displayText;
             ReferenceType =  "uri";
             URItext = makeURI (dt, docType, docIdentifier);
             // ParentType = parentType;
         }
         
         private String makeURI (Date dt, String docType, String docId){
             return new String();
         }
                  
         
         
         public String getActualReferenceName(){
             int nNameIndex = Name.indexOf(":");
             if (nNameIndex != -1)
                return Name.substring(nNameIndex+1);
             else
                 return Name;
         }
         
        @Override
         protected Object clone() throws CloneNotSupportedException{
             DocumentExternalReference cloneRef = (DocumentExternalReference) super.clone();
             return cloneRef;
         }
         

     }

     private void filterTableModel(){
         String fieldFilter = this.txtExternalReference.getText();
         ExtReferencesTableModel model = (ExtReferencesTableModel) this.tblExternalReferences.getModel();
         model.filterByType(fieldFilter);
     }
     
     
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        btnInsertCrossRef = new javax.swing.JButton();
        btnBrowseBroken = new javax.swing.JButton();
        btnClose = new javax.swing.JButton();
        jScrollPane1 = new javax.swing.JScrollPane();
        tblExternalReferences = new javax.swing.JTable();
        txtExternalReference = new javax.swing.JTextField();
        lblNewReference = new javax.swing.JLabel();
        btnAddRef = new javax.swing.JButton();
        lblUriReference = new javax.swing.JLabel();
        dtURIdate = new org.jdesktop.swingx.JXDatePicker();
        lblDate = new javax.swing.JLabel();
        cboDocType = new javax.swing.JComboBox();
        lblType = new javax.swing.JLabel();
        txtDocId = new javax.swing.JTextField();
        btnAddURI = new javax.swing.JButton();
        lblDocId = new javax.swing.JLabel();

        btnInsertCrossRef.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        btnInsertCrossRef.setText("Insert External Ref");
        btnInsertCrossRef.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnInsertCrossRefActionPerformed(evt);
            }
        });

        btnBrowseBroken.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        btnBrowseBroken.setText("Browse Broken ");
        btnBrowseBroken.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnBrowseBrokenActionPerformed(evt);
            }
        });

        btnClose.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        btnClose.setText("Close");
        btnClose.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnCloseActionPerformed(evt);
            }
        });

        tblExternalReferences.setFont(new java.awt.Font("DejaVu Sans", 0, 11));
        tblExternalReferences.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null}
            },
            new String [] {
                "Title 1", "Title 2", "Title 3", "Title 4"
            }
        ));
        tblExternalReferences.setSelectionMode(javax.swing.ListSelectionModel.SINGLE_SELECTION);
        jScrollPane1.setViewportView(tblExternalReferences);

        txtExternalReference.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        txtExternalReference.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent evt) {
                txtExternalReferenceKeyPressed(evt);
            }
        });

        lblNewReference.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        lblNewReference.setText("New External Reference");

        btnAddRef.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        btnAddRef.setText("Add..");
        btnAddRef.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnAddRefActionPerformed(evt);
            }
        });

        lblUriReference.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        lblUriReference.setText("New URI reference");

        dtURIdate.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N

        lblDate.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        lblDate.setText("Date");

        cboDocType.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        cboDocType.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Act", "Bill", "Debaterecord" }));

        lblType.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        lblType.setText("Type");

        txtDocId.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N

        btnAddURI.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        btnAddURI.setText("Add..");

        lblDocId.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        lblDocId.setText("Identifier");

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 401, Short.MAX_VALUE)
                        .addContainerGap())
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(btnInsertCrossRef, javax.swing.GroupLayout.PREFERRED_SIZE, 132, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(btnBrowseBroken, javax.swing.GroupLayout.PREFERRED_SIZE, 135, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(btnClose, javax.swing.GroupLayout.DEFAULT_SIZE, 122, Short.MAX_VALUE)
                        .addContainerGap())
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(lblNewReference, javax.swing.GroupLayout.DEFAULT_SIZE, 277, Short.MAX_VALUE)
                        .addGap(136, 136, 136))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(lblUriReference, javax.swing.GroupLayout.PREFERRED_SIZE, 286, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addContainerGap())
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                            .addGroup(javax.swing.GroupLayout.Alignment.LEADING, layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(dtURIdate, javax.swing.GroupLayout.PREFERRED_SIZE, 146, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addComponent(lblDate, javax.swing.GroupLayout.PREFERRED_SIZE, 120, javax.swing.GroupLayout.PREFERRED_SIZE))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(cboDocType, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addComponent(lblType))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(lblDocId)
                                    .addComponent(txtDocId, javax.swing.GroupLayout.PREFERRED_SIZE, 61, javax.swing.GroupLayout.PREFERRED_SIZE)))
                            .addComponent(txtExternalReference, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, 334, Short.MAX_VALUE))
                        .addGap(12, 12, 12)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(btnAddRef, javax.swing.GroupLayout.DEFAULT_SIZE, 55, Short.MAX_VALUE)
                            .addComponent(btnAddURI, javax.swing.GroupLayout.DEFAULT_SIZE, 55, Short.MAX_VALUE))
                        .addContainerGap())))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(5, 5, 5)
                .addComponent(lblNewReference)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(btnAddRef)
                    .addComponent(txtExternalReference, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(lblUriReference)
                .addGap(3, 3, 3)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(lblDate)
                    .addComponent(lblType)
                    .addComponent(lblDocId))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(dtURIdate, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(cboDocType, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(txtDocId, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(btnAddURI))
                .addGap(18, 18, 18)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 148, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(7, 7, 7)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(btnClose)
                    .addComponent(btnInsertCrossRef)
                    .addComponent(btnBrowseBroken))
                .addContainerGap(14, Short.MAX_VALUE))
        );
    }// </editor-fold>//GEN-END:initComponents

private void btnInsertCrossRefActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnInsertCrossRefActionPerformed
// TODO add your handling code here:
     applyInsertCrossReference();
}//GEN-LAST:event_btnInsertCrossRefActionPerformed

private void btnBrowseBrokenActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnBrowseBrokenActionPerformed
// TODO add your handling code here:
   // parentFrame.dispose();
}//GEN-LAST:event_btnBrowseBrokenActionPerformed

private void btnCloseActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnCloseActionPerformed
// TODO add your handling code here:
    parentFrame.dispose();
}//GEN-LAST:event_btnCloseActionPerformed

private void txtExternalReferenceKeyPressed(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_txtExternalReferenceKeyPressed
// TODO add your handling code here:
    if (evt.getKeyCode() == KeyEvent.VK_ENTER){
       filterTableModel();
    }
    
}//GEN-LAST:event_txtExternalReferenceKeyPressed

private void btnAddRefActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnAddRefActionPerformed
// TODO add your handling code here:
    ExtReferencesTableModel model = (ExtReferencesTableModel) this.tblExternalReferences.getModel();
    model.resetModel();
}//GEN-LAST:event_btnAddRefActionPerformed


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnAddRef;
    private javax.swing.JButton btnAddURI;
    private javax.swing.JButton btnBrowseBroken;
    private javax.swing.JButton btnClose;
    private javax.swing.JButton btnInsertCrossRef;
    private javax.swing.JComboBox cboDocType;
    private org.jdesktop.swingx.JXDatePicker dtURIdate;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JLabel lblDate;
    private javax.swing.JLabel lblDocId;
    private javax.swing.JLabel lblNewReference;
    private javax.swing.JLabel lblType;
    private javax.swing.JLabel lblUriReference;
    private javax.swing.JTable tblExternalReferences;
    private javax.swing.JTextField txtDocId;
    private javax.swing.JTextField txtExternalReference;
    // End of variables declaration//GEN-END:variables

    @Override
    public Component getObjectHandle() {
        return this;
    }

    @Override
    public void initUI() {
        initComponents();
        init();
    }

    @Override
    public String getPanelTitle() {
        return __TITLE__;
    }

}
