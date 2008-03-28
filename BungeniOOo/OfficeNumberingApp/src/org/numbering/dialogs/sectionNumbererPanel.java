/*
 * sectionNumbererPanel.java
 *
 * Created on March 27, 2008, 6:39 PM
 */

package org.numbering.dialogs;

import com.sun.star.container.NoSuchElementException;
import com.sun.star.container.XNamed;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.lang.XComponent;
import com.sun.star.text.XTextSection;
import com.sun.star.uno.XComponentContext;
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
        panelNumberingScheme.setVisible(false);
    }
    
    
    private void initSectionsArray(){
  
        openofficeObject = new org.bungeni.ooo.BungenioOoHelper(xContext);
        openofficeObject.initoOo();
        xComponent = openofficeObject.openDocument("/home/undesa/downloads/setSectionMetadata(2).odt");
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
                                            if(metaName.startsWith("BungeniSectionType")){
                                                model.addElement(metaName + " " + "-" + sectionMetadataMap.get(metaName));
                                            }
                                            
                                           
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

        listSectionTypes.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        jScrollPane1.setViewportView(listSectionTypes);

        txtSectionType.setEditable(false);

        cboNumberingScheme.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Base Numbering", "Point Numbering", "Roman Numerals", "Alphabet" }));

        btnApplyNumberingScheme.setText("Apply Numbering Scheme");

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

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(org.jdesktop.layout.GroupLayout.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, panelNumberingScheme, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, jScrollPane1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(jScrollPane1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(34, 34, 34)
                .add(panelNumberingScheme, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents
    
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnApplyNumberingScheme;
    private javax.swing.JComboBox cboNumberingScheme;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JList listSectionTypes;
    private javax.swing.JPanel panelNumberingScheme;
    private javax.swing.JTextField txtSectionType;
    // End of variables declaration//GEN-END:variables

   
    
}
