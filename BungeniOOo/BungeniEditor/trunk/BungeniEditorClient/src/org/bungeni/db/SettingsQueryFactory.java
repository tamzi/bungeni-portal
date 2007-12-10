/*
 * SettingsQueryFactory.java
 *
 * Created on August 16, 2007, 4:40 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.db;

import org.bungeni.editor.BungeniEditorProperties;

/**
 *
 * @author Administrator
 */
public class SettingsQueryFactory {
    
    /** Creates a new instance of SettingsQueryFactory */
    public SettingsQueryFactory() {
    }
    
    public static String Q_FETCH_CHILD_TOOLBAR_ACTIONS(String parent_name) {
        String query = new String("" +
                "Select doc_type,action_name,action_order,action_state,action_class, " +
                "action_type,action_naming_convention,action_numbering_convention," +
                "action_icon,action_display_text,action_dimension" +
                "from action_settings " +
                "where action_parent='"+ parent_name  + "' and action_state=1 " +
                "order by action_order");
        return  query;
    }
    
    private static String Common_ToolbarAction_Selection() {
        String query = "" +
                "SELECT distinct act.doc_type, act.action_name, act.action_order, " +
                "act.action_state, act.action_class, act.action_type, act.action_naming_convention, "+
                "act.action_numbering_convention, "+
                "act.action_icon, act.action_display_text, act.action_dimension, act.action_section_type, act.action_edit_dlg_allowed ";
         return query;       
    }
    public static String Q_FETCH_PARENT_ACTIONS() {
        String query = "" +
                "SELECT distinct act.doc_type, act.action_name, act.action_order, " +
                "act.action_state, act.action_class, act.action_type, act.action_naming_convention, "+
                "act.action_numbering_convention,  "+
                "act.action_icon, act.action_display_text, act.action_dimension, act.action_section_type, act.action_edit_dlg_allowed "+
                " FROM action_settings act inner join " +
                "action_parent p on (act.action_name = p.parent_action)"+
                " where p.parent_action not in (select action_name from action_parent) "+
                " order by action_order";
        return query;
    }
    
    public static String Q_FETCH_PARENT_ACTIONS (String byAction) {
       String query= "SELECT distinct act.doc_type, act.action_name, act.action_order," +
               "act.action_state, act.action_class, act.action_type, act.action_naming_convention, " +
               "act.action_numbering_convention, " +
               "act.action_icon, act.action_display_text, act.action_dimension, act.action_section_type, act.action_edit_dlg_allowed " +
               " FROM " +
               "action_settings act where act.action_name in " +
               "(select action_name from action_parent where " +
               "parent_action='"+byAction+"')";
       return query;        
    }
    
    public static String Q_FETCH_ACTION_BY_NAME(String byActionName ) {
        String query = Common_ToolbarAction_Selection() +
                " from action_settings act " +
                "where act.action_name = '"+ byActionName +"'";
               return query;
    }
    
    public static String Q_FETCH_DOCUMENT_METADATA_VARIABLES() {
        String activeDocument = BungeniEditorProperties.getEditorProperty("activeDocumentMode");
        String query = "select metadata_name, metadata_datatype, metadata_type, display_name, visible  " +
                " from document_metadata " +
                "where metadata_type = 'document'" +
                "and doc_type = '"+activeDocument+"' " +
                "order by display_order asc";
        return query;        
    }
    public static String Q_CHECK_IF_ACTION_HAS_PARENT(String actionName) {
        String query = "select count(parent_action) as the_count  from action_parent " +
                " where action_name ='"+actionName+"'";
        return query;

    }
    
       
    public static String Q_GET_PARENT_ACTIONS (String byAction) {
       String query= "SELECT distinct act.doc_type, act.action_name, act.action_order," +
               "act.action_state, act.action_class, act.action_type, act.action_naming_convention, " +
               "act.action_numbering_convention,  " +
               "act.action_icon, act.action_display_text, act.action_dimension FROM " +
               "action_settings act where act.action_name in " +
               "(select parent_action from action_parent where " +
               "action_name='"+byAction+"')";
       return query;        
    }
    
    public static String Q_GET_SECTION_PARENT (String actionName) {
        String query = "select action_naming_convention from action_settings  " +
                "where action_name in (select distinct parent_action from action_parent " +
                "where action_name  = '"+actionName+"')";
        return query;
    }
    
    public static String Q_FETCH_EDITOR_PROPERTY(String propertyName) {
        String query = new String("" +
                "Select property_name, property_value from general_editor_properties " +
                "where property_name='"+ propertyName  + "' " );
        return  query;
    }
        
   public static String Q_FETCH_NEIGBOURING_ACTIONS_deprecated (String preceeding, String following) {
        String query = "SELECT * FROM action_settings where action_type  = 'section'" +
                " and action_name not in (select action_name from action_parent) " +
                " and action_order in  ("+ preceeding +","+ following +") order by action_order asc";
         return query;       
   }

   public static String Q_FETCH_ALL_SELECTION_ACTIONS(String docType){
       String query = "select doc_type, parent_action_name, sub_action_name, sub_action_order, sub_action_state, action_type, " +
               "action_display_text, action_fields, action_class, system_container from sub_action_settings " +
               "where doc_type ='"+ docType +"'" ;
       return query;
   }


   public static String Q_FETCH_ZERO_LEVEL_SELECTION_ACTIONS(String docType){
       String query = "select doc_type, parent_action_name, sub_action_name, sub_action_order, sub_action_state, action_type, " +
               "action_display_text, action_fields, action_class, system_container from sub_action_settings " +
               "where doc_type = '"+ docType +"' and sub_action_order = 0 ";
       return query;
   }

   public static String Q_FETCH_CHILDREN_SELECTION_ACTIONS(String docType, String parentAction){
       String query = "select doc_type, parent_action_name, sub_action_name, sub_action_order, sub_action_state, action_type, " +
               "action_display_text, action_fields, action_class, system_container from sub_action_settings " +
               "where doc_type = '"+ docType +"' and parent_action_name = '"+ parentAction +"'  and sub_action_order > 0 ";
       return query;
   }
      
}

        