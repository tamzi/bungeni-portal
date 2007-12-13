/*
 * BungeniError.java
 *
 * Created on December 12, 2007, 3:00 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.error;

/**
 *
 * @author Administrator
 */
public class BungeniError {
    /** Creates a new instance of BungeniError */
    public BungeniError() {
    }
   
    
    //Editor Selection Action errors
    
    public static final int SYSTEM_CONTAINER_NOT_REQD = -1000;
    public static final int SYSTEM_CONTAINER_CHECK_OK = -1001;
    public static final int SYSTEM_CONTAINER_WRONG_POSITION = -1002;
    public static final int SYSTEM_CONTAINER_NOT_PRESENT = -1003;
    
    public static final int NO_TEXT_SELECTED = -2001;
    public static final int DOCUMENT_ROOT_EXISTS = 2002 ;
    public static final int DOCUMENT_ROOT_DOES_NOT_EXIST = -2002;
    
    public static final int DOCUMENT_LEVEL_ACTION_RO0T_EXISTS = 3001;
    public static final int DOCUMENT_LEVEL_ACTION_ROOT_DOES_NOT_EXIST = 3002;
    
    public static final int METHOD_NOT_IMPLEMENTED = -9000;
    
}
