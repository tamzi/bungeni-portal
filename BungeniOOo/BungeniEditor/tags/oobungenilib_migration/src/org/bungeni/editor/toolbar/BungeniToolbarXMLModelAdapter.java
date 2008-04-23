/*
 * BungeniToolbarXMLModelAdapter.java
 *
 * Created on January 10, 2008, 10:05 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.toolbar;

import java.util.ArrayList;
import java.util.Iterator;
import javax.swing.event.TreeModelEvent;
import javax.swing.event.TreeModelListener;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreeModel;
import javax.swing.tree.TreePath;
import org.jdom.Attribute;
import org.jdom.Document;

/**
 *
 * @author Administrator
 */
public class BungeniToolbarXMLModelAdapter extends AbstractTreeModel {
    private Document document;
      private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(BungeniToolbarXMLModelAdapter.class.getName());
 
    /** Creates a new instance of BungeniToolbarXMLModelAdapter */
    public BungeniToolbarXMLModelAdapter() {
    }

    
    /** Creates a new instance of BungeniToolbarXMLModelAdapter */
    public BungeniToolbarXMLModelAdapter(Document doc) {
        this.document = doc;
    }
 
    public Object getRoot() {
        if (document == null ) return null;
        return new BungeniToolbarXMLAdapterNode(document.getRootElement().getChild("root"));
    }

   public Object getChild(Object parent, int index) {
        BungeniToolbarXMLAdapterNode node = (BungeniToolbarXMLAdapterNode) parent;
        return node.child(index);
   }

   public int getIndexOfChild(Object parent, Object child) {
        BungeniToolbarXMLAdapterNode node = (BungeniToolbarXMLAdapterNode) parent;
        return node.index((BungeniToolbarXMLAdapterNode) child);
    }
   
    public int getChildCount(Object parent) {
        BungeniToolbarXMLAdapterNode jdomNode = (BungeniToolbarXMLAdapterNode)parent;
        return jdomNode.childCount();
    }

   //override from TreeModel
    public boolean isLeaf(Object node) {
        BungeniToolbarXMLAdapterNode jdomNode = (BungeniToolbarXMLAdapterNode)node;
        return (jdomNode.node.getTextTrim().length() > 0);
    }
 }
