package org.bungeni.utils.compare;

import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import org.bungeni.utils.BungeniBNode;
import org.bungeni.utils.BungeniBTree;

public class BungeniTreeRefactorTree {
    private DefaultTreeModel treeModel;
    private BungeniBNode treeRootNode;
    private BungeniBNode treeMergeRootNode;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(BungeniTreeRefactorTree.class.getName());
           
    public BungeniTreeRefactorTree(DefaultTreeModel model, BungeniBNode rootNode, BungeniBNode newRootNode){
        this.treeModel  = model;
        this.treeRootNode = rootNode;
        this.treeMergeRootNode = newRootNode;
    }

    public void doMerge() {
        //do a recursive merge of the tree
        //step1 do a merge for the rootnodes
        //
        /*
        
         root      (1)          root          (2)
            |                      |
            |____child1            |____child3
            |____child2            |____child1
            |____child3            |____child7
            |____child4            |____child5
            |____child5            |____child4
            |____child6                    |
            |____child7                    |''''''child4.1
            |____child8                    |......child4.2
                                           |______child4.3

         */
        // the original root structure (1) is converted to structure (2)
        // once (2) has been transformed to (2) for the first iteration, 
        // it accquires some nodes and loses some nodes... in the above example,
        // child4 has been reordered and has accquired 3 children 4.1, 4,2 and 4.3
        // these child notes do not have defaultmutabletreenode objects, but exist
        // merely as BungeniBNode structures.
        // NOTE that the functionality presently doesnt handle node movement/updates across
        // hierarchies, movement and update is handled only within the same sibling hierarchy,
        // a node moving to a new hierarchy is treated as a deletion from the original, and 
        // a subsequent addition to a different hierarchy
        log.debug("doMerge : starting for orig : " + getTreeRootNode() + " , merge : " + this.getTreeMergeRootNode());
        BungeniTreeRefactorNode nodeRefactor = new BungeniTreeRefactorNode(getDefaultTreeModel(),getTreeRootNode(),getTreeMergeRootNode());
        nodeRefactor.doMerge();
        log.debug("doMerge : merging children ");
        doMergeChildren(this.getTreeRootNode(), this.getTreeMergeRootNode());
        log.debug("After doMergeChildren : ");
        //viewDmtNodes(getTreeRootNode());
        //at this point any new children now exist within the rootnode structure as BungeniNodes,
        //we need to create the corresponding UI defaultmutabletreenode structure for the 
        //empty bnode structures.
        //step2 recurse within the root node's children and iterate them...
        /*
        child4   (3)                        child4    (4)
           |                                   |
           |''''''child4.1 (without dmt)       |''''''child4.1 (with dmt)
           |......child4.2 (without dmt)       |......child4.2 (with dmt)
           |______child4.3 (without dmt)       |______child4.3 (with dmt)
       */
       //the children of any updated / new nodes are recursed and the NodeObject of the 
       //BNodes is examined (3), if it is null, a DetaultMutableTreeNode object
       //is  created and set into the NodeObject field of the BungeniBNode
       for (Integer nKey : getTreeRootNode().getChildrenByOrder().keySet()) {
            seedTreeWithUITreeNodes(getTreeRootNode().getNodeAtIndex(nKey));         
       }
       /*
        log.debug("After seedTreeWithUITreeNodes : ");
        viewDmtNodes(getTreeRootNode());
       
       BungeniBTree tmpTree = new BungeniBTree();
       tmpTree.addRootNode(treeRootNode);
       log.debug("doMerge : original tree = " + tmpTree.toString());
       
       BungeniBTree tmpCopyTree = new BungeniBTree();
       tmpCopyTree.addRootNode(this.treeMergeRootNode);
       log.debug("doMerge : merge tree = " + tmpCopyTree.toString());
       */
      
    }

    private void viewDmtNodes(BungeniBNode nodeRoot ) {
        DefaultMutableTreeNode anode = (DefaultMutableTreeNode) nodeRoot.getNodeObject();
        log.debug("dmt = " + anode.toString() + ", bbnode = " + nodeRoot.toString());
        log.debug(" anode dmt count = " + anode.getChildCount() + " bnode count = " + nodeRoot.getChildCount());
    } 
    
 private void seedTreeWithUITreeNodes(BungeniBNode nodeDMTnodes){
     //recurse children of rootnodes
     try {
     DefaultMutableTreeNode dmtofNodeDMT = (DefaultMutableTreeNode) nodeDMTnodes.getNodeObject();
      dmtofNodeDMT.setAllowsChildren(true);
     boolean structureChanged = false;
     for (Integer nKey : nodeDMTnodes.getChildrenByOrder().keySet()){
         BungeniBNode childofNodeDmtNode = nodeDMTnodes.getNodeAtIndex(nKey);
         Object nodeObject = childofNodeDmtNode.getNodeObject();
         if (nodeObject == null){
             DefaultMutableTreeNode dmt = new DefaultMutableTreeNode(childofNodeDmtNode);
             childofNodeDmtNode.setNodeObject(dmt);
             dmtofNodeDMT.add(dmt);
             structureChanged = true;
         }
         seedTreeWithUITreeNodes(childofNodeDmtNode);
     }
     if (structureChanged) {
         this.getDefaultTreeModel().nodeStructureChanged(dmtofNodeDMT);
     }
     } catch (Exception ex) {
         log.error("seedTreeWithUITreeNodes : " + ex.getMessage());
     }
 }   
    
 
 
 private void doMergeChildren(BungeniBNode origNode, BungeniBNode mergeNode) {
      try {
       for (String nodeName : origNode.getChildrenByName().keySet()) {
           //this root node has an updated UI, but its children dont
           BungeniBNode childOfOriginal = origNode.getChildNodeByName(nodeName);
           BungeniBNode childOfMergeNode = mergeNode.getChildNodeByName(nodeName);
           //check if nodeNewChild has children, if it doesnt we wipe out the children of the orignal node
           BungeniTreeRefactorNode childnodesRefactor = new BungeniTreeRefactorNode(getDefaultTreeModel(), childOfOriginal, childOfMergeNode);
           childnodesRefactor.doMerge();
           doMergeChildren(childOfOriginal, childOfMergeNode);
       }
       } catch (Exception ex) {
           log.error("doMergeChildren : "+ex.getMessage());
       }
 }
 


    public DefaultTreeModel getDefaultTreeModel() {
        return treeModel;
    }

    public BungeniBNode getTreeRootNode() {
        return treeRootNode;
    }

    public BungeniBNode getTreeMergeRootNode() {
        return treeMergeRootNode;
    }
}