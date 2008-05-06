/*
 * editorTabbedPanel.java
 *
 * Created on May 28, 2007, 3:55 PM
 */

package org.bungeni.editor.dialogs;

import com.sun.star.animations.Event;
import com.sun.star.beans.IllegalTypeException;
import com.sun.star.beans.PropertyExistException;
import com.sun.star.beans.PropertyVetoException;
import com.sun.star.beans.UnknownPropertyException;
import com.sun.star.beans.XPropertyContainer;
import com.sun.star.beans.XPropertySet;
import com.sun.star.beans.XPropertySetInfo;
import com.sun.star.container.NoSuchElementException;
import com.sun.star.container.XContentEnumerationAccess;
import com.sun.star.container.XEnumeration;
import com.sun.star.container.XEnumerationAccess;
import com.sun.star.container.XNameContainer;
import com.sun.star.container.XNamed;
import com.sun.star.document.XDocumentInfo;
import com.sun.star.document.XDocumentInfoSupplier;
import com.sun.star.document.XEventBroadcaster;
import com.sun.star.frame.XFrame;
import com.sun.star.frame.XModel;
import com.sun.star.lang.EventObject;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.lang.XComponent;
import com.sun.star.lang.XServiceInfo;
import com.sun.star.table.XCell;
import com.sun.star.text.XRelativeTextContentInsert;
import com.sun.star.text.XText;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextCursor;
import com.sun.star.text.XTextDocument;
import com.sun.star.text.XTextRange;
import com.sun.star.text.XTextSection;
import com.sun.star.text.XTextTable;
import com.sun.star.text.XTextViewCursor;
import com.sun.star.text.XTextViewCursorSupplier;
import com.sun.star.uno.Any;
import com.sun.star.uno.Any;
import com.sun.star.uno.AnyConverter;
import com.sun.star.uno.Type;
import com.sun.star.uno.UnoRuntime;
import com.sun.star.uno.XComponentContext;
import com.sun.star.xml.AttributeData;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.EventQueue;
import java.awt.FlowLayout;
import java.awt.Frame;
import java.awt.GridLayout;
import java.awt.Point;
import java.awt.Toolkit;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.Transferable;
import java.awt.datatransfer.UnsupportedFlavorException;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.InputEvent;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.beans.PropertyChangeEvent;
import java.beans.VetoableChangeListener;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.Iterator;
import java.util.ListIterator;
import java.util.Set;
import java.util.TreeMap;
import java.util.Vector;
import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.BorderFactory;
import javax.swing.ComboBoxModel;
import javax.swing.DefaultComboBoxModel;
import javax.swing.DefaultListModel;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTree;
import javax.swing.ListCellRenderer;
import javax.swing.ListModel;
import javax.swing.ListSelectionModel;
import javax.swing.Timer;
import javax.swing.WindowConstants;
import javax.swing.border.Border;
import javax.swing.border.EtchedBorder;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableColumn;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreeCellRenderer;
import javax.swing.tree.TreePath;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.BungeniRegistryFactory;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.db.GeneralQueryFactory;
import org.bungeni.db.QueryResults;
import org.bungeni.editor.dialogs.tree.NodeMoveTransferHandler;
import org.bungeni.editor.dialogs.tree.TreeDropTarget;
import org.bungeni.editor.macro.ExternalMacro;
import org.bungeni.editor.macro.ExternalMacroFactory;
import org.bungeni.editor.metadata.DocumentMetadata;
import org.bungeni.editor.metadata.DocumentMetadataEditInvoke;
import org.bungeni.editor.metadata.DocumentMetadataSupplier;
import org.bungeni.editor.metadata.DocumentMetadataTableModel;
import org.bungeni.editor.panels.CollapsiblePanelFactory;
import org.bungeni.editor.panels.FloatingPanelFactory;
import org.bungeni.editor.panels.ICollapsiblePanel;
import org.bungeni.editor.panels.IFloatingPanel;
import org.bungeni.ooo.BungenioOoHelper;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooDocNoteStructure;
import org.bungeni.ooo.ooDocNotes;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.ooo.ooUserDefinedAttributes;
import org.bungeni.utils.BungeniDataReader;
import org.bungeni.ooo.utils.CommonExceptionUtils;
import org.bungeni.utils.CommonTreeFunctions;
import org.bungeni.utils.DocStructureElement;
import org.bungeni.utils.MessageBox;
import org.bungeni.utils.StackedBox;
import org.bungeni.utils.TextSizeFilter;
import org.bungeni.utils.BungeniBTree;
import org.bungeni.utils.BungeniBNode;
import org.bungeni.editor.BungeniEditorProperties;
import java.beans.*;
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
    private XComponent Component;
    private XComponentContext ComponentContext;
    private BungenioOoHelper ooHelper;
    private OOComponentHelper ooDocument;
    private ooDocNotes m_ooNotes;
    private JFrame parentFrame;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(editorTabbedPanel.class.getName());
    private String[] arrDocTypes = { "Acts" , "DebateRecords", "Bills" };
    //vector that houses the list of document headings used by the display tree
    private Vector<DocStructureElement> mvDocumentHeadings = new Vector<DocStructureElement>();
    private Vector<String> mvSections = new Vector<String>();
    private DefaultMutableTreeNode sectionsRootNode;
    private Timer sectionNameTimer;
    private String currentSelectedSectionName = "";
    private Timer docStructureTimer;
    private Timer componentsTrackingTimer;
    
    private Thread tStructure;
    private changeStructureItem selectedChangeStructureItem;
    private JTree treeDocStructureTree;
    private JPopupMenu popupMenuTreeStructure = new JPopupMenu();
    private boolean mouseOver_TreeDocStructureTree = false;
    private boolean program_refresh_documents = false;
    private TreeMap<String, componentHandleContainer> editorMap;
    private String activeDocument; 
    private DocumentMetadataTableModel docMetadataTableModel;
    
    private HashMap<String, ICollapsiblePanel> dynamicPanelMap = new HashMap<String,ICollapsiblePanel>();
    private HashMap<String, IFloatingPanel> floatingPanelMap = new HashMap<String,IFloatingPanel>();
    
    private metadataTabbedPanel metadataTabbedPanel = null;

    private JFrame metadataPanelParentFrame = null;

    /** Creates new form SwingTabbedJPanel */
    public editorTabbedPanel() {
        initComponents();
    }
    
    /**
     * Constructor for main Tabbed panel interface
     */
    public editorTabbedPanel(XComponent impComponent, BungenioOoHelper helperObj, JFrame parentFrame){
        
       this.Component = impComponent;
       this.ooHelper = helperObj;
       this.ComponentContext = ooHelper.getComponentContext();
       editorMap = new TreeMap<String, componentHandleContainer>();
       ooDocument = new OOComponentHelper(impComponent, ComponentContext);
       this.parentFrame = parentFrame;
       this.activeDocument = BungeniEditorProperties.getEditorProperty("activeDocumentMode");
       init();
      
    }
    
    /* we need three options,
     *one that launches with a blank document
     *the other that allows the user to edit a document
     *the last that launches just the editor panel and attaches it self to existing instances of oOo
     */
    /*this one prompts the user to select a currently open document */
    public editorTabbedPanel(BungenioOoHelper helperObj, JFrame parentFrame){
        
      // this.Component = impComponent;
     //  this.ComponentContext = impComponentContext;
       this.ooHelper = helperObj;
       editorMap = new TreeMap<String, componentHandleContainer>();
       //prompt the user to select a document 
       //ooDocument = new OOComponentHelper(impComponent, impComponentContext);
       this.parentFrame = parentFrame;
       
       init();
    }
   
    private void init() {
       initComponents();   
       //initListDocuments();
       initFields();
       initializeValues();
       initFloatingPane();
        //initCollapsiblePane();
       initNotesPanel();
       initBodyMetadataPanel();
       initTimers();
       initDialogListeners();
       log.debug("calling initOpenDOcuments");
       initOpenDocuments();
       updateListDocuments();
       initTableDocMetadata();
       //metadataChecks();
    }
    
    private boolean checkTableDocMetadata(){
        DocumentMetadata [] mMetaData=docMetadataTableModel.getMetadataSupplier().getDocumentMetadata();
        for(int i=0;i<mMetaData.length;i++){
              if ((mMetaData[i].getName().equals("doctype") && mMetaData[i].getValue().equals("")))
              {
                  log.debug("Setting document type value from document metadata");
                  try{
                       
                       mMetaData[i].setValue(ooDocument.getPropertyValue("doctype"));
                  }catch(UnknownPropertyException ex){
                      log.debug("Property bungeni_document_type does not exist" + ex.getMessage());
                  }
                 
                 
                 // docMetadataTableModel.getMetadataSupplier().updateMetadataToDocument("doctype");
             } else if (mMetaData[i].getValue().equals("")) {
                     mMetaData[i].setValue("test_value");
              }
          }
        return true;
    }

    private void initTableDocMetadata(){
        
        //document metadata table model is created
        docMetadataTableModel = new DocumentMetadataTableModel(ooDocument);
        //add the check for valid metadata here 
        //if (true) set it to the table, else error 
       
       if(checkTableDocMetadata()){
            docMetadataTableModel.getMetadataSupplier().updateMetadataToDocument("doctype");
            tableDocMetadata.setModel(docMetadataTableModel );
       }
       /*
         //DocumentMetadataTableModel mModel  = (DocumentMetadataTableModel) tableDocMetadata.getModel();
         DocumentMetadata [] m=docMetadataTableModel.getMetadataSupplier().getDocumentMetadata();
         
         
         //checkDocument Type here
         //check to see if current document has docttype
    
         for(int i=0;i<m.length;i++){
              if ((m[i].getName().equals("doctype") && m[i].getValue().equals("")))
              {
                  log.debug("Setting document type value");
                  m[i].setValue(activeDocument);
                  // docMetadataTableModel.getMetadataSupplier().updateMetadataToDocument("doctype");
             } 
          }
          
         
         
        
        */
        
        //table model is set
        //tableDocMetadata.setModel(docMetadataTableModel );
        //various listeners are added 
       tableDocMetadata.addMouseListener(new DocumentMetadataTableMouseListener());
       //the actionListener uses the tableDocMetadata's custom model in the refreshMetadata call
       //so we move the call to the addaction listener after the table model has been set.
       cboListDocuments.addActionListener(new cboListDocumentsActionListener());
       //cboListDocuments.addVetoableChangeListener(new cboListDocumentsVetoableChangeListener());
    }    

    protected void setOODocumentObject (OOComponentHelper ooDoc) {
        this.ooDocument = ooDoc;
    }
    
    private void refreshTableDocMetadataModel(){
       
        docMetadataTableModel = new DocumentMetadataTableModel(ooDocument);
        tableDocMetadata.setModel(docMetadataTableModel );
        /*
        DocumentMetadataTableModel tblModel = (DocumentMetadataTableModel) tableDocMetadata.getModel();
        tblModel.setOOComponentHelper(this.ooDocument);
        tblModel.refreshMetaData();
        */
        
    }
    
  
    /*
     *
     *at this point the table model for the metadata table has already been set,
     *we are checking the metadata of the table
     */
    private boolean metadataChecks(){
        try {
      DocumentMetadataTableModel mModel  = (DocumentMetadataTableModel) tableDocMetadata.getModel();
      DocumentMetadata [] m=mModel.getMetadataSupplier().getDocumentMetadata();
     //checkDocument Type here
      //check to see if current document has docttype
    
       for(int i=0;i<m.length;i++){
              if(m[i].getName().equals("doctype") && m[i].getValue().equals("")){
                  log.debug("Setting document type value");
                  m[i].setValue(activeDocument);
                 // mModel.getMetadataSupplier().updateMetadataToDocument("doctype");
             }
          }
        
          mModel.refreshMetaData();
        } catch (Exception ex) {
            log.error ("metadataChecks = " + ex.getMessage());
            log.error("metadataChecks = " + CommonExceptionUtils.getStackTrace(ex));
        } finally {
      
       return true;
        }
    }
	
    private void initListDocuments(){
        log.debug("initListDocuments: init");
        //this.cboListDocuments.removeAll();
       // Iterator docIterator = editorMap.keySet().iterator();
       // while (docIterator.hasNext()) {
       //     String docKey = (String) docIterator.next();
          //  cboListDocuments.addItem(docKey);
       // }
        String[] listDocuments = editorMap.keySet().toArray(new String[editorMap.keySet().size()]);
        cboListDocuments.setModel(new DefaultComboBoxModel(listDocuments));
        cboListDocuments.updateUI();
        //cboListDocuments.add
    }
    
    private void updateListDocuments(){
        XTextDocument xDoc = (XTextDocument)UnoRuntime.queryInterface(XTextDocument.class, this.Component);
        String strTitle = OOComponentHelper.getFrameTitle(xDoc);
        cboListDocuments.setSelectedItem(strTitle);
    }
    
    private void initOpenDocumentsList(){
             try {
        log.debug("initOpenDocumentsList: getting components");
        XEnumerationAccess enumComponentsAccess = ooHelper.getDesktop().getComponents();
        XEnumeration enumComponents = enumComponentsAccess.createEnumeration();
        log.debug("initOpenDocumentsList: enumerating components");
        int i=0;
        //cboListDocuments.removeAllItems();
        
        while (enumComponents.hasMoreElements()) {
            Object nextElem = enumComponents.nextElement();
            log.debug("initOpenDocumentsList: getting model interface");
            XModel docModel = ooQueryInterface.XModel(nextElem);
            
            if (docModel != null ) { //supports XModel interface 
                log.debug("initOpenDocumentsList: docModel != null");
                XServiceInfo serviceInfo = ooQueryInterface.XServiceInfo(nextElem);
                if (serviceInfo.supportsService("com.sun.star.text.TextDocument")) {
                    log.debug("initOpenDocumentsList: supports TextDocument "+ (++i));
                    XTextDocument xDoc = (XTextDocument) UnoRuntime.queryInterface(XTextDocument.class, nextElem);
                    /*
                     XFrame xframe = xDoc.getCurrentController().getFrame();
                    String strTitle = (String) ooQueryInterface.XPropertySet(xframe).getPropertyValue("Title");
                    int dashIndex = strTitle.lastIndexOf("-");
                    if (dashIndex != -1)
                        strTitle = strTitle.substring(0, dashIndex);
                     */
                    String strTitle = OOComponentHelper.getFrameTitle(xDoc);
                    XComponent xComponent = (XComponent)UnoRuntime.queryInterface(XComponent.class, nextElem);
                    componentHandleContainer compContainer = new componentHandleContainer(strTitle, xComponent);
                    editorMap.put(compContainer.toString(), compContainer);
                   // this.cboOpenDocuments.addItem(i+ " - " + strTitle);
                }
            }
        }
        } catch (Exception ex) {
           log.error("InitOpenDocumentsList error :" + ex.getMessage());
        }
    }
    /*
    private String getFrameTitle(XTextDocument xDoc) {
        String strTitle = "";
        try {
            XFrame xframe = xDoc.getCurrentController().getFrame();
            strTitle = (String) ooQueryInterface.XPropertySet(xframe).getPropertyValue("Title");
            int dashIndex = strTitle.lastIndexOf("-");
            if (dashIndex != -1)
               strTitle = strTitle.substring(0, dashIndex);
 
        } catch (WrappedTargetException ex) {
            log.error(ex.getMessage());
        } catch (UnknownPropertyException ex) {
            log.error(ex.getMessage());
        } finally {
        return strTitle;
        }
    }
    */
    private void initOpenDocuments(){
        log.debug("initOpenDocuments: calling");
        //commented here for listener synchronization issues, as the combox action
        //listener depends on the tree data model being set.
       // cboListDocuments.addActionListener(new cboListDocumentsActionListener());
        initOpenDocumentsList();
        initListDocuments();
    }
    
    public void setOOoHelper(BungenioOoHelper helper) {
        this.ooHelper = helper;
        //cboListDocuments.addItemListener(new cboListDocumentsItemListener());
        initOpenDocuments();
    }
    
    private void initDialogListeners() {
    }
    private void initFields(){
        //initTree();
        treeDocStructure.setModel(new DefaultListModel());
        treeDocStructureTree = new JTree();
        treeDocStructureTree.setExpandsSelectedPaths(true);
        treeDocStructureTree.addMouseListener(new treeDocStructureTreeMouseListener());
        NodeMoveTransferHandler transferHandler = new NodeMoveTransferHandler(ooDocument, this);
        treeDocStructureTree.setTransferHandler(transferHandler);
        treeDocStructureTree.setDropTarget(new TreeDropTarget(transferHandler));
        treeDocStructureTree.setDragEnabled(true);
        //initList();
        //initSectionList();
        //clear meatada listbox
        listboxMetadata.setModel(new DefaultListModel());
        //init combo change structure
        changeStructureItem[] items = initChangeStructureItems();
        for (int i=0; i < items.length; i++) {
            comboChangeStructure.addItem(items[i]);    
        }
        comboChangeStructure.addActionListener (new comboChangeStructureListener());
        selectedChangeStructureItem = (changeStructureItem)comboChangeStructure.getSelectedItem();
        initList();
    }
    
    public void uncheckEditModeButton() {
        toggleEditSection.setSelected(false);
    }
    
    public void bringEditorWindowToFront(){
   	if (ooDocument.isXComponentValid()) {
        XFrame xDocFrame = ooDocument.getDocumentModel().getCurrentController().getFrame();
        Object docFrameWindow = xDocFrame.getContainerWindow();
        if (docFrameWindow == null) return;
        
        Object queryInterface=ooQueryInterface.XTopWindow(docFrameWindow);
        if (queryInterface==null){
            return;
        }else{
            log.debug("Bring selected window to the front");
            ooQueryInterface.XTopWindow(xDocFrame.getContainerWindow()).toFront();
        }
      }
   } 
   
    /*
     *this is invoked on window closing, by the JFrame that contains the panel
     */
    public void cleanup() {
        //shutdown timers
            docStructureTimer.stop();   
            sectionNameTimer.stop();
            componentsTrackingTimer.stop();
        //cleanup component listners
            Iterator keyIterator = editorMap.keySet().iterator();
            while (keyIterator.hasNext()) {
                String key = (String) keyIterator.next();
                componentHandleContainer compHandle = editorMap.get(key);
                compHandle.removeListener();
            }
    }
    
    private changeStructureItem[] initChangeStructureItems() {
        changeStructureItem itema = new changeStructureItem ("VIEW_PARAGRAPHS", "View Paragraphs");
        changeStructureItem itemb = new changeStructureItem ("VIEW_SECTIONS", "View Sections");
        changeStructureItem[] items = new changeStructureItem[2];
        items[0] = itemb;
        items[1] = itema;
        return items;
    }
    
    class comboChangeStructureListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            JComboBox box = (JComboBox) e.getSource();
            changeStructureItem theItem = (changeStructureItem) box.getSelectedItem();
            String theIndex = theItem.getIndex();
            selectedChangeStructureItem = theItem;
        }
        
    }
    
    private void initFloatingPane() {
            //load the map here 
            javax.swing.JFrame floatingFrame = new javax.swing.JFrame();
            IFloatingPanel floatingPanel = FloatingPanelFactory.getPanelClass("generalEditorPanel4");
            floatingPanel.setOOComponentHandle(ooDocument);
            floatingPanel.setParentWindowHandle(parentFrame);
            floatingFrame.setTitle(FloatingPanelFactory.panelDescription);
            floatingPanelMap.put("generalEditorPanel4", floatingPanel);
           //panel.setOOoHelper(this.openofficeObject);
            floatingFrame.add(floatingPanel.getObjectHandle());
            //frame.setSize(243, 650);
            floatingFrame.setSize(Integer.parseInt(FloatingPanelFactory.panelWidth), Integer.parseInt(FloatingPanelFactory.panelHeight));
            floatingFrame.setResizable(false);
           
            floatingFrame.setAlwaysOnTop(true);
            floatingFrame.setVisible(true);
            //position frame
            Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
            Dimension windowSize = floatingFrame.getSize();
            log.debug("screen size = "+ screenSize);
            log.debug("window size = "+ windowSize);
           
            int windowX = 5;
            int windowY = (screenSize.height - floatingFrame.getHeight())/3;
            floatingFrame.setLocation(windowX, windowY);  // Don't use "f." inside constructor.
            floatingFrame.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
    }
    
    
    private void initCollapsiblePane(){
     try {
     
     panelMarkup.removeAll();    
     panelMarkup.setLayout(new FlowLayout());
     
     StackedBox box = new StackedBox(); 
     
     //create scroll pane with stacked box
     log.debug("initializing stackedbox");
     
     JScrollPane scrollPane = new JScrollPane(box);
     scrollPane.setBorder(null);
     //add the scroll pane to the scroll pane
     panelMarkup.add(scrollPane, BorderLayout.CENTER);
   
     ICollapsiblePanel generalEditorPanel = CollapsiblePanelFactory.getPanelClass("generalEditorPanel4");
     generalEditorPanel.setOOComponentHandle(ooDocument);
     generalEditorPanel.setParentWindowHandle(parentFrame);
     dynamicPanelMap.put("generalEditorPanel4", generalEditorPanel);
     
     box.addBox("Editor Tools", generalEditorPanel.getObjectHandle());
     
     
     }
     catch (Exception e){
         log.error("InitCollapsiblePane: exception : "+ e.getMessage());
         log.error("InitCollapsiblePane: stacktrace: " + org.bungeni.ooo.utils.CommonExceptionUtils.getStackTrace(e));
     }
     
    }
    
    private void updateFloatingPanels(){
        if (!floatingPanelMap.isEmpty()){
            Iterator<String> panelNames = floatingPanelMap.keySet().iterator();
                         while (panelNames.hasNext  ()) {
                             
                             IFloatingPanel panelObj = floatingPanelMap.get(panelNames.next());
                             panelObj.setOOComponentHandle(ooDocument);
                         }
        }
    }
    
    private void updateCollapsiblePanels(){
                  if (!dynamicPanelMap.isEmpty()) {
                         Iterator<String> panelNames = dynamicPanelMap.keySet().iterator();
                         while (panelNames.hasNext  ()) {
                             
                             ICollapsiblePanel panelObj = dynamicPanelMap.get(panelNames.next());
                             panelObj.setOOComponentHandle(ooDocument);
                         }
                    }
    }
    
    private editorTabbedPanel self() {
        return this;
    }
    
    private void initNotesPanel() {
        try {
        //restrict editor note text field
        javax.swing.text.Document txtEditorNoteDoc = txtEditorNote.getDocument();
        if (txtEditorNoteDoc instanceof javax.swing.text.AbstractDocument) {
            javax.swing.text.AbstractDocument doc = (javax.swing.text.AbstractDocument)txtEditorNoteDoc;
            doc.setDocumentFilter(new TextSizeFilter(100));
        } else {
            log.debug("initNotesPanel: not an AbstratDocument instance");
        }
        //populate editor notes list
        initEditorNotesList();
        
        } catch (Exception ex) {
            log.error("exception initNotesPanel:"+ ex.getMessage());
            ex.printStackTrace();
        }
    }
    
    private void initEditorNotesList() {
        try {
        m_ooNotes = new ooDocNotes (ooDocument);
        Vector<ooDocNoteStructure> allNotes = new Vector<ooDocNoteStructure>();
        log.debug("after initializing ooDocNotes");
        allNotes = m_ooNotes.readNotes();
        DefaultListModel notesList = new DefaultListModel();
        log.debug("getting default listmodel");
   
        if (allNotes != null) {
            log.debug("allNotes is not null = "+ allNotes.size());
            for (int i=0; i < allNotes.size(); i++ ) {
                ooDocNoteStructure docNote = null;
                docNote = allNotes.elementAt(i);
                notesList.addElement(docNote);
                log.debug("docNote no."+ i + " , value = "+ docNote.getNoteDate());
            }
        } 
        listboxEditorNotes.setModel(notesList);
        log.debug("initEditorNotesList: size = "+ listboxEditorNotes.getModel().getSize());
        listboxEditorNotes.ensureIndexIsVisible(listboxEditorNotes.getModel().getSize());
        listboxEditorNotes.setSelectedIndex(listboxEditorNotes.getModel().getSize());
        } catch (Exception e) {
            log.error("initEditorNotesList: exception : " + e.getMessage());
        }
        
    }
    
    private class selectMetadataModel {
        String query;
        String text;
        public selectMetadataModel(String t, String q) {
            text = t;
            query = q;
        }
        public String toString() {
            return text;
        }
    }
    private void initBodyMetadataPanel(){
        //initilize cboSelectBodyMetadata
        
        cboSelectBodyMetadata.removeAllItems();
        cboSelectBodyMetadata.addItem(new selectMetadataModel("Members of Parliament", GeneralQueryFactory.Q_FETCH_ALL_MPS()));;
        panelEditDocumentMetadata.setVisible(false);
    }
    public Component getComponentHandle(){
        return this;
    }
    
    private void initList() {
        if (!ooDocument.isXComponentValid()) return;
        if (selectedChangeStructureItem.getIndex().equals("VIEW_PARAGRAPHS")) {
            log.debug("initList: initParagraphList");
            scrollPane_treeDocStructure.setViewportView(treeDocStructure);
            initParagraphList(); 
        } else {
            log.debug("initList: initSectionList");
            scrollPane_treeDocStructure.setViewportView(treeDocStructureTree);
            //do not refresh if the mouse is over the tree
            if (mouseOver_TreeDocStructureTree) {
                log.debug("initList: mouseOver treeDocStructure = true");
                return;
            }
            initSectionList();
        }    
   }
        
    private void clearTree(){
        treeDocStructureTree.removeAll();
        treeDocStructureTree.updateUI();
        treeDocStructureTreeCellRenderer render = new treeDocStructureTreeCellRenderer();
        treeDocStructureTree.setCellRenderer(render);
    }
   

    private void initSectionsArray(){
        BungeniBTree treeRoot = new BungeniBTree();
        TreeMap<Integer,String> namesMap = new TreeMap<Integer,String>();
        try {
            if (!ooDocument.isXComponentValid()) return;
         	/*
         	first clear the JTree
         	*/
            clearTree();
            /*
            do a basic check to see if the root section exists
            */
            if (!ooDocument.getTextSections().hasByName("root")) {
                log.error("InitSectionsArray: no root section found");
                return;
            }
            /*
            get the root section and it as the root node to the JTree
            */
            Object root = ooDocument.getTextSections().getByName("root");
            log.debug("InitSectionsArray: Adding root node");
            treeRoot.addRootNode(new String("root"));
            /*
            now get the enumeration of the TextSection
            */

            int currentIndex = 0;
            String parentObject = "root";
            XTextSection theSection = ooQueryInterface.XTextSection(root);
            XTextRange range = theSection.getAnchor();
            XText xText = range.getText();
            XEnumerationAccess enumAccess = (XEnumerationAccess) UnoRuntime.queryInterface(XEnumerationAccess.class, xText);
            //namesMap.put(currentIndex++, parentObject);
            XEnumeration enumeration = enumAccess.createEnumeration();
             log.debug("InitSectionsArray: starting Enumeration ");
            /*
            start the enumeration of sections first
            */ 
             while (enumeration.hasMoreElements()) {
                 Object elem = enumeration.nextElement();
                 XPropertySet objProps = ooQueryInterface.XPropertySet(elem);
                 XPropertySetInfo objPropsInfo = objProps.getPropertySetInfo();
                 /*
                  *enumerate only TextSection objects
                  */
                 if (objPropsInfo.hasPropertyByName("TextSection")) {
                     XTextSection xConSection = (XTextSection) ((Any)objProps.getPropertyValue("TextSection")).getObject();
                     if (xConSection != null ) {
                         /*
                          *Get the section name 
                          */   
                         XNamed objSectProps = ooQueryInterface.XNamed(xConSection);
                         String sectionName = objSectProps.getName();
                         /*
                          *only enumerate non root sections
                          */ 
                         if (!sectionName.equals("root")) {
                             log.debug("InitSectionsArray: Found Section :"+ sectionName);
                              /*
                              *check if the node exists in the tree
                              */
                              if (!namesMap.containsValue(sectionName)) {
                              		namesMap.put(currentIndex++, sectionName);
                              }
                         } // if (!sectionName...)     
                     } // if (xConSection !=...)
                 } // if (objPropsInfo.hasProper....)
             } // while (enumeration.hasMore.... )
             
             /*
              *now scan through the enumerated list of sections
              */
             Iterator namesIterator = namesMap.keySet().iterator();
              while (namesIterator.hasNext()) {
                  Integer iOrder = (Integer) namesIterator.next();
                  String sectionName = namesMap.get(iOrder);
                  /*
                   *check if the sectionName exists in our section tree
                   */
                  BungeniBNode theNode = treeRoot.getNodeByName(sectionName);
                  if (theNode == null ) {
                      /*
                       *the node does not exist, build its parent chain
                       */
                       ArrayList<String> parentChain = buildParentChain(sectionName);
                       /*
                        *now iterate through the paren->child hierarchy of sections
                        */
                       Iterator<String> sections = parentChain.iterator();
                       BungeniBNode currentNode = null, previousNode = null;
                       while (sections.hasNext()) {
                           String hierSection = sections.next();
                           currentNode =  treeRoot.getNodeByName(hierSection);
                           if (currentNode == null ) {
                               /* the node doesnt exist in the tree */
                               if (previousNode != null ) {
                                    treeRoot.addNodeToNamedNode(previousNode.getName(), hierSection);
                                    previousNode = treeRoot.getNodeByName(hierSection);
                                    if (previousNode == null ) 
                                        log.error("previousNode was null");
                               } else {
                                   log.error("The root section was not in the BungeniBTree hierarchy, this is an error condition");
                               }
                           } else {
                               /* the node already exists...*/
                               previousNode = currentNode;
                           }
                       }
                  }
                  
                 
              }
               convertBTreetoJTreeNodes(treeRoot);
        } catch (NoSuchElementException ex) {
            log.error(ex.getMessage());
        } catch (UnknownPropertyException ex) {
            log.error(ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error(ex.getMessage());
        }
    }

    private ArrayList<String> buildParentChain(String Sectionname){
          XTextSection currentSection = ooDocument.getSection(Sectionname);
          XTextSection sectionParent=currentSection.getParentSection();
          XNamed parentProps = ooQueryInterface.XNamed(sectionParent);
          String parentSectionname = parentProps.getName();
          String currentSectionname = Sectionname;
          ArrayList<String> nodeHierarchy = new ArrayList<String>();
          //array list goes from child(0) to ancestors (n)
          log.debug("buildParentChain: nodeHierarchy: Adding "+ currentSectionname);
          nodeHierarchy.add(currentSectionname);
          while (1==1) {
              //go up the hierarchy until you reach root.
              //break upon reaching the parent
              if (parentSectionname.equals("root")) {
                  nodeHierarchy.add(parentSectionname);
                  log.debug("buildParentChain: nodeHierarchy: Adding "+ parentSectionname + " and breaking.");
                  break;
              }
             nodeHierarchy.add(parentSectionname);
             log.debug("buildParentChain: nodeHierarchy: Adding "+ parentSectionname + ".");
             currentSectionname = parentSectionname;
             sectionParent = sectionParent.getParentSection();
             parentProps = ooQueryInterface.XNamed(sectionParent);
             parentSectionname = parentProps.getName();
          } //end while (1== 1)
          if (nodeHierarchy.size() > 1 )
            Collections.reverse(nodeHierarchy);
          return nodeHierarchy;
    }
    
    private void convertBTreetoJTreeNodes(BungeniBTree theTree){
        //TreeMap<Integer,BungeniBNode> sectionMap = theTree.getTree();
        BungeniBNode rootNode = theTree.getNodeByName("root");
        this.sectionsRootNode = null;
        this.sectionsRootNode = new DefaultMutableTreeNode(new String("root"));
        TreeMap<Integer,BungeniBNode> sectionMap = rootNode.getChildrenByOrder();
        Iterator<Integer> rootIter = sectionMap.keySet().iterator();
           int depth = 0;
           while (rootIter.hasNext()) {
                Integer key = (Integer) rootIter.next();
                BungeniBNode n = sectionMap.get(key);
                DefaultMutableTreeNode n_child = new DefaultMutableTreeNode(n.getName());
                sectionsRootNode.add(n_child);
                //sbOut.append(padding(depth) + n.getName()+ "\n");
                //walkNodeByOrder(n, depth);
                walkBNodeTree(n , n_child);
            }
    }
    
    private void walkBNodeTree(BungeniBNode theNode, DefaultMutableTreeNode pNode){
        if (theNode.hasChildren()) {
           TreeMap<Integer, BungeniBNode> n_children = theNode.getChildrenByOrder();
           Iterator<Integer> nodesByOrder = n_children.keySet().iterator();
           while (nodesByOrder.hasNext()) {
               Integer key = (Integer) nodesByOrder.next();
               BungeniBNode n = n_children.get(key);
               DefaultMutableTreeNode dmt_node = new DefaultMutableTreeNode(n.getName());
               pNode.add(dmt_node);
               walkBNodeTree(n, dmt_node);
           }
        } else
            return;
    }
    
    /****this is the old sections iterator, it uses getTextSections(), and the getChildSections() API, 
     * which does not display sections in the correct order
     * see http://www.openoffice.org/issues/show_bug.cgi?id=82420
     *****/
    
    private void initSectionsArray__Old() {
        try {
            log.debug("initSectionsArray....");
            if (!ooDocument.isXComponentValid()) return;
            log.debug("emptying treeDocStructureTree");
            treeDocStructureTree.removeAll();
            treeDocStructureTree.updateUI();
            //this.sectionsRootNode = null ; //new DefaultMutableTreeNode(new String("root"));
            
            //mvSections.removeAllElements();
            if (!ooDocument.getTextSections().hasByName("root")) {
                log.debug("no root section found");
                return;
            }
            log.debug("InitSectionsArray = getting root section");
            Object rootSection = ooDocument.getTextSections().getByName("root");
            XTextSection theSection = ooQueryInterface.XTextSection(rootSection);
            sectionsRootNode = null;
            sectionsRootNode = new DefaultMutableTreeNode(new String("root"));
            log.debug("about to recurseSections()...");
            recurseSections (theSection, sectionsRootNode);
            
            //-tree-deprecated--CommonTreeFunctions.expandAll(treeDocStructureTree, true);
            CommonTreeFunctions.expandAll(treeDocStructureTree);
            
        } catch (NoSuchElementException ex) {
            log.error(ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error(ex.getMessage());
        }
    }
    
    private void recurseSections (XTextSection theSection, DefaultMutableTreeNode node ) {
        try {
     
      //  mvSections.add(padding + sectionName);
      //  log.debug("recurse sections, section name:"+padding+sectionName);
        //recurse children
        XTextSection[] sections = theSection.getChildSections();
         
        if (sections != null ) {
            if (sections.length > 0 ) {
                //start from last index and go to first
                for (int nSection = sections.length - 1 ; nSection >=0 ; nSection--) {
                    log.debug ("section name = "+ooQueryInterface.XNamed(sections[nSection]).getName() );
                    //get the name for the section and add it to the root node.
                    XPropertySet childSet = ooQueryInterface.XPropertySet(sections[nSection]);
                    String childSectionName = (String) childSet.getPropertyValue("LinkDisplayName");
                    DefaultMutableTreeNode newNode = new DefaultMutableTreeNode(childSectionName);
                    
                    node.add(newNode);
                    
                    recurseSections (sections[nSection], newNode);
                    
                }
            } else 
                return;
        } else 
            return;
        } catch (UnknownPropertyException ex) {
            log.error(ex.getMessage());
        } catch (WrappedTargetException ex ) {
            log.error(ex.getMessage());
        }
    }
    
    private void initSectionList() {
        initSectionsArray();  
        log.debug("setting defaultTreeModel to sectionsRootNode");
        //sectionsRootNode = new DefaultMutableTreeNode ("root");
        treeDocStructureTree.setModel(new DefaultTreeModel(sectionsRootNode));
        //-tree-deprecated--CommonTreeFunctions.expandAll(treeDocStructureTree, true);
        CommonTreeFunctions.expandAll(treeDocStructureTree);
      }
    
    
    private void initParagraphList(){
       
       try { 
     
       mvDocumentHeadings.removeAllElements();
       XText objText = ooDocument.getTextDocument().getText();//getTextDocument().getText();
       
       XEnumerationAccess objEnumAccess = (XEnumerationAccess) UnoRuntime.queryInterface( XEnumerationAccess.class, objText); 
       XEnumeration paraEnum =  objEnumAccess.createEnumeration();
       int nHeadsFound = 0;
       int nMaxLevel = 0;
       int nPrevLevel = 0;
       DocStructureElement previousElement = null;
                
       
        // While there are paragraphs, do things to them 
        //first we find the number of heading paragraphs
        //log.debug("Inside getDocumentTree, entering, hasMoreElements");
        
        while (paraEnum.hasMoreElements()) { 
            log.debug("Inside getDocumentTree, inside, hasMoreElements");

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
                log.debug("Inside getDocumentTree, supportsService paragraph");

                XPropertySet xSet = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, xInfo);
                     // Set the justification to be center justified 
                    log.debug("Inside getDocumentTree, before , NumberingLevel");
                    short nLevel = -1;
                    nLevel = AnyConverter.toShort(xSet.getPropertyValue("ParaChapterNumberingLevel"));
                    log.debug("Inside getDocumentTree, after , NumberingLevel = "+ nLevel);
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
                           
                        log.debug("adding heading level =" + nLevel + " and heading count = "+nHeadsFound);
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
                log.error(ex.getMessage());
            } catch (WrappedTargetException ex) {
                log.error(ex.getMessage());           }
            catch (com.sun.star.lang.IllegalArgumentException ex) {
               log.error(ex.getMessage());
            } 
            catch (UnknownPropertyException ex) {
               log.error(ex.getMessage());
            }
}
   


     class treePopupMenu {
        TreeMap<String,String> popupMenuMap = new TreeMap<String, String>();
       
        treePopupMenu (String menu_name_to_load_from_settings) {
            //load the menu from settings, probably the db.
            if (menu_name_to_load_from_settings.equals("treeDocStructureTree")) {
                addItem("0_GOTO_SECTION", "Goto Section");
                addItem("1_ADD_PARA_BEFORE_SECTION", "Add Para Before Section");
                addItem("2_ADD_PARA_AFTER_SECTION", "Add Para After Section");
                addItem("3_DELETE_SECTION", "Remove This Section");
            }
        }
        
        public void addItem(String menu_id, String text) {
            popupMenuMap.put(menu_id, text);
        }
        
        public TreeMap<String, String> getMenus() {
            return popupMenuMap;
        }
        
        
    }
    
   class treeDocStructureTreeMouseListener implements MouseListener {
       private treePopupMenu theMenu ; 
       treeDocStructureTreeMouseListener() {
            theMenu  = new treePopupMenu("treeDocStructureTree");
        }
        
        public void mouseClicked(MouseEvent e) {
        }     
        
         public void mousePressed(MouseEvent evt) {
             
                if (!toggleEditSection.isSelected()) {
                    int selRow = treeDocStructureTree.getRowForLocation(evt.getX(), evt.getY());
                    TreePath selPath = treeDocStructureTree.getPathForLocation(evt.getX(), evt.getY());
                     if (selRow != -1 ) {
                         if (evt.getClickCount() == 1) {
                             DefaultMutableTreeNode node = (DefaultMutableTreeNode) selPath.getLastPathComponent();
                             System.out.println("node = "+ (String) node.getUserObject());   
                             String selectedSection = (String)node.getUserObject();
                             createPopupMenuItems (selectedSection);
                             popupMenuTreeStructure.show(evt.getComponent(), evt.getX(), evt.getY());
                          return;
                         }  

                     }
                }      
        }

        
        public void mouseReleased(MouseEvent e) {
        }

        public void mouseEntered(MouseEvent e) {
            log.debug("treeDocStructureTree: mouseEntered!!");
            mouseOver_TreeDocStructureTree = true;
        }

        public void mouseExited(MouseEvent e) {
            log.debug("treeDocStructureTree: mouseExiting!!");
            mouseOver_TreeDocStructureTree = false;
        }
       
               
       private void createPopupMenuItems (String selectedSection){
                popupMenuTreeStructure.removeAll();
                //treePopupMenu menu = new treePopupMenu("treeDocStructureTree");
                //popupMenu.add(new treePopupMenuAction(popup_section_actions[0], baseNodeAction, PopupTypeIdentifier.VIEW_ACTIONS));
                TreeMap<String,String> menus = theMenu.getMenus();
                Iterator<String> keys = menus.keySet().iterator();
                while (keys.hasNext()) {
                    String key = keys.next();
                    popupMenuTreeStructure.add(new treeDocStructureTreePopupAction(key, menus.get(key), selectedSection));
                }
                //popupMenuTreeStructure.add(new treeDocStructureTreePopupAction(org.bungeni.editor.dialogs.editorTabbedPanel.PopupTypeIdentifier.GOTO_SECTION.popup_id(), selectedSection));
               
           }
   }
    
   /*
    *Drag and Drop handlers for JTree - treeDocStructureTree
    * available under the tree package
    */
    
   
      class treeDocStructureTreePopupAction extends AbstractAction {
           
          treeDocStructureTreePopupAction () {
              
          }
          
          treeDocStructureTreePopupAction (String actionId, String actionText, String sectionName) {
                super(actionText);
                putValue("ACTION_ID", actionId);
                putValue("USER_OBJECT", sectionName);
            }
       
          public void actionPerformed(ActionEvent e) {
              Object value = getValue("USER_OBJECT");
              Object action_id = getValue("ACTION_ID");
              if (value != null ) {
                  processPopupSelection((String)value, (String) action_id);
              }
            }
          
          public void processPopupSelection(String sectionName, String action_id ) {
              //go to selected range
             XTextSection xSelectSection = ooDocument.getSection(sectionName);
          
              if (action_id.equals("0_GOTO_SECTION")) {
                      if (xSelectSection != null  ) {
                          XTextRange sectionRange = xSelectSection.getAnchor();
                          XTextViewCursor xViewCursor = ooDocument.getViewCursor();
                          xViewCursor.gotoRange(sectionRange, false);
                      }
                  
              } else if (action_id.equals("1_ADD_PARA_BEFORE_SECTION")) {
                   XTextContent oPar = ooQueryInterface.XTextContent(ooDocument.createInstance("com.sun.star.text.Paragraph"));
                   XRelativeTextContentInsert xRelativeText = ooQueryInterface.XRelativeTextContentInsert(ooDocument.getTextDocument().getText());
                    try {
                        xRelativeText.insertTextContentBefore(oPar, ooQueryInterface.XTextContent(xSelectSection));
                    } catch (com.sun.star.lang.IllegalArgumentException ex) {
                        log.debug("insertTextContentbefore :" + ex.getMessage());
                    }
                    //move visible cursor to the point where the new para was added
                   ooDocument.getViewCursor().gotoRange(xSelectSection.getAnchor().getStart(), false);
              } else if (action_id.equals("2_ADD_PARA_AFTER_SECTION")) {
                     XTextContent oPar = ooQueryInterface.XTextContent(ooDocument.createInstance("com.sun.star.text.Paragraph"));
                     XRelativeTextContentInsert xRelativeText = ooQueryInterface.XRelativeTextContentInsert(ooDocument.getTextDocument().getText());
                     try {
                            xRelativeText.insertTextContentAfter(oPar, ooQueryInterface.XTextContent(xSelectSection));
                     } catch (com.sun.star.lang.IllegalArgumentException ex) {
                            log.error("insertTextContentbefore :" + ex.getMessage());
                     }
                     //move visible cursor to point where para was added
                    ooDocument.getViewCursor().gotoRange(xSelectSection.getAnchor().getEnd(), false);
              } else if (action_id.equals("3_DELETE_SECTION")) {
                    //first select the range...
                    
                    XTextContent sectionContent = ooQueryInterface.XTextContent(xSelectSection);
                    XTextRange sectionRange = sectionContent.getAnchor();
                    ooDocument.getViewCursor().gotoRange(sectionRange, false);
                    
                    //now prompt with a warning....
                    int nRet = MessageBox.Confirm(self(), "WARNING, The section: "+sectionName+ ", and its contents, \n" +
                            "and any other sections nested inside it will be removed. \n " +
                            "Are you sure you want to proceed ?", "Deletion Warning");
                    if (nRet == JOptionPane.YES_OPTION) {
                        //delete section and contents
                         //aTextRange=section.getAnchor()
                        ExternalMacro RemoveSectionAndContents = ExternalMacroFactory.getMacroDefinition("RemoveSectionAndContents");
                        RemoveSectionAndContents.addParameter(ooDocument.getComponent());
                        RemoveSectionAndContents.addParameter(sectionName);
                        ooDocument.executeMacro(RemoveSectionAndContents.toString(), RemoveSectionAndContents.getParams());
            
                       } else 
                        return;
              }
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
            if ((e.getModifiers() & InputEvent.BUTTON3_MASK) == InputEvent.BUTTON3_MASK ){
                //trap right click
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

    
   private class documentNodeMapKey {
       int level;
       int count;
   }
   
   
   
    private void initializeValues(){
        //get metadata property alues
        String strAuthor = ""; String strDocType = "";
          try {
        if (ooDocument.propertyExists("Bungeni_DocAuthor")){
          
                strAuthor = ooDocument.getPropertyValue("Bungeni_DocAuthor");
           
        }
        if (ooDocument.propertyExists("doctype")){
            strDocType = ooDocument.getPropertyValue("doctype");
        }
        
        //txtDocAuthor.setText(strAuthor);
        //txtDocType.setText(strDocType);
         } catch (UnknownPropertyException ex) {
                ex.printStackTrace();
            }
       
    }
    
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
        this.setHorizontalAlignment(JLabel.LEFT);
        this.setIconTextGap(0);
        setText(entry.toString());
        setFont(new java.awt.Font("Tahoma", 0, 10));
        /*
        if (entry.hasChildren()) {
        String imgLocation = "/gui/"
                             + "icon-list"
                             + ".png";
            URL imageURL = editorTabbedPanel.class.getResource(imgLocation);
        //Create and initialize the button.
        if (imageURL != null)                     //image found
           setIcon(new ImageIcon(imageURL, entry.toString()));
        }
         */
        setIcon(null);
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
 
private void displayUserMetadata(XTextRange xRange) {
         try {
       XTextCursor xRangeCursor = xRange.getText().createTextCursorByRange(xRange);
       XText objText = xRangeCursor.getText();
       
       XEnumerationAccess objEnumAccess = (XEnumerationAccess) UnoRuntime.queryInterface( XEnumerationAccess.class, objText); 
       XEnumeration paraEnum =  objEnumAccess.createEnumeration();
    
        // While there are paragraphs, do things to them 
        //first we find the number of heading paragraphs
        log.debug("Inside displayUserMetadata, entering, displayUserMetadata");
        
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

                XPropertySet xSet = ooQueryInterface.XPropertySet(objNextElement);
                     // Set the justification to be center justified 
                    //log.debug("Inside getDocumentTree, before , NumberingLevel");
                XPropertySetInfo xSetInfo = xSet.getPropertySetInfo();     
                if (xSetInfo.hasPropertyByName("TextUserDefinedAttributes")) {
                    XNameContainer uda=null;
                    Type t = AnyConverter.getType(xSet.getPropertyValue("TextUserDefinedAttributes"));
                    log.debug("TypeName = "+ t.getTypeName());
                    Object att = xSet.getPropertyValue("TextUserDefinedAttributes");
                        try {
                   // uda =  ooQueryInterface.XNameContainer(att);
                            
                            uda = (XNameContainer) AnyConverter.toObject(
                                          new Type(XNameContainer.class),
                                           att);
                        } catch (com.sun.star.lang.IllegalArgumentException ex) {
                            ex.printStackTrace();
                        }
                    if (uda != null ) {
                    if (uda.hasElements()) {
                        log.debug("uda has elements");
                        String[] elements = uda.getElementNames();
                        AttributeData[] adData = new AttributeData[elements.length];
                        for (int i=0; i < elements.length; i++ ){
                             adData[i] = (AttributeData) uda.getByName(elements[i]);
                             log.debug("ns:"+adData[i].Namespace+" ; type:"+adData[i].Type+" ; value:"+adData[i].Value);
                         } 
                    }
                    }
                }
            }    
        else           
                log.debug("Inside getDocumentTree, paragraph not supproted");
        }
            
    } catch (NoSuchElementException ex) {
                log.error("displayUserMetadata : "+ ex.getLocalizedMessage());
    } catch (WrappedTargetException ex) {
                log.error("displayUserMetadata : "+ ex.getLocalizedMessage());
    } /*catch (com.sun.star.lang.IllegalArgumentException ex) {
                log.error("displayUserMetadata : "+ ex.getLocalizedMessage());
    } */ catch (UnknownPropertyException ex) {
                log.error("displayUserMetadata : "+ ex.getLocalizedMessage());
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
        jScrollPane2 = new javax.swing.JScrollPane();
        jTree1 = new javax.swing.JTree();
        jScrollPane3 = new javax.swing.JScrollPane();
        jTree2 = new javax.swing.JTree();
        jTabsContainer = new javax.swing.JTabbedPane();
        panelMetadata = new javax.swing.JPanel();
        scrollDocMetadata = new javax.swing.JScrollPane();
        tableDocMetadata = new javax.swing.JTable();
        cboListDocuments = new javax.swing.JComboBox();
        panelEditDocumentMetadata = new javax.swing.JPanel();
        btnApplyDocMetadata = new javax.swing.JButton();
        btnMetadataCancel = new javax.swing.JButton();
        editStringTxt = new javax.swing.JTextField();
        editDateLbl = new javax.swing.JLabel();
        editDateTxt = new org.jdesktop.swingx.JXDatePicker();
        editStringLbl = new javax.swing.JLabel();
        lblOpenDocuments = new javax.swing.JLabel();
        check_floatingMetadataWindow = new javax.swing.JCheckBox();
        panelBodyMetadata = new javax.swing.JPanel();
        lblSelectBodyMetadata = new javax.swing.JLabel();
        cboSelectBodyMetadata = new javax.swing.JComboBox();
        lblEnterMetadataValue = new javax.swing.JLabel();
        btnLookupMetadata = new javax.swing.JButton();
        btnClearMetadataValue = new javax.swing.JButton();
        btnApplyMetadata = new javax.swing.JButton();
        radioSelectedText = new javax.swing.JRadioButton();
        jLabel1 = new javax.swing.JLabel();
        radioDocumentSection = new javax.swing.JRadioButton();
        scrollListboxMetadata = new javax.swing.JScrollPane();
        listboxMetadata = new javax.swing.JList();
        panelMarkup = new javax.swing.JPanel();
        panelHistory = new javax.swing.JPanel();
        jLabel3 = new javax.swing.JLabel();
        jComboBox1 = new javax.swing.JComboBox();
        jLabel2 = new javax.swing.JLabel();
        jComboBox2 = new javax.swing.JComboBox();
        jLabel5 = new javax.swing.JLabel();
        jButton1 = new javax.swing.JButton();
        panelNotes = new javax.swing.JPanel();
        scroll_panelNotes = new javax.swing.JScrollPane();
        listboxEditorNotes = new javax.swing.JList();
        lblEditorNotes = new javax.swing.JLabel();
        btnNewEditorNote = new javax.swing.JButton();
        btnSaveEditorNote = new javax.swing.JButton();
        jLabel4 = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        txtEditorNote = new javax.swing.JTextArea();
        scrollPane_treeDocStructure = new javax.swing.JScrollPane();
        treeDocStructure = new javax.swing.JList();
        lbl_DocStructTitle = new javax.swing.JLabel();
        comboChangeStructure = new javax.swing.JComboBox();
        toggleEditSection = new javax.swing.JCheckBox();
        lbl_SectionName = new javax.swing.JTextField();

        jScrollPane2.setViewportView(jTree1);

        jScrollPane3.setViewportView(jTree2);

        setFont(new java.awt.Font("Tahoma", 0, 10));
        jTabsContainer.setTabLayoutPolicy(javax.swing.JTabbedPane.SCROLL_TAB_LAYOUT);
        jTabsContainer.setFont(new java.awt.Font("Tahoma", 0, 10));
        panelMetadata.setFont(new java.awt.Font("Tahoma", 0, 10));
        tableDocMetadata.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {
                {"DOC_AUTHOR", null},
                {"DOC_TYPE", "debaterecord"},
                {"PARLIAMENT_ID", null},
                {"PARLIAMENT_SITTING", null}
            },
            new String [] {
                "METADATA", "VALUE"
            }
        ));
        scrollDocMetadata.setViewportView(tableDocMetadata);

        btnApplyDocMetadata.setFont(new java.awt.Font("Tahoma", 0, 10));
        btnApplyDocMetadata.setText("Apply");
        btnApplyDocMetadata.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnApplyDocMetadataActionPerformed(evt);
            }
        });

        btnMetadataCancel.setFont(new java.awt.Font("Tahoma", 0, 10));
        btnMetadataCancel.setText("Cancel");
        btnMetadataCancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnMetadataCancelActionPerformed(evt);
            }
        });

        editStringTxt.setFont(new java.awt.Font("Tahoma", 0, 10));

        editDateLbl.setFont(new java.awt.Font("Tahoma", 0, 10));
        editDateLbl.setText("Edit Date Value");

        editDateTxt.setFont(new java.awt.Font("SansSerif", 0, 10));

        editStringLbl.setFont(new java.awt.Font("Tahoma", 0, 10));
        editStringLbl.setText("Edit Text Value");

        org.jdesktop.layout.GroupLayout panelEditDocumentMetadataLayout = new org.jdesktop.layout.GroupLayout(panelEditDocumentMetadata);
        panelEditDocumentMetadata.setLayout(panelEditDocumentMetadataLayout);
        panelEditDocumentMetadataLayout.setHorizontalGroup(
            panelEditDocumentMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelEditDocumentMetadataLayout.createSequentialGroup()
                .addContainerGap()
                .add(panelEditDocumentMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(panelEditDocumentMetadataLayout.createSequentialGroup()
                        .add(panelEditDocumentMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, editDateTxt, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 179, Short.MAX_VALUE)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, panelEditDocumentMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING, false)
                                .add(editStringTxt)
                                .add(org.jdesktop.layout.GroupLayout.LEADING, panelEditDocumentMetadataLayout.createSequentialGroup()
                                    .add(btnApplyDocMetadata, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 69, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                                    .add(31, 31, 31)
                                    .add(btnMetadataCancel, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 69, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))))
                        .addContainerGap(29, Short.MAX_VALUE))
                    .add(panelEditDocumentMetadataLayout.createSequentialGroup()
                        .add(editDateLbl, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 139, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addContainerGap(69, Short.MAX_VALUE))
                    .add(panelEditDocumentMetadataLayout.createSequentialGroup()
                        .add(editStringLbl, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 121, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addContainerGap(87, Short.MAX_VALUE))))
        );
        panelEditDocumentMetadataLayout.setVerticalGroup(
            panelEditDocumentMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(org.jdesktop.layout.GroupLayout.TRAILING, panelEditDocumentMetadataLayout.createSequentialGroup()
                .addContainerGap(org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .add(editStringLbl, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 13, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(editStringTxt, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(editDateLbl)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(editDateTxt, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 22, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(panelEditDocumentMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(btnMetadataCancel, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 20, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(btnApplyDocMetadata, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 20, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)))
        );

        lblOpenDocuments.setText("Open Documents:");

        check_floatingMetadataWindow.setText("Show Floating Metadata Window");
        check_floatingMetadataWindow.setBorder(javax.swing.BorderFactory.createEmptyBorder(0, 0, 0, 0));
        check_floatingMetadataWindow.setMargin(new java.awt.Insets(0, 0, 0, 0));
        check_floatingMetadataWindow.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                check_floatingMetadataWindowActionPerformed(evt);
            }
        });

        org.jdesktop.layout.GroupLayout panelMetadataLayout = new org.jdesktop.layout.GroupLayout(panelMetadata);
        panelMetadata.setLayout(panelMetadataLayout);
        panelMetadataLayout.setHorizontalGroup(
            panelMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelMetadataLayout.createSequentialGroup()
                .addContainerGap()
                .add(panelMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(scrollDocMetadata, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 218, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, lblOpenDocuments, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(cboListDocuments, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 218, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(check_floatingMetadataWindow, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 210, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(panelEditDocumentMetadata, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                .addContainerGap())
        );
        panelMetadataLayout.setVerticalGroup(
            panelMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(org.jdesktop.layout.GroupLayout.TRAILING, panelMetadataLayout.createSequentialGroup()
                .addContainerGap()
                .add(check_floatingMetadataWindow)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(scrollDocMetadata, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 79, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(panelEditDocumentMetadata, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 19, Short.MAX_VALUE)
                .add(lblOpenDocuments)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(cboListDocuments, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );
        jTabsContainer.addTab("Doc. Metadata", panelMetadata);

        lblSelectBodyMetadata.setText("Select Metadata Element");

        cboSelectBodyMetadata.setFont(new java.awt.Font("Tahoma", 0, 10));
        cboSelectBodyMetadata.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Members Of Parliament", "Ontology", "Keywords", "Tabled Documents" }));

        lblEnterMetadataValue.setText("Selected Metadata Value");

        btnLookupMetadata.setText("Lookup...");
        btnLookupMetadata.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                userMetadataLookup_Clicked(evt);
            }
        });

        btnClearMetadataValue.setText("Clear");
        btnClearMetadataValue.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnClearMetadata_Clicked(evt);
            }
        });

        btnApplyMetadata.setText("Apply Metadata");
        btnApplyMetadata.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnApplyMetadata_Clicked(evt);
            }
        });

        btnGrpBodyMetadataTarget.add(radioSelectedText);
        radioSelectedText.setSelected(true);
        radioSelectedText.setText("Selected Text");
        radioSelectedText.setBorder(javax.swing.BorderFactory.createEmptyBorder(0, 0, 0, 0));
        radioSelectedText.setMargin(new java.awt.Insets(0, 0, 0, 0));

        jLabel1.setText("Select Target for Applying Metadata");

        btnGrpBodyMetadataTarget.add(radioDocumentSection);
        radioDocumentSection.setText("Current Document Section");
        radioDocumentSection.setBorder(javax.swing.BorderFactory.createEmptyBorder(0, 0, 0, 0));
        radioDocumentSection.setMargin(new java.awt.Insets(0, 0, 0, 0));

        listboxMetadata.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        scrollListboxMetadata.setViewportView(listboxMetadata);

        org.jdesktop.layout.GroupLayout panelBodyMetadataLayout = new org.jdesktop.layout.GroupLayout(panelBodyMetadata);
        panelBodyMetadata.setLayout(panelBodyMetadataLayout);
        panelBodyMetadataLayout.setHorizontalGroup(
            panelBodyMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelBodyMetadataLayout.createSequentialGroup()
                .addContainerGap()
                .add(panelBodyMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(scrollListboxMetadata, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(jLabel1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(cboSelectBodyMetadata, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 218, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(lblSelectBodyMetadata, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(lblEnterMetadataValue, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, panelBodyMetadataLayout.createSequentialGroup()
                        .add(btnClearMetadataValue, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 85, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 52, Short.MAX_VALUE)
                        .add(btnLookupMetadata))
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, btnApplyMetadata, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(panelBodyMetadataLayout.createSequentialGroup()
                        .add(10, 10, 10)
                        .add(panelBodyMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                            .add(radioSelectedText, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 156, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                            .add(radioDocumentSection))
                        .add(52, 52, 52)))
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
                .add(3, 3, 3)
                .add(scrollListboxMetadata, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 73, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(panelBodyMetadataLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(btnLookupMetadata)
                    .add(btnClearMetadataValue))
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jLabel1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 23, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(radioSelectedText)
                .add(14, 14, 14)
                .add(radioDocumentSection)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btnApplyMetadata)
                .addContainerGap(26, Short.MAX_VALUE))
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

        jLabel3.setText("Transform Document");

        jComboBox1.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "AkomaNtoso XML", "XHTML - eXtensible HTML", "Marginalia-safe HTML export", "Portable Document Format (PDF)" }));

        jLabel2.setText("Transformation Target");

        jComboBox2.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Export to Server", "Export to File-System path" }));

        jLabel5.setText("Export To:");

        jButton1.setText("Transform...");
        jButton1.setEnabled(false);

        org.jdesktop.layout.GroupLayout panelHistoryLayout = new org.jdesktop.layout.GroupLayout(panelHistory);
        panelHistory.setLayout(panelHistoryLayout);
        panelHistoryLayout.setHorizontalGroup(
            panelHistoryLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelHistoryLayout.createSequentialGroup()
                .add(panelHistoryLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(panelHistoryLayout.createSequentialGroup()
                        .addContainerGap()
                        .add(panelHistoryLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING, false)
                            .add(jComboBox1, 0, 209, Short.MAX_VALUE)
                            .add(jLabel2, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                            .add(jLabel3, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 142, Short.MAX_VALUE)
                            .add(jLabel5)
                            .add(jComboBox2, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)))
                    .add(panelHistoryLayout.createSequentialGroup()
                        .add(53, 53, 53)
                        .add(jButton1)))
                .addContainerGap(19, Short.MAX_VALUE))
        );
        panelHistoryLayout.setVerticalGroup(
            panelHistoryLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelHistoryLayout.createSequentialGroup()
                .addContainerGap()
                .add(jLabel3)
                .add(8, 8, 8)
                .add(jLabel2)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jComboBox1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jLabel5)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jComboBox2, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(23, 23, 23)
                .add(jButton1)
                .addContainerGap(142, Short.MAX_VALUE))
        );
        jTabsContainer.addTab("Transform", panelHistory);

        listboxEditorNotes.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        listboxEditorNotes.addListSelectionListener(new javax.swing.event.ListSelectionListener() {
            public void valueChanged(javax.swing.event.ListSelectionEvent evt) {
                listboxEditorNotesValueChanged(evt);
            }
        });

        scroll_panelNotes.setViewportView(listboxEditorNotes);

        lblEditorNotes.setText("Editor Note");

        btnNewEditorNote.setText("New Note");
        btnNewEditorNote.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnNewEditorNoteActionPerformed(evt);
            }
        });

        btnSaveEditorNote.setText("Save Note");
        btnSaveEditorNote.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnSaveEditorNoteActionPerformed(evt);
            }
        });

        jLabel4.setText("View Archived Notes");

        txtEditorNote.setColumns(20);
        txtEditorNote.setEditable(false);
        txtEditorNote.setFont(new java.awt.Font("Tahoma", 0, 11));
        txtEditorNote.setLineWrap(true);
        txtEditorNote.setRows(5);
        txtEditorNote.setToolTipText("Type in your editor notes here.");
        jScrollPane1.setViewportView(txtEditorNote);

        org.jdesktop.layout.GroupLayout panelNotesLayout = new org.jdesktop.layout.GroupLayout(panelNotes);
        panelNotes.setLayout(panelNotesLayout);
        panelNotesLayout.setHorizontalGroup(
            panelNotesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelNotesLayout.createSequentialGroup()
                .addContainerGap()
                .add(panelNotesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(jScrollPane1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(scroll_panelNotes, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(lblEditorNotes, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 163, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(panelNotesLayout.createSequentialGroup()
                        .add(btnNewEditorNote)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 52, Short.MAX_VALUE)
                        .add(btnSaveEditorNote))
                    .add(jLabel4, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE))
                .addContainerGap())
        );
        panelNotesLayout.setVerticalGroup(
            panelNotesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelNotesLayout.createSequentialGroup()
                .addContainerGap()
                .add(lblEditorNotes)
                .add(4, 4, 4)
                .add(jScrollPane1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(panelNotesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(btnNewEditorNote)
                    .add(btnSaveEditorNote))
                .add(14, 14, 14)
                .add(jLabel4)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(scroll_panelNotes, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 134, Short.MAX_VALUE)
                .addContainerGap())
        );
        jTabsContainer.addTab("Notes", panelNotes);

        treeDocStructure.setFont(new java.awt.Font("Tahoma", 0, 10));
        treeDocStructure.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        scrollPane_treeDocStructure.setViewportView(treeDocStructure);

        lbl_DocStructTitle.setText("Current Section Name:");

        toggleEditSection.setText("Edit Section");
        toggleEditSection.setBorder(javax.swing.BorderFactory.createEmptyBorder(0, 0, 0, 0));
        toggleEditSection.setMargin(new java.awt.Insets(0, 0, 0, 0));

        lbl_SectionName.setEditable(false);

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(jTabsContainer, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 243, Short.MAX_VALUE)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(toggleEditSection)
                .add(14, 14, 14)
                .add(comboChangeStructure, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 136, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(scrollPane_treeDocStructure, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 223, Short.MAX_VALUE)
                .addContainerGap())
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(lbl_SectionName, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 223, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(lbl_DocStructTitle, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 142, Short.MAX_VALUE)
                .add(91, 91, 91))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(jTabsContainer, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 335, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lbl_DocStructTitle)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 10, Short.MAX_VALUE)
                .add(lbl_SectionName, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(scrollPane_treeDocStructure, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 183, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(comboChangeStructure, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(toggleEditSection)))
        );
    }// </editor-fold>//GEN-END:initComponents

    private void check_floatingMetadataWindowActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_check_floatingMetadataWindowActionPerformed
// TODO add your handling code here:
        if (this.check_floatingMetadataWindow.isSelected()) {
            log.debug("Show Doc Metadata button clicked " + evt.getActionCommand());
            metadataPanelParentFrame = new javax.swing.JFrame("Document Metadata Panel");
            if (metadataTabbedPanel == null) {
                metadataTabbedPanel = new org.bungeni.editor.dialogs.metadataTabbedPanel(this.ooDocument, metadataPanelParentFrame);
            } else {
                metadataTabbedPanel.updateOOhandle(ooDocument, metadataPanelParentFrame);
            }
            //panel.setOOoHelper(this.openofficeObject);
            metadataPanelParentFrame.add(metadataTabbedPanel);
            //frame.setSize(243, 650);
            metadataPanelParentFrame.setSize(320, 400);
            metadataPanelParentFrame.setResizable(false);
           
            metadataPanelParentFrame.setAlwaysOnTop(true);
            metadataPanelParentFrame.setVisible(true);
            //position frame
            Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
            Dimension windowSize = metadataPanelParentFrame.getSize();
            log.debug("screen size = "+ screenSize);
            log.debug("window size = "+ windowSize);
           
            int windowX = (screenSize.width  - metadataPanelParentFrame.getWidth())/2;
            int windowY = (screenSize.height - metadataPanelParentFrame.getHeight())/2;
            metadataPanelParentFrame.setLocation(windowX, windowY);  // Don't use "f." inside constructor.
        } else {
            if (metadataPanelParentFrame != null ) {
                metadataPanelParentFrame.dispose();
                metadataPanelParentFrame.setVisible(false);
                metadataPanelParentFrame = null;
            }
        }
    }//GEN-LAST:event_check_floatingMetadataWindowActionPerformed


   
   private void btnMetadataCancelActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnMetadataCancelActionPerformed
// TODO add your handling code here:
       this.panelEditDocumentMetadata.setVisible(false);
   }//GEN-LAST:event_btnMetadataCancelActionPerformed

   private void listboxEditorNotesValueChanged(javax.swing.event.ListSelectionEvent evt) {//GEN-FIRST:event_listboxEditorNotesValueChanged
// TODO add your handling code here:
       JList listbox = (JList)evt.getSource();
       ListModel model = listbox.getModel();
       int index = listbox.getMaxSelectionIndex();
       if (index != -1 ) {
           ooDocNoteStructure ooNote = (ooDocNoteStructure) model.getElementAt(index);
           String noteText = ooNote.getNoteText();
           txtEditorNote.setText(noteText);
       }
   }//GEN-LAST:event_listboxEditorNotesValueChanged

   private void btnSaveEditorNoteActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnSaveEditorNoteActionPerformed
// TODO add your handling code here:
       Date current = new Date();
       GregorianCalendar calendar = new GregorianCalendar();
       calendar.setTime(current);
       SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
       String strNoteDate = formatter.format(current);
       String strAuthor= "Ashok";
       String strEditorNote = txtEditorNote.getText();
       log.debug("actionPerformed:saveEditorNote");
       ooDocNoteStructure ooNote = new ooDocNoteStructure (strNoteDate, strAuthor, strEditorNote);
       m_ooNotes.addNote(ooNote);
       initEditorNotesList();
       txtEditorNote.setEditable(false);
   
   }//GEN-LAST:event_btnSaveEditorNoteActionPerformed

   private void btnNewEditorNoteActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnNewEditorNoteActionPerformed
// TODO add your handling code here:
   txtEditorNote.setText("");
   txtEditorNote.setEditable(true);
     
   }//GEN-LAST:event_btnNewEditorNoteActionPerformed


    private void btnApplyMetadata_Clicked(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnApplyMetadata_Clicked
// TODO add your handling code here:
       DefaultListModel model = (DefaultListModel) listboxMetadata.getModel();
       int count = model.getSize();
       log.debug("capacity:"+model.getSize());
       if (count == 0) 
       {
           log.debug("apply_metadata: no attribute was selected");
           MessageBox.OK("You have not selected any metadata values to set");
           return;
       }
       String[] listContents = new String[count];
       model.copyInto(listContents);
   
        try {
            HashMap xmlAttribs = ooUserDefinedAttributes.make(listContents);
            ooDocument.setAttributesToSelectedText(xmlAttribs, new Integer(0xECECEC));
            
           ooDocument.setSelectedTextBackColor(new Integer(0xECECEC));
        } catch (Exception ex) {
           log.error("adding_attribute : "+ex.getLocalizedMessage());
        }
       
    }//GEN-LAST:event_btnApplyMetadata_Clicked

    private void btnClearMetadata_Clicked(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnClearMetadata_Clicked
// TODO add your handling code here:
        listboxMetadata.setModel(new DefaultListModel());
    }//GEN-LAST:event_btnClearMetadata_Clicked

  
    private void btnSelectMP_Clicked(java.awt.event.ActionEvent evt){
       int nRow =  mpTable.getSelectedRow();
       if (nRow == -1 ) {
          lblMessage.setForeground(new Color(255,0,0));
           lblMessage.setText("You must select an MP");
           return;
       }
      String mp_name = (String)  mpTable.getValueAt(nRow, 1)+ " "+ (String) mpTable.getValueAt(nRow, 2);
      String mp_name_display = mp_name;
      String mp_uri = (String) mpTable.getValueAt(nRow, 3);
      String newLine = "\n";
      listboxMetadata.setModel(new DefaultListModel());
      DefaultListModel metadataModel = (DefaultListModel) listboxMetadata.getModel();
      metadataModel.addElement("Name: "+ mp_name);
      metadataModel.addElement("URI: "+mp_uri);
     //set the MP data in parent list box
       
    }
 
  private void btnCloseMpDialog_Clicked(java.awt.event.ActionEvent evt){
      mpDialog.dispose();
  }

/*
 *
 *
 *
 *
 *
 */  
  class CurrentSectionNameUpdater implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            
            String strSection="";
            strSection = currentSectionName();
            if (strSection.trim().length() == 0)
                self().lbl_SectionName.setText("Cursor not in section");
            else
                self().lbl_SectionName.setText(strSection);
            
        }

        public String getSectionHierarchy(XTextSection thisSection) {
            String sectionName = "";
            sectionName = ooQueryInterface.XNamed(thisSection).getName();
            if (thisSection.getParentSection() != null) {
                sectionName = getSectionHierarchy(thisSection.getParentSection()) + ">" + sectionName;
            } else
                return sectionName;
            return sectionName;    
        }
       
        
        
        public String currentSectionName() {
            XTextSection loXTextSection;
            XTextViewCursor loXTextCursor;
            XPropertySet loXPropertySet;
            String lstrSectionName = "";

         try
         {
            if (ooDocument.isXComponentValid() ) {
                loXTextCursor = ooDocument.getViewCursor();
                loXPropertySet = ooQueryInterface.XPropertySet(loXTextCursor);
                loXTextSection = (XTextSection)((Any)loXPropertySet.getPropertyValue("TextSection")).getObject();
                if (loXTextSection != null)
                {
                    //loXPropertySet = ooQueryInterface.XPropertySet(loXTextSection);
                    //XNamed objSectProps = ooQueryInterface.XNamed(loXTextSection);
                    //lstrSectionName =  objSectProps.getName(); // (String)loXPropertySet.getPropertyValue("LinkDisplayName");
                    self().currentSelectedSectionName  = ooQueryInterface.XNamed(loXTextSection).getName();
                    lstrSectionName = getSectionHierarchy(loXTextSection);
                } else
                    self().currentSelectedSectionName = "";
            }
          }
          catch (java.lang.Exception poException)
            {
                log.error("currentSectionName:" + poException.getLocalizedMessage());
            }
          finally {  
             return lstrSectionName; 
          }
        }

        
  }
    
    
  
    
    
    
    private synchronized void initTimers(){
   
      //  synchronized(this);
        try {
            //structure list & tree structure refresh timer
            Action DocStructureListRunner = new AbstractAction() {
                public void actionPerformed (ActionEvent e) {
                    initList();
                }
            };
            docStructureTimer = new Timer(3000, DocStructureListRunner);
            docStructureTimer.start();   
            
            //section name timer
            sectionNameTimer = new Timer(1000, new CurrentSectionNameUpdater());
            sectionNameTimer.start();
          
            //component handle tracker timer
            Action componentsTrackingRunner = new AbstractAction(){
                public void actionPerformed(ActionEvent e) {
                  componentHandlesTracker();
                }
            };
            componentsTrackingTimer = new Timer(5000, componentsTrackingRunner);
            componentsTrackingTimer.start();
            
            //docStructureTimer = new java.util.Timer();
            //docStructureTimer.schedule(task, 0, 3000);
        } catch (Exception e) {
            log.error(e.getMessage());
        }
    }
    
    private JTable mpTable;
    private JDialog mpDialog;
    private JLabel lblMessage;
    private String colNames[] = {"id", "First Name", "Last Name", "URI"};
   
    private void userMetadataLookup_Clicked(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_userMetadataLookup_Clicked
     //collect the data
      HashMap<String,String> registryMap = BungeniRegistryFactory.fullConnectionString();  
      BungeniClientDB dbReg = new BungeniClientDB(registryMap);
      dbReg.Connect();
      HashMap<String,Vector<Vector<String>>> results = dbReg.Query(GeneralQueryFactory.Q_FETCH_ALL_MPS());
      dbReg.EndConnect();
      QueryResults theResults = new QueryResults(results);
      if (theResults.hasResults()) {
          String[] columns = theResults.getColumns();
          Vector<String> vMpColumns = new Vector<String>();
          Vector<Vector<String>> vMps = new Vector<Vector<String>>();
          Collections.addAll(vMpColumns, columns);
          vMps = theResults.theResults();
          
           DefaultTableModel dtm = new DefaultTableModel(vMps,vMpColumns);
             mpTable = new JTable() {
                 public boolean isCellEditable(int rowIndex, int vColIndex) {
                    return false;
                    }
             };
             mpTable.setModel(dtm);
             mpTable.setRowSelectionAllowed(true);
             mpTable.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
             //mpTable.getSelectionModel().addListSelectionListener(new tblMembersOfParliamentListRowListener());

             JScrollPane sp = new JScrollPane(mpTable);
             sp.setPreferredSize(new Dimension(400,200));
             JPanel panel = new JPanel(new FlowLayout());
             panel.setPreferredSize(new Dimension(400,300));
             panel.add(sp);
             lblMessage = new JLabel();
             lblMessage.setPreferredSize(new Dimension(400, 20));
             lblMessage.setText("Please select an MP");

             JButton btnSelectMp = new JButton();
             JButton btnClose = new JButton();
             btnClose.setText("Close");
             btnClose.addActionListener(new java.awt.event.ActionListener() {
                    public void actionPerformed(java.awt.event.ActionEvent evt) {
                        btnCloseMpDialog_Clicked(evt);
                    }
                });
             btnSelectMp.setText("Select an MP");
             btnSelectMp.addActionListener(new java.awt.event.ActionListener() {
                    public void actionPerformed(java.awt.event.ActionEvent evt) {
                        btnSelectMP_Clicked(evt);
                    }
                });
             panel.add(lblMessage);
             panel.add(btnSelectMp);
             panel.add(btnClose);

             mpDialog = new JDialog();
             mpDialog.setLocationRelativeTo(null);
             mpDialog.setTitle("Select an MP");
             mpDialog.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
             mpDialog.setPreferredSize(new Dimension(420, 300));
             mpDialog.getContentPane().add(panel);
             mpDialog.pack();
             mpDialog.setVisible(true);
             mpDialog.setAlwaysOnTop(true);
          log.debug("there are results :" + columns[0] + "," + columns[1]);
      } else {
          log.debug("there are no results");
      }
      

// TODO add your handling code here:
    }//GEN-LAST:event_userMetadataLookup_Clicked

    private synchronized void componentHandlesTracker() {
        
                    //array list caches keys to be removed
                    ArrayList<String> keysToRemove = new ArrayList<String>();
                    
                    //find the components that have been disposed
                    Iterator iterKeys = editorMap.keySet().iterator();
                    while (iterKeys.hasNext()) {
                        String key = (String) iterKeys.next();
                        componentHandleContainer cont = editorMap.get(key);
                        if (cont.isComponentDisposed()) {
                            cont.removeListener();
                            keysToRemove.add(key);
                        }
                    }
                  
                  String selectedItem = (String)cboListDocuments.getSelectedItem();
                  boolean selectedItemWasRemoved = false;
                  //now remove the disposed components from the map
                   ListIterator<String> iterKeysToRemove = keysToRemove.listIterator() ;
                   while (iterKeysToRemove.hasNext()) {
                       String key = iterKeysToRemove.next();
                       if (key.equals(selectedItem)) {
                           selectedItemWasRemoved = true;
                       }
                       editorMap.remove(key);
                   }
                   
                   //now update the combo box... 
                   String[] listDocuments = editorMap.keySet().toArray(new String[editorMap.keySet().size()]);
                   cboListDocuments.setModel(new DefaultComboBoxModel(listDocuments));
                   this.program_refresh_documents = true;
                   if (selectedItemWasRemoved)
                       cboListDocuments.setSelectedIndex(0);
                   else
                       cboListDocuments.setSelectedItem(selectedItem);
                   cboListDocuments.updateUI();
                   this.program_refresh_documents = false;
    }
    private void btnApplyDocMetadataActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnApplyDocMetadataActionPerformed
// TODO add your handling code here:
        DocumentMetadataSupplier dms = ((DocumentMetadataTableModel)tableDocMetadata.getModel()).getMetadataSupplier();
        DocumentMetadata docMetadataSelectedRow = dms.getDocumentMetadata()[currentMetadataSelectedRow];
        
        if (docMetadataSelectedRow.getDataType().equals("datetime") ){
             Date ctlValue = this.editDateTxt.getDate();
             SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
             docMetadataSelectedRow.setValue(formatter.format(ctlValue));
        } else if (docMetadataSelectedRow.getDataType().equals("string") ) {
             String ctlValue = this.editStringTxt.getText();
             
           //ctlValue.equals(activeDocument)
             //check if selected row is the doctype row
             if(docMetadataSelectedRow.getName().equals("doctype")){
                
                 log.debug("doctype row selected " +  tableDocMetadata.getValueAt(0,1) + " " + tableDocMetadata.getSelectedRow());
                
                //if row is selected ensure that textbox value and row value are equal to activeDocument
                 //if(ctlValue.equals(activeDocument) && ooDocument.propertyExists("doctype")){
                 if(ooDocument.propertyExists("doctype")){
                     //row value is equal to activeDocument
                     //set the value
                     docMetadataSelectedRow.setValue(ctlValue);
                 }else{
                    log.debug("Invalid document type");
                    
                    //value is not equal to activeDocument so show error message
                    JOptionPane.showMessageDialog(null,"This document does not have a document type.","Document Type Error",JOptionPane.ERROR_MESSAGE);
                 }
                
             }else{
               //another row was selected so skip the validation
               docMetadataSelectedRow.setValue(ctlValue); 
             }
            
              
        }
        
        this.panelEditDocumentMetadata.setVisible(false);
        dms.updateMetadataToDocument(docMetadataSelectedRow.getName());
        this.tableDocMetadata.updateUI();
     
            //set the new values into the document
     
    }//GEN-LAST:event_btnApplyDocMetadataActionPerformed
    
    class changeStructureItem {
        String itemText;
        String itemIndex;
        changeStructureItem(String itemIndex, String itemText) {
            this.itemText = itemText;
            this.itemIndex = itemIndex;
        }
        
        public String getIndex() {
            return itemIndex;
        }
        public String toString(){
            return itemText;
        }
        
    }
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnApplyDocMetadata;
    private javax.swing.JButton btnApplyMetadata;
    private javax.swing.JButton btnClearMetadataValue;
    private javax.swing.ButtonGroup btnGrpBodyMetadataTarget;
    private javax.swing.JButton btnLookupMetadata;
    private javax.swing.JButton btnMetadataCancel;
    private javax.swing.JButton btnNewEditorNote;
    private javax.swing.JButton btnSaveEditorNote;
    private javax.swing.JComboBox cboListDocuments;
    private javax.swing.JComboBox cboSelectBodyMetadata;
    private javax.swing.JCheckBox check_floatingMetadataWindow;
    private javax.swing.JComboBox comboChangeStructure;
    private javax.swing.JLabel editDateLbl;
    private org.jdesktop.swingx.JXDatePicker editDateTxt;
    private javax.swing.JLabel editStringLbl;
    private javax.swing.JTextField editStringTxt;
    private javax.swing.JButton jButton1;
    private javax.swing.JComboBox jComboBox1;
    private javax.swing.JComboBox jComboBox2;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JScrollPane jScrollPane3;
    private javax.swing.JTabbedPane jTabsContainer;
    private javax.swing.JTree jTree1;
    private javax.swing.JTree jTree2;
    private javax.swing.JLabel lblEditorNotes;
    private javax.swing.JLabel lblEnterMetadataValue;
    private javax.swing.JLabel lblOpenDocuments;
    private javax.swing.JLabel lblSelectBodyMetadata;
    private javax.swing.JLabel lbl_DocStructTitle;
    private javax.swing.JTextField lbl_SectionName;
    private javax.swing.JList listboxEditorNotes;
    private javax.swing.JList listboxMetadata;
    private javax.swing.JPanel panelBodyMetadata;
    private javax.swing.JPanel panelEditDocumentMetadata;
    private javax.swing.JPanel panelHistory;
    private javax.swing.JPanel panelMarkup;
    private javax.swing.JPanel panelMetadata;
    private javax.swing.JPanel panelNotes;
    private javax.swing.JRadioButton radioDocumentSection;
    private javax.swing.JRadioButton radioSelectedText;
    private javax.swing.JScrollPane scrollDocMetadata;
    private javax.swing.JScrollPane scrollListboxMetadata;
    private javax.swing.JScrollPane scrollPane_treeDocStructure;
    private javax.swing.JScrollPane scroll_panelNotes;
    private javax.swing.JTable tableDocMetadata;
    private javax.swing.JCheckBox toggleEditSection;
    private javax.swing.JList treeDocStructure;
    private javax.swing.JTextArea txtEditorNote;
    // End of variables declaration//GEN-END:variables
   // private static listDocumentsItemChanged = false;
    class cboListDocumentsItemListener implements ItemListener {
        public void itemStateChanged(ItemEvent evt) {
            JComboBox listDocs = (JComboBox)evt.getSource();
            Object item= evt.getItem();
            
            if (evt.getStateChange() == ItemEvent.SELECTED) {
               
                //item was just selected
              //  MessageBox.Confirm(parent, "This will switch the document context from the document \n" +
                //        "titled :" + item.toString())
            } else if (evt.getStateChange() == ItemEvent.DESELECTED) {
                //item is no longer selected
            }
        }
        
    }
/**
 * This action listener updates document handles when switching between documents
 * 
 * @author  Administrator
 */
    class cboListDocumentsActionListener implements ActionListener {
        Object oldItem;
        public void actionPerformed(ActionEvent e) {
            JComboBox cb = (JComboBox) e.getSource();
            Object newItem = cb.getSelectedItem();
            boolean same = newItem.equals(oldItem);
            oldItem = newItem;
            
            if ("comboBoxChanged".equals(e.getActionCommand())) {
                if (same) {
                    if (self().program_refresh_documents == true)
                        return;
                    else
                        //check and see if the doctype property exists before you bring the window front
                     //  if(ooDocument.propertyExists("doctype")){
                            bringEditorWindowToFront();
                      // }
                        
                    //return;
                } else {
                    String key = (String)newItem;
                    componentHandleContainer xComp = editorMap.get(key);
                    if (xComp == null ) {
                        log.debug("XComponent is invalid");
                    }
                   // ooDocument.detachListener();
                    setOODocumentObject(new OOComponentHelper(xComp.getComponent(), ComponentContext));
                 
                    initFields();
                    //initializeValues();
                   
                    // removed call to collapsiblepane function
                    //retrieve the list of dynamic panels from the the dynamicPanelMap and update their component handles
                    //updateCollapsiblePanels();
                    updateFloatingPanels();
                    initNotesPanel();
                    initBodyMetadataPanel();
                    initDialogListeners();
                    //check and see if the doctype property exists before you refresh the metadata table
                    if(!ooDocument.propertyExists("doctype")){
                       JOptionPane.showMessageDialog(null,"This is not a bungeni document.","Document Type Error",JOptionPane.ERROR_MESSAGE);
                       
                    } 
                    refreshTableDocMetadataModel();
                    
                                                               
                    if (self().program_refresh_documents == false)
                        bringEditorWindowToFront();
                    
                   
                   
                       
                }
            }
            
        }
        
    }
    
    private int currentMetadataSelectedRow = 0;
    
    public class DocumentMetadataTableMouseListener implements MouseListener {
    
    /** Creates a new instance of DocumentMetadataTableMouseListener */
    public DocumentMetadataTableMouseListener() {
      }

    public void mouseClicked(MouseEvent e) {
           JTable tbl = (JTable) e.getSource();
           
          if (e.getClickCount() == 2){
            Point p = e.getPoint();
            int row = tbl.rowAtPoint(p);
            DocumentMetadataTableModel mModel  = (DocumentMetadataTableModel) tbl.getModel();
            DocumentMetadata metadataObj = mModel.getMetadataSupplier().getDocumentMetadata()[row];
            currentMetadataSelectedRow = row;
            //update the controls with the value
            if (metadataObj.getDataType().equals("datetime")) {
                try {
                self().editStringLbl.setVisible(false);
                self().editStringTxt.setVisible(false);
                self().editDateLbl.setVisible(true);
                self().editDateTxt.setVisible(true);
                
                String metaValue = metadataObj.getValue().trim();
                SimpleDateFormat formatter = new SimpleDateFormat ("yyyy-MM-dd");
                if (metaValue.length() == 0)
                    self().editDateTxt.setDate(new Date());
                else
                    self().editDateTxt.setDate(formatter.parse(metaValue));
                } catch (java.text.ParseException ex) {
                    log.error("documentMetadataMouseListener error :" + ex.getMessage());
                }
            } else if (metadataObj.getDataType().equals("string")) {
                self().editStringLbl.setVisible(true);
                self().editStringTxt.setVisible(true);
                self().editDateLbl.setVisible(false);
                self().editDateTxt.setVisible(false);
                
                String metaValue = metadataObj.getValue();
                self().editStringTxt.setText(metaValue);
            }
            self().panelEditDocumentMetadata.setVisible(true);
                    
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
    /*
     *This is the class contained in the map of all open documents
     *Adds an eventListener()
     */
    class componentHandleContainer {
        
        private String aName;
        private XComponent aComponent;
        private boolean componentDisposed = false;
        private xComponentListener compListener = new xComponentListener();
        
        componentHandleContainer(String name, XComponent xComponent) {
            log.debug("componentHandleContainer: in constructor()");
            aName = name;
            aComponent = xComponent;
            aComponent.addEventListener(compListener);
            //add the event broadcaster to the same listener
            XEventBroadcaster xEventBroadcaster = (com.sun.star.document.XEventBroadcaster) UnoRuntime.queryInterface (com.sun.star.document.XEventBroadcaster.class, aComponent);
            xEventBroadcaster.addEventListener (compListener); 
        }
        
        public XComponent getComponent(){
            return aComponent;
        }
        
        public String toString(){
            return getName();
        }
        
        public String getName(){
            return aName;
        }
        
        public boolean isComponentDisposed() {
            return componentDisposed;
        }
        
        public void removeListener(){
            aComponent.removeEventListener(compListener);
        }
    
        class xComponentListener implements com.sun.star.document.XEventListener {
                 public void disposing(com.sun.star.lang.EventObject eventObject) {
                    //document window is closing
                     log.debug("xComponentListner : the document window is closing" + getName());
                     componentDisposed = true;
                }
                
                public void notifyEvent(com.sun.star.document.EventObject eventObject) {
                    if (eventObject.EventName.equals("OnFocus")) {
                        log.error("xComponentListner : the document window OnFocus()" + getName());
                        //getName() for this document compare it with the current documetn in the editorTabbedPanel lis
                        //if it isnt equal notify the user with a message box that the 
                        Object selected = cboListDocuments.getSelectedItem();
                        String selectedDocument = "";
                        if (selected != null) {
                            selectedDocument = (String) selected;
                            if (selectedDocument.trim().equals(getName().trim())) {
                              /** commented below to prevent swing thread-sync bug **/
                               // parentFrame.setAlwaysOnTop(true);
                              //  parentFrame.setAlwaysOnTop(false);
                              //   parentFrame.toFront();
                              //  parentFrame.setAlwaysOnTop(true);
                               
                            } else {
                              /** commented below to prevent thread synchronization bug **/  
                                //parentFrame.setAlwaysOnTop(true);
                               // parentFrame.setAlwaysOnTop(false);
                               // parentFrame.toFront();
                               // parentFrame.setAlwaysOnTop(true);
                               
                                //MessageBox.OK(self(), "The current window is not the one being edited using the Bungeni Editor, please select this document :" +  getName() + " from the Editor Selector to be able to edit it!");
                            }
                        } else {
                            log.error("xComponentListner :  selected document object is null"  );
                        }
                    }
                }
        
            }        
    }
    
    class treeDocStructureTreeCellRenderer extends JLabel implements TreeCellRenderer {
        public treeDocStructureTreeCellRenderer(){

        }
        public Component getTreeCellRendererComponent(JTree tree, Object value, boolean selected, boolean expanded, boolean leaf, int row, boolean hasFocus) {
            setText(value.toString());
            if (value instanceof DefaultMutableTreeNode) {
                  DefaultMutableTreeNode uo = (DefaultMutableTreeNode)value;
                  String act = (String) uo.getUserObject();
                  if (act.trim().equals(self().currentSelectedSectionName)) {
                      setBorder( BorderFactory.createRaisedBevelBorder());
                      setBackground(new java.awt.Color(0,200,0));
                  } else {
                      setBorder(null);
                      setBackground(null);
                  }
                      
            }
            return this;
        }
        
    
    
    }
    
    public static void main(String args[]) {
    JFrame frame = new JFrame("Oval Sample");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

   editorTabbedPanel panel = new editorTabbedPanel();
   frame.add(panel);
   frame.setSize(200,400);
   frame.setVisible(true);
  }   


}
