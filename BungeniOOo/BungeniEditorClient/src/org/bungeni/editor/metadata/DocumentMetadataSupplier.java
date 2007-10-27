/*
 * DocumentMetadataFactory.java
 *
 * Created on October 26, 2007, 1:21 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.metadata;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Vector;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.db.QueryResults;
import org.bungeni.db.SettingsQueryFactory;

/**
 *
 * @author Administrator
 */
public class DocumentMetadataSupplier {
    
    private HashMap<String, DocumentMetadata> metadataMap = new HashMap<String, DocumentMetadata>();
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(DocumentMetadataSupplier.class.getName());

    private static int METADATA_NAME_COLUMN=0;
    private static int METADATA_DATATYPE_COLUMN=1;
    
    /** Creates a new instance of DocumentMetadataFactory */
    public DocumentMetadataSupplier() {
    }
    
    public DocumentMetadata[] getDocumentMetadataVariables () {
        String query = SettingsQueryFactory.Q_FETCH_DOCUMENT_METADATA_VARIABLES();
        ArrayList<DocumentMetadata> arrayMeta = new ArrayList<DocumentMetadata>();
        log.debug("getDocumentMetadataVariables :query = "+ query);
        String settingsInstance = DefaultInstanceFactory.DEFAULT_INSTANCE();
        BungeniClientDB db = new BungeniClientDB(settingsInstance, "");
        db.Connect();
        HashMap<String,Vector<Vector<String>>> resultsMap = db.Query(query);
        db.EndConnect();
        Vector<String> tableRow = new Vector<String>();
        QueryResults results = new QueryResults(resultsMap);
           if (results.hasResults() ) {
           Vector<Vector<String>> resultRows  = new Vector<Vector<String>>();
           resultRows = results.theResults();
           //it should always return a single row.... 
           //so we process the first row and brea
           for (int i = 0 ; i < resultRows.size(); i++ ) {
                   //get the results row by row into a string vector
                   tableRow = resultRows.elementAt(i);
                   String metaName = tableRow.elementAt(METADATA_NAME_COLUMN);
                   String metaDataType = tableRow.elementAt(METADATA_DATATYPE_COLUMN);
                   DocumentMetadata meta = new DocumentMetadata(metaName, "document", metaDataType);
                   arrayMeta.add(meta);
                   break;
           }
        } 
        if (arrayMeta.size() > 0 )
            return arrayMeta.toArray(new DocumentMetadata[arrayMeta.size()]);
        else
            return null;
    }
    
}
