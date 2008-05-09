/*
 * sectionNumbererPanel.java
 *
 * Created on March 27, 2008, 6:39 PM
 */

package org.numbering.dialogs;

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
import org.bungeni.numbering.impl.IGeneralNumberingScheme;
import org.bungeni.numbering.impl.NumberRange;
import org.bungeni.numbering.impl.NumberingSchemeFactory;

import org.bungeni.ooo.BungenioOoHelper;
import org.bungeni.ooo.OOComponentHelper;
import org.apache.log4j.Logger;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.ooo.ooUserDefinedAttributes;
import org.bungeni.utils.BungeniUUID;
import org.bungeni.ooo.utils.CommonExceptionUtils;
import org.bungeni.utils.CommonTreeFunctions;
import org.bungeni.utils.MessageBox;


/**
 *
 * @author  undesa
 */
public class sectionNumbererPanel extends javax.swing.JPanel {
    private XComponentContext xContext;
    private OOComponentHelper ooDocument;
    private XComponent xComponent;
    private BungenioOoHelper openofficeObject;
   //  HashMap<String, String> sectionMetadataMap=new HashMap<String, String>();
   //HashMap<String, String> sectionTypeMetadataMap=new HashMap<String, String>();
    private static org.apache.log4j.Logger log = Logger.getLogger(sectionNumbererPanel.class.getName());
   
    private boolean m_useParentPrefix = false;
    
    //private HashMap<String,String> metadata = new HashMap();
    private ArrayList<String> sectionTypeMatchedSections = new ArrayList<String>();
    private ArrayList<String> docListReferences = new ArrayList<String>();
    private ArrayList<String> docReferences = new ArrayList<String>();
    private ArrayList<String> insertedNumbers = new ArrayList<String>();
    private ArrayList<String> sectionHierarchy = new ArrayList<String>();
    private int headCount=1;
    //DefaultListModel model=new DefaultListModel();
    private IGeneralNumberingScheme inumScheme;
    private String numParentPrefix="";
    private Set attributeSet=new HashSet();
    private Timer sectionNameTimer;
    private String currentSelectedSectionName = "";
    private String selectSection="";
   
    private DefaultMutableTreeNode sectionRootNode = null;
    private String m_selectedSection = "";
    private String m_selectedActionCommand = "";
    private boolean emptyRootNode = false;
    private boolean cancelClicked = false;
    private String[] m_validParentSections;
    private String selectedNodeName="";
     private JFrame parentFrame;
     private BungeniUUID bungeniUUID;
     private HashMap<String,String> arrPortions = new HashMap();
     
     TreeMap<String, sectionHeadingReferenceMarks> refMarksMap = new TreeMap<String, sectionHeadingReferenceMarks>();
     private ArrayList<Object> refMarksInHeadingMatched= new ArrayList<Object>(0);
     private ArrayList<Object> refMarksForHeading= new ArrayList<Object>(0);
   
    /** Creates new form sectionNumbererPanel */
    public sectionNumbererPanel() {
       
    }
    
    public sectionNumbererPanel(XComponentContext xContext){
        this.xContext=xContext;
        initComponents();
        init();
    }
    
    private void init(){
        oooInit();
        fetchSectionTypesAndInitTree();
        initSectionTypesListBox();
       // listSectionTypes.addListSelectionListener(new NumberingSchemeListener());
        //panelNumberingScheme.setVisible(false);
        /*init parent prefix checkbox */
        checkbxUseParentPrefix.setSelected(false);
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
        initSectionTree();
        initNumberingSchemesCombo();
        //the following is commented becuase its definitely not required !
        //findBrokenReferences();
    }
    
  
    private void oooInit(){
        openofficeObject = new org.bungeni.ooo.BungenioOoHelper(xContext);
        openofficeObject.initoOo();
        xComponent = openofficeObject.openDocument("file:///E:/projects/WorkingProjects/OfficeNumberingApp/testsection4.odt");
        ooDocument = new OOComponentHelper(xComponent, xContext);
    }
    
    class numberingSchemeSelection extends Object {
        String schemeName;
        String schemeDesc;
        String schemeClass;
        public String toString(){
            return schemeName;
        }
    }
    
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
    
    private void fetchSectionTypesAndInitTree(){
        try{
            if (!ooDocument.getTextSections().hasByName("root")) {
                System.out.println("no root section found");
                return;
            }
            Object rootSection = ooDocument.getTextSections().getByName("root");
            XTextSection theSection = ooQueryInterface.XTextSection(rootSection);
            //create the tree here
             sectionRootNode = new DefaultMutableTreeNode(new String("root"));
             CommonTreeFunctions.expandAll(treeSectionStructure);
             recurseSectionTypesAndInitTree (theSection,sectionRootNode);
         }catch (NoSuchElementException ex) {
            log.error(ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error(ex.getMessage());
        }
        
        
    }
    
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
    
    private void initSectionTypesListBox(){
         DefaultListModel listModel = new DefaultListModel();
         Iterator attributeSetIterator = attributeSet.iterator();
              while (attributeSetIterator.hasNext()) {
                 Object element = attributeSetIterator.next();
                 listModel.addElement(element);
            }
        this.listSectionTypes.setModel(listModel);
    }
    
     private void findSectionsMatchingSectionType(String sectionType ){
         try{
           //change this check later to get the root section from the editor properties
            if (!ooDocument.getTextSections().hasByName("root")) {
                 log.info("readSections by type "+ sectionType + " no root section found, returning");
                return;
            }
            //start from the root section
            Object rootSection = ooDocument.getTextSections().getByName("root");
            XTextSection theSection = ooQueryInterface.XTextSection(rootSection);
            /*clear the arraylist that holds the list of sections matching the type*/
            this.sectionTypeMatchedSections.clear();
            /*recurse through section hierarchy for sections of type sectionType*/
            recurseSectionsForSectionType(theSection,sectionType);
           /*now the arraylist for sectionTypematchdSections should have matching sections */
         }catch (NoSuchElementException ex) {
            log.error(ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error(ex.getMessage());
        }
   }
    
   private void recurseSectionsForSectionType(XTextSection theSection, String sectionType){
            /*get all child sections of the incoming section */
            XTextSection[] sections = theSection.getChildSections();
            if (sections != null ) {
                if (sections.length > 0 ) {
                    //start from last index and go to first
                    for (int nSection = sections.length - 1 ; nSection >=0 ; nSection--) {
                        /*get the name of the child section*/
                         XNamed xSecName = ooQueryInterface.XNamed(sections[nSection]);
                         String childSectionName = (String) xSecName.getName();
                         /*get the section metadata*/
                         HashMap<String,String> sectionMetadataMap=ooDocument.getSectionMetadataAttributes(childSectionName);
                         /*check if the section has a sectionType property*/
                         if (sectionMetadataMap.containsKey("BungeniSectionType") ) {
                            /*get the sectionType of the current section*/
                            String matchedSectionType= sectionMetadataMap.get("BungeniSectionType");
                            /*if section type of the section matches the section type we are looking for*/
                            if(matchedSectionType.equalsIgnoreCase(sectionType)){
                                /*add the child section to the list of matching sections array list*/
                              sectionTypeMatchedSections.add(childSectionName);
                            }
                        }
                        log.debug("recurseSectionsForSectionType: recursive call: " + childSectionName);
                        recurseSectionsForSectionType(sections[nSection],sectionType);
                     } /*end of for() */ 
                }  /*end of if (sections.length > 0)*/
            }  /*end of if (sections != null)*/
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
    

   private void insertAppliedNumberToMetadata(String sectionElement, int appliedNumber){
        String strAppliedNumber="" + appliedNumber + "";
        //clear the metadata map
        HashMap<String,String> metadata = new HashMap<String,String>();
        //insert key=>value attribute into metadata map
        metadata.put("AppliedNumber",strAppliedNumber);
        System.out.println("insertAppliedNumberToMetadata function " + metadata + " to " + sectionElement.toString());
        //insert the applied number into the metadata
        ooDocument.setSectionMetadataAttributes(sectionElement.toString(),metadata);
        
   }
    

   
  
   private void findBrokenReferences(){
    
        String sourceName=null;
       try {
    //dim oDoc as object
    //oDoc=thisComponent
    XTextDocument xDoc = ooDocument.getTextDocument();
    //dim oRefMarks as object
    //oRefMarks=oDoc.Referencemarks
    XReferenceMarksSupplier xRefSupplier = (XReferenceMarksSupplier) UnoRuntime.queryInterface(
                     XReferenceMarksSupplier.class, xDoc);
    XNameAccess xRefMarks = xRefSupplier.getReferenceMarks();
   
    String[] refs=xRefMarks.getElementNames();
    for(int i=0;i<refs.length;i++){
        System.out.println(refs[i]);
    }
    
    /*
    nCount = 0
    bCancel = false
    oFieldEnum = oDoc.textFields.createEnumeration
    */
    XEnumerationAccess xEnumFieldsAccess = ooDocument.getTextFields();
    XEnumeration xFields = xEnumFieldsAccess.createEnumeration();
    /*
    do while oFieldEnum.hasMoreElements
	oTextField = oFieldEnum.nextElement
    */
    int nCount = 0;
    while (xFields.hasMoreElements()) {
        Object oField = xFields.nextElement();
        
        /*
      	If oTextField.supportsService("com.sun.star.text.TextField.GetReference") then
        */
        
        XServiceInfo xService = ooQueryInterface.XServiceInfo(oField);
       if (xService.supportsService("com.sun.star.text.TextField.GetReference")){
              
               XTextField xField =  (XTextField) UnoRuntime.queryInterface(XTextField.class, oField ) ;
               XPropertySet xFieldProperties = ooQueryInterface.XPropertySet(xField);
               XPropertySetInfo xFieldPropsInfo  = xFieldProperties.getPropertySetInfo();

                /*
		if oTextField.ReferenceFieldSource = com.sun.star.text.ReferenceFieldSource.REFERENCE_MARK then
			if not oRefMarks.hasByName(oTextField.Sourcename) then
				nCount = nCount + 1
			
			end if
		elseif oTextField.ReferenceFieldSource = com.sun.star.text.ReferenceFieldSource.BOOKMARK then
			if not oBookMarks.hasByName(oTextField.Sourcename) then
				nCount = nCount + 1
			
			end if
		elseif oTextField.ReferenceFieldSource = com.sun.star.text.ReferenceFieldSource.SEQUENCE_FIELD then
		
		end if
                */
               
               short refSourceRefMark = AnyConverter.toShort(xFieldProperties.getPropertyValue("ReferenceFieldSource")); 
               sourceName = AnyConverter.toString(xFieldProperties.getPropertyValue("SourceName"));
               switch (refSourceRefMark) {
                   case com.sun.star.text.ReferenceFieldSource.REFERENCE_MARK :
                       if (!xRefMarks.hasByName(sourceName)) 
                           nCount++;
                          
                       break;
                   default:
                       break;
               }
       }
      
                
      }
   System.out.println("DEAD LINKS FOUND = " + nCount + " " + sourceName);
        
    } catch (Exception ex) {
        
    }
       
         
         
         
   }
    
    private void insertNumber(XTextRange aTextRange, int testCount, Object elem){
       
     
       String numberingScheme =cboNumberingScheme.getSelectedItem().toString();
       int numberingSchemeIndex=cboNumberingScheme.getSelectedIndex();
       System.out.println("numbering scheme selected " + numberingScheme);
       inumScheme =NumberingSchemeFactory.getNumberingScheme(numberingScheme);
       
       XText xRangeText=aTextRange.getText();
       String heading=aTextRange.getString();
       XTextCursor xTextCursor = xRangeText.createTextCursorByRange(aTextRange.getStart());
       xTextCursor.gotoRange(aTextRange.getEnd(), true);
       
      
       XTextContent xContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, xTextCursor);
       
       inumScheme.setRange (new NumberRange(testCount, testCount));
     
       if(!numParentPrefix.equals("")){
            inumScheme.setParentPrefix(numParentPrefix);
       }
       inumScheme.generateSequence();
       ArrayList<String> seq = inumScheme.getGeneratedSequence();
        Iterator<String> iter = seq.iterator();
        while (iter.hasNext()) {
           Object insertedNumber=(String)iter.next();
           String num=insertedNumber + ") ";
           int refLength=num.length();
            xRangeText.insertString(xTextCursor,num,false);
           // xRangeText.insertString(xTextCursor," ",false);
            //insertedNumbers.add(num);
       
            insertReferenceMarkOnNumber(aTextRange, elem, refLength);
          
        }
        
        
       
     
      
    }
    
private void insertNumberOnRenumbering(XTextRange aTextRange, int testCount, Object elem, Object refMark){
       
     
       String numberingScheme =cboNumberingScheme.getSelectedItem().toString();
       int numberingSchemeIndex=cboNumberingScheme.getSelectedIndex();
       System.out.println("numbering scheme selected " + numberingScheme);
       inumScheme =NumberingSchemeFactory.getNumberingScheme(numberingScheme);
       
       XText xRangeText=aTextRange.getText();
       String heading=aTextRange.getString();
       XTextCursor xTextCursor = xRangeText.createTextCursorByRange(aTextRange.getStart());
       xTextCursor.gotoRange(aTextRange.getEnd(), true);
       
      
       XTextContent xContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, xTextCursor);
       
       inumScheme.setRange (new NumberRange(testCount, testCount));
     
       if(!numParentPrefix.equals("")){
            inumScheme.setParentPrefix(numParentPrefix);
       }
       inumScheme.generateSequence();
       ArrayList<String> seq = inumScheme.getGeneratedSequence();
        Iterator<String> iter = seq.iterator();
        while (iter.hasNext()) {
           Object insertedNumber=(String)iter.next();
           String num=insertedNumber + ") ";
           Short numLength=(short)num.length();
           xRangeText.insertString(xTextCursor,num,false);
            //insertedNumbers.add(num);
           
           
       
            insertReferenceMarkOnReNumbering(aTextRange, elem, numLength,refMark);
          
        }
        
        
       
     
      
    }
    
    private ArrayList getNumberReferenceFromHeading(Object elem){
      ArrayList<Object> referenceMarkText = new ArrayList<Object>(0);
             
        XEnumerationAccess xRangeAccess = (XEnumerationAccess)UnoRuntime.queryInterface(com.sun.star.container.XEnumerationAccess.class,elem);
         XEnumeration portionEnum =  xRangeAccess.createEnumeration();
         while (portionEnum.hasMoreElements()){
             try{
                 Object textPortion =  portionEnum.nextElement();  
                  XServiceInfo xTextPortionService= ooDocument.getServiceInfo(textPortion);
                   if (xTextPortionService.supportsService( "com.sun.star.text.TextPortion")){
                      XPropertySet xTextPortionProps = (XPropertySet)UnoRuntime.queryInterface(XPropertySet.class, textPortion);
                      String textPortionType="";
                      
                        
                            textPortionType = AnyConverter.toString(xTextPortionProps.getPropertyValue("TextPortionType"));
                            if (textPortionType.equals("ReferenceMark")){
                                XPropertySet xPortionProps = ooQueryInterface.XPropertySet(textPortion);
                                Object oRefMark =  xPortionProps.getPropertyValue("ReferenceMark");
                                XNamed xRefMark= (XNamed) AnyConverter.toObject(new Type(XNamed.class), oRefMark);
                               // System.out.println("refmark " + xRefMark.getName());
                                if (!referenceMarkText.contains(xRefMark)) {
                                    if(xRefMark.getName().toString().startsWith("numRef_")){
                                        //referenceMarkNames.add(xRefMark.getName().toString());
                                        referenceMarkText.add(xRefMark);
                                        refMarksForHeading.add(xRefMark.getName().toString());
                                    }
                                    
                                }
                                
                                
                                
                          } 
                             
                     
                   }
                  
             }catch(NoSuchElementException ex){
                 log.error(ex.getMessage());
             }catch (WrappedTargetException ex) {
                log.error(ex.getMessage());
             }catch (com.sun.star.lang.IllegalArgumentException ex) {
                  log.error(ex.getMessage());
             }catch (UnknownPropertyException ex) {
                  log.error(ex.getMessage());
             }finally{
                
             }
             
             
         }   
         return referenceMarkText;
    }
    
    private void removeNumberFromHeading(XTextRange aTextRange, Object elem){
        Matcher m=null;
        XText xRangeText=aTextRange.getText();
       
        XEnumerationAccess xRangeAccess = (XEnumerationAccess)UnoRuntime.queryInterface(com.sun.star.container.XEnumerationAccess.class,elem);
         XEnumeration portionEnum =  xRangeAccess.createEnumeration();
         while (portionEnum.hasMoreElements()){
             try{
                 Object textPortion =  portionEnum.nextElement();  
                  XServiceInfo xTextPortionService= ooDocument.getServiceInfo(textPortion);
                   if (xTextPortionService.supportsService( "com.sun.star.text.TextPortion")){
                      XPropertySet xTextPortionProps = (XPropertySet)UnoRuntime.queryInterface(XPropertySet.class, textPortion);
                      String textPortionType="";
                      
                        
                            textPortionType = AnyConverter.toString(xTextPortionProps.getPropertyValue("TextPortionType"));
                            if (textPortionType.equals("ReferenceMark")){
                                String refHeading=aTextRange.getString();
                                String refHeadingCleared="";
                               XTextCursor xTextCursor = xRangeText.createTextCursorByRange(aTextRange.getStart());
                               
                               if(cboNumberingScheme.getSelectedItem().toString()=="Base Numbering"){
                                    //create a pattern for base numbering
                                   Pattern p = Pattern.compile("[0-9]+\\)");
                                   m = p.matcher(refHeading);
                               }else if(cboNumberingScheme.getSelectedItem().toString()=="ALPHA"){
                                   //create a patter for alphabet
                                   Pattern p = Pattern.compile("[A-Za-z]+\\)");
                                   m = p.matcher(refHeading);
                               }else if(cboNumberingScheme.getSelectedItem().toString()=="ROMAN"){
                                   //pattern for roman numerals
                                   Pattern p = Pattern.compile("[mdclxvi]+\\)");
                                   m = p.matcher(refHeading);
                               }
                              
                             //check if pattern is found
                               
                                 // MessageBox.OK("The selected scheme does not exist in the section");
                                
                                    while (m.find()) {
                                        // Get the matching string
                                        String match = m.group();
                                        System.out.println(match + " length " + match.length());
                                        refHeadingCleared = refHeading.substring(match.length());
                                       
                                    }
                                   System.out.println("removeNumberFromHeading " + refHeadingCleared.trim());
                                   aTextRange.setString(refHeadingCleared.trim());
                            
                              
                               break;
                          } 
                             
                     
                   }
                  
             }catch(NoSuchElementException ex){
                 log.error(ex.getMessage());
             }catch (WrappedTargetException ex) {
                log.error(ex.getMessage());
             }catch (com.sun.star.lang.IllegalArgumentException ex) {
                  log.error(ex.getMessage());
             }catch (UnknownPropertyException ex) {
                  log.error(ex.getMessage());
             }
             
             
         } 
    }
    
    
    private void getNumberedHeadings() {
       Iterator typedMatchSectionItr = sectionTypeMatchedSections.iterator();
         while(typedMatchSectionItr.hasNext()){
           
            Object matchedSectionElem=typedMatchSectionItr.next();
           // System.out.println("getNumberedHeadings " + matchedSectionElem);
            
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
                            
                            System.out.println("getNumberedHeadings: heading found " + strHeading);
                      
                            getReferenceMark(aTextRange,elem,strHeading.trim());
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
            }
            
       }
       
    }
    
     
   
    
   
    
    //Returns 1st heading in the section
    
     private Object getNumberedHeadingsInsertCrossRef(String results) {
     
           Object objHeading = null;
           
           try{
               
                Object sectionName = ooDocument.getTextSections().getByName(results);
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
                            System.out.println("strHeading " + strHeading);
                        
                            objHeading = elem;
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
            } finally {
                return objHeading;
            }
    }
    
   private ArrayList<String> getReferenceMarksOnCross(Object elem){
        ArrayList<String> referenceMarkNames = new ArrayList<String>(0);
        String textPortionType="";
        XEnumerationAccess xRangeAccess  = (XEnumerationAccess) UnoRuntime.queryInterface(XEnumerationAccess.class, elem);
      
        XEnumeration portionEnum =  xRangeAccess.createEnumeration();
         
         while (portionEnum.hasMoreElements()){
             try{
                 Object textPortion =  portionEnum.nextElement();  
                  XServiceInfo xTextPortionService= ooDocument.getServiceInfo(textPortion);
                   if (xTextPortionService.supportsService( "com.sun.star.text.TextPortion")){
                      XPropertySet xTextPortionProps = (XPropertySet)UnoRuntime.queryInterface(XPropertySet.class, textPortion);
                      
                          textPortionType = AnyConverter.toString(xTextPortionProps.getPropertyValue("TextPortionType"));
                         
                            if (textPortionType.equals("ReferenceMark")){
                           
                                XPropertySet xPortionProps = ooQueryInterface.XPropertySet(textPortion);
                                Object oRefMark =  xPortionProps.getPropertyValue("ReferenceMark");
                                XNamed xRefMark= (XNamed) AnyConverter.toObject(new Type(XNamed.class), oRefMark);
                                System.out.println("refmark " + xRefMark.getName());
                                if (!referenceMarkNames.contains(xRefMark.getName().toString())) {
                                    referenceMarkNames.add(xRefMark.getName().toString());
                                }
                          } 
                   }
                  
             }catch(NoSuchElementException ex){
                 log.error(ex.getMessage());
             }catch (WrappedTargetException ex) {
                log.error(ex.getMessage());
             }catch (com.sun.star.lang.IllegalArgumentException ex) {
                  log.error(ex.getMessage());
             }catch(UnknownPropertyException ex){
                 log.error(ex.getMessage());
             } finally {
                 
                 
             }
             
             
         }
        return referenceMarkNames;
   }
     
    
    //method to get and set reference mark for headings
    private void getReferenceMark(XTextRange aTextRange, Object elem, String refHeading){
      
        XText xRangeText=aTextRange.getText();
        Matcher m=null;
        String refHeadingCleared=null;
        XEnumerationAccess xRangeAccess = (XEnumerationAccess)UnoRuntime.queryInterface(com.sun.star.container.XEnumerationAccess.class,elem);
         XEnumeration portionEnum =  xRangeAccess.createEnumeration();
         while (portionEnum.hasMoreElements()){
             try{
                 Object textPortion =  portionEnum.nextElement();  
                  XServiceInfo xTextPortionService= ooDocument.getServiceInfo(textPortion);
                   if (xTextPortionService.supportsService( "com.sun.star.text.TextPortion")){
                      XPropertySet xTextPortionProps = (XPropertySet)UnoRuntime.queryInterface(XPropertySet.class, textPortion);
                      String textPortionType="";
                      
                        
                       if(cboNumberingScheme.getSelectedItem().toString()=="Base Numbering"){
                                    //create a pattern for base numbering
                                   Pattern p = Pattern.compile("[0-9]+\\)");
                                   m = p.matcher(refHeading);
                               }else if(cboNumberingScheme.getSelectedItem().toString()=="ALPHA"){
                                   //create a patter for alphabet
                                   Pattern p = Pattern.compile("[A-Za-z]+\\)");
                                   m = p.matcher(refHeading);
                               }else if(cboNumberingScheme.getSelectedItem().toString()=="ROMAN"){
                                   //pattern for roman numerals
                                   Pattern p = Pattern.compile("[mdclxvi]+\\)");
                                   m = p.matcher(refHeading);
                               }
                              
                             //check if pattern is found
                               
                                 // MessageBox.OK("The selected scheme does not exist in the section");
                                
                                    while (m.find()) {
                                        // Get the matching string
                                        String match = m.group();
                                        System.out.println(match + " length " + match.length());
                                        refHeadingCleared = refHeading.substring(match.length());
                                       
                                    }
                              int refLength=refHeadingCleared.length();
                              refLength=refLength-1;
                             
                                //insert reference mark
                              // XTextCursor xTextCursor = xRangeText.createTextCursorByRange(aTextRange.getStart());
                               XTextCursor xTextCursor = xRangeText.createTextCursorByRange(aTextRange.getEnd());
                              
                               xTextCursor.goLeft((short)refLength, true);
                               
                               XNamed xRefMark = (XNamed) UnoRuntime.queryInterface(XNamed.class,
                                        ooDocument.createInstance("com.sun.star.text.ReferenceMark"));
                              
                                 //xRefMark.setName("headRef:" + aTextRange.getString());
                                 xRefMark.setName("headRef_" + bungeniUUID.getStringUUID());
                                 
                                 //System.out.println("refText:" + aTextRange.getString());
                                 XTextContent xContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, xRefMark);
                                 xRangeText.insertTextContent(xTextCursor,xContent,true);
                                 
                                
                                break;
                          
                             
                     
                   }
                  
             }catch(NoSuchElementException ex){
                 log.error(ex.getMessage());
             }catch (WrappedTargetException ex) {
                log.error(ex.getMessage());
             }catch (com.sun.star.lang.IllegalArgumentException ex) {
                  log.error(ex.getMessage());
             }
             
             
         }
         
        
    }
    
    
    
    
     //method to get reference mark from heading when renumbering
    private void setReferenceMarkOnRenumbering(XTextRange aTextRange, Object elem, Object refMark){
      
       XText xRangeText=aTextRange.getText();
            
        XEnumerationAccess xRangeAccess = (XEnumerationAccess)UnoRuntime.queryInterface(com.sun.star.container.XEnumerationAccess.class,elem);
         XEnumeration portionEnum =  xRangeAccess.createEnumeration();
     
                               
           try {                       
                               
                   
                           
                        XTextCursor xTextCursor = xRangeText.createTextCursorByRange(aTextRange.getStart());
                        xTextCursor.gotoRange(aTextRange.getEnd(), true);

                        XNamed xRefMark = (XNamed) UnoRuntime.queryInterface(XNamed.class,
                        ooDocument.createInstance("com.sun.star.text.ReferenceMark"));

                       xRefMark.setName(refMark.toString());
                       System.out.println("new ref " + refMark.toString());    
                       
                       XTextContent xContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, xRefMark);
           
                      xRangeText.insertTextContent(xTextCursor,xContent,true);
              
                                 
            } catch (com.sun.star.lang.IllegalArgumentException ex) {
                ex.printStackTrace();
            }

        
    }
    
    
    private void insertReferenceMarkOnReNumbering(XTextRange aTextRange, Object elem, int refLength, Object refMark){
      
        XText xRangeText=aTextRange.getText();
     
        XEnumerationAccess xRangeAccess = (XEnumerationAccess)UnoRuntime.queryInterface(com.sun.star.container.XEnumerationAccess.class,elem);
         XEnumeration portionEnum =  xRangeAccess.createEnumeration();
         while (portionEnum.hasMoreElements()){
            
             try{
                 Object textPortion =  portionEnum.nextElement();  
                  XServiceInfo xTextPortionService= ooDocument.getServiceInfo(textPortion);
                   if (xTextPortionService.supportsService( "com.sun.star.text.TextPortion")){
                      XPropertySet xTextPortionProps = (XPropertySet)UnoRuntime.queryInterface(XPropertySet.class, textPortion);
                      String textPortionType="";
                      
                        
                            textPortionType = AnyConverter.toString(xTextPortionProps.getPropertyValue("TextPortionType"));
                            if (textPortionType.equals("ReferenceMark")){
                                return;
                          } else{
                              
                                System.out.println("no reference mark found ");
                                
                                                         
                                //insert reference mark
                              XTextCursor xTextCursor = xRangeText.createTextCursorByRange(aTextRange.getStart());
                          
                               xTextCursor.goLeft((short)refLength, true);
                               XNamed xRefMark = (XNamed) UnoRuntime.queryInterface(XNamed.class,
                                        ooDocument.createInstance("com.sun.star.text.ReferenceMark"));
                             
                              
                           
                                 //xRefMark.setName("headRef:" + aTextRange.getString());
                              
                                 xRefMark.setName(refMark.toString());
                                 
                                 //System.out.println("refText:" + aTextRange.getString());
                                 XTextContent xContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, xRefMark);
                                 
                                 xRangeText.insertTextContent(xTextCursor,xContent,true);
                                
                                
                          }
                             
                     
                   }
                  
             }catch(NoSuchElementException ex){
                 log.error(ex.getMessage());
             }catch (WrappedTargetException ex) {
                log.error(ex.getMessage());
             }catch (com.sun.star.lang.IllegalArgumentException ex) {
                  log.error(ex.getMessage());
             }catch (UnknownPropertyException ex) {
                  log.error(ex.getMessage());
             }
             
             
        
      }
                
    }
    
    
    
     private void insertReferenceMarkOnNumber(XTextRange aTextRange, Object elem, int refLength){
     
        XText xRangeText=aTextRange.getText();
        
        XEnumerationAccess xRangeAccess = (XEnumerationAccess)UnoRuntime.queryInterface(com.sun.star.container.XEnumerationAccess.class,elem);
         XEnumeration portionEnum =  xRangeAccess.createEnumeration();
         while (portionEnum.hasMoreElements()){
             try{
                 Object textPortion =  portionEnum.nextElement();  
                  XServiceInfo xTextPortionService= ooDocument.getServiceInfo(textPortion);
                   if (xTextPortionService.supportsService( "com.sun.star.text.TextPortion")){
                      XPropertySet xTextPortionProps = (XPropertySet)UnoRuntime.queryInterface(XPropertySet.class, textPortion);
                      String textPortionType="";
                      
                        
                            textPortionType = AnyConverter.toString(xTextPortionProps.getPropertyValue("TextPortionType"));
                            if (textPortionType.equals("ReferenceMark")){
                                return;
                          } else{
                              
                                System.out.println("no reference mark found ");
                               
           
                             aTextRange.getString().trim();                       
                                //insert reference mark
                              XTextCursor xTextCursor = xRangeText.createTextCursorByRange(aTextRange.getStart());
                              
                              //XWordCursor xWordCursor = (XWordCursor) UnoRuntime.queryInterface(
                                //       XWordCursor.class, xTextCursor);
                              //xWordCursor.gotoNextWord(false);
                                                           
                               xTextCursor.goLeft((short)refLength, true);
                               XNamed xRefMark = (XNamed) UnoRuntime.queryInterface(XNamed.class,
                                        ooDocument.createInstance("com.sun.star.text.ReferenceMark"));
                              
                                 //xRefMark.setName("headRef:" + aTextRange.getString());
                                 xRefMark.setName("numRef_" + bungeniUUID.getStringUUID());
                                 
                                 //System.out.println("refText:" + aTextRange.getString());
                                 XTextContent xContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, xRefMark);
                                 
                                 xRangeText.insertTextContent(xTextCursor,xContent,true);
                                
                                
                          }
                             
                     
                   }
                  
             }catch(NoSuchElementException ex){
                 log.error(ex.getMessage());
             }catch (WrappedTargetException ex) {
                log.error(ex.getMessage());
             }catch (com.sun.star.lang.IllegalArgumentException ex) {
                  log.error(ex.getMessage());
             }catch (UnknownPropertyException ex) {
                  log.error(ex.getMessage());
             }
             
             
         }
                
    }
   

    //method to get heading from section with selected sectionType
     ///variable sectionName added below for compilation success
    private void getHeadingInSection( ) throws NoSuchElementException, WrappedTargetException, UnknownPropertyException, com.sun.star.lang.IllegalArgumentException {
        
        String prevParent="";
        int parentPrefix=0;;
        /*iterate through the sectionTypeMatchedSections and look for heading in section*/
        Iterator<String> typedMatchSectionItr = sectionTypeMatchedSections.iterator();
        while(typedMatchSectionItr.hasNext()){
            String sectionName = typedMatchSectionItr.next();
            Object sectionObject = ooDocument.getTextSections().getByName(sectionName);
            /*get the XTextSection object of the matching section*/
            XTextSection theSection = ooQueryInterface.XTextSection(sectionObject);
            /*get the anchor of the matching section*/
            XTextRange range = theSection.getAnchor();
            /*get the enumeration object of the section */
         //   enumerateSectionContent (range, theSection, prevParent);
            
            XEnumerationAccess enumAcc  = (XEnumerationAccess) UnoRuntime.queryInterface(XEnumerationAccess.class, range);
            XEnumeration xEnum = enumAcc.createEnumeration();
            /*enumerate the elements in the section */
            while (xEnum.hasMoreElements()) {
                /*get the next enumerated element*/
                Object elem = xEnum.nextElement();
                /*query the matching element for its service info */
                XServiceInfo xInfo = (XServiceInfo)UnoRuntime.queryInterface(XServiceInfo.class, elem);
                /*match only paragraphs*/
                if(xInfo.supportsService("com.sun.star.text.Paragraph")){
                    /*get the properties of the paragraph */
                    XPropertySet objProps = ooQueryInterface.XPropertySet(xInfo);
                    short nLevel = -1;
                    /*get the paragraphs numbering level */
                    nLevel = com.sun.star.uno.AnyConverter.toShort(objProps.getPropertyValue("ParaChapterNumberingLevel"));
                    /*check if the paragraph is a heading type nLevel >= 0 */
                    if(nLevel >= 0) {
                        /* get the textcontent object of the matching enumerated element*/
                        XTextContent xContent = ooDocument.getTextContent(elem);
                        /*get the heading text of the matching heading */
                        XTextRange aTextRange =   xContent.getAnchor();
                        String strHeading = aTextRange.getString();
                         log.debug("getHeadingInSection: heading found " + strHeading);
                         /*get the parent section of the section containing the heading */
                         XNamed xParentSecName= ooQueryInterface.XNamed(theSection.getParentSection());
                         String currentParent=(String)xParentSecName.getName();
                         log.debug("getHeadingInSection" + currentParent);
                         /*check if the currentParent of the seciton is equal to the previous matching parent */
                         if(!currentParent.equalsIgnoreCase(prevParent)){
                             /* If not equals, restart numbering here */
                             headCount=1;
                             /*if currentParent is "root" use 1 as the starting point for numbering*/
                             if(currentParent.equals("root")){
                                  insertParentPrefix(sectionName, headCount);
                              }else{
                                 parentPrefix=headCount;
                                 insertParentPrefix(sectionName, parentPrefix);
                              }
                             insertNumber(aTextRange, headCount,elem);
                             
                             // insertAppliedNumberToMetadata(matchedSectionElem,headCount);
                             
                             
                             
                         }else{
                             //continue numbering
                            headCount++;
                            if(currentParent.equals("root")){
                                 // insertParentPrefix(matchedSectionElem, headCount);
                                  
                              }else{
                                parentPrefix=headCount;
                                 //insertParentPrefix(matchedSectionElem, parentPrefix);
                              }
                            
                            //getReferenceMark(aTextRange, elem);
                            insertNumber(aTextRange, headCount,elem); 
                           
                            //insertAppliedNumberToMetadata(matchedSectionElem,headCount);
                            
                         } // if (currentParent....)
                         
                        prevParent=(String)xParentSecName.getName();
                                              
                      
                      
                        break;
                        
                         
                      }//if nLevel 
                }
                
            }
           
             
            /*
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
            } */
            
       }
       
         
        
        
    }

    private void getHeadingInMatchingSections() throws NoSuchElementException, WrappedTargetException, UnknownPropertyException, com.sun.star.lang.IllegalArgumentException {
        String prevParent="";
        int parentPrefix=0;;
        /*iterate through the sectionTypeMatchedSections and look for heading in section*/
        Iterator<String> typedMatchSectionItr = sectionTypeMatchedSections.iterator();
        while(typedMatchSectionItr.hasNext()){
            String sectionName = typedMatchSectionItr.next();
            Object sectionObject = ooDocument.getTextSections().getByName(sectionName);
            /*get the XTextSection object of the matching section*/
            XTextSection theSection = ooQueryInterface.XTextSection(sectionObject);
            /*get the parent section of the current setion */
            XTextSection theSectionsParent = theSection.getParentSection();
            /*get the anchor of the matching section*/
            XTextRange range = theSection.getAnchor();
            enumerateSectionContent (range, theSection, prevParent);
            /*set prevparent to the name of the previous parent section */
            prevParent = ooQueryInterface.XNamed(theSectionsParent).getName();
        }
    }
    
    private String enumerateSectionContent (XTextRange sectionRange, XTextSection theSection, String prevParent ) throws NoSuchElementException, WrappedTargetException, UnknownPropertyException, com.sun.star.lang.IllegalArgumentException {
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
                if(xInfo.supportsService("com.sun.star.text.Paragraph")){
                    breakFromLoop = enumerateParagraphInSectionContent(xInfo, elem, theSection, prevParent);
                } /*for the future ... else if ("com.sun.star.text.TextTable*/
                if (breakFromLoop)
                    break;
                //
                //prevParent=(String)xParentSecName.getName();
                //break;
           }
            return new String("");
      }
   
    private boolean enumerateParagraphInSectionContent(XServiceInfo xInfo, Object elemParagraph, XTextSection theSection, String previousParent) throws UnknownPropertyException, com.sun.star.lang.IllegalArgumentException, WrappedTargetException {
                boolean bMatched = false;
                    /*get the properties of the paragraph */
                    XPropertySet objProps = ooQueryInterface.XPropertySet(xInfo);
                    short nLevel = -1;
                    /*get the paragraphs numbering level */
                    nLevel = com.sun.star.uno.AnyConverter.toShort(objProps.getPropertyValue("ParaChapterNumberingLevel"));
                    /*check if the paragraph is a heading type nLevel >= 0 */
                    if(nLevel >= 0) {
                            bMatched = true;
                            XTextContent xContent = ooDocument.getTextContent(elemParagraph);
                            //enumerateHeadingInParagraph(xContent, theSection, previousParent);
                    }
                return bMatched;
      }
/*
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
         if(!currentParent.equalsIgnoreCase(previousParent)){
             // If not equals, restart numbering here 
             headCount=1;
             // if currentParent is "root" use 1 as the starting point for numbering
             if(currentParent.equals("root")){
                  insertParentPrefix(sectionName, headCount);
              }else{
                 parentPrefix=headCount;
                 insertParentPrefix(sectionName, parentPrefix);
              }
             //getReferenceMark(aTextRange, elem);
             insertNumber(aTextRange, headCount,elem);
             insertAppliedNumberToMetadata(matchedSectionElem,headCount);
         } else {
             //continue numbering
            headCount++;
            if(currentParent.equals("root")){
                  insertParentPrefix(matchedSectionElem, headCount);
              }else{
                parentPrefix=headCount;
                 insertParentPrefix(matchedSectionElem, parentPrefix);
              }
            //getReferenceMark(aTextRange, elem);
            insertNumber(aTextRange, headCount,elem); 
            insertAppliedNumberToMetadata(matchedSectionElem,headCount);
            }
   }
  */  
    
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
   
     private void getHeadingInSectionOnRenumbering() {
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
    
    
    
    private void findAndReplace(){
        XReplaceable xReplaceable = (XReplaceable) UnoRuntime.queryInterface(XReplaceable.class, ooDocument.getTextDocument()); 
        XReplaceDescriptor xRepDesc = xReplaceable.createReplaceDescriptor(); 
       
        xRepDesc.setSearchString("iii)");
        xRepDesc.setReplaceString(" ");
        
        
        long nResult = xReplaceable.replaceAll(xRepDesc); 
      
    }
   
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
    
    
    private String getNodeName(String nodeName){
        selectSection=nodeName;
        return selectSection;
    }
    
    public static Object[] reverse(Object[] arr)
    {
        List<Object> list = Arrays.asList(arr);
        Collections.reverse(list);
        return list.toArray();
    }
    
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
    
    private void crossRef(){
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
           ArrayList<String> arrSectionTree = new ArrayList();
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
    
     
    private class ParentSchemeListener implements ItemListener{
        public void itemStateChanged(ItemEvent itemEvent) {
            int state = itemEvent.getStateChange();
            if (state == ItemEvent.SELECTED) {
              System.out.println("apply parent prefix checkbox selected");
                numParentPrefix="1";
              
            }   
        }
        
    }
    
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

     private void initTree(){
        treeSectionStructure.addTreeSelectionListener(new treeSectionStructureSelectionListener());
       
    }
  
        private void initSectionTree() {
        // initTreeSectionsArray();   
         treeSectionStructure.setModel(new DefaultTreeModel(sectionRootNode));
         treeSectionStructure.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
         CommonTreeFunctions.expandAll(treeSectionStructure);
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
     class treeSectionStructureSelectionListener implements TreeSelectionListener {
         DefaultMutableTreeNode selNode;
         
        String oldSelectedNodeName;
        public void valueChanged(TreeSelectionEvent e) {
            selNode=(DefaultMutableTreeNode)treeSectionStructure.getLastSelectedPathComponent();
            if (selNode == null) return;
            Object nodeInfo = selNode.getUserObject();
            if(selNode.isLeaf()){
             selectedNodeName=nodeInfo.toString();
             System.out.println("selectedNodeName " + selectedNodeName);
             getNodeName(selectedNodeName);
             //pass the node name to function to get tree
            }else{
                 System.out.println("error");
            }
        
            
           
        }
         
     }
       
   
    
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
        jScrollPane2 = new javax.swing.JScrollPane();
        treeSectionStructure = new javax.swing.JTree();
        cboNumberingScheme = new javax.swing.JComboBox();
        checkbxUseParentPrefix = new javax.swing.JCheckBox();
        btnApplyNumberingScheme = new javax.swing.JButton();
        btnRenumberSections = new javax.swing.JButton();
        btnInsertCrossReference = new javax.swing.JButton();

        listSectionTypes.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        listSectionTypes.setSelectionMode(javax.swing.ListSelectionModel.SINGLE_SELECTION);
        panelSectionTypes.setViewportView(listSectionTypes);

        jLabel1.setText("Bungeni Section Types");

        jScrollPane2.setViewportView(treeSectionStructure);

        cboNumberingScheme.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Base Numbering", "ROMAN", "ALPHA" }));

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

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, jScrollPane2, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 215, Short.MAX_VALUE)
                    .add(jLabel1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 215, Short.MAX_VALUE)
                    .add(checkbxUseParentPrefix)
                    .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING, false)
                        .add(org.jdesktop.layout.GroupLayout.LEADING, btnApplyNumberingScheme, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .add(org.jdesktop.layout.GroupLayout.LEADING, cboNumberingScheme, 0, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .add(org.jdesktop.layout.GroupLayout.LEADING, panelSectionTypes, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 202, Short.MAX_VALUE)
                        .add(org.jdesktop.layout.GroupLayout.LEADING, btnRenumberSections, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .add(org.jdesktop.layout.GroupLayout.LEADING, btnInsertCrossReference, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(jLabel1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 15, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(panelSectionTypes, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 85, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(cboNumberingScheme, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(14, 14, 14)
                .add(checkbxUseParentPrefix)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btnApplyNumberingScheme)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btnRenumberSections)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(btnInsertCrossReference)
                .add(16, 16, 16)
                .add(jScrollPane2, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 203, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(20, Short.MAX_VALUE))
        );
    }// </editor-fold>//GEN-END:initComponents

    private void btnInsertCrossReferenceActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnInsertCrossReferenceActionPerformed
// TODO add your handling code here:
        crossRef();
    }//GEN-LAST:event_btnInsertCrossReferenceActionPerformed

    private void btnRenumberSectionsActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnRenumberSectionsActionPerformed
// TODO add your handling code here:
        ArrayList<Object> sectionHeadings = new ArrayList<Object>(0);
       // ArrayList<Object> refMarksInHeadingMatched= new ArrayList<Object>(0);
        sectionHeadings.clear();
        refMarksInHeadingMatched.clear();
         Object sectHeading=null;
         ////-- commented for compile success readSections();
         findBrokenReferences();
        
         
         Iterator typedMatchSectionItr = sectionTypeMatchedSections.iterator();
         while(typedMatchSectionItr.hasNext()){
           
             Object matchedSectionElem=typedMatchSectionItr.next();
             sectHeading=getHeadingFromMatchedSection(matchedSectionElem);
             sectionHeadings.add(sectHeading);
         }
         //iterate through the headings arraylist and get the references marks
         Iterator itrSectionHeads=sectionHeadings.iterator();
         while(itrSectionHeads.hasNext()){
             Object heading=itrSectionHeads.next();
             refMarksInHeadingMatched=getNumberReferenceFromHeading(heading);
              Iterator<Object> refMarksIterator = refMarksInHeadingMatched.iterator();
              
              while(refMarksIterator.hasNext()){
                   Object refMark=refMarksIterator.next();
                                   
                   XTextContent xContent = ooDocument.getTextContent(refMark);
                   XTextRange aTextRange =   xContent.getAnchor();
                   String strRef = aTextRange.getString();
                  
                   System.out.println("strRef " + strRef);
                   aTextRange.setString(" ");
                   
                    
            }
         }
         
         
          getHeadingInSectionOnRenumbering();
             
          //iterate through the headings and apply references to the numbers now
         
         //insert number by calling insertNumber method within the getHeadingInSectionOnRenumbering() method
        
         //get the numbered headings and insert the references again since they were broken during the renumbering
        //getNumberedHeadingsOnRenumbering(); 
       //getNumberedHeadings();
      
      
      
       
    }//GEN-LAST:event_btnRenumberSectionsActionPerformed
    
   private HashMap<String, String> defaultSectionMetadata  = new HashMap<String,String>();
    
    private void btnApplyNumberingSchemeActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnApplyNumberingSchemeActionPerformed
        //get section type selected for numbering 
        try {
        String sectionType=listSectionTypes.getSelectedValue().toString();            
        /*find all sections matching that section type, and populate arraylist*/
        /*was called readSection()*/
        findSectionsMatchingSectionType(sectionType);
        /*iterate through arraylist and set numberingscheme metadata to matching sections*/
        /*was called applyNumberingScheme() */
        setNumberingSchemeMetadataIntoMatchingSections();
        /*why is the above being done...when the same section is iterated over again ??? */
         getHeadingInSection();
         getNumberedHeadings();
        } catch (Exception ex) {
            
        }
         
     
        
    }//GEN-LAST:event_btnApplyNumberingSchemeActionPerformed

   private void setNumberingSchemeMetadataIntoMatchingSections(){
       /*map to store section metadata apply to section*/
       HashMap<String,String> sectionMetadata = new HashMap<String,String>();
       /*set metadata into section identifying numbering scheme*/
       sectionMetadata.put("NumberingScheme",cboNumberingScheme.getSelectedItem().toString());
       /*iterate through matching sections */
       Iterator<String> typedMatchSectionItr = sectionTypeMatchedSections.iterator();
       while(typedMatchSectionItr.hasNext()){
            String matchedSection=typedMatchSectionItr.next();
            log.debug("applyNumberingScheme " + sectionMetadata + " to " + matchedSection);
            ooDocument.setSectionMetadataAttributes(matchedSection, sectionMetadata);
       }
   }
   
    
    public void setOOComponentHandle(OOComponentHelper ooComponent) {
        ooDocument = ooComponent;
    }

    public Component getObjectHandle() { 
        return this;
        
    }


    public void setParentWindowHandle(JFrame c) {
        this.parentFrame = c;
    }
   
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnApplyNumberingScheme;
    private javax.swing.JButton btnInsertCrossReference;
    private javax.swing.JButton btnRenumberSections;
    private javax.swing.JComboBox cboNumberingScheme;
    private javax.swing.JCheckBox checkbxUseParentPrefix;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JList listSectionTypes;
    private javax.swing.JScrollPane panelSectionTypes;
    private javax.swing.JTree treeSectionStructure;
    // End of variables declaration//GEN-END:variables

   
    
}
