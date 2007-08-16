/*
 * SettingsDb.java
 *
 * Created on August 15, 2007, 4:06 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.utils;

import java.io.File;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashMap;
import java.util.Vector;

/**
 *
 * @author Administrator
 */
public class SettingsDb {

    Connection m_Connection = null ;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(SettingsDb.class.getName());

    /** Creates a new instance of SettingsDb */
    static String path_prefix="settings"+File.separator+"db";
    static String db_name_prefix ="settings.db";
    
    public static void setDbPath(String path){
        path_prefix = path;
    }
    
      SettingsDb() {
        try {
            Class.forName("org.hsqldb.jdbcDriver");
            Installation install = new Installation(); 
            File dir = install.getInstallDirectory(this.getClass());
            
            String full_path = dir.getAbsolutePath();
            String relative_path = dir.getPath();
            System.out.println("full path = "+ full_path);
            System.out.println("relative path = " + relative_path);
            
            String connectionString = "jdbc:hsqldb:" + full_path + File.separator+ path_prefix + File.separator + db_name_prefix ;
            System.out.println("Connection String = "+ connectionString);
            m_Connection = DriverManager.getConnection( connectionString,    // filenames
                                                        "sa",   // username
                                                        "");   // password 
        } catch (SQLException ex) {
            log.debug("SettingsDB construct:"+ex.getLocalizedMessage());
        } catch (ClassNotFoundException ex) {
           log.debug("SettingsDB construct:"+ex.getLocalizedMessage());
        } 
     }
     
     SettingsDb(String db_file_name_prefix)  {    // note more general exception
        try { 
        Class.forName("org.hsqldb.jdbcDriver");
        // It can contain directory names relative to the
        // current working directory
        m_Connection = DriverManager.getConnection("jdbc:hsqldb:"
                                           + db_file_name_prefix,    // filenames
                                           "sa",                     // username
                                           "");                      // password
         } catch (SQLException ex) {
            log.debug("SettingsDB construct:"+ex.getLocalizedMessage());
        } catch (ClassNotFoundException ex) {
           log.debug("SettingsDB construct:"+ex.getLocalizedMessage());
        } 
    }

    public boolean isConnected() {
        if (m_Connection != null ) {
            return true;
        }
        return false;
    } 
    public synchronized HashMap query(String expression) {

        Statement st = null;
        ResultSet rs = null;
        HashMap results = new HashMap();
        
        try {
            
            st = m_Connection.createStatement();         // statement objects can be reused with
            // repeated calls to execute but we
            // choose to make a new one each time
            rs = st.executeQuery(expression);    // run the query

            // do something with the result set.
            results = dump(rs);
            st.close();    // NOTE!! if you close a statement the associated ResultSet is

            return results;
        } catch (SQLException ex) {
            log.debug("query:"+ ex.getLocalizedMessage());
        } finally {
            return results;
        }   
    }
 
   public static HashMap dump(ResultSet rs) {
        ResultSetMetaData meta;
        HashMap tblRecords = new HashMap();
        
        try {
            meta = rs.getMetaData();
            int colmax = meta.getColumnCount();
            int  i;
            String oField = "";

            for (; rs.next(); ) {
                String key = "";
                Vector<String> vRecord = new Vector<String>();
                for (i = 0; i < colmax; ++i) {
                    oField = (String) rs.getObject(i + 1);   
                    // with 1 not 0
                    vRecord.addElement(oField);
                }
                tblRecords.put(vRecord.elementAt(0), vRecord);
          }
         } catch (SQLException ex) {
            log.debug("dump:"+ex.getLocalizedMessage());
        } finally {
            return tblRecords;
        }
    }    
   
     public void shutdown() throws SQLException {

        Statement st = m_Connection.createStatement();

        // db writes out to files and performs clean shuts down
        // otherwise there will be an unclean shutdown
        // when program ends
        st.execute("SHUTDOWN");
        m_Connection.close();    // if there are no other open connection
    }
     
    
    
}
