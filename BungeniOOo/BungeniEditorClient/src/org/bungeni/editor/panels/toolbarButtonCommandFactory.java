/*
 * toolbarButtonCommandFactory.java
 *
 * Created on July 24, 2007, 4:09 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.panels;

import java.util.Map;
import org.apache.commons.collections.map.HashedMap;
import org.apache.log4j.varia.NullAppender;
import org.bungeni.editor.panels.toolbarevents.toolbarButtonEventHandler;

/**
 *
 * @author Administrator
 */
public class toolbarButtonCommandFactory extends Object {
    private static Map commandsMap=null;
    private static final ItoolbarButtonEvent DEFAULT_EVENT_HANDLER = new org.bungeni.editor.panels.toolbarevents.toolbarButtonEventHandler();
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(toolbarButtonCommandFactory.class.getName());
 
    /** Creates a new instance of toolbarButtonCommandFactory */
    public toolbarButtonCommandFactory() {
    }
    
    public static ItoolbarButtonEvent getButtonEventHandler(String cmdName){
        log.debug("in factory class command = "+cmdName);
        ItoolbarButtonEvent iEvent = null;
        try {
            String className = getClassName( cmdName );
            if( className != null )
            {
            log.debug("in factory: getButtonEventHandler :" + className );    
            Class eventHandlerClass;
                eventHandlerClass = Class.forName(className);
                iEvent = (ItoolbarButtonEvent) eventHandlerClass.newInstance();
            }    
            else
                log.debug("in factory, class name was null ");
         } 
        catch (IllegalAccessException ex) {
                ex.printStackTrace();
            } catch (InstantiationException ex) {
                ex.printStackTrace();
            } catch (ClassNotFoundException ex) {
                ex.printStackTrace();
            }
         finally {   
            if( iEvent == null ) {
                log.debug("in factory, iEvent is null");
                return DEFAULT_EVENT_HANDLER;
            }
            else
                 return iEvent;
         }
    }
    
    
    private static String getClassName(String clsName){
        log.debug("in factory: getClass("+clsName+")");
        String strClass =  (String) getIdNameMap().get(clsName);
        if (strClass == null ){
            log.debug("in factory: getClass is null");
            return null;
        }
        else{
            log.debug("in factory: getClass is not null and is: "+ strClass);
            return strClass;
        }

    }
      /** Return the Id/Name map, create if necessary */
    private static Map getIdNameMap()
    {
        log.debug("in factory, getIdNameMap()");
        if( commandsMap == null )
            commandsMap = createCommandsMap();
        
        return commandsMap;
    }

    private static Map createCommandsMap(){
        Map cmds = new HashedMap();
        cmds.put("makePaperSection", "toolbarButtonEventHandler");
        cmds.put("makePrayerSection",  "toolbarButtonEventHandler");
        log.debug("in factory, createCommandsMap()");
        return cmds;
    }

    
}
