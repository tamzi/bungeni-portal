/*
 * MessageBox.java
 *
 * Created on June 21, 2007, 11:22 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.utils;

/**
 *
 * @author Administrator
 */
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JButton;
import javax.swing.JWindow;



public class MessageBox {
    public static int MB_OK = 1;
    public static int MB_CANCEL = 2;
    public static int MB_IGNORE = 2;
    public static int MB_RETRY = 2;

    public static int message(String caption, String title, int buttons) {
        MessageWindow mw = new MessageWindow(caption, title, buttons);
        
        return 0;
    
    }
    
    public static int message(String caption, String title) {
        return message(caption, title, MB_OK);    
    }             

    
    
    static class MessageWindow extends JWindow {
        private int result;
        
        MessageWindow(String title, String caption, int buttons) {
            setLayout(new FlowLayout(FlowLayout.CENTER));
            
            addWindowListener(new WindowAdapter() {
                public void windowClosing(WindowEvent e) {
                    dispose();
                }

                public void windowClosed(WindowEvent e) {
                    dispose();
                }
            });           
            
            
                        
            JButton btn = new JButton("Ok");
            btn.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent ae) {
                    result = MB_OK;
                    close();                    
                }                
            });
            add(btn);
            

            // retry            
            if ( (buttons & MB_RETRY) > 0 ) {
                btn = new JButton("Retry");
                btn.addActionListener(new ActionListener() {
                    public void actionPerformed(ActionEvent ae) {
                        result = MB_RETRY;
                        close();                    
                    }                
                });  
                add(btn);  
            }

            // ignore             
            if ( (buttons & MB_IGNORE) > 0 ) {
                btn = new JButton("Ignore");
                btn.addActionListener(new ActionListener() {
                    public void actionPerformed(ActionEvent ae) {
                        result = MB_IGNORE;
                        close();                    
                    }                
                });    
                add(btn);
            }

            // cancel
            if ( (buttons & MB_CANCEL) > 0 ) {
                btn = new JButton("Cancel");
                btn.addActionListener(new ActionListener() {
                    public void actionPerformed(ActionEvent ae) {
                        result = MB_CANCEL;
                        close();                    
                    }    
                });    
                add(btn);
            }
            
            pack();
            setVisible(true);
        }


        
        
        private void close() {
                    
                    
        }
    }
    

}
