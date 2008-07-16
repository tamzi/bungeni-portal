/*
 * browseReferences.java
 *
 * Created on July 14, 2008, 3:43 PM
 */

package org.bungeni.editor.panels.loadable.refmgr;

import com.sun.star.container.XNamed;
import com.sun.star.text.XTextSection;
import java.awt.Component;
import java.awt.event.KeyEvent;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.ExecutionException;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JTable;
import javax.swing.SwingWorker;
import javax.swing.table.AbstractTableModel;
import org.bungeni.editor.document.DocumentSectionsContainer;
import org.bungeni.editor.numbering.ooo.OOoNumberingHelper;
import org.bungeni.editor.panels.impl.BaseLaunchablePanel;
import org.bungeni.editor.providers.DocumentSectionIterator;
import org.bungeni.editor.providers.IBungeniSectionIteratorListener;
import org.bungeni.ooo.ooDocMetadata;
import org.bungeni.ooo.ooDocMetadataFieldSet;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.utils.BungeniBNode;

/**
 *
 * @author  undesa
 */
public class browseReferences extends BaseLaunchablePanel {
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(browseReferences.class.getName());
          
    /** Creates new form browseReferences */
    public browseReferences() {
       // initComponents();
    }

    private void init(){
        initTableModel();
        initFilter();
    }
    
    private void initTableModel(){
        //lazy load of tree....
        ReferencesTableModelAgent rtmAgent = new ReferencesTableModelAgent(this.tblAllReferences);
        rtmAgent.execute();
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
    
    private void initFilter(){
        ArrayList<FilterSettings> filterSettings=new ArrayList<FilterSettings>(0);
        filterSettings.add(new FilterSettings("by-container", "By Containers"));
        filterSettings.add(new FilterSettings("by-type", "By Type"));
        cboFilterSettings.setModel(new DefaultComboBoxModel(filterSettings.toArray()));
    }
        /**
     * SwingWorker agent to do a lazy load of the references tree...
     * The document references are gathered using threaded agent
     * and the tree is loaded once all the references have been gathered.
     */
    class ReferencesTableModelAgent extends SwingWorker<ReferencesTableModel, Void>{
        JTable updateThisTable = null;
        ReferencesTableModelAgent(JTable inputTable){
           // tableModel = model;
            updateThisTable = inputTable;
        }
        @Override
        protected ReferencesTableModel doInBackground() throws Exception {
            ReferencesTableModel rtm = buildReferencesTableModel();
            return rtm;
        }
        
        @Override
        protected void done(){
            try {
                ReferencesTableModel rtm = get();
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
    
      class ReferencesInSectionListener implements IBungeniSectionIteratorListener{
         ArrayList<ooDocMetadataFieldSet> referenceNames = new ArrayList<ooDocMetadataFieldSet>(0);
         HashMap<String, String> documentReferences = new HashMap<String,String>();
         ArrayList<DocumentInternalReference> referenceList = new ArrayList<DocumentInternalReference>(0);
         ReferencesInSectionListener(ArrayList<ooDocMetadataFieldSet> meta) {
             referenceNames = meta;
         }
         
         private void findMatchingRefs (XTextSection foundSection, String uuidStr) {
             for (ooDocMetadataFieldSet metaField : referenceNames) {
                 if (metaField.getMetadataName().indexOf(uuidStr) != -1) {
                     if (! documentReferences.containsKey(metaField.getMetadataName())) {
                         String foundSectionType = ooDocument.getSectionType(foundSection);
                         XNamed secName = ooQueryInterface.XNamed(foundSection);
                         String visibility = DocumentSectionsContainer.getDocumentSectionsContainer().get(foundSectionType).getSectionVisibilty();
                         DocumentInternalReference refObj = new DocumentInternalReference(metaField.getMetadataName(), metaField.getMetadataValue());
                       //  MessageBox.OK("Section : " + secName.getName() + " , visiblity = " + visibility);
                         if (visibility.equals("user")) {
                            refObj.setParentType(foundSectionType);
                         } else {
                             //if its not a user section, we get the parent section
                             //and check its visibility
                             XTextSection xSection = foundSection.getParentSection();
                             if (xSection != null) {
                                 String sectionType = ooDocument.getSectionType(xSection);
                                 if (sectionType != null) {
                                     refObj.setParentType(sectionType);
                                 } else {
                                     refObj.setParentType(foundSectionType);
                                 }
                             } else {
                                refObj.setParentType(foundSectionType);
                             }
                         }
                         documentReferences.put(metaField.getMetadataName(), "");
                         this.referenceList.add(refObj);
                     }
                         
                 }
             }
         }
         
         public boolean iteratorCallback(BungeniBNode bNode) {
             String sectionName = bNode.getName();
             XTextSection foundSection = ooDocument.getSection(sectionName);
             HashMap<String,String> sectionmeta = ooDocument.getSectionMetadataAttributes(foundSection);
             if (sectionmeta.containsKey(OOoNumberingHelper.SECTION_IDENTIFIER)) {
                 String sectionUUID = sectionmeta.get(OOoNumberingHelper.SECTION_IDENTIFIER);
                 //look for references with this UUID
                 findMatchingRefs (foundSection,  sectionUUID);
             }
            return true;
        }

     }
    
     private ReferencesTableModel buildReferencesTableModel(){
        //we can get all the references from the document properties
         ArrayList<ooDocMetadataFieldSet> metadataFieldSets = ooDocMetadata.getMetadataObjectsByType(ooDocument, OOoNumberingHelper.INTERNAL_REF_PREFIX);
        //but they are not in document sequential order
         ReferencesInSectionListener allRefsListener = new ReferencesInSectionListener(metadataFieldSets);
         DocumentSectionIterator iterateRefs = new DocumentSectionIterator(allRefsListener);
        //so we iterate through all the sections in the document
         iterateRefs.startIterator();
        //find the references in each section
         ArrayList<DocumentInternalReference> docRefs = allRefsListener.referenceList;
         //add them sequentially to our table with their contained text
        //the contained text can be retrieved form the cached document metadata
         ReferencesTableModel rtm = new ReferencesTableModel(docRefs);
         return rtm;
    }
     
     class ReferencesTableModel extends AbstractTableModel {
         
         ArrayList<DocumentInternalReference> documentReferences = new ArrayList<DocumentInternalReference>();
         ArrayList<DocumentInternalReference> filteredDocumentReferences = new ArrayList<DocumentInternalReference>();
         
         public ReferencesTableModel (ArrayList<DocumentInternalReference> dref) {
            super();
            documentReferences = dref;
            //make a memcopy of the dref variable since refArr will be changing
           filteredDocumentReferences = (ArrayList<DocumentInternalReference>) dref.clone();
         }
        
         public void resetModel() {
            synchronized(filteredDocumentReferences) {
                filteredDocumentReferences = documentReferences;
            }
            fireTableDataChanged();
         }
         
         public void filterByType(String filterRefTo) {
             
             filterRefTo = filterRefTo.toLowerCase();
             log.debug("filterByType : filter for : " + filterRefTo);
             FilterSettings filterBy = (FilterSettings) cboFilterSettings.getSelectedItem();
             synchronized(filteredDocumentReferences) {
                 filteredDocumentReferences.clear();
                 for (DocumentInternalReference dref : documentReferences) {
                     String matchWithThis = "";
                      if (filterBy.Name.equals("by-container")) {
                         matchWithThis = dref.ParentType.toLowerCase();
                          
                      } else if (filterBy.Name.equals("by-type")) {
                         matchWithThis = dref.ReferenceType.toLowerCase();  
                      }
                    log.debug("filterByType : filter by : " + matchWithThis);
                    if (matchWithThis.contains(filterRefTo)) {
                        //matching table model
                        filteredDocumentReferences.add(dref);
                    }
                }
             }
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
           DocumentInternalReference rfObj = filteredDocumentReferences.get(row);
           //DocumentInternalReference rfObj = documentReferences.get(keys[row]);
           switch (col) {
               case 0: 
                   return rfObj.Name;
               case 1:
                   return rfObj.ParentType;
               case 2:
                   return rfObj.ReferenceType;
               case 3:
                   return rfObj.ReferenceText;
               default:
                   return rfObj.Name;
           }
        }
         
     }

     class DocumentInternalReference {
         String Name;
         String ReferenceText;
         String ReferenceType;
         String ParentType;
         
         private String getReferenceType(String name) {
             if (name.startsWith(OOoNumberingHelper.INTERNAL_REF_PREFIX + OOoNumberingHelper.HEADING_REF_PREFIX)) {
                 return "heading";
             }
             if (name.startsWith(OOoNumberingHelper.INTERNAL_REF_PREFIX + OOoNumberingHelper.NUMBER_REF_PREFIX)) {
                 return "number";
             } else 
                 return "other";
         }
         
         DocumentInternalReference(String name, String refText) {
             Name = name;
             ReferenceText = refText;
             ReferenceType =  getReferenceType(name);
            // ParentType = parentType;
         }
         
         public void setParentType(String ppType) {
             ParentType = ppType;
         }
     }

     private void filterTableModel(){
         String fieldFilter = this.txtFilterReferences.getText();
         ReferencesTableModel model = (ReferencesTableModel) this.tblAllReferences.getModel();
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

        btnFixBrokenReferences = new javax.swing.JButton();
        btnCloseFrame = new javax.swing.JButton();
        btnClose = new javax.swing.JButton();
        jScrollPane1 = new javax.swing.JScrollPane();
        tblAllReferences = new javax.swing.JTable();
        txtFilterReferences = new javax.swing.JTextField();
        lblFilterReferences = new javax.swing.JLabel();
        cboFilterSettings = new javax.swing.JComboBox();
        btnRefresh = new javax.swing.JButton();

        btnFixBrokenReferences.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        btnFixBrokenReferences.setText("Insert Cross Ref");
        btnFixBrokenReferences.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnFixBrokenReferencesActionPerformed(evt);
            }
        });

        btnCloseFrame.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        btnCloseFrame.setText("Browse Broken ");
        btnCloseFrame.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnCloseFrameActionPerformed(evt);
            }
        });

        btnClose.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        btnClose.setText("Close");
        btnClose.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnCloseActionPerformed(evt);
            }
        });

        tblAllReferences.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        tblAllReferences.setModel(new javax.swing.table.DefaultTableModel(
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
        jScrollPane1.setViewportView(tblAllReferences);

        txtFilterReferences.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        txtFilterReferences.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent evt) {
                txtFilterReferencesKeyPressed(evt);
            }
        });

        lblFilterReferences.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        lblFilterReferences.setText("Filter References");

        cboFilterSettings.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        cboFilterSettings.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));

        btnRefresh.setFont(new java.awt.Font("DejaVu Sans", 0, 11)); // NOI18N
        btnRefresh.setText("Refresh");
        btnRefresh.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnRefreshActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(btnFixBrokenReferences, javax.swing.GroupLayout.PREFERRED_SIZE, 138, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(btnCloseFrame, javax.swing.GroupLayout.PREFERRED_SIZE, 129, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(btnClose, javax.swing.GroupLayout.DEFAULT_SIZE, 97, Short.MAX_VALUE)
                        .addContainerGap())
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(lblFilterReferences, javax.swing.GroupLayout.DEFAULT_SIZE, 252, Short.MAX_VALUE)
                        .addGap(136, 136, 136))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 376, Short.MAX_VALUE)
                        .addContainerGap())
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(txtFilterReferences, javax.swing.GroupLayout.PREFERRED_SIZE, 187, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(cboFilterSettings, javax.swing.GroupLayout.PREFERRED_SIZE, 90, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(btnRefresh, javax.swing.GroupLayout.DEFAULT_SIZE, 87, Short.MAX_VALUE)
                        .addContainerGap())))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(5, 5, 5)
                .addComponent(lblFilterReferences)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(txtFilterReferences, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(cboFilterSettings, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(btnRefresh))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 228, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(7, 7, 7)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(btnFixBrokenReferences)
                    .addComponent(btnCloseFrame)
                    .addComponent(btnClose))
                .addContainerGap(13, Short.MAX_VALUE))
        );
    }// </editor-fold>//GEN-END:initComponents

private void btnFixBrokenReferencesActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnFixBrokenReferencesActionPerformed
// TODO add your handling code here:
    //    applyInsertCrossReference();
}//GEN-LAST:event_btnFixBrokenReferencesActionPerformed

private void btnCloseFrameActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnCloseFrameActionPerformed
// TODO add your handling code here:

}//GEN-LAST:event_btnCloseFrameActionPerformed

private void btnCloseActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnCloseActionPerformed
// TODO add your handling code here:
    parentFrame.dispose();
}//GEN-LAST:event_btnCloseActionPerformed

private void txtFilterReferencesKeyPressed(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_txtFilterReferencesKeyPressed
// TODO add your handling code here:
    if (evt.getKeyCode() == KeyEvent.VK_ENTER){
       filterTableModel();
    }
    
}//GEN-LAST:event_txtFilterReferencesKeyPressed

private void btnRefreshActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnRefreshActionPerformed
// TODO add your handling code here:
    ReferencesTableModel model = (ReferencesTableModel) this.tblAllReferences.getModel();
    model.resetModel();
}//GEN-LAST:event_btnRefreshActionPerformed


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnClose;
    private javax.swing.JButton btnCloseFrame;
    private javax.swing.JButton btnFixBrokenReferences;
    private javax.swing.JButton btnRefresh;
    private javax.swing.JComboBox cboFilterSettings;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JLabel lblFilterReferences;
    private javax.swing.JTable tblAllReferences;
    private javax.swing.JTextField txtFilterReferences;
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

}
