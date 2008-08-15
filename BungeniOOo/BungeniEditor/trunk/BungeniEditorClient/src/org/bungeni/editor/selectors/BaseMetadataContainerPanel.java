/*
 * Main.java
 *
 * Created on August 8, 2008, 1:56 PM
 */

package org.bungeni.editor.selectors;

import com.l2fprod.common.swing.JTaskPaneGroup;
import java.util.ArrayList;
import javax.swing.JFrame;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.actions.toolbarSubAction;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author  undesa
 */
public abstract class BaseMetadataContainerPanel extends javax.swing.JPanel {
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(BaseMetadataContainerPanel.class.getName());
    /**
     * openoffice component handle
     */
    private OOComponentHelper ooDocument;
    private JFrame parentFrame;
    private toolbarAction theAction = null;
    private toolbarSubAction theSubAction = null;
    private SelectorDialogModes dialogMode;
    /**
     * error messages
     */
    private ArrayList<ErrorMessage> errorMessages = new ArrayList<ErrorMessage>(0);
    /** Creates new form Main */
    /**
     *In the derived class, always call super(), and then execute initVariables to set the requireed parameters
     */
    public BaseMetadataContainerPanel() {
        super();
        initComponents();
    }
    
    public class ErrorMessage {
        java.awt.Component focusField;
        String errorMessage;
        
        ErrorMessage(java.awt.Component field, String msg) {
            this.focusField = field;
            this.errorMessage = msg;
        }
        
        void setFocusOnField(){
            if (focusField != null) {
                focusField.requestFocus();
            }
        }
        
        @Override
        public String toString(){
            return errorMessage;
        }
    }
    
    public String ErrorMessagesAsString(){
       StringBuilder sb = new StringBuilder();
        int count = 0;
        for (ErrorMessage msg : errorMessages) {
             sb.append(msg.toString());
             if (++count != errorMessages.size()) {
                 sb.append("\n");
             }
        }
        return sb.toString();
    }

    public void addErrorMessage(java.awt.Component comp, String msg){
        errorMessages.add(new ErrorMessage(comp, msg));
    }

   
    /**
     * The initvariables function sets the appropriate parameters used by the application. 
     * This function is called immediately after the constructor has been called.
     * @param ooDoc
     * @param parentFrm
     * @param aAction
     * @param aSubAction
     * @param dlgMode
     */
    public void initVariables(OOComponentHelper ooDoc, JFrame parentFrm, toolbarAction aAction, toolbarSubAction aSubAction, SelectorDialogModes dlgMode) {
        this.ooDocument = ooDoc;
        this.parentFrame = parentFrm;
        this.theAction = aAction;
        this.theSubAction = aSubAction;
        this.dialogMode = dlgMode;
    }

    /**
     * Call initialize() afte the constructor and after calling initvariables
     */
    public void initialize(){
        setupPanels();
        init();
    }
      
    public OOComponentHelper getOoDocument() {
        return ooDocument;
    }

    public JFrame getParentFrame() {
        return parentFrame;
    }

    public toolbarAction getTheAction() {
        return theAction;
    }

    public toolbarSubAction getTheSubAction() {
        return theSubAction;
    }

    public SelectorDialogModes getDialogMode() {
        return dialogMode;
    }
    
   public class panelInfo {
        String panelName;
        String panelClass;
        
        public panelInfo(String pname, String pclass){
            panelName = pname;
            panelClass = pclass;
        }
        
        @Override
        public String toString(){
            return panelName;
        }

        public IMetadataPanel getPanelObject() {
            IMetadataPanel panel = null;
            try {
                Class metadataPanel = Class.forName(panelClass);
                panel = (IMetadataPanel) metadataPanel.newInstance();
             } catch (InstantiationException ex) {
               log.debug("getPanelObject :"+ ex.getMessage());
               } catch (IllegalAccessException ex) {
               log.debug("getPanelObject :"+ ex.getMessage());
               }  catch (ClassNotFoundException ex) {
               log.debug("getPanelObject :"+ ex.getMessage());
              } catch (NullPointerException ex) {
               log.debug("getPanelObject :"+ ex.getMessage());
              } 
            finally {
                  return panel;
              }
        }

    
    }
    
    protected ArrayList<panelInfo> m_allPanels = new ArrayList<panelInfo>(0);
    /*
    {
            {
                add(new panelInfo("Title","org.bungeni.editor.selectors.debaterecord.masthead.Title"));
                add(new panelInfo("TabledDocuments", "org.bungeni.editor.selectors.debaterecord.masthead.TabledDocuments"));
            }
    };
     */ 
    
    protected ArrayList<panelInfo> m_activePanels = new ArrayList<panelInfo>();
    /*
    {
            {
                add(new panelInfo("Title","org.bungeni.editor.selectors.debaterecord.masthead.Title"));
                add(new panelInfo("TabledDocuments", "org.bungeni.editor.selectors.debaterecord.masthead.TabledDocuments"));
            }
    };*/
    
    abstract protected void setupPanels();
    
    protected ArrayList<panelInfo> getAllPanels(){
        return m_allPanels;
    }

    protected ArrayList<panelInfo> getActivePanels(){
        return m_activePanels;
    }
    
    protected void init(){
        //set null borders
        setBorder(null);
        paneMain.setBorder(null);
        
        JTaskPaneGroup mainTPgroup = new JTaskPaneGroup();
        
        for (panelInfo panelInf : getActivePanels()) {
            IMetadataPanel panel = panelInf.getPanelObject();
            panel.initVariables(this);
            mainTPgroup.add(panel.getPanelComponent());
        }
        mainTPgroup.setCollapsable(false);
        paneMain.add(mainTPgroup);
     //   paneMain.add(tpgTD);
    }
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        paneMain = new com.l2fprod.common.swing.JTaskPane();
        btnApply = new javax.swing.JButton();
        btnCancel = new javax.swing.JButton();

        com.l2fprod.common.swing.PercentLayout percentLayout2 = new com.l2fprod.common.swing.PercentLayout();
        percentLayout2.setGap(14);
        percentLayout2.setOrientation(1);
        paneMain.setLayout(percentLayout2);

        btnApply.setText("Apply");

        btnCancel.setText("Cancel");

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addGap(80, 80, 80)
                .addComponent(btnApply, javax.swing.GroupLayout.PREFERRED_SIZE, 88, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(btnCancel, javax.swing.GroupLayout.PREFERRED_SIZE, 85, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(86, 86, 86))
            .addComponent(paneMain, javax.swing.GroupLayout.DEFAULT_SIZE, 345, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addComponent(paneMain, javax.swing.GroupLayout.DEFAULT_SIZE, 70, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(btnCancel)
                    .addComponent(btnApply)))
        );

        getAccessibleContext().setAccessibleName("Enter Masthead");
    }// </editor-fold>//GEN-END:initComponents


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnApply;
    private javax.swing.JButton btnCancel;
    private com.l2fprod.common.swing.JTaskPane paneMain;
    // End of variables declaration//GEN-END:variables

    public static void main(String[] args){
       
    }
}
