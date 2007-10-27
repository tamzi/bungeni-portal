/*
 * DocumentMetadataTableModel.java
 *
 * Created on October 27, 2007, 2:35 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.metadata;

import javax.swing.table.AbstractTableModel;
import org.apache.log4j.Logger;

/**
 *
 * @author Administrator
 */
public class DocumentMetadataTableModel extends AbstractTableModel {
    DocumentMetadata[] documentMetadata;
    String[] column_names = {"Name", "Value" };
    private static org.apache.log4j.Logger log = Logger.getLogger(DocumentMetadataTableModel.class.getName());
  
    /** Creates a new instance of DocumentMetadataTableModel */
    public DocumentMetadataTableModel() {
        //retrieve set of metadata applicable for this document
        DocumentMetadataSupplier metaSupplier = new DocumentMetadataSupplier();
        documentMetadata = DocumentMetametaSupplier.getDocumentMetadataVariables();
    }

    public int getRowCount() {
        return 0;
    }

    public int getColumnCount() {
        return 0;
    }

    public Object getValueAt(int rowIndex, int columnIndex) {
        return 0;
    }
    
}
