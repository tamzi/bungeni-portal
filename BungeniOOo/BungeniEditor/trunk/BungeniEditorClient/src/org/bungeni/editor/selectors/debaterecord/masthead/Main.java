/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.editor.selectors.debaterecord.masthead;

import java.util.ArrayList;
import org.bungeni.editor.selectors.BaseMetadataContainerPanel;

/**
 *
 * @author undesa
 */
public class Main extends BaseMetadataContainerPanel {

    public Main() {
        super();
    }
    
    @Override
    protected void setupPanels() {
       m_allPanels = new ArrayList<panelInfo>(){
                {
                    add(new panelInfo("DebateRecordDate","org.bungeni.editor.selectors.debaterecord.masthead.DebateRecordDate"));
                    add(new panelInfo("DebateRecordTime", "org.bungeni.editor.selectors.debaterecord.masthead.DebateRecordTime"));
                    add(new panelInfo("DebateRecordLogo", "org.bungeni.editor.selectors.debaterecord.masthead.DebateRecordLogo"));
                }
        };
    
       m_activePanels = new ArrayList<panelInfo>(){
            {
                    add(new panelInfo("DebateRecordDate","org.bungeni.editor.selectors.debaterecord.masthead.DebateRecordDate"));
                    add(new panelInfo("DebateRecordTime", "org.bungeni.editor.selectors.debaterecord.masthead.DebateRecordTime"));
                    add(new panelInfo("DebateRecordLogo", "org.bungeni.editor.selectors.debaterecord.masthead.DebateRecordLogo"));
            }
         };
    }

     public static void main(String[] args){
        Main m = new Main();
        javax.swing.JFrame f = new javax.swing.JFrame("MastHead title");
        f.add(m);
        f.pack();
        f.setVisible(true);
    }
}
