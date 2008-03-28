/*
 * OfficeNumberingApp.java
 *
 * Created on 2008.02.19 - 15:09:07
 *
 */

package com.example;

import com.sun.star.uno.XComponentContext;
import com.sun.star.comp.helper.Bootstrap;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.JComponent;
import javax.swing.JFrame;
import org.bungeni.ooo.BungenioOoHelper;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooDocNoteStructure;
import org.bungeni.ooo.ooDocNotes;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.ooo.ooUserDefinedAttributes;
import org.numbering.dialogs.sectionNumbererPanel;

/**
 *
 * @author undesa
 */
public class OfficeNumberingApp {

    private static sectionNumbererPanel panel;
    
  
    
    /** Creates a new instance of OfficeNumberingApp */
    public OfficeNumberingApp() {
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        
       
        try {
            // get the remote office component context
            XComponentContext xContext = Bootstrap.bootstrap();
            
           javax.swing.JFrame frame = new javax.swing.JFrame("Section Numbering");
                  
            panel=new sectionNumbererPanel();
            JComponent newContentPane = new sectionNumbererPanel(xContext);
            frame.setContentPane(newContentPane);
            
            
            frame.pack();
            frame.setSize(320, 400);
            frame.setResizable(false);
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

            frame.setAlwaysOnTop(true);
            frame.setVisible(true);
        }
        catch (java.lang.Exception e){
            e.printStackTrace();
        }
        finally {
            //System.exit( 0 );
        }
    }
    
}
