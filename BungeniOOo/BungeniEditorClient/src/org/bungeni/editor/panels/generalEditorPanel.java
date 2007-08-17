/*
 * generalEditorPanel.java
 *
 * Created on August 16, 2007, 4:06 PM
 */

package org.bungeni.editor.panels;

import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.net.URL;
import java.util.HashMap;
import java.util.Vector;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import org.bungeni.db.toolbarAction;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.utils.Installation;
import org.bungeni.db.QueryResults;
import org.bungeni.utils.SettingsDb;
import org.bungeni.db.SettingsQueryFactory;

/**
 *
 * @author  Administrator
 */
public class generalEditorPanel extends templatePanel implements ICollapsiblePanel , ActionListener {
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(generalEditorPanel.class.getName());
    private OOComponentHelper ooDocument;    
    /** Creates new form generalEditorPanel */
    public generalEditorPanel() {
        initComponents();
        loadToolbarButtons();
    }
    
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    // <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    private void initComponents() {
        generalEditorScrollPane = new javax.swing.JScrollPane();
        treeGeneralEditor = new javax.swing.JTree();

        generalEditorScrollPane.setViewportView(treeGeneralEditor);

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(generalEditorScrollPane, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 216, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(generalEditorScrollPane, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 156, Short.MAX_VALUE)
        );
    }// </editor-fold>//GEN-END:initComponents

    public void setOOComponentHandle(OOComponentHelper ooComponent) {
        ooDocument = ooComponent;
    }

    public Component getObjectHandle() {
        return this;
    }

    public ItoolbarButtonEvent getEventClass(String btnCommand) {
        return new ItoolbarButtonEvent() {

            public void doCommand(OOComponentHelper ooDocument) {
            }

            public void doCommand(OOComponentHelper ooDocument, String cmd) {
            }
        };
    }

    public void actionPerformed(ActionEvent e) {
    }

    private void initButtons() {
        /*
        toolbarGeneralToolbar.setFloatable(false);
        //toolbarSectionButtons.setBorder(contentBorder);
        toolbarGeneralToolbar.setRollover(true);
        toolbarGeneralToolbar.setOpaque(false);
        JButton btnSectionPrayer = createButton("icon_01", "makePrayerSection", "Create a Prayer Section", "Prayer");
        toolbarGeneralToolbar.add(btnSectionPrayer);
        JButton btnSectionPaper = createButton("icon_02", "makePaperSection", "Create a Paper Section", "Paper");
        toolbarGeneralToolbar.add(btnSectionPaper);
        JButton btnNoticeOfMotion = createButton("icon_03", "makeNoticeOfMotionSection", "Create a Notice-of-Motion Section", "Notice of Motion");
        toolbarGeneralToolbar.add(btnNoticeOfMotion);
        JButton btnQuestionAnswerSection = createButton("icon_04", "makeQASection", "Create a Question-Answer Section", "Question Answer Section");
        toolbarGeneralToolbar.add(btnQuestionAnswerSection);
        JButton btnQuestionBlockSection = createButton("icon_05", "makeQuestionBlockSection", "Create a Question-Block Section", "Question Answer Section");
        toolbarGeneralToolbar.add(btnQuestionBlockSection);
        */ 
    }
    
    protected JButton createButton(String imageName, String actionCommand, String tooltipText, String altText){
        JButton btn = super.createButton( imageName,  actionCommand,  tooltipText,  altText);
        btn.addActionListener(this);
        return btn;
    }
    
    private void buildActionTree(String point) {
      //  static boolean bStart = false;
    }
    
    toolbarAction baseAction;
    public void loadToolbarButtons() {
        
        //toolbarGeneralToolbar.setFloatable(false);
        //toolbarSectionButtons.setBorder(contentBorder);
        //toolbarGeneralToolbar.setRollover(true);
        //toolbarGeneralToolbar.setOpaque(false);
        log.debug("in loadToolbarButtons");
        Installation install = new Installation();
        String installDirectory = install.getAbsoluteInstallDir();
        BungeniClientDB instance = new BungeniClientDB(installDirectory + File.separator + "settings" + File.separator + "db" + File.separator, "");
        
        if (instance.Connect()) {
            log.debug("db connected");
           Vector<Vector> results = new Vector<Vector>();
           //query the db for the parent level buttons
           results = instance.Query(SettingsQueryFactory.Q_FETCH_PARENT_TOOLBAR_ACTIONS());
           log.debug("no.of results = "+ results.size());
           
           QueryResults query_results = new QueryResults (results);
           log.debug("Query has results = "+ (query_results.hasResults()? "true":"false" ));
           int nLevel = 0;
           if (query_results.hasResults() ) {
               results = query_results.theResults();
               //query_results.print_columns();
               //toolbarAction actionRoot = new toolbarAction("rootNode");
               
               HashMap columns = query_results.columnNameMap();
               for (int i = 0 ; i < results.size(); i++ ) {
                   //get the results row by row into a string vector
                   Vector<String> tableRow = new Vector<String>();
                   tableRow = results.elementAt(i);
                   //addToTree (tableRow, columns);
                   toolbarAction action = new toolbarAction(tableRow, columns);
                  
                    //action.brains();
                   System.out.println(" ");
                   //results are contained in the tableRow object
                   //row by row...
                //System.out.println(" action order = " + query_results.getColumnIndex("ACTION_ORDER"));
                //System.out.println(" action name = " + query_results.getColumnIndex("ACTION_NAME"));
               }
               
           } 
        } else {
            log.debug("connection failed ");
        }
    }
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JScrollPane generalEditorScrollPane;
    private javax.swing.JTree treeGeneralEditor;
    // End of variables declaration//GEN-END:variables
    
}
