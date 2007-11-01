/*
 * DocumentMetadataTableMouseListener.java
 *
 * Created on October 30, 2007, 5:55 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.metadata;

import java.awt.Point;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import javax.swing.JDialog;
import javax.swing.JTable;

/**
 *
 * @author Administrator
 */
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
            JDialog dlg;
            dlg = panelEditDocumentMetadata.Launch( metadataObj);
            panelEditDocumentMetadata objPanel = (panelEditDocumentMetadata)dlg.getContentPane().getComponent(0);
            if (objPanel.isCancelClicked())
                   return;
            metadataObj = objPanel.getDocumentMetadata(); 
            //pass the metadata object to update the document to metadata;
            mModel.getMetadataSupplier().updateMetadataToDocument();
            //System.out.println("metadata OnClick = " + metadataObj.toString()); 
            /*
            if (fileType.equals("folder")) {
                log.debug("folder: "+fileName + "was clicked");
                //switch to the clicked folder
                //first get the table model
                WebDavTableModel davModel = (WebDavTableModel) tblServerFiles.getModel();
                davModel.brains();
                davModel.setPathRelative(fileName);
            }
            else
                log.debug("file was clicked");
             */
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
