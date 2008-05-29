/*
 * sectionNumbererPanel.java
 *
 * Created on March 27, 2008, 6:39 PM
 */

package org.bungeni.editor.panels.loadable;

import com.sun.star.beans.PropertyValue;
import com.sun.star.beans.PropertyVetoException;
import com.sun.star.beans.UnknownPropertyException;
import com.sun.star.beans.XPropertySet;
import com.sun.star.beans.XPropertySetInfo;
import com.sun.star.container.NoSuchElementException;
import com.sun.star.container.XContentEnumerationAccess;
import com.sun.star.container.XEnumeration;
import com.sun.star.container.XEnumerationAccess;
import com.sun.star.container.XNameAccess;
import com.sun.star.container.XNamed;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.lang.XComponent;
import com.sun.star.lang.XServiceInfo;
import com.sun.star.text.ReferenceFieldPart;
import com.sun.star.text.ReferenceFieldSource;
import com.sun.star.text.XReferenceMarksSupplier;
import com.sun.star.text.XSimpleText;
import com.sun.star.text.XText;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextCursor;
import com.sun.star.text.XTextDocument;
import com.sun.star.text.XTextField;
import com.sun.star.text.XTextRange;
import com.sun.star.text.XTextSection;
import com.sun.star.text.XTextViewCursor;
import com.sun.star.text.XTextViewCursorSupplier;
import com.sun.star.text.XWordCursor;
import com.sun.star.uno.Any;
import com.sun.star.uno.AnyConverter;
import com.sun.star.uno.Type;
import com.sun.star.uno.UnoRuntime;
import com.sun.star.uno.XComponentContext;
import com.sun.star.util.XNumberFormatTypes;
import com.sun.star.util.XNumberFormats;
import com.sun.star.util.XNumberFormatsSupplier;
import com.sun.star.util.XPropertyReplace;
import com.sun.star.util.XRefreshable;
import com.sun.star.util.XReplaceDescriptor;
import com.sun.star.util.XReplaceable;
import com.sun.star.util.XSearchDescriptor;
import com.sun.star.util.SearchOptions;
import com.sun.star.view.XViewCursor;
import com.sun.star.xforms.XModel;
import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.swing.DefaultComboBoxModel;
import javax.swing.DefaultListModel;
import javax.swing.JFrame;
import javax.swing.Timer;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.event.TreeSelectionEvent;
import javax.swing.event.TreeSelectionListener;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreePath;
import javax.swing.tree.TreeSelectionModel;

import org.bungeni.editor.BungeniEditorProperties;
import org.bungeni.editor.panels.impl.BaseClassForITabbedPanel;
import org.bungeni.editor.providers.DocumentSectionIterator;
import org.bungeni.editor.providers.DocumentSectionProvider;
import org.bungeni.editor.providers.IBungeniSectionIteratorListener;
import org.bungeni.numbering.impl.IGeneralNumberingScheme;
import org.bungeni.numbering.impl.NumberRange;
import org.bungeni.numbering.impl.NumberingSchemeFactory;
import org.bungeni.editor.numbering.ooo.OOoNumberingHelper;

import org.bungeni.ooo.BungenioOoHelper;
import org.bungeni.ooo.OOComponentHelper;
import org.apache.log4j.Logger;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.ooo.ooUserDefinedAttributes;
import org.bungeni.utils.BungeniBNode;
import org.bungeni.utils.BungeniUUID;
import org.bungeni.ooo.utils.CommonExceptionUtils;
import org.bungeni.utils.CommonTreeFunctions;
import org.bungeni.utils.MessageBox;


/**
 *
 * @author  undesa
 */
public class sectionNumbererPanel extends  BaseClassForITabbedPanel {
   //  HashMap<String, String> sectionMetadataMap=new HashMap<String, String>();
   //HashMap<String, String> sectionTypeMetadataMap=new HashMap<String, String>();
    private static org.apache.log4j.Logger log = Logger.getLogger(sectionNumbererPanel.class.getName());
   
    private boolean m_useParentPrefix = false;
    private IGeneralNumberingScheme m_selectedNumberingScheme ;
    //private HashMap<String,String> metadata = new HashMap();
    private ArrayList<String> sectionTypeMatchedSections = new ArrayList<String>();
    private ArrayList<String> sectionTypeMatchedSectionsMissingNumbering = new ArrayList<String>();
  //  private ArrayList<String> docListReferences = new ArrayList<String>();
 //    private ArrayList<String> docReferences = new ArrayList<String>();
 //   private ArrayList<String> insertedNumbers = new ArrayList<String>();
    private ArrayList<String> sectionHierarchy = new ArrayList<String>();
    private int headCount=1;
    //DefaultListModel model=new DefaultListModel();
    private IGeneralNumberingScheme inumScheme;
    private String numParentPrefix="";
    private ArrayList<String> sectionTypesInDocument = new ArrayList<String>();
    private String selectSection="";
   
    private DefaultMutableTreeNode sectionRootNode = null;
    private String[] m_validParentSections;
    private String selectedNodeName="";
     
     TreeMap<String, sectionHeadingReferenceMarks> refMarksMap = new TreeMap<String, sectionHeadingReferenceMarks>();
     private ArrayList<Object> refMarksInHeadingMatched= new ArrayList<Object>(0);
     private ArrayList<Object> refMarksForHeading= new ArrayList<Object>(0);


     
     private HashMap<String, String> defaultSectionMetadata  = new HashMap<String,String>();
     private static String NUMBER_SPACE = " ";
     private static String PARENT_PREFIX_SEPARATOR=".";

    private Timer timerSectionTypes;

     
    /** Creates new form sectionNumbererPanel */
    public sectionNumbererPanel() {
       initComponents();
    }
    /*
    public sectionNumbererPanel(XComponentContext xContext){
        this.xContext=xContext;
        initComponents();
        init();
    }
    */
    private void init(){
        //initComponents();
        initSectionTypesMap();
        initSectionTypesListBox();
       // listSectionTypes.addListSelectionListener(new NumberingSchemeListener());
        //panelNumberingScheme.setVisible(false);
        /*init parent prefix checkbox */
        checkbxUseParentPrefix.setSelected(false);
        m_useParentPrefix = false;
        checkbxUseParentPrefix.addActionListener(
                new java.awt.event.ActionListener() {
                    public void actionPerformed(java.awt.event.ActionEvent evt) {
                        javax.swing.AbstractButton btn = (javax.swing.AbstractButton) evt.getSource();
                        m_useParentPrefix = btn.getModel().isSelected();
                    }
        } );
        //all commented below ... not required ??
        //checkbxUseParentPrefix.addItemListener(new ParentSchemeListener());
        //packReferences();
        //initTree();
        //initSectionTree();
        initNumberingSchemesCombo();
        initTimer();
        //the following is commented becuase its definitely not required !
        //findBrokenReferences();
    }
    
     private synchronized void initTimer(){
          timerSectionTypes = new Timer(4000, new ActionListener() {
              public void actionPerformed(ActionEvent e) {
                refreshSectionTypesList();
              }
           });
           timerSectionTypes.start();
    }
    
     private void refreshSectionTypesList(){
            java.awt.EventQueue.invokeLater(new Runnable() {
                    public void run() {
                         String selectedItem = (String) listSectionTypes.getSelectedValue();
                         initSectionTypesMap();
                         initSectionTypesListBox();
                         if (selectedItem != null )
                            listSectionTypes.setSelectedValue(selectedItem, true);
                    }
            });
     }
     
    class numberingSchemeSelection extends Object {
        String schemeName;
        String schemeDesc;
        String schemeClass;
        public String toString(){
            return schemeName;
        }
    }
    
    /*
     *gets the selected numbering scheme in the numbering scheme combo box 
     */
    private numberingSchemeSelection getSelectedNumberingScheme() {
       numberingSchemeSelection schemeSelection = (numberingSchemeSelection) cboNumberingScheme.getSelectedItem();
       return schemeSelection;
    }
    
    /*
     *create a numbering scheme object from the selected scheme 
     */
    private IGeneralNumberingScheme createSchemeFromSelection() {
        numberingSchemeSelection schemeSelection = getSelectedNumberingScheme();
        IGeneralNumberingScheme inumScheme = NumberingSchemeFactory.getNumberingScheme(schemeSelection.schemeName);
        return inumScheme;
    }
    /*
     *initiliazes the numbering scheme combo by setting values in it
     */
    private void initNumberingSchemesCombo(){
        Iterator<String> schemeIterator = NumberingSchemeFactory.numberingSchemes.keySet().iterator();
        numberingSchemeSelection[] sels = new numberingSchemeSelection[NumberingSchemeFactory.numberingSchemes.size()];
        int i = 0;
        while (schemeIterator.hasNext()) {
            sels[i] = new numberingSchemeSelection();
            sels[i].schemeName = schemeIterator.next();
            sels[i].schemeClass = NumberingSchemeFactory.numberingSchemes.get(sels[i].schemeName);
            i++;
        }
        this.cboNumberingScheme.setModel(new DefaultComboBoxModel(sels));
    }
    
    private void initSectionTypesMap() {
        this.sectionTypesInDocument.clear();
       XNameAccess docSections = ooDocument.getTextSections();
       String[] sectionNames = docSections.getElementNames();
       for (String aSection : sectionNames) {
            HashMap<String,String> sectionMeta = ooDocument.getSectionMetadataAttributes(aSection);
            if (sectionMeta.containsKey("BungeniSectionType")) {
                String sectionType = sectionMeta.get("BungeniSectionType");
                if (!this.sectionTypesInDocument.contains(sectionType))
                    this.sectionTypesInDocument.add(sectionType);
            }
       }
       if (sectionTypesInDocument.size() > 0 )
        Collections.sort(sectionTypesInDocument);
    }
    
    /*
    private void fetchSectionTypesAndInitTree(){
        try{
            if (!ooDocument.getTextSections().hasByName("root")) {
                System.out.println("no root section found");
                return;
            }
            Object rootSection = ooDocument.getTextSections().getByName("root");
            XTextSection theSection = ooQueryInterface.XTextSection(rootSection);
            //create the tree here
         //    sectionRootNode = new DefaultMutableTreeNode(new String("root"));
         //    CommonTreeFunctions.expandAll(treeSectionStructure);
             recurseSectionTypesAndInitTree (theSection,sectionRootNode);
         }catch (NoSuchElementException ex) {
            log.error(ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error(ex.getMessage());
        }
        
        
    }
    */
    /*
    private void recurseSectionTypesAndInitTree(XTextSection theSection,DefaultMutableTreeNode node){
          //recurse children
            XTextSection[] sections = theSection.getChildSections();
            if (sections != null ) {
                if (sections.length > 0 ) {
                    //start from last index and go to first
                    for (int nSection = sections.length - 1 ; nSection >=0 ; nSection--) {
                        XNamed xSecName = ooQueryInterface.XNamed(sections[nSection]);
                        String childSectionName = (String) xSecName.getName();
                        //build section tree here also 
                        DefaultMutableTreeNode newNode = new DefaultMutableTreeNode(childSectionName);
                        node.add(newNode);
                        HashMap<String,String> sectionMetadataMap=ooDocument.getSectionMetadataAttributes(childSectionName);
                        if (sectionMetadataMap.containsKey("BungeniSectionType"))
                            attributeSet.add(sectionMetadataMap.get("BungeniSectionType").trim());
                        recurseSectionTypesAndInitTree(sections[nSection],newNode);
                     }
                   
                } 
            }
            
    }
    */
    private void initSectionTypesListBox(){
         DefaultListModel listModel = new DefaultListModel();
         
         for (String sectionType: sectionTypesInDocument ) {
            listModel.addElement(sectionType);
         }
        this.listSectionTypes.setModel(listModel);
    }
    
    

    
   
     private void applyNumberingScheme(){
         m_bFoundHeading = false;
         if (listSectionTypes.getSelectedIndex() == -1 ) {
             MessageBox.OK(parentFrame, "Please select a section type to apply numbering upon !");
             return;
         }
        String sectionType=listSectionTypes.getSelectedValue().toString();            
        ////find all sections matching that section type, and populate arraylist
        ///was called readSection()
        initNumbering();
        buildArrayOfSectionsMatchingType(sectionType);
        System.out.println("matched sections =  " + this.sectionTypeMatchedSections);
        //findSectionsMatchingSectionType(sectionType);
       // iterate through arraylist and set numberingscheme metadata to matching sections
       // was called applyNumberingScheme() 
        if (checkIfSectionsHaveNumberingScheme() == true ) {
            MessageBox.OK(parentFrame, "The section type already has a numbering scheme ! \n If you wish you to re-number the sections, please use the 'Renumbering' button ");
            return;
        }
        //setNumberingSchemeMetadataIntoMatchingSections();
        ///why is the above being done...when the same section is iterated over again ??? 
        this.IterateSectionTypesForNumberedHeadings();
        /*
        matchHeadingsInTypedSections();
        if (! m_bFoundHeading ) {
            MessageBox.OK(parentFrame, "No headings were found to apply numbering upon !");
            return;
        }
         */
     }
   
     
     private void initNumbering(){

         this.sectionTypeMatchedSections.clear();
         this.sectionTypeMatchedSectionsMissingNumbering.clear();
                 
     }
     
     private void buildArrayOfSectionsMatchingType(String sectionType) {
    
         BungeniBNode bNode = DocumentSectionProvider.getTreeRoot();
         recurseNodes(bNode, sectionType);
    }
         
     private void recurseNodes(BungeniBNode theNode, String filterSectionType) {
        BungeniBNode theBNode = theNode;
        String sectionName = theBNode.getName();
        String sectionType = ooDocument.getSectionType(sectionName);
        if (sectionType != null ) {
            if (sectionType.equals(filterSectionType)){
                this.sectionTypeMatchedSections.add(sectionName);
            }
        }
        if (theBNode.hasChildren()) {
            TreeMap<Integer, BungeniBNode> children = theBNode.getChildrenByOrder();
            Iterator<Integer> childIterator = children.keySet().iterator();
            while (childIterator.hasNext()) {
                Integer nodeKey = childIterator.next();
                BungeniBNode childNode = children.get(nodeKey);
                recurseNodes(childNode, filterSectionType);
            }
        }
        
     }
     
     private void applyRenumberingScheme(){
       // String sectionType=listSectionTypes.getSelectedValue().toString();            
       /// findSectionsMatchingSectionType(sectionType);
      //renumber happes for all sections
         //1) iterate through numbered headings (sections containing a child NumberedContainer section)
         //2) find those that dont have numbers (sections without NumberingScheme or AppliedNumber properties...)
         //3) apply blank numbering metadata to them (do an apply numbering markup on these sections but dont put any numbers...)
         //4) make another pass and apply numbering (finally apply numbering on the whole structure...)
         
         //1)
         ArrayList<String>numberedContainers = findNumberedContainers();
         //2) & 3)
         applyNumberingMarkupToNonNumberedContainers(numberedContainers);
         //4)
         reApplyNumberingOnNumberedContainers();
     }
    
     private ArrayList<String> findNumberedContainers(){
        ArrayList<String> numberedContainers = new ArrayList<String>(0);
        BungeniBNode bRootNode = DocumentSectionProvider.getTreeRoot();
        recurseNumberedNodes(bRootNode, numberedContainers );
        return numberedContainers;
     }

       private void recurseNumberedNodes(BungeniBNode theBNode, ArrayList<String> numberedContainers) {
       // BungeniBNode theBNode = (BungeniBNode) theNode.getUserObject();
        if (theBNode.hasChildren()) {
            TreeMap<Integer, BungeniBNode> children = theBNode.getChildrenByOrder();
            Iterator<Integer> childIterator = children.keySet().iterator();
            while (childIterator.hasNext()) {
                Integer nodeKey = childIterator.next();
                BungeniBNode newBNode = children.get(nodeKey);
                String sectionName = newBNode.getName();
                String matchingSectionType = ooDocument.getSectionType(sectionName);
                if (matchingSectionType != null) {
                    if (matchingSectionType.equals(OOoNumberingHelper.NUMBERING_SECTION_TYPE)) {
                        numberedContainers.add(sectionName);
                    }
                }
                recurseNumberedNodes(newBNode, numberedContainers);
            }
        }
    }
    
   private static String MARKED_FOR_RENUMBERING="RENUMBERING...";
   private void applyNumberingMarkupToNonNumberedContainers(ArrayList<String> numberedContainers){
           for (String containerSection : numberedContainers) {
                XTextSection numberedSection = ooDocument.getSection(containerSection);
                if (!isSectionContainingAppliedNumber(numberedSection)) {
                    ooDocument.protectSection(numberedSection, false);
                    this.markupNumberedHeading(numberedSection, MARKED_FOR_RENUMBERING);
                    ooDocument.protectSection(numberedSection, true);
                }
           }
   }
   
   private boolean isSectionContainingAppliedNumber (XTextSection numberedSection ) {
                boolean bState= false;
                HashMap<String,String> sectionMeta = ooDocument.getSectionMetadataAttributes(numberedSection);
                XNamed nameSection = ooQueryInterface.XNamed(numberedSection);
                Set<String> numberingMeta = OOoNumberingHelper.numberingMetadata.keySet();
                for (String numberMetaKey : numberingMeta) {
                    if (sectionMeta.containsKey(OOoNumberingHelper.numberingMetadata.get(numberMetaKey))) {
                        log.debug("isSectionContainingAppliedNumber : ("+ nameSection.getName() +") true " );
                        bState = true;
                        break;
                    }
                }
                log.debug("isSectionContainingAppliedNumber : ("+ nameSection.getName() +") false " );
                return bState;
   }
   
   ///replace later with proper factory provider class
    ArrayList<String> validNumberedSectionTypes = new ArrayList<String>() {
        {
                add("Article");
                add("Clause");
        }
    };
    
    private void reApplyNumberingOnNumberedContainers(){
        //now iterate through the numbered sections and apply 
        sectionRenumberingIteratorListener sril = new sectionRenumberingIteratorListener();
        DocumentSectionIterator sectionIterator = new DocumentSectionIterator(sril);
        sectionIterator.startIterator();
        for (String numberedSectionType : sril.numberTheseSectionTypes) {
            
        }
    }

    class sectionRenumberingIteratorListener implements IBungeniSectionIteratorListener{
             ArrayList<String> numberTheseSectionTypes = new ArrayList<String>(0) ;   
                    //return tru to continue , false to break
                    public boolean iteratorCallback(BungeniBNode bNode) {
                        String sectionName = bNode.getName();
                        log.debug("reApplyNumberingonNumberedContainers, iterator callback : "+ sectionName);
                        String sectionType = ooDocument.getSectionType(sectionName);
                        if (sectionType != null ) {
                            if (validNumberedSectionTypes.contains(sectionType)) {
                                //this type of section can be numbered
                                if (!numberTheseSectionTypes.contains(sectionType)) { //has it been already numbered ?
                                    log.debug("reApplyNumberingonNumberedContainers, iterator numbering "+ sectionType);
                                    // renumberSectionType (sectionType);
                                     numberTheseSectionTypes.add(sectionType);
                                }
                                if (numberTheseSectionTypes.size() == validNumberedSectionTypes.size())
                                    return false;
                            }
                        }
                        return true;
                    }
        }
        
    private void func(String sectionType){
        ArrayList<String> sectionsMatchingType = getSectionsMatchingType(sectionType);
        System.out.println("matched sections =  " + this.sectionTypeMatchedSections);
        this.initializeNumberingSchemeGenerator(1, sectionsMatchingType.size());
        //findSectionsMatchingSectionType(sectionType);
        ///why is the above being done...when the same section is iterated over again ??? 
        for (String matchingSection: sectionsMatchingType) {
            XTextSection matchedSection = ooDocument.getSection(matchingSection);
            XTextSection numberedChild = ooDocument.getChildSectionByType(matchedSection, OOoNumberingHelper.NUMBERING_SECTION_TYPE);
            String theNumber = this.m_selectedNumberingScheme.sequence_next();
            ooDocument.protectSection(numberedChild, false);
            HashMap<String,String> childMeta = ooDocument.getSectionMetadataAttributes(numberedChild);
            String sectionUUID = childMeta.get("BungeniSectionUUID");
            ////update the field here ooDocument.getTextFields();
        }  
        
    }
    
    private ArrayList<String> getSectionsMatchingType (String sectionType){
      //  ArrayList<String> sectionsMatchingType = new ArrayList<String>(0);
        sectionTypeIteratorListener  typeIterator = new sectionTypeIteratorListener(sectionType);
        DocumentSectionIterator sectionTypeIterator = new DocumentSectionIterator(typeIterator);
        sectionTypeIterator.startIterator();
        return typeIterator.sectionsMatchingType;
    }
    
    class sectionTypeIteratorListener implements IBungeniSectionIteratorListener {
        ArrayList<String> sectionsMatchingType = new ArrayList<String>(0);
        String inputSectionType ;
        
        sectionTypeIteratorListener(String input) {
            this.inputSectionType = input;
        }
        
        public boolean iteratorCallback(BungeniBNode bNode) {
            String foundsectionName = bNode.getName();
            String foundsectionType =  ooDocument.getSectionType(foundsectionName);
            if (foundsectionType.equals(inputSectionType)) {
                sectionsMatchingType.add(foundsectionName);
            }
            return true;       
        }
        
    }
    
     private frameBrokenReferences brokenReferencesFrame = null;
     private void applyFixBrokenReferences() {
        this.orphanedReferences.clear();
       
        findBrokenReferences();
        
        if (this.orphanedReferences.size() > 0  ) {
               if (brokenReferencesFrame != null  ) {
                   if (brokenReferencesFrame.getLaunchedState()){
                       brokenReferencesFrame.dispose();
                   }
               }
               java.awt.EventQueue.invokeLater(new Runnable() {
                    public void run() {
                            frameBrokenReferences.LaunchMode mode = frameBrokenReferences.LaunchMode.BrowseBroken; 
                            brokenReferencesFrame = frameBrokenReferences.Launch(ooDocument,  parentFrame, orphanedReferences, mode);
                    }
               });
        } else {
            MessageBox.OK(this, "No Broken references found !");
        }
         
     }
     
     
     private void applyInsertCrossReferences(){
        this.orphanedReferences.clear();
        findBrokenReferences();
        if (brokenReferencesFrame != null  ) {
                   if (brokenReferencesFrame.getLaunchedState()){
                       brokenReferencesFrame.dispose();
                   }
               }
               java.awt.EventQueue.invokeLater(new Runnable() {
                    public void run() {
                            frameBrokenReferences.LaunchMode mode = frameBrokenReferences.LaunchMode.CrossReferences; 
                            brokenReferencesFrame = frameBrokenReferences.Launch(ooDocument,  parentFrame, orphanedReferences, mode);
                    }
               });     
     }
     
     private boolean checkIfSectionsHaveNumberingScheme(){
        for (String matchedSection: sectionTypeMatchedSections) {
            //has child heading marked for numbering
            XTextSection numberedSection =  ooDocument.getChildSectionByType(ooDocument.getSection(matchedSection),OOoNumberingHelper.NUMBERING_SECTION_TYPE);
           if (numberedSection != null ) { // it has a numbered heading  so fail     
                //check if section marked for numbering actually has a number 
                if (this.isSectionContainingAppliedNumber(numberedSection))
                    return true;
           } 
        }
        return false;
     }
     
  private void getParentFromSection(XTextRange aTextRange){
      
       String prevParent="";
        Iterator typedMatchSectionItr = sectionTypeMatchedSections.iterator();
          while(typedMatchSectionItr.hasNext()){
                Object matchedSectionElem=typedMatchSectionItr.next();
            try {
                    Object rootSection = ooDocument.getTextSections().getByName(matchedSectionElem.toString());
                    XTextSection theSection = ooQueryInterface.XTextSection(rootSection);

                     XNamed xParentSecName= ooQueryInterface.XNamed(theSection.getParentSection());
                     String currentParent=(String)xParentSecName.getName();
                     if(!currentParent.equalsIgnoreCase(prevParent)){
                         //restart numbering here
                         headCount=1;
                         System.out.println("different parent" + "testCount " + headCount);
                       
                     }else{
                         //continue numbering
                        headCount++;
                                     
                        System.out.println("same parent" + "testCount " + headCount);
                     }
                    prevParent=(String)xParentSecName.getName();

                    } catch (NoSuchElementException ex) {
                        ex.printStackTrace();
                    } catch (WrappedTargetException ex) {
                        ex.printStackTrace();
                    }
                
                 
          }
     
        
   }
    
  private ArrayList<XTextField> orphanedReferences = new ArrayList<XTextField>();
  private void findBrokenReferences(){
      try {
      XTextDocument oDoc = ooDocument.getTextDocument();
      //get reference mark objects
      XNameAccess refMarks = ooDocument.getReferenceMarks();
      //get text fields
      XEnumerationAccess refFields = ooDocument.getTextFields(); 
      XEnumeration fieldEnum = refFields.createEnumeration();
      while (fieldEnum.hasMoreElements()) {
          Object objField = fieldEnum.nextElement();
          XServiceInfo servInfo = ooDocument.getServiceInfo(objField);
          if (servInfo.supportsService("com.sun.star.text.TextField.GetReference")) {
              /*
              	if oTextField.ReferenceFieldSource = com.sun.star.text.ReferenceFieldSource.REFERENCE_MARK then
			if not oRefMarks.hasByName(oTextField.Sourcename) then
				nCount = nCount + 1
				subOrphan(oTextField)
			end if
		else*/
              XTextField foundField = ooQueryInterface.XTextField(objField);
              XPropertySet propSet = ooDocument.getObjectPropertySet(foundField);
              short refFieldSource = AnyConverter.toShort(propSet.getPropertyValue("ReferenceFieldSource"));
                    String refSourceName;
                        refSourceName = AnyConverter.toString(propSet.getPropertyValue("SourceName"));
              switch (refFieldSource) {
                  case com.sun.star.text.ReferenceFieldSource.REFERENCE_MARK :
                       if (!refMarks.hasByName(refSourceName)) {
                            //this is a dead reference
                           addOrphanedField(foundField);
                       }
                      break;
                      
                  case com.sun.star.text.ReferenceFieldSource.BOOKMARK :
                      
                      break;
                      
                  case com.sun.star.text.ReferenceFieldSource.SEQUENCE_FIELD :
                      
                      break;

                      
                  case com.sun.star.text.ReferenceFieldSource.FOOTNOTE :
                      
                      break;
                      
                  case com.sun.star.text.ReferenceFieldSource.ENDNOTE :
                      
                      break;
                      
                             
                           
              }
               
          }
      }
      } catch (WrappedTargetException ex) {
            log.error(ex.getClass().getName() + " - " + ex.getMessage());
      } catch (com.sun.star.lang.IllegalArgumentException ex) {
            log.error(ex.getClass().getName() + " - " + ex.getMessage());
      } catch (UnknownPropertyException ex) {
            log.error(ex.getClass().getName() + " - " + ex.getMessage());
      } catch (com.sun.star.container.NoSuchElementException ex) {
            log.error(ex.getClass().getName() + " - " + ex.getMessage());
      }
  }
  
  private void addOrphanedField (XTextField field) {
        orphanedReferences.add(field);
  }
  

  // was
  //private void insertNumberOnRenumbering(XTextRange aTextRange, int testCount, Object elem, Object refMark){
  //was
  //private ArrayList getNumberReferenceFromHeading(Object elem){
  
  
    
//removed removeNumberFromHeading();
      
   
    
   
    
    //Returns 1st heading in the section
    //      was private Object getNumberedHeadingsInsertCrossRef(String results) ;
    //was 
    //private ArrayList<String> getReferenceMarksOnCross(Object elem);
        
    
    
    
    
     //method to get reference mark from heading when renumbering
    // was private void setReferenceMarkOnRenumbering(XTextRange aTextRange, Object elem, Object refMark)
    
    
    //was private void insertReferenceMarkOnReNumbering(XTextRange aTextRange, Object elem, int refLength, Object refMark)
  
    
   private XTextSection getChildSectionByType(XTextSection parentSection) {
       XTextSection[] childSections = parentSection.getChildSections();
       for (XTextSection childSection: childSections) {
            HashMap<String,String> childMeta = ooDocument.getSectionMetadataAttributes(childSection);
            if (childMeta.containsKey("BungeniSectionType")){
                String sectionType = childMeta.get("BungeniSectionType");
                if (sectionType.equals("NumberedContainer")){
                    return childSection;
                }
            }
       }
       return null;
   }  
    
   private void IterateSectionTypesForNumberedHeadings(){
        try {
            String prevParent="";
           //set member variable that stores current numbering scheme
            //and then generate sequence.. with the upper range set to number of matched sections
            initializeNumberingSchemeGenerator((long)1, (long) sectionTypeMatchedSections.size() );
            //check if parent prefix was selected
            
            /*iterate through the sectionTypeMatchedSections and look for heading in section*/
            Iterator<String> typedMatchSectionItr = sectionTypeMatchedSections.iterator();
            while(typedMatchSectionItr.hasNext()){

                String sectionName = typedMatchSectionItr.next();
                 /*get the XTextSection object of the matching section*/
                XTextSection theSection = ooDocument.getSection(sectionName);
                /*get the parent of the matching section*/
                 XTextSection theSectionsParent = theSection.getParentSection();
                 /*get the child numbered heading */
                 XTextSection childSection = this.getChildSectionByType(theSection);
                 if (childSection == null ) {
                     this.sectionTypeMatchedSectionsMissingNumbering.add(sectionName);
                 } else {
                     //valid numbering header found
                     //unprotect section
                     ooDocument.protectSection(childSection, false);
                     applyNumberToNumberContainer(theSection, theSectionsParent, childSection, prevParent );
                     //prootct section again
                     ooDocument.protectSection(childSection, true);
                 }
                 
                /*get the anchor of the matching section*/
    
                prevParent = ooQueryInterface.XNamed(theSectionsParent).getName();
            }
        } catch (Exception ex) {
            log.error("matchHeadingsInTypedSections : " + ex.getMessage());
            log.error("matchHeadingsInTypedSections : " + CommonExceptionUtils.getStackTrace(ex));
        }    
       
   }

   private void applyNumberToNumberContainer(XTextSection theSection, XTextSection parentSection, XTextSection childSection, String prevParent) {
       //get the name of the current parent
       String currentParent ="";
       XNamed parentName = ooQueryInterface.XNamed(parentSection);
       currentParent  = parentName.getName();
       if (!currentParent.equals(prevParent)) {
           //reset iterator
           this.m_selectedNumberingScheme.sequence_initIterator();
       }
       markHeadingAndApplyNumber(theSection, parentSection, childSection, prevParent);

   }
   
   
      private void markHeadingAndApplyNumber(XTextSection theCurrentSection, XTextSection parentSection, XTextSection childSection, String prevParent){
            //get the current numbering
            //restart numbering, by resetting the iterator
            //this.m_selectedNumberingScheme.sequence_initIterator();
            //get the next number in the sequence
            String theNumber = this.m_selectedNumberingScheme.sequence_next();
            String parentPrefix = "";
            //if number has parent prefix
            /*
            if (this.m_useParentPrefix) {
                //get parent prefix
                //attache the parent prefix to the number.
                  parentPrefix =   getParentPrefix(theCurrentSection, parentSection);
            }*/
            // we want insert  number + space before heading
            // and set a reference mark over the number
            
            markupNumberedHeading (childSection, theNumber); 
            /*
            HashMap<String, String> numberedHeadingMap = ooDocument.getSectionMetadataAttributes(childSection);
            //get section UUID
            String sectionUUID = numberedHeadingMap.get("BungeniSectionUUID");
            //get the anchor to the numbered heading section
            XTextRange sectionRange = childSection.getAnchor();
            //get the text of the heading in the section
            String headingInSection = sectionRange.getString();
            //create a cursor to walk the heading
            XTextCursor sectionCursor = ooDocument.getTextDocument().getText().createTextCursor();
            //map the cursor to the heading range
            sectionCursor.gotoRange(sectionRange, false);
            //insert a field for the number
            insertField(sectionCursor.getStart(), OOoNumberingHelper.NUM_FIELD_PREFIX, sectionUUID, theNumber);
            sectionCursor.goLeft( (short) 0,false);
            sectionCursor.getText().insertString(sectionCursor, " ", true);
            sectionCursor.goLeft((short) 0, false);
            sectionCursor.goRight((short) 1, false);
            sectionCursor.gotoRange(sectionRange.getEnd(), true);
            //insert a field for the heading
            insertField(sectionCursor, OOoNumberingHelper.HEAD_FIELD_PREFIX, sectionUUID, headingInSection);
            //finally create a reference for the complete heading
            sectionCursor.gotoRange(childSection.getAnchor(), true);
            insertReferenceMark(sectionCursor, sectionUUID);
            updateSectionNumberingMetadata(childSection, theNumber);
             */
   }
  
      private void markupNumberedHeading (XTextSection childSection, String theNumber) {
            HashMap<String, String> numberedHeadingMap = ooDocument.getSectionMetadataAttributes(childSection);
            //get section UUID
            String sectionUUID = numberedHeadingMap.get("BungeniSectionUUID");
            //get the anchor to the numbered heading section
            XTextRange sectionRange = childSection.getAnchor();
            //get the text of the heading in the section
            String headingInSection = sectionRange.getString();
            //create a cursor to walk the heading
            XTextCursor sectionCursor = ooDocument.getTextDocument().getText().createTextCursor();
            //map the cursor to the heading range
            sectionCursor.gotoRange(sectionRange, false);
            //insert a field for the number
            insertField(sectionCursor.getStart(), OOoNumberingHelper.NUM_FIELD_PREFIX, sectionUUID, theNumber);
            sectionCursor.goLeft( (short) 0,false);
            sectionCursor.getText().insertString(sectionCursor, " ", true);
            sectionCursor.goLeft((short) 0, false);
            sectionCursor.goRight((short) 1, false);
            sectionCursor.gotoRange(sectionRange.getEnd(), true);
            //insert a field for the heading
            insertField(sectionCursor, OOoNumberingHelper.HEAD_FIELD_PREFIX, sectionUUID, headingInSection);
            //finally create a reference for the complete heading
            sectionCursor.gotoRange(childSection.getAnchor(), true);
            insertReferenceMark(sectionCursor, sectionUUID);
            updateSectionNumberingMetadata(childSection, theNumber);
      }
      
   private void insertField(XTextRange cursorRange, String fieldPrefix , String uuidOfField, String fieldContent) {   
        String nameOfField =fieldPrefix + uuidOfField;
        Object refField = ooDocument.createInstance("com.sun.star.text.TextField.Input");
        XPropertySet propSet = ooQueryInterface.XPropertySet(refField);
        try {
            propSet.setPropertyValue("Hint", nameOfField );
            propSet.setPropertyValue("Content", fieldContent);
            //insert the field into the document
            XTextContent fieldContentObject = ooQueryInterface.XTextContent(refField);
            cursorRange.getText().insertTextContent(cursorRange, fieldContentObject, true);
            
        } catch (PropertyVetoException ex) {
            log.error("ïnsertField :( " +ex.getClass().getName() + ")"+  ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error("ïnsertField :( " +ex.getClass().getName() + ")"+  ex.getMessage());
        } catch (UnknownPropertyException ex) {
            log.error("ïnsertField :( " +ex.getClass().getName() + ")"+  ex.getMessage());
        } catch (com.sun.star.lang.IllegalArgumentException ex) {
            log.error("ïnsertField :( " +ex.getClass().getName() + ")"+  ex.getMessage());
        }
   }
   
   
   private void insertReferenceMark (XTextCursor thisCursor, String uuidStr) {
       Object referenceMark = ooDocument.createInstance("com.sun.star.text.ReferenceMark");
       XNamed xRefMark = ooQueryInterface.XNamed(referenceMark);
       String refMarkName = OOoNumberingHelper.HEADING_REF_PREFIX + uuidStr;
       xRefMark.setName(refMarkName);
       XTextContent xContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, xRefMark);
       try {
       thisCursor.getText().insertTextContent(thisCursor, xContent, true);
       } catch (com.sun.star.lang.IllegalArgumentException ex) {
           log.error("insertReferenceMark :" + ex.getMessage()); 
       }
   }

   
   private void updateSectionNumberingMetadata(XTextSection childSection, String theNumber){
         HashMap<String,String> sectionMeta = new HashMap<String,String>();
         sectionMeta.put(OOoNumberingHelper.numberingMetadata.get("APPLIED_NUMBER"), theNumber);
         sectionMeta.put(OOoNumberingHelper.numberingMetadata.get("NUMBERING_SCHEME"), this.getSelectedNumberingScheme().schemeName);
         sectionMeta.put(OOoNumberingHelper.numberingMetadata.get("PARENT_PREFIX_NUMBER"), "");
         ooDocument.setSectionMetadataAttributes(childSection, sectionMeta);
   }
   
    //method to get heading from section with selected sectionType
     ///variable sectionName added below for compilation success
    /*
     *
     *  1) initialize numbering scheme generator
     *  2) enumerate sections matching sectionType attribute
     *      2.1) for each section enumerate section content
     *          call enumerateSectionContent()
     *  3
     *
     */
    
    private void matchHeadingsInTypedSections() {
   //  private void getHeadingInSection( ) {
        try {
            String prevParent="";
           //set member variable that stores current numbering scheme
            //and then generate sequence.. with the upper range set to number of matched sections
                initializeNumberingSchemeGenerator((long)1, (long) sectionTypeMatchedSections.size() );
            //check if parent prefix was selected
            
            /*iterate through the sectionTypeMatchedSections and look for heading in section*/
            Iterator<String> typedMatchSectionItr = sectionTypeMatchedSections.iterator();
            while(typedMatchSectionItr.hasNext()){

                String sectionName = typedMatchSectionItr.next();
                Object sectionObject = ooDocument.getTextSections().getByName(sectionName);
                /*get the XTextSection object of the matching section*/
                XTextSection theSection = ooQueryInterface.XTextSection(sectionObject);
                /*get the parent of the matching section*/
                 XTextSection theSectionsParent = theSection.getParentSection();
                /*get the anchor of the matching section*/
                XTextRange range = theSection.getAnchor();
                /*get the enumeration object of the section */
                log.debug("matchHeadinsinTypedSection: enumerating section content for :" + theSection + ", prevParent = " + prevParent);
                enumerateSectionContent (range, theSection, prevParent);
                 /*set prevparent to the name of the previous parent section */
                prevParent = ooQueryInterface.XNamed(theSectionsParent).getName();
            }
        } catch (Exception ex) {
            log.error("matchHeadingsInTypedSections : " + ex.getMessage());
            log.error("matchHeadingsInTypedSections : " + CommonExceptionUtils.getStackTrace(ex));
        }    
    }
   

/*
 *section1
 *  section1.1
 *  section1.2
 *  section1.3
 *section2
 *  section2.1
 *  section2.2
 *
 *the above sections ... section1 and section will be numbered 1 & 2
 *section1.1, section1.2 and section1.3 will be numbered serially
 */
    /*
    private void getHeadingInMatchingSections() throws NoSuchElementException, WrappedTargetException, UnknownPropertyException, com.sun.star.lang.IllegalArgumentException {
        String prevParent="";
        int parentPrefix=0;;
        ///iterate through the sectionTypeMatchedSections and look for heading in section
        Iterator<String> typedMatchSectionItr = sectionTypeMatchedSections.iterator();
        

        //set member variable that stores current numbering scheme
        //and then generate sequence.. with the upper range set to number of matched sections
        initializeNumberingSchemeGenerator((long)1, (long) sectionTypeMatchedSections.size() );
   
        
        while(typedMatchSectionItr.hasNext()){
            String sectionName = typedMatchSectionItr.next();
            Object sectionObject = ooDocument.getTextSections().getByName(sectionName);
             XTextSection theSection = ooQueryInterface.XTextSection(sectionObject);
            XTextSection theSectionsParent = theSection.getParentSection();
            XTextRange range = theSection.getAnchor();
            enumerateSectionContent (range, theSection, prevParent);
            prevParent = ooQueryInterface.XNamed(theSectionsParent).getName();
        }
    }
    */
            
            
    private void initializeNumberingSchemeGenerator(long startRange, long endRange) {
        m_selectedNumberingScheme = createSchemeFromSelection();
        m_selectedNumberingScheme.setRange(new NumberRange(startRange, endRange));
        m_selectedNumberingScheme.generateSequence();
        m_selectedNumberingScheme.sequence_initIterator();
    }
    /*
     * 1) within the section look for paragraphs
     *  1.1) enumerate the paragrap
     *      enumerateParagraphInSectionContent
     *
     *
     */
    private String enumerateSectionContent (XTextRange sectionRange, XTextSection theSection, String prevParent )  {
            try {
                    XEnumerationAccess enumAcc  = (XEnumerationAccess) UnoRuntime.queryInterface(XEnumerationAccess.class, sectionRange);
                    XEnumeration xEnum = enumAcc.createEnumeration();
                    /*enumerate the elements in the section */
                    while (xEnum.hasMoreElements()) {
                        /*get the next enumerated element*/
                        Object elem = xEnum.nextElement();
                        /*query the matching element for its service info */
                        XServiceInfo xInfo = (XServiceInfo)UnoRuntime.queryInterface(XServiceInfo.class, elem);
                        /*if paragraph */
                        boolean breakFromLoop = false;
                        //enumerate the paragraph to get the heading
                        if(xInfo.supportsService("com.sun.star.text.Paragraph")){
                            //call paragraph enumerator
                            breakFromLoop = enumerateParagraphInSectionContent(xInfo, elem, theSection, prevParent);
                        } /*for the future ... else if ("com.sun.star.text.TextTable*/
                        if (breakFromLoop)
                            break;
                        //
                        //prevParent=(String)xParentSecName.getName();
                        //break;
                    }
            } catch(WrappedTargetException ex) {
                log.error("enumerateSectionContent : " +  ex.getMessage()); 
            } finally {
            return new String("");
            }
    }
   
    private boolean m_bFoundHeading = false;
    private boolean enumerateParagraphInSectionContent(XServiceInfo xInfo, Object elemParagraph, XTextSection theSection, String previousParent) {
               //we want to match only the first heading
                boolean bMatched = false;
               // m_bFoundHeading = false;
                try {
                    /*get the properties of the paragraph */
                    XPropertySet objProps = ooQueryInterface.XPropertySet(xInfo);
                    short nLevel = -1;
                    /*get the paragraphs numbering level */
                    nLevel = com.sun.star.uno.AnyConverter.toShort(objProps.getPropertyValue("ParaChapterNumberingLevel"));
                    /*check if the paragraph is a heading type nLevel >= 0 */
                    if(nLevel >= 0) {
                            //first heading has been matched
                            bMatched = m_bFoundHeading = true;
                            //get the content object we want to enumerate
                            XTextContent xContent = ooDocument.getTextContent(elemParagraph);
                            enumerateHeadingInParagraph(xContent, theSection, previousParent);
                    }
                } catch (UnknownPropertyException ex) {
                    log.error("enumerateParagraphInSectionContent: " +  ex.getMessage()); 
                } finally {
                return bMatched;
                }
      }

   private String enumerateHeadingInParagraph(XTextContent xContent, XTextSection theSection, String previousParent) {
       // get the current section name 
       int parentPrefix = 0; int headCount = 0;
       String sectionName = ooQueryInterface.XNamed(theSection).getName() ;
       // get the heading text of the matching heading 
        XTextRange aTextRange =   xContent.getAnchor();
        String strHeading = aTextRange.getString();
         log.debug("getHeadingInSection: heading found " + strHeading);
         // get the parent section of the section containing the heading 
         XNamed xParentSecName= ooQueryInterface.XNamed(theSection.getParentSection());
         String currentParent=(String)xParentSecName.getName();
         log.debug("getHeadingInSection" + currentParent);
         // check if the currentParent of the seciton is equal to the previous matching parent 
         // if they are not equal we need to restart numbering
         // else we continue numbering
         if(!currentParent.equalsIgnoreCase(previousParent)){
            restartNumbering(aTextRange, theSection, currentParent);
         } else {
            continueNumbering(aTextRange, theSection, currentParent); 
         }
             
         return new String("");
   }

   private void restartNumbering(XTextRange aRange, XTextSection theCurrentSection, String parentSection){
            //get the current numbering
            //restart numbering, by resetting the iterator
            this.m_selectedNumberingScheme.sequence_initIterator();
            //get the next number in the sequence
            String theNumber = this.m_selectedNumberingScheme.sequence_next();
            String parentPrefix = "";
            //if number has parent prefix
            if (this.m_useParentPrefix) {
                //get parent prefix
                //attache the parent prefix to the number.
                  parentPrefix =   getParentPrefix(theCurrentSection, parentSection);
            }
            // we want insert  number + space before heading
            // and set a reference mark over the number
             /////COMMENTED TEMPORARILAY insertNumberForHeading(aRange, theNumber, parentPrefix, theCurrentSection);
          //   insertAppliedNumberToMetadata(matchedSectionElem,headCount);
   }
  
   private void continueNumbering(XTextRange aRange, XTextSection theCurrentSection, String parentSection ) {
            String theNumber = this.m_selectedNumberingScheme.sequence_next();
             // if currentParent is "root" use 1 as the starting point for numbering
            // we want insert  number + space before heading
            // and set a reference mark over the number
            String parentPrefix ="";
             if (this.m_useParentPrefix) {
                //get parent prefix
                //attache the parent prefix to the number.
                  parentPrefix =   getParentPrefix(theCurrentSection, parentSection);
            }
             /////COMMEnTED TEMPORARILY insertNumberForHeading(aRange, theNumber, parentPrefix, theCurrentSection);
   }

   private String getParentPrefix ( XTextSection theCurrentSection, String parentSectionName) {
        //get the parent
        //get the number set in the parent.
    return OOoNumberingHelper.getSectionAppliedNumber(ooDocument, parentSectionName);
   }
   
   /*******
    *
    **** OOBasic Unit test for the below function *****
    *
    *
    Sub Main
  Dim oSel: oSel =  thisComponent.getCurrentSelection().getByIndex(0)
  Dim oCur: oCur = oSel.getText().createTextCursorByRange(oSel.getText().getStart())
  oCur.getText().insertString(oSel.getText().getStart(), "IV ", false)

       oCur.goLeft(1, false)
       oCur.goLeft(2, true)
       insertRef(oCur, "myNumRef")

       oCur.goRight(3, false)
       oCur.gotoEnd(true)
       insertRef(oCur, "myHeadRef")

End Sub

Sub insertRef (oCur, nameRef )
	Dim refMark
	Set refMark = thisComponent.createInstance("com.sun.star.text.ReferenceMark")
	refMark.setName(nameRef)
	oCur.getText().insertTextContent(oCur,refMark, true)
end Sub
    ******/
   
   /*
   private void insertField (XTextRange range, String theNumber, String fieldname) {
        Object refField = ooDocument.createInstance("com.sun.star.text.TextField.Input");
        XPropertySet propSet = ooQueryInterface.XPropertySet(refField);
        try {
            propSet.setPropertyValue("Hint", fieldname );
            propSet.setPropertyValue("Content", theNumber);
            //insert the field into the document
            XTextContent fieldContent = ooQueryInterface.XTextContent(refField);
            range.getText().insertTextContent(range, (XTextContent) fieldContent , true);
            
        } catch (PropertyVetoException ex) {
            log.error("ïnsertField :( " +ex.getClass().getName() + ")"+  ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error("ïnsertField :( " +ex.getClass().getName() + ")"+  ex.getMessage());
        } catch (UnknownPropertyException ex) {
            log.error("ïnsertField :( " +ex.getClass().getName() + ")"+  ex.getMessage());
        } catch (com.sun.star.lang.IllegalArgumentException ex) {
            log.error("ïnsertField :( " +ex.getClass().getName() + ")"+  ex.getMessage());
        }
   }
    */
   
   /*
    * 
    
    insertField(oCur.getStart(), "myFieldRef")
      oCur.goLeft(0,false)
      oCur.getText().insertString(oCur, " ", true)
      oCur.goLeft(0, false)
      oCur.goLeft(1, true)
      insertRef(oCur, "myNumRef")
      oCur.goRight(2, false)
      oCur.gotoEnd(true)
    insertRef(oCur, "myHeadRef")
    */
   /*
   private void insertNumberForHeading(XTextRange aRange, String theNumber, String parentPrefix, XTextSection theCurrentSection) {
      //get the text object of the heading range  
       XText xRangeText =    aRange.getText();
       //get the heading string
       String strHeading   =  aRange.getString();
       //String theNumberPlusSpace = theNumber+NUMBER_SPACE;
       String uuidStr = BungeniUUID.getStringUUID();
       //create a cursor to walk the heading
       XTextCursor headingCur = ooDocument.getTextDocument().getText().createTextCursor();
       //map the cursor to the heading range
       headingCur.gotoRange(aRange, false);
       if (this.m_useParentPrefix)  {
            insertField(headingCur.getStart(), parentPrefix + PARENT_PREFIX_SEPARATOR + theNumber, "numField_"+uuidStr);
       } else {
            insertField(headingCur.getStart(), theNumber, "numField_"+uuidStr);
       }
       headingCur.gotoRange(headingCur.getStart(), false);
       //remmed headingCur.goRight((short)1, false);
       //headingCur.goLeft((short)0, false);
       headingCur.getText().insertString(headingCur, NUMBER_SPACE, true);
       headingCur.goLeft((short) 0, false);
       headingCur.goLeft((short) 1, true);
       createReferenceMarkOverCursor("numRef_"+uuidStr , headingCur);
       headingCur.goRight((short) 2, false);
       headingCur.gotoEnd(true);
       createReferenceMarkOverCursor("headRef_"+uuidStr , headingCur);
       updateSectionNumberingMetadata(ooQueryInterface.XNamed(theCurrentSection).getName(),  theNumber, parentPrefix);
  }
  */

   
   private void createReferenceMarkOverCursor (String refName, XTextCursor thisCursor) {
       Object referenceMark = ooDocument.createInstance("com.sun.star.text.ReferenceMark");
       XNamed xRefMark = ooQueryInterface.XNamed(referenceMark);
       xRefMark.setName(refName);
       XTextContent xContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, xRefMark);
       try {
       thisCursor.getText().insertTextContent(thisCursor, xContent, true);
       } catch (com.sun.star.lang.IllegalArgumentException ex) {
           log.error("createReferenceMarkOverCursor :" + ex.getMessage()); 
       }
   }
   

   private void insertParentPrefix(String sectionElement, int parentPrefix){
        String strParentPrefix="" + parentPrefix + "";
        //clear the metadata map
        HashMap<String,String> metadata = new HashMap<String,String>();
        //insert key=>value attribute into metadata map
        metadata.put("ParentPrefix",strParentPrefix);
        System.out.println("insertParentPrefix function " + metadata + " to " + sectionElement.toString());
        //insert the applied number into the metadata
        //ooDocument.setSectionMetadataAttributes(sectionElement.toString(),metadata);
        
   }
   
    /* private void getHeadingInSectionOnRenumbering() {
        Iterator refIterator = refMarksForHeading.iterator();
        String prevParent="";
        int parentPrefix=0;;
        //iterate through the sectionTypeMatchedSections and look for heading in section
       Iterator typedMatchSectionItr = sectionTypeMatchedSections.iterator();
       while(typedMatchSectionItr.hasNext()){
           Object refMark=refIterator.next();
            Object matchedSectionElem=typedMatchSectionItr.next();
            
            try{
               
            Object sectionName = ooDocument.getTextSections().getByName(matchedSectionElem.toString());
            XTextSection theSection = ooQueryInterface.XTextSection(sectionName);
            XTextRange range = theSection.getAnchor();
            
            XEnumerationAccess enumAcc  = (XEnumerationAccess) UnoRuntime.queryInterface(XEnumerationAccess.class, range);
            XEnumeration xEnum = enumAcc.createEnumeration();
           
           
            while (xEnum.hasMoreElements()) {
                Object elem = xEnum.nextElement();
                XServiceInfo xInfo = (XServiceInfo)UnoRuntime.queryInterface(XServiceInfo.class, elem);
                if(xInfo.supportsService("com.sun.star.text.Paragraph")){
                   
                    XPropertySet objProps = ooQueryInterface.XPropertySet(xInfo);
                    
                     short nLevel = -1;
                     nLevel = com.sun.star.uno.AnyConverter.toShort(objProps.getPropertyValue("ParaChapterNumberingLevel"));
                     if(nLevel>=0){
                        XTextContent xContent = ooDocument.getTextContent(elem);
                        XTextRange aTextRange =   xContent.getAnchor();
                        String strHeading = aTextRange.getString();
                                              
                       
                         log.debug("getHeading: heading found " + strHeading);
                          //insert number here
                         XNamed xParentSecName= ooQueryInterface.XNamed(theSection.getParentSection());
                         String currentParent=(String)xParentSecName.getName();
                       
                         System.out.println("currentParent " + currentParent);
                         
                       
                         if(!currentParent.equalsIgnoreCase(prevParent)){
                             //restart numbering here
                             headCount=1;
                             insertNumberOnRenumbering(aTextRange, headCount,elem,refMark);
                            
                         }else{
                             //continue numbering
                            headCount++;
                            insertNumberOnRenumbering(aTextRange, headCount,elem,refMark);                 
                          
                            
                         }
                         
                        prevParent=(String)xParentSecName.getName();
                                              
                      
                      
                        break;
                        
                         
                      }
                }
                
            }
           
             
        
            }catch (NoSuchElementException ex) {
                log.error(ex.getClass().getName() + " - " + ex.getMessage());
                log.error(ex.getClass().getName() + " - " + CommonExceptionUtils.getStackTrace(ex));
            } catch (WrappedTargetException ex) {
                log.error(ex.getClass().getName() + " - " + ex.getMessage());
                log.error(ex.getClass().getName() + " - " + CommonExceptionUtils.getStackTrace(ex));
            } catch(UnknownPropertyException ex){
                log.error(ex.getClass().getName() + " - " + ex.getMessage());
                log.error(ex.getClass().getName() + " - " + CommonExceptionUtils.getStackTrace(ex));
            }catch(com.sun.star.lang.IllegalArgumentException ex){
                log.error(ex.getClass().getName() + " - " + ex.getMessage());
                log.error(ex.getClass().getName() + " - " + CommonExceptionUtils.getStackTrace(ex));
            }
            
       }
       
         
        
        
    }
    
    */
    /*
    private void findAndReplace(){
        XReplaceable xReplaceable = (XReplaceable) UnoRuntime.queryInterface(XReplaceable.class, ooDocument.getTextDocument()); 
        XReplaceDescriptor xRepDesc = xReplaceable.createReplaceDescriptor(); 
       
        xRepDesc.setSearchString("iii)");
        xRepDesc.setReplaceString(" ");
        
        
        long nResult = xReplaceable.replaceAll(xRepDesc); 
      
    }*/
   /*
    private void insertCrossReference(String sourceName){
      int i=0;
    
       try { 
       
         XTextDocument xDoc = ooDocument.getTextDocument();
            
         XTextViewCursor xViewCursor=ooDocument.getViewCursor();
         Object oRefField=ooDocument.createInstance("com.sun.star.text.TextField.GetReference");
         
         XReferenceMarksSupplier xRefSupplier = (XReferenceMarksSupplier) UnoRuntime.queryInterface(
             XReferenceMarksSupplier.class, xDoc);
         
         // Get an XNameAccess which refers to all inserted reference marks
         XNameAccess xMarks = (XNameAccess) UnoRuntime.queryInterface(XNameAccess.class,
             xRefSupplier.getReferenceMarks());
         
        String[] aNames = xMarks.getElementNames();
        XPropertySet oFieldSet = ooQueryInterface.XPropertySet(oRefField);
     
           
            
        
             oFieldSet.setPropertyValue("ReferenceFieldSource",com.sun.star.text.ReferenceFieldSource.REFERENCE_MARK); 
            
         oFieldSet.setPropertyValue("SourceName", sourceName);
             oFieldSet.setPropertyValue("ReferenceFieldPart",com.sun.star.text.ReferenceFieldPart.TEXT);


             XTextContent xRefContent = (XTextContent) UnoRuntime.queryInterface(
                     XTextContent.class, oFieldSet);
             
              xDoc.getText().insertTextContent(xViewCursor , xRefContent, true);
               xDoc.getText().insertString(xViewCursor , " , ", false);
            
            
              XRefreshable xRefresh = (XRefreshable) UnoRuntime.queryInterface(
                 XRefreshable.class, xDoc);
            xRefresh.refresh();   
            
         
          
        
          } catch (UnknownPropertyException ex) {
                ex.printStackTrace();
            } catch (WrappedTargetException ex) {
                ex.printStackTrace();
            } catch (PropertyVetoException ex) {
                ex.printStackTrace();
            } catch (com.sun.star.lang.IllegalArgumentException ex) {
                ex.printStackTrace();
            } 
         
        
   
    }
    */
    /*
    
    private void packReferences(){
           int i=0;
     XTextDocument xDoc = ooDocument.getTextDocument();
         XTextViewCursor xViewCursor=ooDocument.getViewCursor();
         Object oRefField=ooDocument.createInstance("com.sun.star.text.TextField.GetReference");
         
         XReferenceMarksSupplier xRefSupplier = (XReferenceMarksSupplier) UnoRuntime.queryInterface(
             XReferenceMarksSupplier.class, xDoc);
         
         // Get an XNameAccess which refers to all inserted reference marks
         XNameAccess xMarks = (XNameAccess) UnoRuntime.queryInterface(XNameAccess.class,
             xRefSupplier.getReferenceMarks());
         
        String[] aNames = xMarks.getElementNames();
        XPropertySet oFieldSet = ooQueryInterface.XPropertySet(oRefField);
       
           
          while(i<aNames.length){
                docReferences.add(aNames[i].toString());
             i++;
            }
          
        
         
    }
    */
    
    
  

    class sectionHeadingReferenceMarks {
        public String sectionName = "";
        public Integer nOrder = 0;
        public Object containedHeading = null;
        public ArrayList<String> refMarks = new ArrayList<String>(0);
      
        public sectionHeadingReferenceMarks() {
            sectionName = "";
            nOrder = 0;
            refMarks = new ArrayList<String>(0);
        }
        
        public sectionHeadingReferenceMarks(String sectionName, int order , Object heading) {
            this.sectionName = sectionName;
            this.nOrder = order;
            this.refMarks = new ArrayList<String>(0);
            this.containedHeading = heading;
        }
        
        
        public String toString(){
            return sectionName;
        }
    }
    
    /*private void crossRef(){
           String sectionHierarchy = "";
           //clear the refMarks Map
           refMarksMap.clear();
           String strSection="";
           //get the full hierarchy of the section selected by the user
            sectionHierarchy = currentSectionNameHierarchy(selectedNodeName);
            if (sectionHierarchy.trim().length() == 0){
               
                System.out.println("Cursor not in section");
          } else{
                 System.out.println("selectSection " + sectionHierarchy );
           }
           ArrayList<String> arrSectionTree = new ArrayList<String>();
           //split the section hierarchy into an array
          String[] sectionHeads=sectionHierarchy.split(">");
          for(int i=0;i<sectionHeads.length;i++){
              arrSectionTree.add(sectionHeads[i]);
          }
           //ArrayList<String> arrSectionTree = new ArrayList(sectionHierarchy.split(">"));
          
           arrSectionTree.remove(new String("root"));
           Collections.reverse(arrSectionTree);
           System.out.println("section hierarchy = " + arrSectionTree);
          //we have to reverse the array in order to have Child,Parent
           //String [] refs=(String[]) this.reverse(sectionTree);
            //String [] refs= sectionTree;
           
           //get the section hierarchy and populate a treemap with the order of the sections,
            //and container for the reference marks
            for(int i=0;i<arrSectionTree.size();i++){
                    //refObj.sectionName=refs[i].toString();
                    String sectionName = arrSectionTree.get(i).toString();
                    //get headings contained in section
                Object sectHeading= getNumberedHeadingsInsertCrossRef(sectionName);
                refMarksMap.put(sectionName, new sectionHeadingReferenceMarks(sectionName, i , sectHeading));
           }
           

           //now we get the ReferenceMark objects in each heading for each section
           
           Iterator<String> sectionIter = refMarksMap.keySet().iterator();
           while (sectionIter.hasNext()){
               String sectionKey = sectionIter.next();
               //add not null check for heading
               Object elem = refMarksMap.get(sectionKey).containedHeading;
               XTextRange xRange = ooQueryInterface.XTextRange(elem);
               System.out.println("portion " + xRange.getString());
               ArrayList<String> refMarksInHeading = getReferenceMarksOnCross(elem);
               refMarksMap.get(sectionKey).refMarks = refMarksInHeading;
               
               //iterate through the reference marks and insert into the document
               Iterator<String> refMarksIterator = refMarksInHeading.iterator();
               while(refMarksIterator.hasNext()){
                   Object refMark=refMarksIterator.next();
                    System.out.println("refMarksIterator " + refMark);
                    insertCrossReference(refMark.toString());
               }
               
           }
           
           
         
           
         
    }
    */
     
   
    
private Object getHeadingFromMatchedSection(Object matchedSectionElem){
        
           Object objHeading = null;
            
           try{
               
                Object sectionName = ooDocument.getTextSections().getByName(matchedSectionElem.toString());
                XTextSection theSection = ooQueryInterface.XTextSection(sectionName);
                XTextRange range = theSection.getAnchor();

                XEnumerationAccess enumAcc  = (XEnumerationAccess) UnoRuntime.queryInterface(XEnumerationAccess.class, range);
                XEnumeration xEnum = enumAcc.createEnumeration();


              while (xEnum.hasMoreElements()) {
                  Object elem = xEnum.nextElement();
                   XServiceInfo xInfo = (XServiceInfo)UnoRuntime.queryInterface(XServiceInfo.class, elem);
                   if(xInfo.supportsService("com.sun.star.text.Paragraph")){
                        XPropertySet objProps = ooQueryInterface.XPropertySet(xInfo);
                    
                         short nLevel = -1;
                         nLevel = com.sun.star.uno.AnyConverter.toShort(objProps.getPropertyValue("ParaChapterNumberingLevel"));
                           if(nLevel>=0){
                            //XTextContent xContent = ooDocument.getTextContent(elem);
                            //XTextRange aTextRange =   xContent.getAnchor();
                           // String strHeading = aTextRange.getString();
                            
                          
                          //  docListReferences.add(strHeading);
                         
                           // removeNumberFromHeading2(aTextRange, elem);
                             objHeading=elem;
                            break;
                         }
                   
                   }

                }
        
            }catch (NoSuchElementException ex) {
                log.error(ex.getClass().getName() + " - " + ex.getMessage());
                log.error(ex.getClass().getName() + " - " + CommonExceptionUtils.getStackTrace(ex));
            } catch (WrappedTargetException ex) {
                log.error(ex.getClass().getName() + " - " + ex.getMessage());
                log.error(ex.getClass().getName() + " - " + CommonExceptionUtils.getStackTrace(ex));
            }catch(UnknownPropertyException ex){
                log.error(ex.getClass().getName() + " - " + ex.getMessage());
                log.error(ex.getClass().getName() + " - " + CommonExceptionUtils.getStackTrace(ex));
            }catch(com.sun.star.lang.IllegalArgumentException ex){
                log.error(ex.getClass().getName() + " - " + ex.getMessage());
                log.error(ex.getClass().getName() + " - " + CommonExceptionUtils.getStackTrace(ex));
            }finally{
                 return objHeading;
            }
            
    
    }
    
    private sectionNumbererPanel self() {
            return this;
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
       
        //copied from SelectSection
        
        public String currentSectionNameHierarchy(String sectionName) {
            XTextSection loXTextSection;
            XTextViewCursor loXTextCursor;
            XPropertySet loXPropertySet;
            String lstrSectionName = "";
            XTextSection currentSection = ooDocument.getSection(sectionName);
            lstrSectionName = getSectionHierarchy(currentSection);
        
         
            return lstrSectionName; 
        }


    
/*
    private void initTreeSectionsArray() {
        try {
            if (!ooDocument.isXComponentValid()) return;
            
            treeSectionStructure.removeAll();
            if (!ooDocument.getTextSections().hasByName("root")) {
                log.debug("no root section found");
                return;
            }
            Object rootSection = ooDocument.getTextSections().getByName("root");
            XTextSection theSection = ooQueryInterface.XTextSection(rootSection);
            if (theSection.getChildSections().length == 0) {
                //root is empty and has no children. 
                //set empty status 
                this.emptyRootNode = true;
            }
            sectionRootNode = new DefaultMutableTreeNode(new String("root"));
            
            recurseSections (theSection, sectionRootNode);
            
            //-tree-deprecated--CommonTreeFunctions.expandAll(treeSectionStructure, true);
            CommonTreeFunctions.expandAll(treeSectionStructure);
            
        } catch (NoSuchElementException ex) {
            log.error(ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error(ex.getMessage());
        }
    }
    
    
    private void recurseSections (XTextSection theSection, DefaultMutableTreeNode node ) {
        try {
        //recurse children
        XTextSection[] sections = theSection.getChildSections();
        if (sections != null ) {
            if (sections.length > 0 ) {
                //start from last index and go to first
                for (int nSection = sections.length - 1 ; nSection >=0 ; nSection--) {
                    log.debug ("section name = "+sections[nSection] );
                    //get the name for the section and add it to the root node.
                    XPropertySet childSet = ooQueryInterface.XPropertySet(sections[nSection]);
                    String childSectionName = (String) childSet.getPropertyValue("LinkDisplayName");
                    //if (!childSectionName.trim().equals(theAction.action_naming_convention())) {
                     DefaultMutableTreeNode newNode = new DefaultMutableTreeNode(childSectionName);
                     node.add(newNode);
                     recurseSections (sections[nSection], newNode);
                   // }
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
     */
       
 
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    // <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    private void initComponents() {
        panelSectionTypes = new javax.swing.JScrollPane();
        listSectionTypes = new javax.swing.JList();
        jLabel1 = new javax.swing.JLabel();
        cboNumberingScheme = new javax.swing.JComboBox();
        checkbxUseParentPrefix = new javax.swing.JCheckBox();
        btnApplyNumberingScheme = new javax.swing.JButton();
        btnRenumberSections = new javax.swing.JButton();
        btnInsertCrossReference = new javax.swing.JButton();
        btnfixBrokenReferences = new javax.swing.JButton();
        jLabel2 = new javax.swing.JLabel();

        listSectionTypes.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        listSectionTypes.setSelectionMode(javax.swing.ListSelectionModel.SINGLE_SELECTION);
        panelSectionTypes.setViewportView(listSectionTypes);

        jLabel1.setText("Bungeni Section Types");

        cboNumberingScheme.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Base Numbering", "ROMAN", "ALPHA" }));
        cboNumberingScheme.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                cboNumberingSchemeActionPerformed(evt);
            }
        });

        checkbxUseParentPrefix.setText("Use Parent Prefix");
        checkbxUseParentPrefix.setBorder(javax.swing.BorderFactory.createEmptyBorder(0, 0, 0, 0));
        checkbxUseParentPrefix.setMargin(new java.awt.Insets(0, 0, 0, 0));

        btnApplyNumberingScheme.setText("Apply Numbering Scheme");
        btnApplyNumberingScheme.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnApplyNumberingSchemeActionPerformed(evt);
            }
        });

        btnRenumberSections.setText("Renumber Headings");
        btnRenumberSections.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnRenumberSectionsActionPerformed(evt);
            }
        });

        btnInsertCrossReference.setText("Insert Cross Reference");
        btnInsertCrossReference.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnInsertCrossReferenceActionPerformed(evt);
            }
        });

        btnfixBrokenReferences.setText("Fix Broken Reference");
        btnfixBrokenReferences.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnfixBrokenReferencesActionPerformed(evt);
            }
        });

        jLabel2.setText("Select a Numbering Scheme");

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(layout.createSequentialGroup()
                        .add(jLabel1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 215, Short.MAX_VALUE)
                        .addContainerGap())
                    .add(layout.createSequentialGroup()
                        .add(checkbxUseParentPrefix)
                        .addContainerGap(124, Short.MAX_VALUE))
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, layout.createSequentialGroup()
                        .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, btnInsertCrossReference, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 215, Short.MAX_VALUE)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, btnfixBrokenReferences, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 215, Short.MAX_VALUE)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, btnRenumberSections, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 215, Short.MAX_VALUE)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, btnApplyNumberingScheme, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 215, Short.MAX_VALUE)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, jLabel2, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 215, Short.MAX_VALUE)
                            .add(org.jdesktop.layout.GroupLayout.LEADING, cboNumberingScheme, 0, 215, Short.MAX_VALUE)
                            .add(panelSectionTypes, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 215, Short.MAX_VALUE))
                        .addContainerGap())))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .add(jLabel1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 15, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(panelSectionTypes, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 62, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jLabel2, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 14, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(5, 5, 5)
                .add(cboNumberingScheme, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(checkbxUseParentPrefix)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btnApplyNumberingScheme)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btnRenumberSections)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btnfixBrokenReferences)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btnInsertCrossReference)
                .addContainerGap(40, Short.MAX_VALUE))
        );
    }// </editor-fold>//GEN-END:initComponents

    private void btnfixBrokenReferencesActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnfixBrokenReferencesActionPerformed
// TODO add your handling code here:
        applyFixBrokenReferences();
    }//GEN-LAST:event_btnfixBrokenReferencesActionPerformed

    private void cboNumberingSchemeActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_cboNumberingSchemeActionPerformed
// TODO add your handling code here:
    }//GEN-LAST:event_cboNumberingSchemeActionPerformed

    private void btnInsertCrossReferenceActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnInsertCrossReferenceActionPerformed
// TODO add your handling code here:
       // crossRef();
        applyInsertCrossReferences();
    }//GEN-LAST:event_btnInsertCrossReferenceActionPerformed

    private void btnRenumberSectionsActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnRenumberSectionsActionPerformed
// TODO add your handling code here:
        applyRenumberingScheme();
    }//GEN-LAST:event_btnRenumberSectionsActionPerformed
    
    
    private void btnApplyNumberingSchemeActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnApplyNumberingSchemeActionPerformed
        //get section type selected for numbering 
        applyNumberingScheme();
    }//GEN-LAST:event_btnApplyNumberingSchemeActionPerformed

    
    public void initialize() {
        init();
    }

    public void refreshPanel() {
        //the timer does automatic refreshes....
    }
   
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnApplyNumberingScheme;
    private javax.swing.JButton btnInsertCrossReference;
    private javax.swing.JButton btnRenumberSections;
    private javax.swing.JButton btnfixBrokenReferences;
    private javax.swing.JComboBox cboNumberingScheme;
    private javax.swing.JCheckBox checkbxUseParentPrefix;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JList listSectionTypes;
    private javax.swing.JScrollPane panelSectionTypes;
    // End of variables declaration//GEN-END:variables

   
    
}
