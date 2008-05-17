/*
 * DocumentSectionAdapterTreeModel.java
 *
 * Created on January 10, 2008, 10:05 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.providers;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Iterator;
import javax.swing.Timer;
import javax.swing.event.TreeModelEvent;
import javax.swing.event.TreeModelListener;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreeModel;
import javax.swing.tree.TreePath;
import org.bungeni.utils.BungeniBTree;
import org.jdom.Attribute;
import org.jdom.Document;

/**
 *
 * @author Administrator
 */
public class DocumentSectionAdapterTreeModel extends DefaultTreeModel {
   // private BungeniBTree document;
    private Timer treeModelTimer ;  
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(DocumentSectionAdapterTreeModel.class.getName());
 

    /**
     * Creates a new instance of DocumentSectionAdapterTreeModel
     */
    public DocumentSectionAdapterTreeModel(DocumentSectionAdapterTreeNode rootNode) {
       super(rootNode);
       treeModelTimer = new Timer(DocumentSectionProvider.TIMER_DELAY, new ActionListener(){
            public void actionPerformed(ActionEvent e) {
                setRoot(new DocumentSectionAdapterTreeNode(DocumentSectionProvider.getTreeRoot()));
                reload();
            }
       });
       treeModelTimer.setInitialDelay(1000);
       treeModelTimer.start();
    }
 
    public static DocumentSectionAdapterTreeModel create(){
        return new DocumentSectionAdapterTreeModel(new DocumentSectionAdapterTreeNode(DocumentSectionProvider.getTreeRoot()));
    }
    
    public Object getRoot() {
        return super.getRoot();
        
    }

    
    public void setRoot(DocumentSectionAdapterTreeNode root) {
        super.setRoot(root);
    }
   
   public Object getChild(Object parent, int index) {
        DocumentSectionAdapterTreeNode node = (DocumentSectionAdapterTreeNode) parent;
        return node.child(index);
   }

   public int getIndexOfChild(Object parent, Object child) {
        DocumentSectionAdapterTreeNode node = (DocumentSectionAdapterTreeNode) parent;
        return node.index((DocumentSectionAdapterTreeNode) child);
    }
   
    public int getChildCount(Object parent) {
        DocumentSectionAdapterTreeNode sectionNode = (DocumentSectionAdapterTreeNode)parent;
        return sectionNode.childCount();
    }

   //override from TreeModel
    public boolean isLeaf(Object node) {
        DocumentSectionAdapterTreeNode sectionNode = (DocumentSectionAdapterTreeNode)node;
        return ((sectionNode.childCount() == 0) ? true: false);
    }
 }
