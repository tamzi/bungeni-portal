/*
 * QuestionAddressedTo.java
 *
 * Created on August 12, 2008, 2:06 PM
 */

package org.bungeni.editor.selectors.debaterecord.question;

import com.sun.star.text.XTextSection;
import java.awt.Component;
import java.util.HashMap;
import org.bungeni.editor.selectors.BaseMetadataPanel;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author  undesa
 */
public class QuestionAddressedTo extends BaseMetadataPanel {

    /** Creates new form QuestionAddressedTo */
    public QuestionAddressedTo() {
        initComponents();
    }

    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        txtAddressedTo = new javax.swing.JTextField();
        lblQuestionAddressedTo = new javax.swing.JLabel();

        txtAddressedTo.setName("txt_question_to"); // NOI18N

        lblQuestionAddressedTo.setText("Question Addressed To :");
        lblQuestionAddressedTo.setName("lbl_question_to"); // NOI18N

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(lblQuestionAddressedTo, javax.swing.GroupLayout.PREFERRED_SIZE, 265, javax.swing.GroupLayout.PREFERRED_SIZE)
            .addComponent(txtAddressedTo, javax.swing.GroupLayout.DEFAULT_SIZE, 279, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(lblQuestionAddressedTo)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(txtAddressedTo, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
        );
    }// </editor-fold>//GEN-END:initComponents


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JLabel lblQuestionAddressedTo;
    private javax.swing.JTextField txtAddressedTo;
    // End of variables declaration//GEN-END:variables

public String getPanelName() {
        return getName();
    }

    public Component getPanelComponent() {
        return this;
    }


    @Override
    public boolean doCancel() {
        return true;
    }

    @Override
    public boolean doReset() {
        return true;
    }

    @Override
    public boolean preFullEdit() {
        return true;
    }

    @Override
    public boolean processFullEdit() {
        return true;
    }

    @Override
    public boolean postFullEdit() {
        return true;
    }

    @Override
    public boolean preFullInsert() {
        return true;
    }

    @Override
    public boolean processFullInsert() {
        return true;
    }

    @Override
    public boolean postFullInsert() {
        return true;
    }

    @Override
    public boolean preSelectEdit() {
        return true;
    }

    @Override
    public boolean processSelectEdit() {
        return true;
    }

    @Override
    public boolean postSelectEdit() {
        return true;
    }

    @Override
    public boolean preSelectInsert() {
        return true;
    }

    @Override
    public boolean processSelectInsert() {
        OOComponentHelper ooDoc = getContainerPanel().getOoDocument();
        HashMap<String,String> sectionMeta = new HashMap<String,String>();
        String newSectionName = ((Main)getContainerPanel()).mainSectionName;
        sectionMeta.put("BungeniQuestionTo", this.txtAddressedTo.getText());
        ooDoc.setSectionMetadataAttributes(newSectionName, sectionMeta);
        //ooDoc.setSectionMetadataAttributes(TOOL_TIP_TEXT_KEY, metadataMap);
        return true;
    }

    @Override
    public boolean postSelectInsert() {
       return true;
    }

    @Override
    public boolean validateSelectedEdit() {
        return true;
    }

    @Override
    public boolean validateSelectedInsert() {
        return true;
    }

    @Override
    public boolean validateFullInsert() {
        return true;
    }

    @Override
    public boolean validateFullEdit() {
        return true;
    }

    @Override
    public void commonInitFields(){
          switch (getDialogMode()) {
            case TEXT_EDIT:
                return;
              default: return;
          }
    }
    
    @Override
    protected void initFieldsSelectedEdit() {
        return;
    }

    @Override
    protected void initFieldsSelectedInsert() {
        return;
    }

    @Override
    protected void initFieldsInsert() {
        return;
    }

    @Override
    protected void initFieldsEdit() {
        //connect fields to metadata... 
        this.txtAddressedTo.setText(getSectionMetadataValue("BungeniQuestionTo"));
        return;
    }
    
    @Override
    public boolean doUpdateEvent(){
        HashMap<String,String> selectionData = ((Main)getContainerPanel()).selectionData;   
        if (selectionData != null ) {
            if (selectionData.containsKey("QUESTION_TO"))
            this.txtAddressedTo.setText(selectionData.get("QUESTION_TO"));
        }
        return true;
    }
}
