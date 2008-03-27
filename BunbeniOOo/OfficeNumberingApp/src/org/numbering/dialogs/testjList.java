/*
 * testjList.java
 *
 * Created on March 20, 2008, 12:18 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.numbering.dialogs;

import javax.swing.JFrame;
import javax.swing.JList;

/**
 *
 * @author undesa
 */
public class testjList extends javax.swing.JPanel{

    private static sectionNumbererPanel panel;
    
    /** Creates a new instance of testjList */
    public testjList() {
    }
    
    public static void main(String[] args){
        javax.swing.JFrame frame = new javax.swing.JFrame("Section Numbering");
        String[] data = {"one", "two", "three", "four"};
        JList dataList = new JList(data);
        panel=new sectionNumbererPanel();
          frame.getContentPane().add(panel);
          frame.add(dataList);
            frame.pack();
            frame.setSize(320, 400);
            frame.setResizable(false);
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

            frame.setAlwaysOnTop(true);
            frame.setVisible(true);
        
    }
    
}
