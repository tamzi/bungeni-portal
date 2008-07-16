/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.utils;

import java.awt.Component;
import java.awt.Dimension;
import javax.swing.JFrame;

/**
 *
 * @author undesa
 */
public class FrameLauncher {

  
    public static JFrame InitializeFrame(String frameTitle, Component panelComponent, Dimension launchDimension) {
            //initialize
            JFrame launch = new JFrame();
            launch.setTitle(frameTitle);
            if (launchDimension != null)
                launch.setSize(launchDimension);
            launch.add(panelComponent);
            
            return launch;
    }

    public static void LaunchFrame (JFrame f, boolean alwaysOnTop, boolean centerWindow) {
        f.setVisible(true);
        if (alwaysOnTop) {
            f.toFront();
            f.setAlwaysOnTop(alwaysOnTop);
        }
    }
}
