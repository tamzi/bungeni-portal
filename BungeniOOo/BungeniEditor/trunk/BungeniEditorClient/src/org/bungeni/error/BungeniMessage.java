/*
 * BungeniMessage.java
 *
 * Created on December 17, 2007, 12:22 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.error;

/**
 *
 * @author Administrator
 */
public class BungeniMessage {
    private int n_message;
    private int n_next;
    
    public BungeniMessage(){
        n_message = 0;
        n_next = 0;
    }
    /** Creates a new instance of BungeniMessage */
    public BungeniMessage(int next, int message) {
        n_message = message;
        n_next = next;
    }
    
    public int getMessage(){
        return n_message;
    }
    
    public int getStep(){
        return n_next;
    }
    
}
