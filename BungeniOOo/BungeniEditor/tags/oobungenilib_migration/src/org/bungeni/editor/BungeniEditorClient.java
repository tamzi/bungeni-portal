/*
 * BungeniEditorClient.java
 *
 * Created on 2007.04.30 - 10:30:04
 *
 */

package org.bungeni.editor;

import com.sun.star.uno.XComponentContext;
import com.sun.star.comp.helper.Bootstrap;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import javax.swing.JFrame;
import javax.swing.UIManager;
import org.bungeni.editor.dialogs.editorApplicationController;

/**
 *
 * @author Administrator
 */
public class BungeniEditorClient {
    private static XComponentContext m_xContext;
    private static String __WINDOW_TITLE__="Bungeni Editor Client";
    /** Creates a new instance of BungeniEditorClient */
    public BungeniEditorClient() {
    }
    
    /**
     * @param args the command line arguments
     */
    private static void createAndShowGUI() {
        //Use the Java look and feel.
        try {
           
            UIManager.setLookAndFeel(
               UIManager.getCrossPlatformLookAndFeelClassName());
        } catch (Exception e) { }

        //Make sure we have nice window decorations.
       JFrame.setDefaultLookAndFeelDecorated(true);
       // JDialog.setDefaultLookAndFeelDecorated(true);

        //Instantiate the controlling class.
       JFrame frame = new JFrame(__WINDOW_TITLE__);
       frame.setResizable(false);
 
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        editorApplicationController panel = new editorApplicationController(m_xContext);
       // frame.addWindowListener(new org.bungeni.editor.BungeniPanelFrameWindowListener(panel));
        frame.add(panel);
        frame.setSize(615,400);
        //Display the window.
        frame.pack();
        frame.setLocationRelativeTo(null); //center it
        frame.setVisible(true);
    }
    
    public static void main(String[] args) {
        try {
            // get the remote office component context
            m_xContext = Bootstrap.bootstrap();
            javax.swing.SwingUtilities.invokeLater(
                        new Runnable() {
                                public void run() {
                                    createAndShowGUI();
                                }
                        }
            );
        }
        catch (java.lang.Exception e){
            e.printStackTrace();
        }
       // System.exit( 0 );
    }
    
}
