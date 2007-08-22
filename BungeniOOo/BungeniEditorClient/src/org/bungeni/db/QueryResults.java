/*
 * QueryResults.java
 *
 * Created on August 16, 2007, 5:39 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.db;

import java.util.HashMap;
import java.util.Set;
import java.util.Vector;
/**
 *
 * @author Administrator
 */
public class QueryResults {
   boolean hasResults = false;
   Vector<Vector> theResults = null ;
   HashMap metadataColumnNameMap = null;
   private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(QueryResults.class.getName());
 
    /** Creates a new instance of QueryResults */
    public QueryResults(HashMap results) {
        if (results.containsKey("results")) {
            theResults = (Vector<Vector>)results.get("results");
            hasResults = true;
        }
        metadataColumnNameMap = new HashMap();
        if (results.containsKey("columns")) {
            buildMetadataInfo((Vector<String>)results.get("columns"));
        }
        
    }
   
    public HashMap columnNameMap(){
        return metadataColumnNameMap;
    }
    public void print_columns () {
        Set keys = metadataColumnNameMap.keySet();
        String[] keyNames = new String[keys.size()];
        keyNames = (String[]) keys.toArray();
        System.out.println("Printing Columns");
        for (int i=0; i < keyNames.length ; i++) {
            System.out.println(keyNames[i]);
        }
    }
    public boolean hasResults() {
       return hasResults;
    }
    
    static int METADATA_ROW_INDEX = 0;
    public Vector<Vector> theResults() {
       return theResults;
    }
    
    private void buildMetadataInfo (Vector<String> metadataRow) {
         if (theResults.size() > 0 )  {
           //build metadata column map
                    for (int n=0; n < metadataRow.size(); n++ ) {
                     String column_name= "";
                     column_name = (String) metadataRow.elementAt(n);
                     //add to column name ==> column number mapping map
                     metadataColumnNameMap.put(column_name, new Integer(n+1));
                  }
       }
    }
    
    public int getColumnIndex (String column_name) {
        if (metadataColumnNameMap.containsKey(column_name)) {
           Integer column = (Integer) metadataColumnNameMap.get(column_name);
           return  (int)column;
        }
        return -1;
    }
    
}
