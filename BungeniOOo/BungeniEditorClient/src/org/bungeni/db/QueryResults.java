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
   Vector<Vector> theResults = null ;
   HashMap metadataColumnNameMap = null;
   private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(QueryResults.class.getName());
 
    /** Creates a new instance of QueryResults */
    public QueryResults(Vector<Vector> queryResults) {
        theResults = queryResults;
        metadataColumnNameMap = new HashMap();
        if (hasResults()) {
            buildMetadataInfo();
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
        if (theResults == null)
            return false;
        if (theResults.size() > 1 ) {
            return true;
        }
        return false;
    }
    
    static int METADATA_ROW_INDEX = 0;
    public Vector<Vector> theResults() {
       return theResults;
    }
    
    private void buildMetadataInfo () {
         if (theResults.size() > 1 )  {
           //build metadata column map
                  Vector<String> metadataRow = new Vector<String>();
                  metadataRow = (Vector<String>)theResults.elementAt(METADATA_ROW_INDEX);
                  for (int n=0; n < metadataRow.size(); n++ ) {
                     String column_name= "";
                     column_name = (String) metadataRow.elementAt(n);
                     //add to column name ==> column number mapping map
                     metadataColumnNameMap.put(column_name, new Integer(n+1));
                  }
                  theResults.remove(METADATA_ROW_INDEX);     
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
