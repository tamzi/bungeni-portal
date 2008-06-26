/*
 * DocumentSectionTreeModelProvider.java
 *
 * Created on May 18, 2008, 1:39 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.providers;

import com.sun.star.text.XTextSection;
import javax.swing.tree.DefaultMutableTreeNode;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.utils.BungeniBNode;

/**
 *
 * @author Administrator
 */
public class DocumentSectionFriendlyTreeModelProvider {
    
    /** Creates a new instance of DocumentSectionTreeModelProvider */
    public static DocumentSectionFriendlyAdapterDefaultTreeModel theSectionTreeModel = null;
     private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(DocumentSectionFriendlyTreeModelProvider.class.getName());
           
    /**
     * returns a non-static instance of the section TreeModel which is updated directly by the documentsectionProvider
     */
    public static DocumentSectionFriendlyAdapterDefaultTreeModel create_without_subscription(){
        BungeniBNode bRootNode = DocumentSectionProvider.getTreeRoot();
        DefaultMutableTreeNode dmtRootNode = provideRootNode(bRootNode);
        DocumentSectionFriendlyAdapterDefaultTreeModel model = new DocumentSectionFriendlyAdapterDefaultTreeModel(dmtRootNode, false);
        return model;
    }
    
    public static DocumentSectionFriendlyAdapterDefaultTreeModel create(){
        BungeniBNode bRootNode = DocumentSectionProvider.getNewTree().getFirstRoot();
        DefaultMutableTreeNode dmtRootNode = provideRootNode(bRootNode);
        DocumentSectionFriendlyAdapterDefaultTreeModel model = new DocumentSectionFriendlyAdapterDefaultTreeModel(dmtRootNode, false);
        DocumentSectionProvider.subscribeModel(model);
        return model;
    }
    public static DocumentSectionFriendlyAdapterDefaultTreeModel create_static(){
       if (theSectionTreeModel == null ) {
            BungeniBNode bRootNode = DocumentSectionProvider.getTreeRoot();
            DefaultMutableTreeNode dmtRootNode = provideRootNode(bRootNode);
            //static model is always subscribed, so there is no internal timer required int the model
            theSectionTreeModel = new DocumentSectionFriendlyAdapterDefaultTreeModel(dmtRootNode, false);
            DocumentSectionProvider.subscribeModel(theSectionTreeModel);
            }
       return theSectionTreeModel;    
    }
    

    /**
     * generates a newrootnode for the section model
     */
    public static DefaultMutableTreeNode newRootNode(){
        BungeniBNode bRootNode = DocumentSectionProvider.getTreeRoot();
        return provideRootNode(bRootNode);
    }
    
    /*
    private static String getSectionDisplayText(String sectionName, OOComponentHelper ooDoc){
        String retDisplayText = "";
        boolean bDispTextFound = false;
        log.debug("getSectionDisplayText : for "+ sectionName);
        XTextSection aSect = ooDoc.getSection(sectionName);
        String sectionText = aSect.getAnchor().getString();
        sectionText = sectionText.trim();
        String sectionType = ooDoc.getSectionType(aSect);
        if (sectionType != null ) {
            bDispTextFound = true;
            retDisplayText = sectionType + "-";
        }
        if (sectionText.length() > 0 ) {
            bDispTextFound = true;
            if (sectionText.length() > 15 ) 
                retDisplayText = retDisplayText + sectionText.substring(0, 14)+ "..";
            else
                retDisplayText = retDisplayText + sectionText+ "..";
        }
        if (!bDispTextFound ) {
            retDisplayText = sectionName;
        }
        return retDisplayText;
    }
    */
    
    private static DefaultMutableTreeNode provideRootNode(BungeniBNode rootNode) {
        //walk nodes and build tree
        DefaultMutableTreeNode theRootNode = new DefaultMutableTreeNode(rootNode);
        rootNode.setNodeObject(theRootNode);
        OOComponentHelper ooDoc = DocumentSectionProvider.getOOoDocument();
       // recurseNodes(theRootNode, ooDoc);
        FriendlyNodeIterator nodeIter = new FriendlyNodeIterator(ooDoc);
        DocumentSectionIterator docIterate = new DocumentSectionIterator(rootNode, nodeIter);
        docIterate.startIterator();
        return theRootNode;
    }
    
    private static class FriendlyNodeIterator implements  IBungeniSectionIteratorListener {
        private OOComponentHelper ooDoc;
        FriendlyNodeIterator(OOComponentHelper ooDocument) {
            this.ooDoc = ooDocument;
        }

        public boolean iteratorCallback(BungeniBNode bNode) {
           boolean bState = true;
           try {
           String dispText = getSectionDisplayText(bNode.getName());
           bNode.setDisplayText(dispText);
           bState = true;
           } catch (Exception ex) {
               log.error ("IteratorCallBack = " + ex.getMessage());
           }
           return bState;
        }
        
        private  String getSectionDisplayText(String sectionName){
                    String retDisplayText = "";
                    boolean bDispTextFound = false;
                    log.debug("getSectionDisplayText : for "+ sectionName);
                    try {
                    XTextSection aSect = ooDoc.getSection(sectionName);
                    String sectionText = aSect.getAnchor().getString();
                    sectionText = sectionText.trim();
                    String sectionType = ooDoc.getSectionType(aSect);
                    if (sectionType != null ) {
                        bDispTextFound = true;
                        retDisplayText = sectionType + "-";
                    }
                    if (sectionText.length() > 0 ) {
                        bDispTextFound = true;
                        if (sectionText.length() > 15 ) 
                            retDisplayText = retDisplayText + sectionText.substring(0, 14)+ "..";
                        else
                            retDisplayText = retDisplayText + sectionText+ "..";
                    }
                    if (!bDispTextFound ) {
                        retDisplayText = sectionName;
                    }
                    } catch (Exception ex) {
                        log.error("getSectionDisplayText" + ex.getMessage());
                    } finally {
                    return retDisplayText;
                    }
            }
    
    }
    
    /*
    private static void recurseNodes(DefaultMutableTreeNode theNode, OOComponentHelper ooDoc) {
        BungeniBNode theBNode = (BungeniBNode) theNode.getUserObject();
        if (theBNode.hasChildren()) {
            TreeMap<Integer, BungeniBNode> children = theBNode.getChildrenByOrder();
            Iterator<Integer> childIterator = children.keySet().iterator();
            while (childIterator.hasNext()) {
                Integer nodeKey = childIterator.next();
                BungeniBNode nodeChild  = children.get(nodeKey);
                nodeChild.setDisplayText(getSectionDisplayText(nodeChild.getName(), ooDoc));
                    DefaultMutableTreeNode dmtChildNode = new DefaultMutableTreeNode( nodeChild);
                    nodeChild.setNodeObject(dmtChildNode);
                recurseNodes(dmtChildNode, ooDoc);
                theNode.add(dmtChildNode );
            }
        }
    } */
}
