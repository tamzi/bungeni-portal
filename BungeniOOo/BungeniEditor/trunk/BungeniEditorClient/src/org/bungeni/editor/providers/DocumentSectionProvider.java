/*
 * DocumentSectionIterator.java
 *
 * Created on May 16, 2008, 1:38 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.providers;

import com.sun.star.beans.UnknownPropertyException;
import com.sun.star.beans.XPropertySet;
import com.sun.star.beans.XPropertySetInfo;
import com.sun.star.container.NoSuchElementException;
import com.sun.star.container.XEnumeration;
import com.sun.star.container.XEnumerationAccess;
import com.sun.star.container.XNamed;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.text.XText;
import com.sun.star.text.XTextRange;
import com.sun.star.text.XTextSection;
import com.sun.star.uno.Any;
import com.sun.star.uno.UnoRuntime;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.TreeMap;
import javax.swing.Timer;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.utils.BungeniBNode;
import org.bungeni.utils.BungeniBTree;

/**
 *
 * @author Administrator
 */
public class DocumentSectionProvider {
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(DocumentSectionProvider.class.getName());
    private static OOComponentHelper ooDocument;
    private static BungeniBTree theSectionTree = new BungeniBTree();
    public static int TIMER_DELAY = 4000;
    static Timer sectionRefreshTimer;
    //private static ArrayList<DocumentSectionAdapterDefaultTreeModel> treeModelList = new ArrayList<DocumentSectionAdapterDefaultTreeModel>();
    private static ArrayList<IRefreshableSectionTreeModel> treeModelList = new ArrayList<IRefreshableSectionTreeModel>();
    
    /** Creates a new instance of DocumentSectionIterator */
    public DocumentSectionProvider() {
    }
    
    public static synchronized void updateOOoHandle(OOComponentHelper ooDoc) {
        ooDocument = ooDoc;
    }
    
    public static void initialize(OOComponentHelper ooDoc) {
        updateOOoHandle(ooDoc);
        buildSectionTree();
    }
    
    public static OOComponentHelper getOOoDocument(){
        return ooDocument;
    }
     public static void subscribeModel(IRefreshableSectionTreeModel model) {
        treeModelList.add(model);
    }
    
    /*
     public static void subscribeModel(DocumentSectionAdapterDefaultTreeModel model) {
        treeModelList.add(model);
    }
    */
    /*
    public static void unsubscribeModel(DocumentSectionAdapterDefaultTreeModel model) {
        treeModelList.remove(model);
    }
    */
     
    public static void unsubscribeModel(IRefreshableSectionTreeModel model) {
        treeModelList.remove(model);
    }
     
    public static BungeniBTree getTree(){
        return theSectionTree;
    }
    
    public static BungeniBNode getTreeRoot(){
       
        if (theSectionTree.getTree().size() == 0 ) {
            theSectionTree = generateSectionsTree();
        } 
        
        return theSectionTree.getTree().get(theSectionTree.getTree().firstKey());
            
    }
    public static BungeniBTree getNewTree(){
        BungeniBTree bnewTree = generateSectionsTree();
        return bnewTree;
    }
    
    private static void buildSectionTree() {
        initTimer();
    }
    
    
   
    private static void initTimer(){
          sectionRefreshTimer = new Timer(TIMER_DELAY, new ActionListener() {
              public void actionPerformed(ActionEvent e) {
                  log.debug("DocumentSectionProvider: in timer");
                  final BungeniBTree tmpTreeRoot = generateSectionsTree();
                  log.debug("DocumentSectionProvider: in timer : generated size = " + tmpTreeRoot.getTree().size());
                  log.debug("DocumentSectionProvider: in timer : tree brains = " + tmpTreeRoot.toString());
                  BungeniBNode mergeNode = tmpTreeRoot.getTree().get(tmpTreeRoot.getTree().firstKey());
                 // BungeniBNode origNode = theSectionTree.getTree().get(theSectionTree.getTree().firstKey());
                  synchronized(theSectionTree) {
                    theSectionTree = tmpTreeRoot;
                  }
                  //refresh subscribed tree models
                  /*for( DocumentSectionAdapterDefaultTreeModel model: treeModelList) {
                      model.setRoot(DocumentSectionTreeModelProvider.newRootNode());
                  }*/
                  synchronized (theSectionTree) {
                  for (IRefreshableSectionTreeModel model: treeModelList) {
                      log.debug("DocumentSectionProvider: in timer: updating Model " );
                    //  model.updateTreeModel(mergeNode);
                  }
                 }
              }
           });
           sectionRefreshTimer.start();
    }
     
      private static BungeniBTree generateSectionsTree(){
        BungeniBTree treeRoot = new BungeniBTree();
        final OOComponentHelper localOoDoc;
        synchronized(ooDocument) {
            localOoDoc = ooDocument;
        }
        TreeMap<Integer,String> namesMap = new TreeMap<Integer,String>();
        try {
                    if (!localOoDoc.isXComponentValid()) return treeRoot;
                    /*
                    do a basic check to see if the root section exists
                    */
                    if (!localOoDoc.getTextSections().hasByName("root")) {
                        log.error("generateSectionsTree: no root section found");
                        return treeRoot;
                    }
                    /*
                    get the root section and it as the root node to the JTree
                    */
                    Object root = localOoDoc.getTextSections().getByName("root");
                    log.debug("generateSectionsTree: Adding root node");
                    treeRoot.addRootNode(new String("root"));
                    /*
                    now get the enumeration of the TextSection
                    */

                    int currentIndex = 0;
                    String parentObject = "root";
                    XTextSection theSection = ooQueryInterface.XTextSection(root);
                    XTextRange range = theSection.getAnchor();
                    XText xText = range.getText();
                    XEnumerationAccess enumAccess =(XEnumerationAccess)UnoRuntime.queryInterface(XEnumerationAccess.class, xText);
                    //namesMap.put(currentIndex++, parentObject);
                    XEnumeration enumeration = enumAccess.createEnumeration();
                     log.debug("generateSectionsTree: starting Enumeration ");
                    /*
                    start the enumeration of sections first
                    */ 
                     while (enumeration.hasMoreElements()) {
                         Object elem = enumeration.nextElement();
                         XPropertySet objProps = ooQueryInterface.XPropertySet(elem);
                         XPropertySetInfo objPropsInfo = objProps.getPropertySetInfo();
                         /*
                          *enumerate only TextSection objects
                          */
                         if (objPropsInfo.hasPropertyByName("TextSection")) {
                             XTextSection xConSection = (XTextSection) ((Any)objProps.getPropertyValue("TextSection")).getObject();
                             if (xConSection != null ) {
                                 /*
                                  *Get the section name 
                                  */   
                                 XNamed objSectProps = ooQueryInterface.XNamed(xConSection);
                                 String sectionName = objSectProps.getName();
                                 /*
                                  *only enumerate non root sections
                                  */ 
                                 if (!sectionName.equals("root")) {
                                     log.debug("generateSectionsTree: Found Section :"+ sectionName);
                                      /*
                                      *check if the node exists in the tree
                                      */
                                      if (!namesMap.containsValue(sectionName)) {
                                                namesMap.put(currentIndex++, sectionName);
                                      }
                                 } // if (!sectionName...)     
                             } // if (xConSection !=...)
                         } // if (objPropsInfo.hasProper....)
                     } // while (enumeration.hasMore.... )

                     /*
                      *now scan through the enumerated list of sections
                      */
                     Iterator namesIterator = namesMap.keySet().iterator();
                      while (namesIterator.hasNext()) {
                          Integer iOrder = (Integer) namesIterator.next();
                          String sectionName = namesMap.get(iOrder);
                          /*
                           *check if the sectionName exists in our section tree
                           */
                          BungeniBNode theNode = treeRoot.getNodeByName(sectionName);
                          if (theNode == null ) {
                              /*
                               *the node does not exist, build its parent chain
                               */
                               ArrayList<String> parentChain = buildParentChain(sectionName, localOoDoc);
                               /*
                                *now iterate through the paren->child hierarchy of sections
                                */
                               Iterator<String> sections = parentChain.iterator();
                               BungeniBNode currentNode = null, previousNode = null;
                               while (sections.hasNext()) {
                                   String hierSection = sections.next();
                                   currentNode =  treeRoot.getNodeByName(hierSection);
                                   if (currentNode == null ) {
                                       /* the node doesnt exist in the tree */
                                       if (previousNode != null ) {
                                            treeRoot.addNodeToNamedNode(previousNode.getName(), hierSection);
                                            previousNode = treeRoot.getNodeByName(hierSection);
                                            if (previousNode == null ) 
                                                log.debug("previousNode was null");
                                       } else {
                                           log.info("The root section was not in the BungeniBTree hierarchy, this is an error condition");
                                       }
                                   } else {
                                       /* the node already exists...*/
                                       previousNode = currentNode;
                                   }
                               }
                          }


                      }
         //  convertBTreetoJTreeNodes(treeRoot);
        } catch (NoSuchElementException ex) {
            log.error("generateSectionsTree :" + ex.getMessage());
        } catch (UnknownPropertyException ex) {
            log.error("generateSectionsTree :" + ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error("generateSectionsTree :" + ex.getMessage());
        } finally {
            return treeRoot;
        }
    }

 private static ArrayList<String> buildParentChain(String Sectionname, OOComponentHelper ooDoc){
         ArrayList<String> nodeHierarchy = new ArrayList<String>();
             XTextSection currentSection = ooDoc.getSection(Sectionname);
              XTextSection sectionParent=currentSection.getParentSection();
              XNamed parentProps = ooQueryInterface.XNamed(sectionParent);
              String parentSectionname = parentProps.getName();
              String currentSectionname = Sectionname;
              //array list goes from child(0) to ancestors (n)
              log.debug("buildParentChain: nodeHierarchy: Adding "+ currentSectionname);
              nodeHierarchy.add(currentSectionname);
              while (1==1) {
                  //go up the hierarchy until you reach root.
                  //break upon reaching the parent
                  if (parentSectionname.equals("root")) {
                      nodeHierarchy.add(parentSectionname);
                      log.debug("buildParentChain: nodeHierarchy: Adding "+ parentSectionname + " and breaking.");
                      break;
                  }
                 nodeHierarchy.add(parentSectionname);
                 log.debug("buildParentChain: nodeHierarchy: Adding "+ parentSectionname + ".");
                 currentSectionname = parentSectionname;
                 sectionParent = sectionParent.getParentSection();
                 parentProps = ooQueryInterface.XNamed(sectionParent);
                 parentSectionname = parentProps.getName();
              } //end while (1== 1)
              if (nodeHierarchy.size() > 1 )
                Collections.reverse(nodeHierarchy);
         return nodeHierarchy;
    }
 /*
 private static void walkTree()
  private void convertBTreetoJTreeNodes(BungeniBTree theTree){
        //TreeMap<Integer,BungeniBNode> sectionMap = theTree.getTree();
        BungeniBNode rootNode = theTree.getNodeByName("root");
        this.sectionsRootNode = null;
        this.sectionsRootNode = new DefaultMutableTreeNode(new String("root"));
        TreeMap<Integer,BungeniBNode> sectionMap = rootNode.getChildrenByOrder();
        Iterator<Integer> rootIter = sectionMap.keySet().iterator();
           int depth = 0;
           while (rootIter.hasNext()) {
                Integer key = (Integer) rootIter.next();
                BungeniBNode n = sectionMap.get(key);
                DefaultMutableTreeNode n_child = new DefaultMutableTreeNode(n.getName());
                sectionsRootNode.add(n_child);
                //sbOut.append(padding(depth) + n.getName()+ "\n");
                //walkNodeByOrder(n, depth);
                walkBNodeTree(n , n_child);
            }
    }
    
    private void walkBNodeTree(BungeniBNode theNode, DefaultMutableTreeNode pNode){
        if (theNode.hasChildren()) {
           TreeMap<Integer, BungeniBNode> n_children = theNode.getChildrenByOrder();
           Iterator<Integer> nodesByOrder = n_children.keySet().iterator();
           while (nodesByOrder.hasNext()) {
               Integer key = (Integer) nodesByOrder.next();
               BungeniBNode n = n_children.get(key);
               DefaultMutableTreeNode dmt_node = new DefaultMutableTreeNode(n.getName());
               pNode.add(dmt_node);
               walkBNodeTree(n, dmt_node);
           }
        } else
            return;
    } */

}
