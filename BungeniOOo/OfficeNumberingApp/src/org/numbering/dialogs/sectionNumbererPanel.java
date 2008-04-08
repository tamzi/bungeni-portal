/*
 * sectionNumbererPanel.java
 *
 * Created on March 27, 2008, 6:39 PM
 */

package org.numbering.dialogs;

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
import com.sun.star.text.ReferenceFieldSource;
import com.sun.star.text.XReferenceMarksSupplier;
import com.sun.star.text.XSimpleText;
import com.sun.star.text.XText;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextCursor;
import com.sun.star.text.XTextRange;
import com.sun.star.text.XTextSection;
import com.sun.star.text.XTextViewCursor;
import com.sun.star.uno.AnyConverter;
import com.sun.star.uno.UnoRuntime;
import com.sun.star.uno.XComponentContext;
import com.sun.star.util.XNumberFormatTypes;
import com.sun.star.util.XNumberFormats;
import com.sun.star.util.XNumberFormatsSupplier;
import com.sun.star.view.XViewCursor;
import com.sun.star.xforms.XModel;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import javax.swing.DefaultListModel;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import numberingscheme.impl.IGeneralNumberingScheme;
import numberingscheme.impl.NumberRange;
import numberingscheme.impl.NumberingSchemeFactory;
import org.bungeni.ooo.BungenioOoHelper;
import org.bungeni.ooo.OOComponentHelper;
import org.apache.log4j.Logger;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.ooo.ooUserDefinedAttributes;
import numberingscheme.schemes.*;
import org.bungeni.utils.CommonExceptionUtils;

/**
 *
 * @author  undesa
 */
public class sectionNumbererPanel extends javax.swing.JPanel {
    private XComponentContext xContext;
    private OOComponentHelper ooDocument;
    private XComponent xComponent;
    private BungenioOoHelper openofficeObject;
    HashMap<String, String> sectionMetadataMap=new HashMap<String, String>();
   //HashMap<String, String> sectionTypeMetadataMap=new HashMap<String, String>();
    private static org.apache.log4j.Logger log = Logger.getLogger(sectionNumbererPanel.class.getName());
   
    private HashMap<String,String> metadata = new HashMap();
    private ArrayList<String> sectionTypeMatchedSections = new ArrayList<String>();
    private int countElems=1;
    private int testCount=1;
    DefaultListModel model=new DefaultListModel();
    
    
    Set attributeSet=new HashSet();
   
    
    /** Creates new form sectionNumbererPanel */
    public sectionNumbererPanel() {
       
    }
    
    public sectionNumbererPanel(XComponentContext xContext){
        this.xContext=xContext;
        initComponents();
        init();
    }
    
    private void init(){
        initSectionsArray();
        loadJlist();
        listSectionTypes.addListSelectionListener(new NumberingSchemeListener());
        panelNumberingScheme.setVisible(false);
    }
    
  
    
    private void initSectionsArray(){
  
        openofficeObject = new org.bungeni.ooo.BungenioOoHelper(xContext);
        openofficeObject.initoOo();
        xComponent = openofficeObject.openDocument("/home/undesa/Documents/testsection3.odt");
        ooDocument = new OOComponentHelper(xComponent, xContext);
        try{
            if (!ooDocument.isXComponentValid()) return;
            
           
            if (!ooDocument.getTextSections().hasByName("root")) {
                log.debug("no root section found");
                return;
            }
            Object rootSection = ooDocument.getTextSections().getByName("root");
            XTextSection theSection = ooQueryInterface.XTextSection(rootSection);
            
           recurseSections (theSection);
            
            
         }catch (NoSuchElementException ex) {
            log.error(ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error(ex.getMessage());
        }
        
        
    }
    
    private void recurseSections(XTextSection theSection){
       
       
          //recurse children
            XTextSection[] sections = theSection.getChildSections();
            if (sections != null ) {
                if (sections.length > 0 ) {
                    //start from last index and go to first
                    for (int nSection = sections.length - 1 ; nSection >=0 ; nSection--) {
                        XNamed xSecName = ooQueryInterface.XNamed(sections[nSection]);
                        String childSectionName = (String) xSecName.getName();
                        sectionMetadataMap=ooDocument.getSectionMetadataAttributes(childSectionName);
                        log.debug("SectionMetadataLoad childSectionName: " + childSectionName);
                       if(sectionMetadataMap.size()>0){
                            
                        Iterator metaIterator = sectionMetadataMap.keySet().iterator();

                               while(metaIterator.hasNext()){
                                        for(int i=0; i< sectionMetadataMap.size(); i++) {
                                            String metaName = (String) metaIterator.next();
                                            log.debug("childSectionName: " + childSectionName + " metaName: "  + metaName + " attribute: " + sectionMetadataMap.get(metaName));
                                           
                                          if(metaName.startsWith("BungeniSectionType")){
                                               
                                              
                                               attributeSet.add(sectionMetadataMap.get(metaName).trim());
                                               
                                                
                                           }
                                            
                                           
                                        }
                                 }  
                                 
                            }
                             recurseSections(sections[nSection]);
                       
                     }
                   
                } 
                
            }
            
            
           
            
    }
    
    private void loadJlist(){
         Iterator attributeSetIterator = attributeSet.iterator();
              while (attributeSetIterator.hasNext()) {
               
               Object element = attributeSetIterator.next();
               model.addElement(element);
            }
        listSectionTypes.setModel(model);
    }
    
     private void readSections(){
         String sectionType=listSectionTypes.getSelectedValue().toString();
       try{
            if (!ooDocument.isXComponentValid()) return;
            
           
            if (!ooDocument.getTextSections().hasByName("root")) {
                log.debug("no root section found");
                return;
            }
            Object rootSection = ooDocument.getTextSections().getByName("root");
            XTextSection theSection = ooQueryInterface.XTextSection(rootSection);
            this.sectionTypeMatchedSections.clear();
            recurseSectionsForSectionType(theSection,sectionType);
           
            //now the arraylist should have been populated
            //now iterate through the arraylist and apply the numbering scheme across the matched sections.
         }catch (NoSuchElementException ex) {
            log.error(ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error(ex.getMessage());
        }
   }
    
   private void recurseSectionsForSectionType(XTextSection theSection, String sectionType){
       
            XTextSection[] sections = theSection.getChildSections();
            if (sections != null ) {
                if (sections.length > 0 ) {
                    
                    //start from last index and go to first
                    for (int nSection = sections.length - 1 ; nSection >=0 ; nSection--) {
                        
                        XNamed xSecName = ooQueryInterface.XNamed(sections[nSection]);
                         XNamed xParentSecName= ooQueryInterface.XNamed(sections[nSection].getParentSection());
                        
                        String childSectionName = (String) xSecName.getName();
                        //String currentParentSectionName = (String) xParentSecName.getName();
                        
                        
                        sectionMetadataMap=ooDocument.getSectionMetadataAttributes(childSectionName);
                        if (sectionMetadataMap.containsKey("BungeniSectionType") ) {
                            String matchedSectionType= sectionMetadataMap.get("BungeniSectionType");
                            if(matchedSectionType.equalsIgnoreCase(sectionType)){
                              sectionTypeMatchedSections.add(childSectionName);
                                
                            }
                          
                        }
                        
                        log.debug("recurseSectionsForSectionType: " + childSectionName);
                        recurseSectionsForSectionType(sections[nSection],sectionType);
                       
                     }
                   
                } 
                
            }
            
           
           
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
                         testCount=1;
                        
                         System.out.println("different parent" + "testCount " + testCount);
                        
                        
                     }else{
                         //continue numbering
                        testCount++;
                                     
                        System.out.println("same parent" + "testCount " + testCount);
                     }
                    prevParent=(String)xParentSecName.getName();

                    } catch (NoSuchElementException ex) {
                        ex.printStackTrace();
                    } catch (WrappedTargetException ex) {
                        ex.printStackTrace();
                    }
                
                 
          }
     
        
   }
    
   private void applyNumberingScheme(){
       metadata.put("NumberingScheme",cboNumberingScheme.getSelectedItem().toString());
       Iterator typedMatchSectionItr = sectionTypeMatchedSections.iterator();
       while(typedMatchSectionItr.hasNext()){
            Object matchedSectionElem=typedMatchSectionItr.next();
           System.out.println("applyNumberingScheme function " + metadata + " to " + matchedSectionElem.toString());
            ooDocument.setSectionMetadataAttributes(matchedSectionElem.toString(),metadata);
       }
       
       
      
   }
   
   private void insertAppliedNumberToMetadata(Object sectionElement, int appliedNumber){
        String strAppliedNumber="" + appliedNumber + "";
        //clear the metadata map
        metadata.clear();
        //insert key=>value attribute into metadata map
        metadata.put("AppliedNumber",strAppliedNumber);
        System.out.println("insertAppliedNumberToMetadata function " + metadata + " to " + sectionElement.toString());
        //insert the applied number into the metadata
        ooDocument.setSectionMetadataAttributes(sectionElement.toString(),metadata);
        
   }
    
   
   private void removeNumber(XTextRange aTextRange, int testCount){
       //this function will delete the numbers next to each heading and regenerate based on the numbering
       //scheme again
       
   }
   
   private void findBrokenReferences(){
    
        
      XPropertySet xFieldProps = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, ooDocument.createInstance(
                  "com.sun.star.text.TextField.GetReference"));
       // Get the XReferenceMarksSupplier interface of the document
       XReferenceMarksSupplier xRefSupplier = (XReferenceMarksSupplier) UnoRuntime.queryInterface(
                         XReferenceMarksSupplier.class, ooDocument.getTextDocument());
       // Get an XNameAccess which refers to all inserted reference marks
       XNameAccess xMarks = (XNameAccess) UnoRuntime.queryInterface(XNameAccess.class,
                     xRefSupplier.getReferenceMarks());
         
        // Put the names of each reference mark into an array of strings
         String[] aNames = xMarks.getElementNames();
         if (aNames.length > 0) {
            for(int i=0;i<aNames.length;i++){
                
                System.out.println ("GetReference text field inserted for ReferenceMark : "  + aNames[i]);
                
                try {
                    xFieldProps.setPropertyValue("SourceName", aNames[i]);
                    xFieldProps.setPropertyValue ("ReferenceFieldSource", new Short(ReferenceFieldSource.REFERENCE_MARK));
                  
                 
                 //identify broken references based on the macro code
                 /*	if not oRefMarks.hasByName(oTextField.Sourcename) then
				'orphan or broken reference found
			end if
                  *
                  *
                  *
                  */
                  if(!xMarks.hasByName(xFieldProps.getPropertyValue("SourceName").toString())){
                        System.out.println("hello");
                  }
                   
                    
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
             
         }
       
         
         
         
   }
    
    private void insertNumber(XTextRange aTextRange, int testCount){
       
        
     
       String numberingScheme =cboNumberingScheme.getSelectedItem().toString();
       int numberingSchemeIndex=cboNumberingScheme.getSelectedIndex();
       log.debug("numbering scheme selected " + numberingScheme);
       
       IGeneralNumberingScheme inumScheme =NumberingSchemeFactory.getNumberingScheme(numberingScheme);

       
       XText xRangeText=aTextRange.getText();
       XTextCursor xTextCursor = xRangeText.createTextCursorByRange(aTextRange.getStart());
       xTextCursor.gotoRange(aTextRange.getEnd(), true);
       
      
       XTextContent xContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, xTextCursor);
       
       inumScheme.setRange (new NumberRange(testCount, testCount));
       inumScheme.generateSequence();
       ArrayList<String> seq = inumScheme.getGeneratedSequence();
        Iterator<String> iter = seq.iterator();
        while (iter.hasNext()) {
           
            xRangeText.insertString(xTextCursor,iter.next() + ") ",false);
        }
       
     
      
    }
    
     
    
    
    //method to get reference mark from heading
    private void getReferenceMark(XTextRange aTextRange, Object elem){
      
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
                                xTextCursor.gotoRange(aTextRange.getEnd(), true);
                                XNamed xRefMark = (XNamed) UnoRuntime.queryInterface(XNamed.class,
                                        ooDocument.createInstance("com.sun.star.text.ReferenceMark"));
                                
                                 xRefMark.setName("refText:" + aTextRange.getString());
                                 
                                 System.out.println("refText:" + aTextRange.getString());
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
    private void getHeadingInSection() {
        
        String prevParent="";
        //iterate through the sectionTypeMatchedSections and look for heading in section
       Iterator typedMatchSectionItr = sectionTypeMatchedSections.iterator();
       while(typedMatchSectionItr.hasNext()){
           
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
                         if(!currentParent.equalsIgnoreCase(prevParent)){
                             //restart numbering here
                             testCount=1;
                             
                            // insertNumber(aTextRange, testCount);
                             //insertAppliedNumberToMetadata(matchedSectionElem,testCount);
                         }else{
                             //continue numbering
                            testCount++;
                            
                           // insertNumber(aTextRange, testCount);                 
                            //insertAppliedNumberToMetadata(matchedSectionElem,testCount);
                         }
                         
                        prevParent=(String)xParentSecName.getName();
                                                
                       // getReferenceMark(aTextRange,elem);
                        
                      
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
    
   
    
     private class NumberingSchemeListener implements ListSelectionListener{
        public void valueChanged(ListSelectionEvent listSelectionEvent) {
            txtSectionType.setText(listSectionTypes.getSelectedValue().toString());
            panelNumberingScheme.setVisible(true);
        }
        
    }
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    // <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    private void initComponents() {
        jScrollPane1 = new javax.swing.JScrollPane();
        listSectionTypes = new javax.swing.JList();
        panelNumberingScheme = new javax.swing.JPanel();
        txtSectionType = new javax.swing.JTextField();
        cboNumberingScheme = new javax.swing.JComboBox();
        btnApplyNumberingScheme = new javax.swing.JButton();
        checkbxUseParentPrefix = new javax.swing.JCheckBox();
        jButton1 = new javax.swing.JButton();
        jLabel1 = new javax.swing.JLabel();

        listSectionTypes.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        listSectionTypes.setSelectionMode(javax.swing.ListSelectionModel.SINGLE_SELECTION);
        jScrollPane1.setViewportView(listSectionTypes);

        txtSectionType.setEditable(false);

        cboNumberingScheme.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Base Numbering", "ROMAN", "ALPHA" }));

        btnApplyNumberingScheme.setText("Apply Numbering Scheme");
        btnApplyNumberingScheme.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnApplyNumberingSchemeActionPerformed(evt);
            }
        });

        checkbxUseParentPrefix.setText("Use Parent Prefix");
        checkbxUseParentPrefix.setBorder(javax.swing.BorderFactory.createEmptyBorder(0, 0, 0, 0));
        checkbxUseParentPrefix.setMargin(new java.awt.Insets(0, 0, 0, 0));

        jButton1.setText("test");
        jButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton1ActionPerformed(evt);
            }
        });

        org.jdesktop.layout.GroupLayout panelNumberingSchemeLayout = new org.jdesktop.layout.GroupLayout(panelNumberingScheme);
        panelNumberingScheme.setLayout(panelNumberingSchemeLayout);
        panelNumberingSchemeLayout.setHorizontalGroup(
            panelNumberingSchemeLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelNumberingSchemeLayout.createSequentialGroup()
                .addContainerGap()
                .add(panelNumberingSchemeLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(cboNumberingScheme, 0, 194, Short.MAX_VALUE)
                    .add(txtSectionType, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 194, Short.MAX_VALUE)
                    .add(btnApplyNumberingScheme)
                    .add(checkbxUseParentPrefix)
                    .add(jButton1))
                .addContainerGap())
        );
        panelNumberingSchemeLayout.setVerticalGroup(
            panelNumberingSchemeLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelNumberingSchemeLayout.createSequentialGroup()
                .addContainerGap()
                .add(txtSectionType, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(14, 14, 14)
                .add(cboNumberingScheme, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(18, 18, 18)
                .add(checkbxUseParentPrefix)
                .add(20, 20, 20)
                .add(btnApplyNumberingScheme)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 20, Short.MAX_VALUE)
                .add(jButton1)
                .addContainerGap())
        );

        jLabel1.setText("Bungeni Section Types");

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(org.jdesktop.layout.GroupLayout.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, jLabel1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
                    .add(panelNumberingScheme, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, jScrollPane1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .add(19, 19, 19)
                .add(jLabel1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 15, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jScrollPane1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(panelNumberingScheme, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents

    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton1ActionPerformed
// TODO add your handling code here:
         findBrokenReferences();
    }//GEN-LAST:event_jButton1ActionPerformed

    private void btnApplyNumberingSchemeActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnApplyNumberingSchemeActionPerformed
       // countElems=1;
         readSections();
         applyNumberingScheme();
         getHeadingInSection();
       
       
         
     
        
    }//GEN-LAST:event_btnApplyNumberingSchemeActionPerformed
    
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnApplyNumberingScheme;
    private javax.swing.JComboBox cboNumberingScheme;
    private javax.swing.JCheckBox checkbxUseParentPrefix;
    private javax.swing.JButton jButton1;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JList listSectionTypes;
    private javax.swing.JPanel panelNumberingScheme;
    private javax.swing.JTextField txtSectionType;
    // End of variables declaration//GEN-END:variables

   
    
}
