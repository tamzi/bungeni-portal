/*
 * ooProxyApp.java
 *
 * Created on 2007.08.19 - 15:32:42
 *
 */

package org.bungeni.ooo.proxy;

import com.sun.star.uno.XComponentContext;
import com.sun.star.comp.helper.Bootstrap;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.UIManager;

/**
 *
 * @author Administrator
 */
public class ooProxyApp {
    public static XComponentContext m_xContext = null;
    public static ooProxyPanel panel = null;
    /** Creates a new instance of ooProxyApp */
    public ooProxyApp() {
    }
    
    public static void createAndShowGUI(String url) {
          try {
            UIManager.setLookAndFeel(
                UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) { }

        //Make sure we have nice window decorations.
        JFrame.setDefaultLookAndFeelDecorated(true);
       // JDialog.setDefaultLookAndFeelDecorated(true);

        //Instantiate the controlling class.
       JFrame frame = new JFrame("OOo Proxy");
       frame.setResizable(false);
 
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        panel = new ooProxyPanel(m_xContext, url);
        frame.add(panel);
        frame.setSize(615,400);
        //Display the window.
        frame.pack();
        frame.setLocationRelativeTo(null); //center it
        frame.setVisible(true);
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
         try {
            // get the remote office component context
             final String URL = args[1];
             if (m_xContext == null ) 
             {  
                    m_xContext = Bootstrap.bootstrap();
                    javax.swing.SwingUtilities.invokeLater(
                                new Runnable() {
                                        public void run() {
                                            createAndShowGUI(URL);
                                        }
                                }
                    );
             } else {
                 JOptionPane.showMessageDialog(null, "the application has already been initialized");
             }
        }
        catch (java.lang.Exception e){
            e.printStackTrace();
        }
    }
    
}
