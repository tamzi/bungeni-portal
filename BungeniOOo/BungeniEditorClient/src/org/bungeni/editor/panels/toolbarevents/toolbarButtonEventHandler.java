/*
 * toolbarButtonEventHandler.java
 *
 * Created on July 24, 2007, 4:52 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.panels.toolbarevents;

import com.sun.star.text.XText;
import com.sun.star.text.XTextViewCursor;
import javax.swing.JOptionPane;
import org.bungeni.editor.panels.ItoolbarButtonEvent;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public class toolbarButtonEventHandler extends Object implements ItoolbarButtonEvent {
    private OOComponentHelper ooDocument = null;
    /** Creates a new instance of toolbarButtonEventHandler */
    public toolbarButtonEventHandler() {
    }

    public void doCommand(OOComponentHelper ooDocument, String cmd ) {
        if (this.ooDocument == null ) this.ooDocument = ooDocument;
        if (cmd.equals("makePrayerSection")){
            if (ooDocument.getTextSections().hasByName("prayers")){
               JOptionPane.showMessageDialog(null, "Section already exists!");
            }
            else {
                addTextSection("prayers");
            }
        }
    
    }

    
    public void doCommand(OOComponentHelper ooDocument) {
    }
    
    private void addTextSection(String sectionName){
        String sectionClass = "com.sun.star.text.TextSection";
        XTextViewCursor xCursor = ooDocument.getViewCursor();
        XText xText = xCursor.getText();
        
        
    }
    
}
