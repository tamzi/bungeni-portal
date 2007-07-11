/*
 * editorTabbedPanel.java
 *
 * Created on May 28, 2007, 3:55 PM
 */

package org.bungeni.editor.dialogs;

import com.sun.star.beans.IllegalTypeException;
import com.sun.star.beans.PropertyExistException;
import com.sun.star.beans.PropertyVetoException;
import com.sun.star.beans.UnknownPropertyException;
import com.sun.star.beans.XPropertyContainer;
import com.sun.star.beans.XPropertySet;
import com.sun.star.container.NoSuchElementException;
import com.sun.star.container.XEnumeration;
import com.sun.star.container.XEnumerationAccess;
import com.sun.star.document.XDocumentInfo;
import com.sun.star.document.XDocumentInfoSupplier;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.lang.XComponent;
import com.sun.star.lang.XServiceInfo;
import com.sun.star.table.XCell;
import com.sun.star.text.XText;
import com.sun.star.text.XTextCursor;
import com.sun.star.text.XTextDocument;
import com.sun.star.text.XTextTable;
import com.sun.star.uno.Any;
import com.sun.star.uno.Any;
import com.sun.star.uno.AnyConverter;
import com.sun.star.uno.UnoRuntime;
import com.sun.star.uno.XComponentContext;
import javax.swing.Icon;
import javax.swing.JFrame;
import javax.swing.tree.DefaultTreeCellRenderer;
import org.bungeni.utils.DocStructureTreeModel;
import org.bungeni.utils.DocStructureTreeNode;

/**
 *
 * @author  Administrator
 */
public class editorTabbedPanel extends javax.swing.JPanel {
    XComponent Component;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(editorTabbedPanel.class.getName());
    private String[] arrDocTypes = { "Acts" , "DebateRecords", "Bills" };
    /** Creates new form SwingTabbedJPanel */
    public editorTabbedPanel() {
        initComponents();
    }
    
    public editorTabbedPanel(XComponent impComponent){
        
       this.Component = impComponent;
       initComponents();   
       initFields();
       initializeValues();
    }
    
    private void initFields(){
        initTree();
        
    }
    
    private void initTree(){
       DocStructureTreeModel treeModel = new DocStructureTreeModel(getTree());
       treeDocStructure.setModel(treeModel);
        DefaultTreeCellRenderer renderer = new DefaultTreeCellRenderer();
        Icon personIcon = null;
        renderer.setLeafIcon(personIcon);
        renderer.setClosedIcon(personIcon);
        renderer.setOpenIcon(personIcon);
        treeDocStructure.setCellRenderer(renderer);
      
    }
        
   private DocStructureTreeNode getDocumentTree() throws UnknownPropertyException{
       //get text handle
       XText objText = getTextDocument().getText();
       XEnumerationAccess objEnumAccess = (XEnumerationAccess) UnoRuntime.queryInterface( XEnumerationAccess.class, objText); 
       XEnumeration paraEnum =  objEnumAccess.createEnumeration();
       int nHeadsFound = 0;
       try {
        // While there are paragraphs, do things to them 
        while (paraEnum.hasMoreElements()) { 
            XServiceInfo xInfo;
            xInfo = null;
            Object objNextElement = null;
            objNextElement = paraEnum.nextElement();
                    //get service info
             xInfo = (XServiceInfo) UnoRuntime.queryInterface(XServiceInfo.class, objNextElement);
            if (xInfo.supportsService("com.sun.star.text.Paragraph")) { 
                // Access the paragraph's property set...the properties in this 
                // property set are listed 
                // in: com.sun.star.style.ParagraphProperties 
               
                XPropertySet xSet = (XPropertySet) UnoRuntime.queryInterface( 
                    XPropertySet.class, xInfo);
                     // Set the justification to be center justified 
                    Integer nLevel =  (Integer)xSet.getPropertyValue("NumberingLevel");
                    if (nLevel == 0 ){
                        nHeadsFound++;
                    }
            } /*
            else if (xInfo.supportsService("com.sun.star.TextTable")){
                    ///get texttable object
                    XTextTable xTable = (XTextTable)UnoRuntime.queryInterface(XTextTable.class, objNextElement); 
                    String[] cellNames = xTable.getCellNames();
                    for (int i=0; i < cellNames.length; i++) {
                        XCell tableCell = xTable.getCellByName(cellNames[i]);
                        XText xCellText = (XText) UnoRuntime.queryInterface(XText.class, tableCell); 
                        XTextCursor xCellCurs = xCellText.createTextCursor();
                        XPropertySet xCursorProps = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class,xCellCurs );
                        Integer iNumbering;
                            iNumbering = (Integer) xCursorProps.getPropertyValue("NumberingLevel");
                        if (iNumbering > 0 ) {
                            nHeadsFound++;
                        }
                    }               
                 }  */
        } 
        
        log.debug("no. of headings found = "+ nHeadsFound);
        } catch (WrappedTargetException ex) {
                log.debug(ex.getLocalizedMessage(), ex);
            } catch (NoSuchElementException ex) {
               log.debug(ex.getLocalizedMessage(), ex);
            } 
       finally {
            return new DocStructureTreeNode("return");
       }
   }
    
    /**** TEST METHOD *****/
    private DocStructureTreeNode getTree() {
        //the greatgrandparent generation
        DocStructureTreeNode main = new DocStructureTreeNode("Main");
        DocStructureTreeNode a1 = new DocStructureTreeNode("Jack (great-granddaddy)");
        DocStructureTreeNode a2 = new DocStructureTreeNode("Paul (great-granddaddy)");
 
        //the grandparent generation
        DocStructureTreeNode b1 = new DocStructureTreeNode("Peter (grandpa)");
        DocStructureTreeNode b2 = new DocStructureTreeNode("Simon (grandpa)");
        
        //the parent generation
        DocStructureTreeNode c1 = new DocStructureTreeNode("Frank (dad)");
        DocStructureTreeNode c2 = new DocStructureTreeNode("Louis (dad)");
        DocStructureTreeNode c3 = new DocStructureTreeNode("Laurence (dad)");
        DocStructureTreeNode c4 = new DocStructureTreeNode("Mark (dad)");
        DocStructureTreeNode c5 = new DocStructureTreeNode("Oliver (dad)");

        //the youngest generation
        DocStructureTreeNode d1 = new DocStructureTreeNode("Clement (boy)");
        DocStructureTreeNode d2 = new DocStructureTreeNode("Colin (boy)");
         DocStructureTreeNode d3 = new DocStructureTreeNode("Chamar (boy)");
        DocStructureTreeNode d4 = new DocStructureTreeNode("Cris (boy)");
        DocStructureTreeNode d5 = new DocStructureTreeNode("Claude (boy)");
        DocStructureTreeNode d6 = new DocStructureTreeNode("Camara(boy)");

        DocStructureTreeNode.makeRelation(main, new DocStructureTreeNode[] {a1, a2});
        DocStructureTreeNode.makeRelation(a1,new DocStructureTreeNode[] {b1});
        DocStructureTreeNode.makeRelation(a2,new DocStructureTreeNode[] {b2});
        
        DocStructureTreeNode.makeRelation(b1, new DocStructureTreeNode[] {c1, c2, c3} );
        DocStructureTreeNode.makeRelation(b2,new DocStructureTreeNode[] {c4,c5});
        
        DocStructureTreeNode.makeRelation(c1, new DocStructureTreeNode[] {d1, d2} );
        DocStructureTreeNode.makeRelation(c2,new DocStructureTreeNode[] {d3});
        DocStructureTreeNode.makeRelation(c3, new DocStructureTreeNode[] {d4} );
        DocStructureTreeNode.makeRelation(c4,new DocStructureTreeNode[] {d5});
        DocStructureTreeNode.makeRelation(c5, new DocStructureTreeNode[] {d6} );
        
     

        return a1;
    }

    private void initializeValues(){
        //get metadata property alues
        String strAuthor = ""; String strDocType = "";
          try {
        if (propertyExists("Bungeni_DocAuthor")){
          
                strAuthor = getPropertyValue("Bungeni_DocAuthor");
           
        }
        if (propertyExists("Bungeni_DocType")){
            strDocType = getPropertyValue("Bungeni_DocType");
        }
        
        txtDocAuthor.setText(strAuthor);
        txtDocType.setText(strDocType);
         } catch (UnknownPropertyException ex) {
                ex.printStackTrace();
            }
       
    }
    private XTextDocument getTextDocument(){
        XTextDocument xTextDoc = (XTextDocument) UnoRuntime.queryInterface(XTextDocument.class, this.Component);
        return xTextDoc;
    }
    
    private XDocumentInfo getDocumentInfo(XTextDocument doc){
      XDocumentInfoSupplier xdisInfoProvider =  (XDocumentInfoSupplier) UnoRuntime.queryInterface(XDocumentInfoSupplier.class, doc );
      return  xdisInfoProvider.getDocumentInfo();
    }
    
    private void addProperty (String propertyName, String value){
        
         XPropertyContainer xDocPropertiesContainer = (XPropertyContainer) UnoRuntime.queryInterface(XPropertyContainer.class, getDocumentInfo(getTextDocument()));
        try {
       
            xDocPropertiesContainer.addProperty(propertyName, (short)0, new Any(com.sun.star.uno.Type.STRING, value));
        } catch (PropertyExistException ex) {
            log.debug("Property " + propertyName + " already Exists");
        } catch (com.sun.star.lang.IllegalArgumentException ex) {
            log.debug(ex.getLocalizedMessage(), ex);
        } catch (IllegalTypeException ex) {
            log.debug(ex.getLocalizedMessage(), ex);
        }
    }
    
    private void setPropertyValue(String propertyName, String propertyValue) {
            XDocumentInfo xdi = getDocumentInfo(getTextDocument());
            XPropertySet xDocProperties = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, xdi);
            try{
                xDocProperties.setPropertyValue(propertyName, propertyValue);
            } catch (UnknownPropertyException ex) {
                ex.printStackTrace();
            } catch (WrappedTargetException ex) {
                ex.printStackTrace();
            } catch (com.sun.star.lang.IllegalArgumentException ex) {
                ex.printStackTrace();
            } catch (PropertyVetoException ex) {
                ex.printStackTrace();
            }
    }
    
    private String getPropertyValue(String propertyName ) throws UnknownPropertyException{
            XDocumentInfo xdi = getDocumentInfo(getTextDocument());
            String value="";
        XPropertySet xDocProperties = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, xdi);
        try {
             value = (String) xDocProperties.getPropertyValue(propertyName);
           /// value = anyUnoValue.toString();
        } catch (UnknownPropertyException ex) {
            log.debug("Property "+ propertyName+ " does not exit");
        } catch (WrappedTargetException ex) {
            log.debug(ex.getLocalizedMessage(), ex);
        } finally {
            return value;
        }
            
    }
    
    private boolean propertyExists(String propertyName){
        XDocumentInfo xdi = getDocumentInfo(getTextDocument());
        boolean bExists = false;
        XPropertySet xDocProperties = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, xdi);
        try {
     
                Object objValue =  xDocProperties.getPropertyValue(propertyName);
                bExists = true;
                log.debug("property Exists - value : "+ AnyConverter.toString(objValue) );
            } 
        catch (com.sun.star.lang.IllegalArgumentException ex) {
                        bExists = false;
                         log.debug("propertyExists - unknown property exception");
            }
         catch (UnknownPropertyException ex) {
                 log.debug("propertyExists - unknown property exception");
                //property does not exist
                    bExists = false;
        }
        catch (WrappedTargetException ex) {
                      bExists = false;
            }
        finally {
            return bExists;
        }
     }
    
    
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    // <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    private void initComponents() {
        btnGrpBodyMetadataTarget = new javax.swing.ButtonGroup();
        jTabsContainer = new javax.swing.JTabbedPane();
        panelMetadata = new javax.swing.JPanel();
        lblDocAuthor = new javax.swing.JLabel();
        txtDocAuthor = new javax.swing.JTextField();
        lblDocType = new javax.swing.JLabel();
        lblDocURI = new javax.swing.JLabel();
        cboDocURI = new javax.swing.JComboBox();
        btnSetMetadata = new javax.swing.JButton();
        txtDocType = new javax.swing.JTextField();
        panelBodyMetadata = new javax.swing.JPanel();
        lblSelectBodyMetadata = new javax.swing.JLabel();
        cboSelectBodyMetadata = new javax.swing.JComboBox();
        txtMetadataValue = new javax.swing.JTextField();
        lblEnterMetadataValue = new javax.swing.JLabel();
        btnLookupMetadata = new javax.swing.JButton();
        btnClearMetadataValue = new javax.swing.JButton();
        btnApplyMetaToSelectedText = new javax.swing.JButton();
        jRadioButton1 = new javax.swing.JRadioButton();
        jLabel1 = new javax.swing.JLabel();
        jRadioButton2 = new javax.swing.JRadioButton();
        panelHistory = new javax.swing.JPanel();
        tblDocHistory = new javax.swing.JScrollPane();
        jTable1 = new javax.swing.JTable();
        jLabel3 = new javax.swing.JLabel();
        panelNotes = new javax.swing.JPanel();
        jScrollPane2 = new javax.swing.JScrollPane();
        listboxEditorNotes = new javax.swing.JList();
        txtEditorNote = new javax.swing.JTextField();
        lblEditorNotes = new javax.swing.JLabel();
        btnNewEditorNote = new javax.swing.JButton();
        btnSaveEditorNote = new javax.swing.JButton();
        jLabel4 = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        treeDocStructure = new javax.swing.JTree();
        jLabel2 = new javax.swing.JLabel();

        jTabsContainer.setTabLayoutPolicy(javax.swing.JTabbedPane.SCROLL_TAB_LAYOUT);
        lblDocAuthor.setText("Author");

        lblDocType.setText("Document Type");

        lblDocURI.setText("Document URI");

        btnSetMetadata.setText("Set Metadata");
        btnSetMetadata.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnSetMetadataActionPerformed(evt);
            }
        });

        txtDocType.setEditable(false);

        org.jdesktop.layout.GroupLayout panelMetadataLayout = new org.jdesktop.layout.GroupLayout(panelMetadata);
        panelMetadata.setLayout(panelMetadataLayout);
        panelMetadataLayout.setHorizontalGroup(
            panelMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelMetadataLayout.createSequentialGroup()
                .add(panelMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(panelMetadataLayout.createSequentialGroup()
                        .addContainerGap()
                        .add(panelMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                            .add(txtDocAuthor, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE)
                            .add(lblDocAuthor, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE)
                            .add(lblDocType, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE)
                            .add(lblDocURI)
                            .add(cboDocURI, 0, 207, Short.MAX_VALUE)))
                    .add(panelMetadataLayout.createSequentialGroup()
                        .add(56, 56, 56)
                        .add(btnSetMetadata))
                    .add(panelMetadataLayout.createSequentialGroup()
                        .addContainerGap()
                        .add(txtDocType, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE)))
                .addContainerGap())
        );
        panelMetadataLayout.setVerticalGroup(
            panelMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelMetadataLayout.createSequentialGroup()
                .addContainerGap()
                .add(lblDocAuthor)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(txtDocAuthor, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lblDocType)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(txtDocType, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lblDocURI)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(cboDocURI, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 107, Short.MAX_VALUE)
                .add(btnSetMetadata)
                .add(19, 19, 19))
        );
        jTabsContainer.addTab("Doc. Metadata", panelMetadata);

        lblSelectBodyMetadata.setText("Select Metadata Element");

        cboSelectBodyMetadata.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Members Of Parliament", "Ontology", "Keywords", "Tabled Documents" }));

        lblEnterMetadataValue.setText("Enter Metadata Value");

        btnLookupMetadata.setText("Lookup...");

        btnClearMetadataValue.setText("Clear");

        btnApplyMetaToSelectedText.setText("Apply Metadata");

        btnGrpBodyMetadataTarget.add(jRadioButton1);
        jRadioButton1.setSelected(true);
        jRadioButton1.setText("Selected Text");
        jRadioButton1.setBorder(javax.swing.BorderFactory.createEmptyBorder(0, 0, 0, 0));
        jRadioButton1.setMargin(new java.awt.Insets(0, 0, 0, 0));

        jLabel1.setText("Select Target for Applying Metadata");

        btnGrpBodyMetadataTarget.add(jRadioButton2);
        jRadioButton2.setText("Current Document Section");
        jRadioButton2.setBorder(javax.swing.BorderFactory.createEmptyBorder(0, 0, 0, 0));
        jRadioButton2.setMargin(new java.awt.Insets(0, 0, 0, 0));

        org.jdesktop.layout.GroupLayout panelBodyMetadataLayout = new org.jdesktop.layout.GroupLayout(panelBodyMetadata);
        panelBodyMetadata.setLayout(panelBodyMetadataLayout);
        panelBodyMetadataLayout.setHorizontalGroup(
            panelBodyMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelBodyMetadataLayout.createSequentialGroup()
                .addContainerGap()
                .add(panelBodyMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(jLabel1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE)
                    .add(cboSelectBodyMetadata, 0, 207, Short.MAX_VALUE)
                    .add(lblSelectBodyMetadata, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE)
                    .add(lblEnterMetadataValue, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE)
                    .add(txtMetadataValue, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, panelBodyMetadataLayout.createSequentialGroup()
                        .add(btnClearMetadataValue, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 85, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 41, Short.MAX_VALUE)
                        .add(btnLookupMetadata))
                    .add(btnApplyMetaToSelectedText, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE)
                    .add(panelBodyMetadataLayout.createSequentialGroup()
                        .add(10, 10, 10)
                        .add(panelBodyMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                            .add(jRadioButton2)
                            .add(jRadioButton1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 156, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))))
                .addContainerGap())
        );
        panelBodyMetadataLayout.setVerticalGroup(
            panelBodyMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelBodyMetadataLayout.createSequentialGroup()
                .addContainerGap()
                .add(lblSelectBodyMetadata)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(cboSelectBodyMetadata, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lblEnterMetadataValue)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(txtMetadataValue, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 70, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(panelBodyMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(btnLookupMetadata)
                    .add(btnClearMetadataValue))
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jLabel1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 23, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jRadioButton1)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 11, Short.MAX_VALUE)
                .add(jRadioButton2)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btnApplyMetaToSelectedText)
                .addContainerGap())
        );
        jTabsContainer.addTab("Body Metadata", panelBodyMetadata);

        jTable1.setModel(new javax.swing.table.DefaultTableModel(
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
        tblDocHistory.setViewportView(jTable1);

        jLabel3.setText("Document Workflow History");

        org.jdesktop.layout.GroupLayout panelHistoryLayout = new org.jdesktop.layout.GroupLayout(panelHistory);
        panelHistory.setLayout(panelHistoryLayout);
        panelHistoryLayout.setHorizontalGroup(
            panelHistoryLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelHistoryLayout.createSequentialGroup()
                .addContainerGap()
                .add(panelHistoryLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(tblDocHistory, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 207, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(jLabel3, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 142, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                .addContainerGap(org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        panelHistoryLayout.setVerticalGroup(
            panelHistoryLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelHistoryLayout.createSequentialGroup()
                .addContainerGap()
                .add(jLabel3)
                .add(10, 10, 10)
                .add(tblDocHistory, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 209, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(50, Short.MAX_VALUE))
        );
        jTabsContainer.addTab("Doc. History", panelHistory);

        listboxEditorNotes.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        jScrollPane2.setViewportView(listboxEditorNotes);

        lblEditorNotes.setText("Editor Note");

        btnNewEditorNote.setText("New Note");

        btnSaveEditorNote.setText("Save Note");

        jLabel4.setText("View Archived Notes");

        org.jdesktop.layout.GroupLayout panelNotesLayout = new org.jdesktop.layout.GroupLayout(panelNotes);
        panelNotes.setLayout(panelNotesLayout);
        panelNotesLayout.setHorizontalGroup(
            panelNotesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(org.jdesktop.layout.GroupLayout.TRAILING, panelNotesLayout.createSequentialGroup()
                .addContainerGap()
                .add(panelNotesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, jScrollPane2, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, txtEditorNote, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, lblEditorNotes, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 163, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, panelNotesLayout.createSequentialGroup()
                        .add(btnNewEditorNote)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 41, Short.MAX_VALUE)
                        .add(btnSaveEditorNote))
                    .add(org.jdesktop.layout.GroupLayout.LEADING, jLabel4, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 207, Short.MAX_VALUE))
                .addContainerGap())
        );
        panelNotesLayout.setVerticalGroup(
            panelNotesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelNotesLayout.createSequentialGroup()
                .addContainerGap()
                .add(lblEditorNotes)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(txtEditorNote, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 92, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(panelNotesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(btnNewEditorNote)
                    .add(btnSaveEditorNote))
                .add(14, 14, 14)
                .add(jLabel4)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jScrollPane2, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 97, Short.MAX_VALUE)
                .addContainerGap())
        );
        jTabsContainer.addTab("Notes", panelNotes);

        jScrollPane1.setViewportView(treeDocStructure);

        jLabel2.setText("Document Structure");

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(jLabel2, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 212, Short.MAX_VALUE)
                .addContainerGap())
            .add(jTabsContainer, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 232, Short.MAX_VALUE)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(jScrollPane1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 212, Short.MAX_VALUE)
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(jTabsContainer, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 319, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(22, 22, 22)
                .add(jLabel2)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jScrollPane1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 199, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(21, 21, 21))
        );
    }// </editor-fold>//GEN-END:initComponents

    private void btnSetMetadataActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnSetMetadataActionPerformed
// TODO add your handling code here:
     String strAuthor="";
     String strDocType = "";
     
            strAuthor = this.txtDocAuthor.getText();
            strDocType = this.txtDocType.getText();
            log.debug("setting metadata......");
            
            if (!this.propertyExists("Bungeni_DocAuthor")) {
                this.addProperty("Bungeni_DocAuthor", strAuthor);
                log.debug("adding property - author");
            }
            else {
                this.setPropertyValue("Bungeni_DocAuthor", strAuthor);
                log.debug("setting property - author");
            }
            
            if (!this.propertyExists("Bungeni_DocType")) {
                this.addProperty("Bungeni_DocType", strDocType);
                log.debug("adding property - doctype ");
            }
            else {
                this.setPropertyValue("Bungeni_DocType", strDocType);
                log.debug("setting property - doctype");
            }
                
      
            //set the new values into the document
     
    }//GEN-LAST:event_btnSetMetadataActionPerformed
    
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnApplyMetaToSelectedText;
    private javax.swing.JButton btnClearMetadataValue;
    private javax.swing.ButtonGroup btnGrpBodyMetadataTarget;
    private javax.swing.JButton btnLookupMetadata;
    private javax.swing.JButton btnNewEditorNote;
    private javax.swing.JButton btnSaveEditorNote;
    private javax.swing.JButton btnSetMetadata;
    private javax.swing.JComboBox cboDocURI;
    private javax.swing.JComboBox cboSelectBodyMetadata;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JRadioButton jRadioButton1;
    private javax.swing.JRadioButton jRadioButton2;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JTable jTable1;
    private javax.swing.JTabbedPane jTabsContainer;
    private javax.swing.JLabel lblDocAuthor;
    private javax.swing.JLabel lblDocType;
    private javax.swing.JLabel lblDocURI;
    private javax.swing.JLabel lblEditorNotes;
    private javax.swing.JLabel lblEnterMetadataValue;
    private javax.swing.JLabel lblSelectBodyMetadata;
    private javax.swing.JList listboxEditorNotes;
    private javax.swing.JPanel panelBodyMetadata;
    private javax.swing.JPanel panelHistory;
    private javax.swing.JPanel panelMetadata;
    private javax.swing.JPanel panelNotes;
    private javax.swing.JScrollPane tblDocHistory;
    private javax.swing.JTree treeDocStructure;
    private javax.swing.JTextField txtDocAuthor;
    private javax.swing.JTextField txtDocType;
    private javax.swing.JTextField txtEditorNote;
    private javax.swing.JTextField txtMetadataValue;
    // End of variables declaration//GEN-END:variables
   public static void main(String args[]) {
    JFrame frame = new JFrame("Oval Sample");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

   editorTabbedPanel panel = new editorTabbedPanel();
   frame.add(panel);
   frame.setSize(200,400);
   frame.setVisible(true);
  }   
}
