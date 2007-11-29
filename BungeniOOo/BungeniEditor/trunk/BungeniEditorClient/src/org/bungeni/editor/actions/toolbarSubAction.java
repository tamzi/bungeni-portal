/*
 * toolbarSubAction.java
 *
 * Created on November 28, 2007, 10:19 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.actions;

import java.util.HashMap;
import java.util.Vector;

/**
 *
 * @author Administrator
 */
public class toolbarSubAction {
    
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(toolbarSubAction.class.getName());
 
    private String doc_type;
    private String parent_action_name;
    private String sub_action_name;
    private String sub_action_order;
    private String sub_action_state;
    private String action_type;
    private String action_display_text;
    private String action_fields;
    
    /** Creates a new instance of toolbarSubAction */
    public toolbarSubAction(Vector<String> actionDesc, HashMap action_mapping) {
        
        this.sub_action_name = (String) safeGet(actionDesc, action_mapping, "SUB_ACTION_NAME");
        this.sub_action_order = (String) safeGet(actionDesc, action_mapping, "SUB_ACTION_ORDER");
        this.doc_type = (String) safeGet(actionDesc, action_mapping, "DOC_TYPE");
        this.action_type = (String) safeGet(actionDesc, action_mapping, "ACTION_TYPE");
        this.sub_action_state = (String) safeGet(actionDesc, action_mapping, "SUB_ACTION_STATE");
        this.parent_action_name = (String) safeGet(actionDesc, action_mapping, "PARENT_ACTION_NAME");
        this.action_fields = (String) safeGet(actionDesc, action_mapping, "ACTION_FIELDS");
        this.action_display_text = (String) safeGet(actionDesc, action_mapping, "ACTION_DISPLAY_TEXT");
        
    
    }
    
    public String toString() {
        return this.action_display_text();
    }
 
    private Object safeGet (Vector<String> actions, HashMap map, String key){
        Object o = null ;
        if (map.containsKey(key)) 
        {
            log.debug("safeGet: key matched - "+ key);
            Integer column = (Integer) map.get(key);
            log.debug("safeGet: column matched - "+ column);
            o = actions.elementAt(column-1);
            if (o == null ) log.debug("Key was found but vector reqturned null : " + key);
            return o;
        }
        else {
             log.debug("Key : "+ key + " was not found");
            return null;
        }
            
    }
    


    
    public String doc_type() {
        return doc_type;
    }

    public String parent_action_name() {
        return parent_action_name;
    }

  
    public String sub_action_name() {
        return sub_action_name;
    }

  
    public String sub_action_order() {
        return sub_action_order;
    }

  
    public String sub_action_state() {
        return sub_action_state;
    }

  
    public String action_type() {
        return action_type;
    }

  
    public String action_display_text() {
        return action_display_text;
    }

  
    public String action_fields() {
        return action_fields;
    }
 
}
