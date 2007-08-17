/*
 * toolbarActionSettings.java
 *
 * Created on August 17, 2007, 5:16 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.db;

import java.util.HashMap;
import java.util.Vector;

/**
 *
 * @author Administrator
 */
public class toolbarAction {
    toolbarAction parent;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(toolbarAction.class.getName());
    Vector<toolbarAction> containedActions;
    private static String ROOT_ACTION_DISPLAY="Editing Actions";
    
    public String action_name;
    public String action_order;
    public String action_class;
    public String doc_type;
    public String action_type;
    public String action_naming_convention;
    public String action_numbering_convention;
    public String action_parent;
    public String action_icon;
    public String action_display_text;
    public String action_dimension;
    
           
    /** Creates a new instance of toolbarActionSettings */
    public toolbarAction(Vector<String> actionDesc, HashMap action_mapping) {
        log.debug("in toolbarAction constructor");
        try {
        
        containedActions = new Vector<toolbarAction>();     
        parent = null;
        
        action_name = (String) safeGet(actionDesc, action_mapping, "ACTION_NAME");
        action_order = (String) safeGet(actionDesc, action_mapping, "ACTION_ORDER");
        action_class = (String) safeGet(actionDesc, action_mapping, "ACTION_CLASS");
        doc_type = (String) safeGet(actionDesc, action_mapping, "DOC_TYPE");
        action_type = (String) safeGet(actionDesc, action_mapping, "ACTION_TYPE");
        action_naming_convention = (String) safeGet(actionDesc, action_mapping, "ACTION_NAMING_CONVENTION");
        action_numbering_convention = (String) safeGet(actionDesc, action_mapping, "ACTION_NUMBERING_CONVENTION");
        action_parent = (String) safeGet(actionDesc, action_mapping, "ACTION_PARENT");
        action_icon = (String) safeGet(actionDesc, action_mapping, "ACTION_ICON");
        action_display_text = (String) safeGet(actionDesc, action_mapping, "ACTION_DISPLAY_TEXT");
        action_dimension = (String) safeGet(actionDesc, action_mapping, "ACTION_DIMENSION");
        
        } catch (Exception e) {
            log.debug("error in toolbarAction constructor : " + e.getMessage());
            e.printStackTrace();
        }
        log.debug("finished toolbarAction constructor");
    }
    
    /*
     *Used only for defining the root action
     */
    public toolbarAction(String action) {
        if (action.equals("rootAction")){
            parent = null;
            containedActions = new Vector<toolbarAction>();
            action_display_text = ROOT_ACTION_DISPLAY;
        }
    }
    
    public static void makeLinktoChildren(toolbarAction theFather,
                                            toolbarAction[] childActions) {
        for (toolbarAction childAction : childActions) {
            theFather.containedActions.addElement(childAction);
            childAction.parent = theFather;
        }
    }

   public String toString() {
       return this.action_display_text;
   } 
   
   public toolbarAction getParent() {
       return parent;
   }
   
   public int getContainedActionsCount() {
       return containedActions.size();
   }
   
   public toolbarAction getContainedActionAt(int i) {
        return containedActions.elementAt(i);
   }
   
   public int getIndexOfContainedAction(toolbarAction childAction) {
       return containedActions.indexOf(childAction);
   }
   
    public void brains() {
        System.out.println("action_name = "+ action_name);
        System.out.println("action_parent = " + action_parent);
    }
    private Object safeGet (Vector<String> actions, HashMap map, String key){
        Object o = null ;
        if (map.containsKey(key)) 
        {
            log.debug("safeGet: key matched - "+ key);
            Integer column = (Integer) map.get(key);
            log.debug("safeGet: column matched - "+ column);
            o = actions.elementAt(column-1);
            if (o == null ) log.debug("Key was found but vector returned null : " + key);
            return o;
        }
        else {
             log.debug("Key : "+ key + " was not found");
            return null;
        }
            
    }
}
