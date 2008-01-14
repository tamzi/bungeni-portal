/*
 * CommonTreeFunctions.java
 *
 * Created on August 20, 2007, 12:35 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.utils;

import java.util.Enumeration;
import javax.swing.JTree;
import javax.swing.tree.TreeNode;
import javax.swing.tree.TreePath;
import org.bungeni.editor.toolbar.BungeniToolbarXMLAdapterNode;

/**
 *
 * @author Administrator
 */
public class CommonTreeFunctions {
    
    /** Creates a new instance of CommonTreeFunctions */
    public CommonTreeFunctions() {
    }

    public static void expandAll(JTree tree) {
        int i = 0 ;
        while (i < tree.getRowCount()) {
            tree.expandRow(i);
            i++;
        }
    }
    /*
    public static void expandAll(JTree tree, boolean expand) {
        TreeNode root = (TreeNode)tree.getModel().getRoot();
        // Traverse tree from root
        expandAll(tree, new TreePath(root), expand);
    }
    
    public static void expandAll(JTree tree, org.bungeni.editor.toolbar.BungeniToolbarXMLAdapterNode node, boolean expand) {
       org.bungeni.editor.toolbar.BungeniToolbarXMLAdapterNode root = (org.bungeni.editor.toolbar.BungeniToolbarXMLAdapterNode) ((org.bungeni.editor.toolbar.BungeniToolbarXMLModelAdapter)tree.getModel()).getRoot();
       expandAll(tree, new TreePath(root), root, expand );
    }
    
    private static void expandAll(JTree tree, TreePath parent, boolean expand) {
        // Traverse children
        TreeNode node = (TreeNode)parent.getLastPathComponent();
        if (node.getChildCount() >= 0) {
            for (Enumeration e=node.children(); e.hasMoreElements(); ) {
                TreeNode n = (TreeNode)e.nextElement();
                TreePath path = parent.pathByAddingChild(n);
                expandAll(tree, path, expand);
            }
        }
    
        // Expansion or collapse must be done bottom-up
        if (expand) {
            tree.expandPath(parent);
        } else {
            tree.collapsePath(parent);
        }
    }

    private static void expandAll(JTree tree, TreePath parent, BungeniToolbarXMLAdapterNode root, boolean expand) {
        org.bungeni.editor.toolbar.BungeniToolbarXMLAdapterNode node = (org.bungeni.editor.toolbar.BungeniToolbarXMLAdapterNode)parent.getLastPathComponent();
        if (node.childCount() >= 0) {
            for (Enumeration e=node.children(); e.hasMoreElements(); ) {
                TreeNode n = (TreeNode)e.nextElement();
                TreePath path = parent.pathByAddingChild(n);
                expandAll(tree, path, expand);
            }
        }
    
        // Expansion or collapse must be done bottom-up
        if (expand) {
            tree.expandPath(parent);
        } else {
            tree.collapsePath(parent);
        }
        
    }
*/
   
}
