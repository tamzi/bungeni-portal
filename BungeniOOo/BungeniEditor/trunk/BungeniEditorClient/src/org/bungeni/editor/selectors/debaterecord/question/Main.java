/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.editor.selectors.debaterecord.question;

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
    
    @Override
    protected void setupPanels() {
       m_allPanels = new ArrayList<panelInfo>(){
                {
                    add(new panelInfo("QuestionSelect", "org.bungeni.editor.selectors.debaterecord.question.QuestionSelect"));
                    add(new panelInfo("QuestionTitle", "org.bungeni.editor.selectors.debaterecord.question.QuestionTitle"));
                    add(new panelInfo("QuestionNameAndURI", "org.bungeni.editor.selectors.debaterecord.question.QuestionNameAndURI"));
                    add(new panelInfo("QuestionAddressedTo","org.bungeni.editor.selectors.debaterecord.question.QuestionAddressedTo"));
                    add(new panelInfo("QuestionText", "org.bungeni.editor.selectors.debaterecord.question.QuestionText"));
                }
        };
    
       m_activePanels = new ArrayList<panelInfo>(){
            {
                    add(new panelInfo("QuestionSelect", "org.bungeni.editor.selectors.debaterecord.question.QuestionSelect"));
                    add(new panelInfo("QuestionTitle", "org.bungeni.editor.selectors.debaterecord.question.QuestionTitle"));
                    add(new panelInfo("QuestionerNameAndURI", "org.bungeni.editor.selectors.debaterecord.question.QuestionerNameAndURI"));
                    add(new panelInfo("QuestionAddressedTo","org.bungeni.editor.selectors.debaterecord.question.QuestionAddressedTo"));
                    add(new panelInfo("QuestionText", "org.bungeni.editor.selectors.debaterecord.question.QuestionText"));
            }
         };
    }

     public static void main(String[] args){
        Main m = new Main();
        m.initialize();
        JFrame f = new JFrame("MastHead title");
        f.add(m);
        f.pack();
        f.setVisible(true);
    }

    @Override
    public Component getPanelComponent() {
        return this;
    }

}
