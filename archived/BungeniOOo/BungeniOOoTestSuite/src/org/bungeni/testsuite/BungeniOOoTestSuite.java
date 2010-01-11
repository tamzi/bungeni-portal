/*
 * BungeniOOoTestSuite.java
 *
 * Created on 2007.08.01 - 22:31:29
 *
 */

package org.bungeni.testsuite;
/*
 * Main.java
 *
 * Created on September 1, 2007, 9:42 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */


import com.sun.star.comp.helper.Bootstrap;
import com.sun.star.lang.XComponent;
import com.sun.star.uno.XComponentContext;
import javax.swing.JFrame;
import javax.swing.UIManager;
import org.bungeni.ooo.BungenioOoHelper;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public class BungeniOOoTestSuite {
    private static XComponentContext xContext;

    private static String templatePath;
    /** Creates a new instance of Main */
    public BungeniOOoTestSuite() {
    }
    
      private static void createAndShowGUI() {
        //Use the Java look and feel.
        try {
            UIManager.setLookAndFeel(
                UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) { }

        //Make sure we have nice window decorations.
        JFrame.setDefaultLookAndFeelDecorated(true);
       // JDialog.setDefaultLookAndFeelDecorated(true);

        //Instantiate the controlling class.
       JFrame frame = new JFrame("Bungeni OO Test Suite");
       frame.setResizable(false);
 
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
     
        testBungeniLibs panel = new testBungeniLibs(xContext);
        frame.add(panel);
        frame.setSize(615,400);
        //Display the window.
        frame.pack();
        frame.setLocationRelativeTo(null); //center it
        frame.setAlwaysOnTop(true);
        frame.setVisible(true);
    }
    
    /**
     * @param args the command line arguments
     */
 public static void main(String[] args) {
        try {
            // get the remote office component context
            xContext = Bootstrap.bootstrap();
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
