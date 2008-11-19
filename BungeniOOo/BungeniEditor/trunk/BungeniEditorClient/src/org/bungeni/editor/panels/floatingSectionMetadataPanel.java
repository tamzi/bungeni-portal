/*
 * floatingSectionMetadataPanel.java
 *
 * Created on November 19, 2008, 9:10 PM
 */

package org.bungeni.editor.panels;

import java.awt.Component;
import javax.swing.JFrame;
import org.bungeni.editor.actions.IEditorActionEvent;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.panels.impl.IFloatingPanel;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author  undesa
 */
public class floatingSectionMetadataPanel extends javax.swing.JPanel implements IFloatingPanel {

    /** Creates new form floatingSectionMetadataPanel */
    public floatingSectionMetadataPanel() {
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

        jScrollPane1 = new javax.swing.JScrollPane();
        tblSectionmeta = new javax.swing.JTable();
        lblDisplaySectionName = new javax.swing.JLabel();
        lblSecName = new javax.swing.JLabel();
        jLabel3 = new javax.swing.JLabel();
        jLabel4 = new javax.swing.JLabel();
        btnEdit = new javax.swing.JButton();
        btnHide = new javax.swing.JButton();

        tblSectionmeta.setFont(new java.awt.Font("DejaVu Sans", 0, 10)); // NOI18N
        tblSectionmeta.setModel(new javax.swing.table.DefaultTableModel(
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
        jScrollPane1.setViewportView(tblSectionmeta);

        lblDisplaySectionName.setFont(new java.awt.Font("DejaVu Sans", 0, 10)); // NOI18N
        lblDisplaySectionName.setText("::");

        lblSecName.setFont(new java.awt.Font("DejaVu Sans", 0, 10)); // NOI18N
        lblSecName.setText("Current Section Name :");

        jLabel3.setFont(new java.awt.Font("DejaVu Sans", 0, 10)); // NOI18N
        jLabel3.setText("::");

        jLabel4.setFont(new java.awt.Font("DejaVu Sans", 0, 10)); // NOI18N
        jLabel4.setText("Current Section Type:");

        btnEdit.setFont(new java.awt.Font("DejaVu Sans", 0, 10)); // NOI18N
        btnEdit.setText("Edit...");

        btnHide.setFont(new java.awt.Font("DejaVu Sans", 0, 10)); // NOI18N
        btnHide.setText("Hide");

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(lblDisplaySectionName, javax.swing.GroupLayout.DEFAULT_SIZE, 176, Short.MAX_VALUE)
                    .addComponent(lblSecName, javax.swing.GroupLayout.DEFAULT_SIZE, 176, Short.MAX_VALUE)
                    .addComponent(jLabel4, javax.swing.GroupLayout.DEFAULT_SIZE, 176, Short.MAX_VALUE)
                    .addComponent(jLabel3, javax.swing.GroupLayout.DEFAULT_SIZE, 176, Short.MAX_VALUE))
                .addContainerGap())
            .addGroup(layout.createSequentialGroup()
                .addComponent(btnEdit, javax.swing.GroupLayout.PREFERRED_SIZE, 80, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 30, Short.MAX_VALUE)
                .addComponent(btnHide, javax.swing.GroupLayout.PREFERRED_SIZE, 78, javax.swing.GroupLayout.PREFERRED_SIZE))
            .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 188, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(lblSecName)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(lblDisplaySectionName)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel4)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel3)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 220, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(btnEdit)
                    .addComponent(btnHide)))
        );
    }// </editor-fold>//GEN-END:initComponents


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnEdit;
    private javax.swing.JButton btnHide;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JLabel lblDisplaySectionName;
    private javax.swing.JLabel lblSecName;
    private javax.swing.JTable tblSectionmeta;
    // End of variables declaration//GEN-END:variables

    public void setOOComponentHandle(OOComponentHelper ooComponent) {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public Component getObjectHandle() {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public IEditorActionEvent getEventClass(toolbarAction action) {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public void setParentWindowHandle(JFrame c) {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public JFrame getParentWindowHandle() {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public void initUI() {
        throw new UnsupportedOperationException("Not supported yet.");
    }

}
