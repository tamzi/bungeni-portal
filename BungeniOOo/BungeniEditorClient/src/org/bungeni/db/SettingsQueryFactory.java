/*
 * SettingsQueryFactory.java
 *
 * Created on August 16, 2007, 4:40 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.db;

/**
 *
 * @author Administrator
 */
public class SettingsQueryFactory {
    
    /** Creates a new instance of SettingsQueryFactory */
    public SettingsQueryFactory() {
    }
    
    public static String Q_FETCH_PARENT_TOOLBAR_ACTIONS() {
        String query = new String("" +
                "Select * from toolbar_action_settings " +
                "where action_parent='parent' " +
                "order by action_order");
        return  query;
    }
    
    public static String Q_FETCH_CHILD_TOOLBAR_ACTIONS(String parent_name) {
        String query = new String("" +
                "Select * from toolbar_action_settings " +
                "where action_parent='"+ parent_name  + "' " +
                "order by action_order");
        return  query;
    }
    public static String Q_FETCH_EDITOR_PROPERTY(String propertyName) {
        String query = new String("" +
                "Select * from general_editor_properties " +
                "where property_name='"+ propertyName  + "' " );
        return  query;
    }
        
  
}
