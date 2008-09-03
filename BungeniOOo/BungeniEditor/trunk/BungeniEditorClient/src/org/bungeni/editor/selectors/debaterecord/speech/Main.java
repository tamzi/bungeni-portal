/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.editor.selectors.debaterecord.speech;

import java.awt.Component;
import java.util.ArrayList;
import javax.swing.JFrame;
import org.bungeni.editor.selectors.BaseMetadataContainerPanel;

/**
 *
 * @author undesa
 */
public class Main extends BaseMetadataContainerPanel {
    public Main(){
        super();
    }
    
      public static void main(String[] args){
        Main m = new Main();
        JFrame f = new JFrame("MastHead title");
        f.add(m);
        f.pack();
        f.setVisible(true);
    }
      
    @Override
    protected void setupPanels() {
       m_allPanels = new ArrayList<panelInfo>(){
                {
                    add(new panelInfo("PersonSelector","org.bungeni.editor.selectors.debaterecord.speech.PersonSelector"));
                    add(new panelInfo("PersonURI", "org.bungeni.editor.selectors.debaterecord.speech.PersonURI"));
                    add(new panelInfo("SpeechBy", "org.bungeni.editor.selectors.debaterecord.speech.SpeechBy"));
                }
        };
    
       m_activePanels = new ArrayList<panelInfo>(){
            {
                    add(new panelInfo("PersonSelector","org.bungeni.editor.selectors.debaterecord.speech.PersonSelector"));
                    add(new panelInfo("PersonURI", "org.bungeni.editor.selectors.debaterecord.speech.PersonURI"));
                    add(new panelInfo("SpeechBy", "org.bungeni.editor.selectors.debaterecord.speech.SpeechBy"));
            }
         };
    }

    @Override
    public Component getPanelComponent() {
       return this;
    }

}
