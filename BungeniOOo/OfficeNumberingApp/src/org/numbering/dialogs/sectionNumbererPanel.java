/*
 * sectionNumbererPanel.java
 *
 * Created on March 27, 2008, 6:39 PM
 */

package org.numbering.dialogs;

import com.sun.star.beans.UnknownPropertyException;
import com.sun.star.beans.XPropertySet;
import com.sun.star.beans.XPropertySetInfo;
import com.sun.star.container.NoSuchElementException;
import com.sun.star.container.XContentEnumerationAccess;
import com.sun.star.container.XEnumeration;
import com.sun.star.container.XEnumerationAccess;
import com.sun.star.container.XNamed;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.lang.XComponent;
import com.sun.star.lang.XServiceInfo;
import com.sun.star.text.XSimpleText;
import com.sun.star.text.XText;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextCursor;
import com.sun.star.text.XTextRange;
import com.sun.star.text.XTextSection;
import com.sun.star.uno.AnyConverter;
import com.sun.star.uno.UnoRuntime;
import com.sun.star.uno.XComponentContext;
import com.sun.star.util.XNumberFormatTypes;
import com.sun.star.util.XNumberFormats;
import com.sun.star.util.XNumberFormatsSupplier;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import javax.swing.DefaultListModel;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
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
    private static org.apache.log4j.Logger log = Logger.getLogger(sectionNumbererPanel.class.getName());
    private schemeNumeric numObj;
    

   
    
    /** Creates new form sectionNumbererPanel */
    public sectionNumbererPanel() {
        //initComponents();
    }
    
    public sectionNumbererPanel(XComponentContext xContext){
        this.xContext=xContext;
        initComponents();
        init();
    }
    
    private void init(){
        initSectionsArray();
        listSectionTypes.addListSelectionListener(new NumberingSchemeListener());
        //panelNumberingScheme.setVisible(false);
    }
    
    
    private void initSectionsArray(){
  
        openofficeObject = new org.bungeni.ooo.BungenioOoHelper(xContext);
        openofficeObject.initoOo();
        xComponent = openofficeObject.openDocument("/home/undesa/downloads/sections1.odt");
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
        DefaultListModel model=new DefaultListModel();
        Set attributeSet=new HashSet();
        
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
                                         //  if(metaName.startsWith("BungeniSectionType")){
                                                //model.addElement(metaName + " " + "-" + sectionMetadataMap.get(metaName));
                                                model.addElement(sectionMetadataMap.get(metaName));
                                          // }
                                            
                                           
                                        }
                                 }  
                            }
                       
                          

                            recurseSections(sections[nSection]);
                       
                     }
                   
                } 
                
            }
            
            listSectionTypes.setModel(model);
           
           
            
    }
    
    private class NumberingSchemeListener implements ListSelectionListener{
        public void valueChanged(ListSelectionEvent listSelectionEvent) {
            txtSectionType.setText(listSectionTypes.getSelectedValue().toString());
            panelNumberingScheme.setVisible(true);
        }
        
    }
    
    private void applyNumberingFormat(){
        HashMap<String,String> metadata = new HashMap();
        metadata.put("NumberingScheme",cboNumberingScheme.getSelectedItem().toString());
          
        try{
            Object sectionName = ooDocument.getTextSections().getByName("part2");
            log.debug("set numbering scheme attribute " + cboNumberingScheme.getSelectedItem().toString());
            ooDocument.setSectionMetadataAttributes("part2",metadata);
          
       
        
        }catch (NoSuchElementException ex) {
            log.error(ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error(ex.getMessage());
        }
        
       
       
       
        
    }
    //method to insert reference mark over heading
    private void insertReferenceMark(XTextRange aTextRange, String refName){
        
    }
    
    private void insertNumber(XTextRange aTextRange){
        //get numbering scheme from drop down
        //setup start and end figures
       String numberingScheme =cboNumberingScheme.getSelectedItem().toString();
       int numberingSchemeIndex=cboNumberingScheme.getSelectedIndex();
       log.debug("numbering scheme selected " + numberingScheme);
       XText xRangeText=aTextRange.getText();
        XTextCursor xTextCursor = xRangeText.createTextCursorByRange(aTextRange.getStart());
                                xTextCursor.gotoRange(aTextRange.getEnd(), true);
       switch (numberingSchemeIndex) {
           //numeric numbering scheme
           case 1:
           log.debug("numbering scheme selected " + numberingScheme); 
           
            numObj=new schemeNumeric((long)1, (long) 1);
            numObj.generateSequence();
            ArrayList<String> seq = numObj.getGeneratedSequence();
            Iterator<String> iter = seq.iterator();
            while (iter.hasNext()) {
                String elem = iter.next();
                xRangeText.insertString(xTextCursor,"1" + ") ",false);
            }
           break;
           
           //point numbering scheme
           case 2:
           log.debug("numbering scheme selected " + numberingScheme);
           break;
           
           //roman numerals
           case 3:
           log.debug("numbering scheme selected " + numberingScheme);
           
           break;
           
             //alphabet 
           case 4:
           log.debug("numbering scheme selected " + numberingScheme);
           break;
           
           default: log.debug("numbering scheme selected base numbering");break;
           
       }
       
    }
    
    //nethod to get reference mark from heading
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
                                log.debug("no reference mark found");
                                //insert reference mark
                               // XText xText = aTextRange.getText();
                                XTextCursor xTextCursor = xRangeText.createTextCursorByRange(aTextRange.getStart());
                                xTextCursor.gotoRange(aTextRange.getEnd(), true);
                                XNamed xRefMark = (XNamed) UnoRuntime.queryInterface(XNamed.class,
                                        ooDocument.createInstance("com.sun.star.text.ReferenceMark"));
                                
                                 xRefMark.setName("refText");
                                 XTextContent xContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, xRefMark);
                                 xRangeText.insertTextContent(xTextCursor,xContent,true);
                                 
                                 insertNumber(aTextRange);
                                
                                
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
    //method to get heading from section
    private void getHeading() {
        
        try{
            Object sectionName = ooDocument.getTextSections().getByName("part2");
            XTextSection theSection = ooQueryInterface.XTextSection(sectionName);
            XTextRange range = theSection.getAnchor();
            
            XEnumerationAccess enumAcc  = (XEnumerationAccess) UnoRuntime.queryInterface(XEnumerationAccess.class, range);
            XEnumeration xEnum = enumAcc.createEnumeration();
            while (xEnum.hasMoreElements()) {
                Object elem = xEnum.nextElement();
                XServiceInfo xInfo = (XServiceInfo)UnoRuntime.queryInterface(XServiceInfo.class, elem);
                if(xInfo.supportsService("com.sun.star.text.Paragraph")){
                    System.out.println("found paragraph.... ");
                    XPropertySet objProps = ooQueryInterface.XPropertySet(xInfo);
                     short nLevel = -1;
                     nLevel = com.sun.star.uno.AnyConverter.toShort(objProps.getPropertyValue("ParaChapterNumberingLevel"));
                     if(nLevel>=0){
                        XTextContent xContent = ooDocument.getTextContent(elem);
                        XTextRange aTextRange =   xContent.getAnchor();
                        String strHeading = aTextRange.getString();
                        
                       //insert reference mark
                         getReferenceMark(aTextRange,elem);
                        //apply numbering scheme
                         log.debug("heading found " + strHeading);
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
        jLabel1 = new javax.swing.JLabel();

        listSectionTypes.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        jScrollPane1.setViewportView(listSectionTypes);

        txtSectionType.setEditable(false);

        cboNumberingScheme.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Base Numbering", "Point Numbering", "Roman Numerals", "Alphabet" }));

        btnApplyNumberingScheme.setText("Apply Numbering Scheme");
        btnApplyNumberingScheme.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnApplyNumberingSchemeActionPerformed(evt);
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
                    .add(btnApplyNumberingScheme))
                .addContainerGap())
        );
        panelNumberingSchemeLayout.setVerticalGroup(
            panelNumberingSchemeLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelNumberingSchemeLayout.createSequentialGroup()
                .addContainerGap()
                .add(txtSectionType, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(14, 14, 14)
                .add(cboNumberingScheme, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(27, 27, 27)
                .add(btnApplyNumberingScheme)
                .addContainerGap(83, Short.MAX_VALUE))
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

    private void btnApplyNumberingSchemeActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnApplyNumberingSchemeActionPerformed
       
       // applyNumberingFormat();
        getHeading();
        
    }//GEN-LAST:event_btnApplyNumberingSchemeActionPerformed
    
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnApplyNumberingScheme;
    private javax.swing.JComboBox cboNumberingScheme;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JList listSectionTypes;
    private javax.swing.JPanel panelNumberingScheme;
    private javax.swing.JTextField txtSectionType;
    // End of variables declaration//GEN-END:variables

   
    
}
