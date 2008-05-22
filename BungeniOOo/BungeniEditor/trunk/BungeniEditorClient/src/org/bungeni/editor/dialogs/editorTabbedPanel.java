/*
 * editorTabbedPanel.java
 *
 * Created on May 28, 2007, 3:55 PM
 */

package org.bungeni.editor.dialogs;

import com.sun.corba.se.internal.iiop.ORB;
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
import org.bungeni.editor.BungeniEditorPropertiesHelper;
import org.bungeni.editor.dialogs.tree.NodeMoveTransferHandler;
import org.bungeni.editor.dialogs.tree.TreeDropTarget;
import org.bungeni.editor.macro.ExternalMacro;
import org.bungeni.editor.macro.ExternalMacroFactory;
import org.bungeni.editor.metadata.DocumentMetadata;
import org.bungeni.editor.metadata.DocumentMetadataEditInvoke;
import org.bungeni.editor.metadata.DocumentMetadataSupplier;
import org.bungeni.editor.metadata.DocumentMetadataTableModel;
import org.bungeni.editor.panels.impl.CollapsiblePanelFactory;
import org.bungeni.editor.panels.impl.FloatingPanelFactory;
import org.bungeni.editor.panels.impl.ICollapsiblePanel;
import org.bungeni.editor.panels.impl.IFloatingPanel;
import org.bungeni.editor.panels.impl.ITabbedPanel;
import org.bungeni.editor.panels.impl.TabbedPanelFactory;
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
    
    private  TreeMap<String, editorTabbedPanel.componentHandleContainer> editorMap;
    
    
    private String activeDocument; 
    private DocumentMetadataTableModel docMetadataTableModel;
    
    private HashMap<String, ICollapsiblePanel> dynamicPanelMap = new HashMap<String,ICollapsiblePanel>();
    private HashMap<String, IFloatingPanel> floatingPanelMap = new HashMap<String,IFloatingPanel>();
    private ArrayList<ITabbedPanel> m_tabbedPanelMap = new ArrayList<ITabbedPanel>();
    
    
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
       initProviders();
       initFields();
       initializeValues();
       initFloatingPane();
       
        //initCollapsiblePane();
       //initNotesPanel();
       //initBodyMetadataPanel();
       initTimers();
       log.debug("calling initOpenDOcuments");
       initOpenDocuments();
       /***** control moved to other dialog... 
       updateListDocuments();
        *****/
       //initTableDocMetadata();
       initTabbedPanes();
   
       //metadataChecks();
       
    }
    /*
    private void hideUnusedPanels(){
         this.panelMetadata.setEnabled(false); this.panelMetadata.setVisible(false);
        this.panelBodyMetadata.setEnabled(false); this.panelBodyMetadata.setVisible(false);
        this.panelMarkup.setEnabled(false); this.panelMarkup.setVisible(false);
    }*/
    private void initProviders(){
        org.bungeni.editor.providers.DocumentSectionProvider.initialize(this.ooDocument);
    }
    
    private void updateProviders() {
        org.bungeni.editor.providers.DocumentSectionProvider.updateOOoHandle(this.ooDocument);
    }
    private void initTabbedPanes() {
        log.debug("InitTabbedPanes: begin");
        m_tabbedPanelMap = TabbedPanelFactory.getPanelsByDocType(BungeniEditorProperties.getEditorProperty("activeDocumentMode"));
        for (ITabbedPanel panel: m_tabbedPanelMap ) {
            panel.setOOComponentHandle(ooDocument);
            panel.setParentHandles(parentFrame, this);
            panel.initialize();
            this.jTabsContainer.add(panel.getPanelTitle(), panel.getObjectHandle());
        }
        log.debug("InitTabbedPanes: finished loading");

        
/*        
        org.bungeni.editor.panels.sectionTreeMetadataPanel sectpanel = new org.bungeni.editor.panels.sectionTreeMetadataPanel (ooDocument, parentFrame);
        this.jTabsContainer.insertTab(sectpanel.getAccessibleContext().getAccessibleDescription(), 
                null,
                (Component) sectpanel,  sectpanel.getAccessibleContext().getAccessibleDescription(), 3 );
        
                */
    }

    private void updateTabbedPanes(){
        for (ITabbedPanel panel: m_tabbedPanelMap ) {
            panel.setOOComponentHandle(ooDocument);
            panel.refreshPanel();
        }
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
/*
    private void initTableDocMetadata(){
        
        //document metadata table model is created
        docMetadataTableModel = new DocumentMetadataTableModel(ooDocument);
        //add the check for valid metadata here 
        //if (true) set it to the table, else error 
       
       if(checkTableDocMetadata()){
            docMetadataTableModel.getMetadataSupplier().updateMetadataToDocument("doctype");
            tableDocMetadata.setModel(docMetadataTableModel );
       }
       
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
          
         
         
        
        
        
        //table model is set
        //tableDocMetadata.setModel(docMetadataTableModel );
        //various listeners are added 
       //cboListDocuments.addVetoableChangeListener(new cboListDocumentsVetoableChangeListener());
    }    
*/
    protected void setOODocumentObject (OOComponentHelper ooDoc) {
        this.ooDocument = ooDoc;
    }
    
    /*
    private void refreshTableDocMetadataModel(){
       
        docMetadataTableModel = new DocumentMetadataTableModel(ooDocument);
        tableDocMetadata.setModel(docMetadataTableModel );

        
        
    }
    */
  
    /*
     *
     *at this point the table model for the metadata table has already been set,
     *we are checking the metadata of the table
     */
    /*
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
    } */
	
    private void initListDocuments(){
        log.debug("initListDocuments: init");
        //this.cboListDocuments.removeAll();
       // Iterator docIterator = editorMap.keySet().iterator();
       // while (docIterator.hasNext()) {
       //     String docKey = (String) docIterator.next();
          //  cboListDocuments.addItem(docKey);
       // }
        /**** commment for now as we are moving control to other dialog ****
        String[] listDocuments = editorMap.keySet().toArray(new String[editorMap.keySet().size()]);
        cboListDocuments.setModel(new DefaultComboBoxModel(listDocuments));
         ******/
       // cboListDocuments.updateUI();
        //cboListDocuments.add
    }
    /**** commented because control has been moved***
    private void updateListDocuments(){
        XTextDocument xDoc = (XTextDocument)UnoRuntime.queryInterface(XTextDocument.class, this.Component);
        String strTitle = OOComponentHelper.getFrameTitle(xDoc);
        cboListDocuments.setSelectedItem(strTitle);
    }*****/
    
    private void initOpenDocumentsList(){
             try {
        log.debug("initOpenDocumentsList: getting components");
        XEnumerationAccess enumComponentsAccess = ooHelper.getDesktop().getComponents();
        XEnumeration enumComponents = enumComponentsAccess.createEnumeration();
        log.debug("initOpenDocumentsList: enumerating components");
        int i=0;
        //cboListDocuments.removeAllItems();
        editorMap.clear(); //reset the map before adding things to it.
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
        //listboxMetadata.setModel(new DefaultListModel());
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
       /**
     * Static function invoked by JPanel containing document switcher.
     * @param currentlySelectedDoc currently selected document in switched
     * @param same
     */
    public void updateMain(String currentlySelectedDoc, boolean same) {
                  if (same) {
                    if (self().program_refresh_documents == true)
                        return;
                    else
                         bringEditorWindowToFront();
                } else {
                    String key = currentlySelectedDoc;
                    componentHandleContainer xComp = editorMap.get(key);
                    if (xComp == null ) {
                        log.debug("XComponent is invalid");
                    }
                   // ooDocument.detachListener();
                    setOODocumentObject(new OOComponentHelper(xComp.getComponent(), ComponentContext));
                    updateProviders();
                    initFields();
                    //initializeValues();
                   
                    // removed call to collapsiblepane function
                    //retrieve the list of dynamic panels from the the dynamicPanelMap and update their component handles
                    //updateCollapsiblePanels();
                    updateFloatingPanels();
                    updateTabbedPanes();
                    //initNotesPanel();
                    //initBodyMetadataPanel();
                    //check and see if the doctype property exists before you refresh the metadata table
                    ///if(!ooDocument.propertyExists("doctype")){
                    ///   JOptionPane.showMessageDialog(null,"This is not a bungeni document.","Document Type Error",JOptionPane.ERROR_MESSAGE);
                    ///   
                    ///} 
                    /**** commented *** refreshTableDocMetadataModel();****/
                    if (self().program_refresh_documents == false)
                        bringEditorWindowToFront();
                    
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
            floatingPanel.setParentWindowHandle(floatingFrame);
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
           
            int windowX = screenSize.width - floatingFrame.getWidth();
            int windowY = (screenSize.height - floatingFrame.getHeight())/2;
            floatingFrame.setLocation(windowX, windowY);  // Don't use "f." inside constructor.
            floatingFrame.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
    }
    
    /*
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
    */
    
    private void updateFloatingPanels(){
        if (!floatingPanelMap.isEmpty()){
            Iterator<String> panelNames = floatingPanelMap.keySet().iterator();
                         while (panelNames.hasNext  ()) {
                             
                             IFloatingPanel panelObj = floatingPanelMap.get(panelNames.next());
                             panelObj.setOOComponentHandle(ooDocument);
                         }
        }
    }
    /*
    private void updateCollapsiblePanels(){
                  if (!dynamicPanelMap.isEmpty()) {
                         Iterator<String> panelNames = dynamicPanelMap.keySet().iterator();
                         while (panelNames.hasNext  ()) {
                             
                             ICollapsiblePanel panelObj = dynamicPanelMap.get(panelNames.next());
                             panelObj.setOOComponentHandle(ooDocument);
                         }
                    }
    }
    */
    private editorTabbedPanel self() {
        return this;
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
    /*
    private void initBodyMetadataPanel(){
        //initilize cboSelectBodyMetadata
        
        cboSelectBodyMetadata.removeAllItems();
        cboSelectBodyMetadata.addItem(new selectMetadataModel("Members of Parliament", GeneralQueryFactory.Q_FETCH_ALL_MPS()));;
        panelEditDocumentMetadata.setVisible(false);
    }
     **/
    
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
   
public TreeMap<String, editorTabbedPanel.componentHandleContainer> getCurrentlyOpenDocuments(){
    return this.editorMap;
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
 
public void hidePanelControls(){
    lbl_SectionName.setVisible(false);
    scrollPane_treeDocStructure.setVisible(false);
    lbl_DocStructTitle.setVisible(false);
    comboChangeStructure.setVisible(false);
    toggleEditSection.setVisible(false);
    this.jTabsContainer.setSize(new Dimension(243, 600));
    

    
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
   
    public void setProgrammaticRefreshOfDocumentListFlag (boolean bState) {
        this.program_refresh_documents = bState;
    }
    
    private synchronized void componentHandlesTracker() {
                    log.debug("componentHandlesTracker: begin ");
                    //array list caches keys to be removed
                    ArrayList<String> keysToRemove = new ArrayList<String>();
                    
                    //find the components that have been disposed
                    //and capture them in an array
                    log.debug("componentHandlesTracker: finding disposed documents ");
                    /*** not needed since whole list is refreshed ****
                    Iterator iterKeys = editorMap.keySet().iterator();
                    while (iterKeys.hasNext()) {
                        String key = (String) iterKeys.next();
                        componentHandleContainer cont = editorMap.get(key);
                        if (cont.isComponentDisposed()) {
                            cont.removeListener();
                            keysToRemove.add(key);
                        }
                    }****/
                      log.debug("componentHandlesTracker: capturing selected item ");
                     //store the currently selected item to reset it back after refreshing the combo
                      /***commented since combo is being moved to separate dlg 
                    String selectedItem = (String)cboListDocuments.getSelectedItem();
                    boolean selectedItemWasRemoved = false;
                       *****/
                    //now remove the disposed components from the map
                    
                      log.debug("componentHandlesTracker: removing disposed components ");
                      /**** not needed since the whole list is refreshed
                    ListIterator<String> iterKeysToRemove = keysToRemove.listIterator() ;
                    while (iterKeysToRemove.hasNext()) {
                       String key = iterKeysToRemove.next();
                       if (key.equals(selectedItem)) {
                           selectedItemWasRemoved = true;
                       }
                       editorMap.remove(key);
                   } */
                   
                   //some documents may have been opened in the meanwhile... we look for them and add them
                      log.debug("componentHandlesTracker: refreshing document open keyset map ");
                  
                    initOpenDocumentsList();
                   
                   //now update the combo box... 
                    /****combo being moved to different dlg... 
                   String[] listDocuments = editorMap.keySet().toArray(new String[editorMap.keySet().size()]);
                   cboListDocuments.setModel(new DefaultComboBoxModel(listDocuments));
                   this.program_refresh_documents = true;
                   if (selectedItemWasRemoved)
                       cboListDocuments.setSelectedIndex(0);
                   else
                       cboListDocuments.setSelectedItem(selectedItem);
                   */
                   //this.program_refresh_documents = false;
    }    
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
    private javax.swing.ButtonGroup btnGrpBodyMetadataTarget;
    private javax.swing.JComboBox comboChangeStructure;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JScrollPane jScrollPane3;
    private javax.swing.JTabbedPane jTabsContainer;
    private javax.swing.JTree jTree1;
    private javax.swing.JTree jTree2;
    private javax.swing.JLabel lbl_DocStructTitle;
    private javax.swing.JTextField lbl_SectionName;
    private javax.swing.JScrollPane scrollPane_treeDocStructure;
    private javax.swing.JCheckBox toggleEditSection;
    private javax.swing.JList treeDocStructure;
    // End of variables declaration//GEN-END:variables

    /*
     *This is the class contained in the map of all open documents
     *Adds an eventListener()
     */
    public class componentHandleContainer {
        
        private String aName;
        private XComponent aComponent;
        private boolean componentDisposed = false;
        private xComponentListener compListener = new xComponentListener();
        
        componentHandleContainer(String name, XComponent xComponent) {
            log.debug("componentHandleContainer: in constructor()");
            aName = name;
            aComponent = xComponent;
            log.debug("componentHandleContainer: to string = " + aComponent.toString());
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
                    /*
                    if (eventObject.EventName.equals("OnFocus")) {
                        log.error("xComponentListner : the document window OnFocus()" + getName());
                        //getName() for this document compare it with the current documetn in the editorTabbedPanel lis
                        //if it isnt equal notify the user with a message box that the 
                        Object selected = cboListDocuments.getSelectedItem();
                        String selectedDocument = "";
                        if (selected != null) {
                            selectedDocument = (String) selected;
                            if (selectedDocument.trim().equals(getName().trim())) {
                              /// commented below to prevent swing thread-sync bug 
                               // parentFrame.setAlwaysOnTop(true);
                              //  parentFrame.setAlwaysOnTop(false);
                              //   parentFrame.toFront();
                              //  parentFrame.setAlwaysOnTop(true);
                               
                            } else {
                             ///// commented below to prevent thread synchronization bug 
                                //parentFrame.setAlwaysOnTop(true);
                               // parentFrame.setAlwaysOnTop(false);
                               // parentFrame.toFront();
                               // parentFrame.setAlwaysOnTop(true);
                               
                                //MessageBox.OK(self(), "The current window is not the one being edited using the Bungeni Editor, please select this document :" +  getName() + " from the Editor Selector to be able to edit it!");
                            }
                        } else {
                            log.error("xComponentListner :  selected document object is null"  );
                        }
                    }*/
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

    public HashMap<String, IFloatingPanel> getFloatingPanelMap() {
        return this.floatingPanelMap;
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
