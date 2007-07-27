/*
 * MessageBox.java
 *
 * Created on June 21, 2007, 11:22 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.utils;

import java.awt.Component;
import javax.swing.JOptionPane;



public  class MessageBox extends Object {
    public static void OK(Component parent, String msg){
        JOptionPane.showMessageDialog(parent, msg );
    }
    
    public static void OK(String msg){
        JOptionPane.showMessageDialog(null, msg);
    }
    
    public static void OK(Component parent, String msg, String title,  int type){
        
        JOptionPane.showMessageDialog(parent, msg, title, type);
    }
}

