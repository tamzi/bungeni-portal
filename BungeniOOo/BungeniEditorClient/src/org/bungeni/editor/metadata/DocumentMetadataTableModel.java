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
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public class DocumentMetadataTableModel extends AbstractTableModel {
    DocumentMetadataSupplier metaSupplier;
    OOComponentHelper ooDocument;
    String[] column_names = {"Name", "Value" };
    private static org.apache.log4j.Logger log = Logger.getLogger(DocumentMetadataTableModel.class.getName());
  
    /** Creates a new instance of DocumentMetadataTableModel */
    public DocumentMetadataTableModel(OOComponentHelper ooDoc) {
        //retrieve set of metadata applicable for this document
        this.ooDocument = ooDoc;
        metaSupplier = new DocumentMetadataSupplier(ooDocument);
    }

    public int getRowCount() {
        return metaSupplier.getVisibleCount();
    }

    public int getColumnCount() {
        return this.column_names.length;
    }

    public Object getValueAt(int rowIndex, int columnIndex) {
        DocumentMetadata[] metas = this.metaSupplier.getDocumentMetadata();
        DocumentMetadata rowMeta = metas[rowIndex];
        if (columnIndex == 0){
            rowMeta.getDisplayName();
        } else if (columnIndex == 1) {
            rowMeta.getValue();
        }
        return 0;
    }
    
    public Class getColumnClass(int col) { 
      return String.class;
  }
  
}
