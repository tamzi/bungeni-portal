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
import com.sun.star.frame.XModel;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.lang.XComponent;
import com.sun.star.lang.XServiceInfo;
import com.sun.star.table.XCell;
import com.sun.star.text.XText;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextCursor;
import com.sun.star.text.XTextDocument;
import com.sun.star.text.XTextRange;
import com.sun.star.text.XTextTable;
import com.sun.star.text.XTextViewCursor;
import com.sun.star.text.XTextViewCursorSupplier;
import com.sun.star.uno.Any;
import com.sun.star.uno.Any;
import com.sun.star.uno.AnyConverter;
import com.sun.star.uno.UnoRuntime;
import com.sun.star.uno.XComponentContext;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.Vector;
import javax.swing.BorderFactory;
import javax.swing.DefaultListModel;
import javax.swing.Icon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTree;
import javax.swing.ListCellRenderer;
import javax.swing.ListSelectionModel;
import javax.swing.border.Border;
import javax.swing.border.EtchedBorder;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.tree.DefaultTreeCellRenderer;
import org.apache.commons.collections.map.MultiValueMap;
import org.bungeni.editor.dialogs.swingxpanels.swingXPanel01;
import org.bungeni.editor.panels.ICollapsiblePanel;
import org.bungeni.editor.panels.sectionPanel;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.utils.DocStructureElement;
import org.bungeni.utils.StackedBox;
/*
import org.bungeni.utils.DocStructureTreeModel;
import org.bungeni.utils.DocStructureTreeNode;
*/
/**
 *
 * @author  Administrator
 */
public class editorTabbedPanel extends javax.swing.JPanel {
    /**
     * XComponent object, handle to current openoffice document instance
     */
    XComponent Component;
    private OOComponentHelper ooDocument;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(editorTabbedPanel.class.getName());
    private String[] arrDocTypes = { "Acts" , "DebateRecords", "Bills" };
    //vector that houses the list of document headings used by the display tree
    private Vector<DocStructureElement> mvDocumentHeadings = new Vector<DocStructureElement>();
         
    /** Creates new form SwingTabbedJPanel */
    public editorTabbedPanel() {
        initComponents();
    }
    
    /**
     * Constructor for main Tabbed panel interface
     */
    public editorTabbedPanel(XComponent impComponent){
        
       this.Component = impComponent;
       ooDocument = new OOComponentHelper(impComponent);
       initComponents();   
       initFields();
       initializeValues();
       panelMarkup.setLayout(new FlowLayout());
       initCollapsiblePane();
    }
    
    private void initFields(){
        //initTree();
        initList();
        
    }
    
    private void initCollapsiblePane(){
     try {
     StackedBox box = new StackedBox();    
     //create scroll pane with stacked box
     log.debug("initializing stackedbox");
     
     JScrollPane scrollPane = new JScrollPane(box);
     scrollPane.setBorder(null);
     //add the scroll pane to the scroll pane
     panelMarkup.add(scrollPane, BorderLayout.CENTER);
     sectionPanel panel  = new sectionPanel();
     panel.setOOComponentHandle(ooDocument);
     box.addBox("Section Tools", panel );   
     Class eventHandlerClass;
     eventHandlerClass = Class.forName("org.bungeni.editor.panels.textmarkupPanel");
     ICollapsiblePanel iPanel = (ICollapsiblePanel) eventHandlerClass.newInstance();
     iPanel.setOOComponentHandle(ooDocument); 
     box.addBox("Markup Tools", iPanel.getObjectHandle() ); 
     
     }
     catch (Exception e){
         log.debug("exception : "+ e.getMessage());
     }
     
    }
    
    private void initList(){
       
       try { 
       XText objText = ooDocument.getTextDocument().getText();//getTextDocument().getText();
       
       XEnumerationAccess objEnumAccess = (XEnumerationAccess) UnoRuntime.queryInterface( XEnumerationAccess.class, objText); 
       XEnumeration paraEnum =  objEnumAccess.createEnumeration();
       int nHeadsFound = 0;
       int nMaxLevel = 0;
       int nPrevLevel = 0;
       DocStructureElement previousElement = null;
                
       
        // While there are paragraphs, do things to them 
        //first we find the number of heading paragraphs
        log.debug("Inside getDocumentTree, entering, hasMoreElements");
        
        while (paraEnum.hasMoreElements()) { 
            //log.debug("Inside getDocumentTree, inside, hasMoreElements");

            XServiceInfo xInfo;
            xInfo = null;
            Object objNextElement = null;
     
                objNextElement = paraEnum.nextElement();
       
                    //get service info
             xInfo = ooDocument.getServiceInfo(objNextElement); // UnoRuntime.queryInterface(XServiceInfo.class, objNextElement);
            if (xInfo.supportsService("com.sun.star.text.Paragraph")) { 
                // Access the paragraph's property set...the properties in this 
                // property set are listed 
                // in: com.sun.star.style.ParagraphProperties 
                // log.debug("Inside getDocumentTree, supportsService paragraph");

                XPropertySet xSet = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, xInfo);
                     // Set the justification to be center justified 
                    //log.debug("Inside getDocumentTree, before , NumberingLevel");
                        
                    short nLevel = -1;
                 
                    nLevel = AnyConverter.toShort(xSet.getPropertyValue("ParaChapterNumberingLevel"));
                   
                    
                    //log.debug("Inside getDocumentTree, after , NumberingLevel = "+ nLevel);
                    /*
                     *count total headings >= level 0
                     *iterate through all the headings again
                     *for each heading add the level information for the heading
                     */
                    if (nLevel >= 0 ){
                        
                        nHeadsFound++;
                        XTextContent xContent = ooDocument.getTextContent(objNextElement);
                        XTextRange aTextRange =   xContent.getAnchor();
                        String strHeading = aTextRange.getString();
                        
                        if (nLevel > nMaxLevel)
                            nMaxLevel = nLevel;
                        
                        
                        DocStructureElement element = new DocStructureElement(strHeading, nLevel, nHeadsFound, aTextRange );
                        if (previousElement == null  ){ 
                            previousElement = element;
                        }
                        else{
                            int currentVectorIndex = nHeadsFound - 1;
                            //get prev index
                            DocStructureElement prev = (DocStructureElement) mvDocumentHeadings.elementAt(currentVectorIndex - 1);
                             
                            //get element at previous index
                            if (previousElement.getLevel() <  element.getLevel()) {
                                prev.hasChildren(true);
                                mvDocumentHeadings.setElementAt(prev, currentVectorIndex - 1);
                            }
                            else {
                                prev.hasChildren(false);
                                mvDocumentHeadings.setElementAt(prev, currentVectorIndex - 1);
                            }
                        }
                           
                        //log.debug("adding heading level =" + nLevel + " and heading count = "+nHeadsFound);
                        mvDocumentHeadings.addElement(element);
                        
                        //TextRange can be used to getText()
                        // XText xRangeText = aTextRange.getText();
                        /*
                        XEnumerationAccess xRangeAccess = (XEnumerationAccess)UnoRuntime.queryInterface(com.sun.star.container.XEnumerationAccess.class,
                                                                                                        objNextElement);
                        if (xRangeAccess == null) {
                            log.debug("RangeAccess was null");
                        }                                                                                
                        XEnumeration portionEnum =  xRangeAccess.createEnumeration();
                        while (portionEnum.hasMoreElements()){
                            Object textPortion =  portionEnum.nextElement();  
                            XServiceInfo xTextPortionService= getServiceInfo(textPortion);
                            if (xTextPortionService.supportsService( "com.sun.star.text.TextPortion")){
                                XPropertySet xTextPortionProps = (XPropertySet)UnoRuntime.queryInterface(XPropertySet.class, textPortion);
                                String textPortionType="";
                                textPortionType = AnyConverter.toString(xTextPortionProps.getPropertyValue("TextPortionType"));
                                if (textPortionType.equals("ReferenceMark"){
                                    if ()
                                }
                            }
                        }*/
                 
                    }
            }
            else           log.debug("Inside getDocumentTree, paragraph not supproted");
            

           
          
             //now we look for subheadings of headings....
             /*
             int nHeadCounter = 0;
             int iCounter = 0;
             XEnumerationAccess objEnumAccess2 = (XEnumerationAccess) UnoRuntime.queryInterface( XEnumerationAccess.class, objText); 
             paraEnum =  objEnumAccess2.createEnumeration();
             while ((nHeadCounter < nHeadsFounds ) && paraEnum.hasMoreElements() ) {
                 XServiceInfo xInfo;
                 xInfo = null;
                Object objNextElement = null;
                objNextElement = paraEnum.nextElement();
                        //get service info
                  xInfo = getServiceInfo(objNextElement);
                if (xInfo.supportsService("com.sun.star.text.Paragraph")) { 
                       iCounter++;
                       XPropertySet xSet = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, xInfo);
                     // Set the justification to be center justified 
                        Integer nLevel =  (Integer)xSet.getPropertyValue("NumberingLevel");
                        if (nLevel >= 0) {
                            nHeadCounter++;
                            XTextContent xContent = getTextContent(objNextElement);
                            
                        }
                    }
             }
             
            */
            
             /*
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
             
             //Fill an array with hedings and heading levels....
             
             
        } 
        
            /*
           if (nHeadsFound > 0 ) {
                 log.debug("size of headings array = "+ vHeadings.size());
                DocStructureTreeNode[] docStruct = new DocStructureTreeNode[vHeadings.size()];
                 for (int i=0; i < vHeadings.size(); i++) {
                      log.debug("adding headings to array "+ i);
                     docStruct[i] = (DocStructureTreeNode) vHeadings.elementAt(i);
                 }
             DocStructureTreeNode.makeRelation(mainNode, docStruct);
             }*/
        
             if (nHeadsFound > 0 ){
                //iterate through the vector and add elemnts to list
                DefaultListModel model = new DefaultListModel();
                for (int i=0 ; i < mvDocumentHeadings.size(); i++)
                     {               
                        DocStructureElement elem = (DocStructureElement)mvDocumentHeadings.elementAt(i);
                        model.addElement(elem);
                     }
                    // ListSelectionModel selectionModel = treeDocStructure.getSelectionModel();
                    // selectionModel.addListSelectionListener(new DocStructureListSelectionHandler());
                        
                     treeDocStructure.setModel(model);
                     treeDocStructure.setCellRenderer(new DocStructureListElementRenderer());
                     treeDocStructure.addMouseListener(new DocStructureListMouseListener());
                  }
        
             /*
            For i = 0 to nHeadCount
                    If mOutlines(i, 1) <= nDisplayLevel then
                            nPosn = nPosn + 1
                            SubAddItem(oListBox, i, nPosn, nDisplayLevel)
                            mLinks(nPosn) = i
                    End If
            Next
              */
        
           } catch (NoSuchElementException ex) {
                ex.printStackTrace();
            } catch (WrappedTargetException ex) {
                ex.printStackTrace();
            }
            catch (com.sun.star.lang.IllegalArgumentException ex) {
                        ex.printStackTrace();
                    } 
            catch (UnknownPropertyException ex) {
                        ex.printStackTrace();
                    }
            
   }
    
    /**
     * Mouse event listener for list box displaying document structure
     */
    class DocStructureListMouseListener implements MouseListener{
        public void mouseClicked(MouseEvent e) {
            if (e.getClickCount() == 2){
                JList listBox = (JList)e.getSource();
                listBox.getMaxSelectionIndex();
                int nIndex = listBox.locationToIndex(e.getPoint());
                //JOptionPane.showMessageDialog(null, "current selected index is = "+ nIndex);
                
                //get view cursor 
                XTextViewCursor xViewCursor = ooDocument.getViewCursor();
                //get the current object range
                DocStructureElement docElement = (DocStructureElement)mvDocumentHeadings.elementAt(nIndex);
                //move the view cursor to the element's range
                xViewCursor.gotoRange(docElement.getRange(), false);
            }
        }

        public void mousePressed(MouseEvent e) {
        }

        public void mouseReleased(MouseEvent e) {
        }

        public void mouseEntered(MouseEvent e) {
        }

        public void mouseExited(MouseEvent e) {
        }
        
    }
    class DocStructureListSelectionHandler implements ListSelectionListener {
    public void valueChanged(ListSelectionEvent e) {
        ListSelectionModel lsm = (ListSelectionModel)e.getSource();
        if (lsm.isSelectionEmpty()) {
            return;
        } else {
            // Find out which indexes are selected.
            int minIndex = lsm.getMinSelectionIndex();
            int maxIndex = lsm.getMaxSelectionIndex();
            for (int i = minIndex; i <= maxIndex; i++) {
                if (lsm.isSelectedIndex(i)) {
                    JOptionPane.showMessageDialog(null, "Current Selected Index is = "+ i);
                }
            }
        }
    }
}

    /*
    private void initTree(){
       DocStructureTreeModel treeModel = new DocStructureTreeModel(getDocumentTree());
       treeDocStructure.setModel(treeModel);
        DefaultTreeCellRenderer renderer = new DefaultTreeCellRenderer();
        Icon personIcon = null;
        renderer.setLeafIcon(personIcon);
        renderer.setClosedIcon(personIcon);
        renderer.setOpenIcon(personIcon);
        treeDocStructure.setCellRenderer(renderer);
      
    }
    */
    
   private class documentNodeMapKey {
       int level;
       int count;
   }
   
   
   
   private XServiceInfo getServiceInfo(Object obj){
             XServiceInfo xInfo = (XServiceInfo) UnoRuntime.queryInterface(XServiceInfo.class, obj);
             return xInfo;
   }
    
    private XTextContent getTextContent(Object element){
        XTextContent xContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, element);
        return xContent;
    }
 
    /**** TEST METHOD *****/
  /*
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
*/
    private void initializeValues(){
        //get metadata property alues
        String strAuthor = ""; String strDocType = "";
          try {
        if (ooDocument.propertyExists("Bungeni_DocAuthor")){
          
                strAuthor = ooDocument.getPropertyValue("Bungeni_DocAuthor");
           
        }
        if (ooDocument.propertyExists("Bungeni_DocType")){
            strDocType = ooDocument.getPropertyValue("Bungeni_DocType");
        }
        
        txtDocAuthor.setText(strAuthor);
        txtDocType.setText(strDocType);
         } catch (UnknownPropertyException ex) {
                ex.printStackTrace();
            }
       
    }
    
    /*           
            
    private XTextDocument getTextDocument(){
        XTextDocument xTextDoc = (XTextDocument) UnoRuntime.queryInterface(XTextDocument.class, this.Component);
        return xTextDoc;
    }
    
    private XModel getDocumentModel(){
        return (XModel)UnoRuntime.queryInterface(XModel.class, this.Component);
    }
    
    private XTextViewCursor getViewCursor(){
     XTextViewCursorSupplier xViewCursorSupplier = (XTextViewCursorSupplier)UnoRuntime.queryInterface(XTextViewCursorSupplier.class, getDocumentModel().getCurrentController());
     XTextViewCursor xViewCursor = xViewCursorSupplier.getViewCursor();
     return xViewCursor;
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
    
     */
    
    /**
     * Class that handles rendering of List cell elements, in the Document Structure listbox
     */
public class DocStructureListElementRenderer extends JLabel implements ListCellRenderer {
    private  final Color HIGHLIGHT_COLOR = new Color(0, 0, 128);
    private Color [] COLOR_LEVELS = {
                        new Color(104, 104,104),
                        new Color(124, 124,124),
                        new Color(144, 144,144),
                        new Color(164, 164,164),
                        new Color(184, 184,184),
                        new Color(204, 204,204),
                        new Color(224, 224,224)
    };
    private Border raisedEtched, lineBorder;
        /**
         * Constructor for List cell renderer class
         */
    public DocStructureListElementRenderer( ) {
        setOpaque(true);
        setIconTextGap(12);
         raisedEtched = BorderFactory.createRaisedBevelBorder();
         lineBorder = BorderFactory.createLineBorder(Color.GRAY);
        
    }

    public Component getListCellRendererComponent(
        JList list,
        Object value,
        int index,
        boolean isSelected,
        boolean cellHasFocus)
    {
        DocStructureElement entry = (DocStructureElement)value;
        int nMaxIndex = COLOR_LEVELS.length - 1;
        int nLevel = entry.getLevel();
        if (nLevel > nMaxIndex)
            setBackground(Color.WHITE);
        else
            setBackground(COLOR_LEVELS[nLevel]);
        //setBorder(lineBorder);
        setText(entry.toString());
        setFont(new java.awt.Font("Tahoma", 0, 10));
        
        
        //setIcon(entry.getImage());
        if(isSelected) {
            setForeground(Color.white);
            setBorder(raisedEtched);
        } else {
            setForeground(Color.black);
            setBorder(lineBorder);
        }
        return this;
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
        panelMarkup = new javax.swing.JPanel();
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
        jLabel2 = new javax.swing.JLabel();
        scrollPane_treeDocStructure = new javax.swing.JScrollPane();
        treeDocStructure = new javax.swing.JList();

        setFont(new java.awt.Font("Tahoma", 0, 10));
        jTabsContainer.setTabLayoutPolicy(javax.swing.JTabbedPane.SCROLL_TAB_LAYOUT);
        jTabsContainer.setFont(new java.awt.Font("Tahoma", 0, 10));
        panelMetadata.setFont(new java.awt.Font("Tahoma", 0, 10));
        lblDocAuthor.setFont(new java.awt.Font("Tahoma", 0, 10));
        lblDocAuthor.setText("Author");

        lblDocType.setFont(new java.awt.Font("Tahoma", 0, 10));
        lblDocType.setText("Document Type");

        lblDocURI.setFont(new java.awt.Font("Tahoma", 0, 10));
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
                            .add(txtDocAuthor, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                            .add(lblDocAuthor, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                            .add(lblDocType, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                            .add(lblDocURI)
                            .add(cboDocURI, 0, 218, Short.MAX_VALUE)))
                    .add(panelMetadataLayout.createSequentialGroup()
                        .add(56, 56, 56)
                        .add(btnSetMetadata))
                    .add(panelMetadataLayout.createSequentialGroup()
                        .addContainerGap()
                        .add(txtDocType, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)))
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
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 127, Short.MAX_VALUE)
                .add(btnSetMetadata)
                .add(19, 19, 19))
        );
        jTabsContainer.addTab("Doc. Metadata", panelMetadata);

        lblSelectBodyMetadata.setText("Select Metadata Element");

        cboSelectBodyMetadata.setFont(new java.awt.Font("Tahoma", 0, 10));
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
                    .add(jLabel1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(cboSelectBodyMetadata, 0, 218, Short.MAX_VALUE)
                    .add(lblSelectBodyMetadata, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(lblEnterMetadataValue, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(txtMetadataValue, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, panelBodyMetadataLayout.createSequentialGroup()
                        .add(btnClearMetadataValue, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 85, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 52, Short.MAX_VALUE)
                        .add(btnLookupMetadata))
                    .add(btnApplyMetaToSelectedText, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
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
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 29, Short.MAX_VALUE)
                .add(jRadioButton2)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btnApplyMetaToSelectedText)
                .addContainerGap())
        );
        jTabsContainer.addTab("Body Metadata", panelBodyMetadata);

        org.jdesktop.layout.GroupLayout panelMarkupLayout = new org.jdesktop.layout.GroupLayout(panelMarkup);
        panelMarkup.setLayout(panelMarkupLayout);
        panelMarkupLayout.setHorizontalGroup(
            panelMarkupLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(0, 238, Short.MAX_VALUE)
        );
        panelMarkupLayout.setVerticalGroup(
            panelMarkupLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(0, 311, Short.MAX_VALUE)
        );
        jTabsContainer.addTab("Markup", panelMarkup);

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
                    .add(tblDocHistory, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 197, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(jLabel3, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 142, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                .addContainerGap(31, Short.MAX_VALUE))
        );
        panelHistoryLayout.setVerticalGroup(
            panelHistoryLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelHistoryLayout.createSequentialGroup()
                .addContainerGap()
                .add(jLabel3)
                .add(10, 10, 10)
                .add(tblDocHistory, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 209, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(67, Short.MAX_VALUE))
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
                    .add(org.jdesktop.layout.GroupLayout.LEADING, jScrollPane2, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, txtEditorNote, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, lblEditorNotes, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 163, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, panelNotesLayout.createSequentialGroup()
                        .add(btnNewEditorNote)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 52, Short.MAX_VALUE)
                        .add(btnSaveEditorNote))
                    .add(org.jdesktop.layout.GroupLayout.LEADING, jLabel4, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE))
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
                .add(jScrollPane2, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 114, Short.MAX_VALUE)
                .addContainerGap())
        );
        jTabsContainer.addTab("Notes", panelNotes);

        jLabel2.setText("Document Structure");

        treeDocStructure.setFont(new java.awt.Font("Tahoma", 0, 10));
        treeDocStructure.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        scrollPane_treeDocStructure.setViewportView(treeDocStructure);

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(jLabel2, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 223, Short.MAX_VALUE)
                .addContainerGap())
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(scrollPane_treeDocStructure, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 223, Short.MAX_VALUE)
                .addContainerGap())
            .add(jTabsContainer, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 243, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(jTabsContainer, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 335, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jLabel2)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(scrollPane_treeDocStructure, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 209, Short.MAX_VALUE)
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents

    private void btnSetMetadataActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnSetMetadataActionPerformed
// TODO add your handling code here:
     String strAuthor="";
     String strDocType = "";
     
            strAuthor = this.txtDocAuthor.getText();
            strDocType = this.txtDocType.getText();
            log.debug("setting metadata......");
            
            if (!ooDocument.propertyExists("Bungeni_DocAuthor")) {
                ooDocument.addProperty("Bungeni_DocAuthor", strAuthor);
                log.debug("adding property - author");
            }
            else {
                ooDocument.setPropertyValue("Bungeni_DocAuthor", strAuthor);
                log.debug("setting property - author");
            }
            
            if (!ooDocument.propertyExists("Bungeni_DocType")) {
                ooDocument.addProperty("Bungeni_DocType", strDocType);
                log.debug("adding property - doctype ");
            }
            else {
                ooDocument.setPropertyValue("Bungeni_DocType", strDocType);
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
    private javax.swing.JPanel panelMarkup;
    private javax.swing.JPanel panelMetadata;
    private javax.swing.JPanel panelNotes;
    private javax.swing.JScrollPane scrollPane_treeDocStructure;
    private javax.swing.JScrollPane tblDocHistory;
    private javax.swing.JList treeDocStructure;
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
