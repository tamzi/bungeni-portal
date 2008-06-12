/*
 * BungeniBNode.java
 *
 * Created on October 21, 2007, 5:12 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.utils;

import java.util.HashMap;
import java.util.Iterator;
import java.util.TreeMap;

/**
 *
 * @author Administrator
 */
    
 public class BungeniBNode {
            private String Name;
            private String displayText = "";
            private Object nodeObject = null;
            private BungeniBNode nodeParent = null;
            /*Stores child nodes by order*/
            private TreeMap<Integer, BungeniBNode> childNodes = new TreeMap<Integer,BungeniBNode>();
            /*Stores child nodes by name*/
            private HashMap<String, BungeniBNode> childNodeNames = new HashMap<String,BungeniBNode>();
            private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(BungeniBNode.class.getName());
                
            public BungeniBNode(String n) {
               Name = n;
            }
            
            public BungeniBNode (String n, BungeniBNode parent) {
                Name = n;
                nodeParent = parent;
            }
            
            public BungeniBNode(String n, Object obj) {
                Name = n;
                nodeObject = obj;
            }
            
            
            public String nodeSignature(){
                //unique signature to idenfiy if node has changed.
                //name + childCount + parentName + order_in_parent.
                String orderInParent = "";
                String parentName = "";
                String sig = "";
                if (hasParent()) {
                    parentName = getParent().getName();
                    orderInParent = Integer.toString(getParent().indexOfChild(this));
                }
                sig =  getName()+"-"+Integer.toString(getChildCount())+"-"+parentName+"-"+orderInParent;
                return sig;
            }
            
            public String getName() {
                return Name;
            }
            
            public BungeniBNode getParent(){
                return nodeParent;
            }
            
            public void setParent(BungeniBNode parent) {
                nodeParent = parent;
            }
            public Object getNodeObject(){
                return nodeObject;
            }
            
            public boolean hasParent(){
                return (nodeParent == null ) ? false: true;
            }
            
            public boolean hasNodeObject(){
                return ((nodeObject == null) ? false: true);
            }
    @Override
            public String toString(){
                if (displayText.length() == 0)
                    return getName();
                else
                    return displayText;
            }
            public HashMap<String,BungeniBNode> getChildrenByName() {
                return childNodeNames;
            }
            
            public TreeMap<Integer,BungeniBNode> getChildrenByOrder(){
                return childNodes;
            }
            
            public int indexOfChild(BungeniBNode node) {
                if (containsNodeByName(node.getName())) {
                    Iterator<Integer> orderedNodeIterator = this.getChildrenByOrder().keySet().iterator();
                    while (orderedNodeIterator.hasNext()) {
                        Integer iKey = orderedNodeIterator.next();
                        BungeniBNode matchedNode = getChildrenByOrder().get(iKey);
                        if (matchedNode.equals(node)){
                            return iKey;
                        }
                    }
                }
                return -1;
            }
            
            public void addChild(BungeniBNode node) {
                childNodes.put(childNodes.size()+1, node);
                childNodeNames.put(node.getName(), node);
            }
            
            public void removeChild(BungeniBNode node) {
                //remove from ordered map
                if (childNodeNames.containsKey(node.getName())) {
                    childNodeNames.remove(node.getName());
                    Iterator<Integer> orderedNodeIterator = childNodes.keySet().iterator();
                    while (orderedNodeIterator.hasNext()) {
                        Integer iKey = orderedNodeIterator.next();
                        BungeniBNode foundNode = childNodes.get(iKey);
                        if (foundNode == node) {
                            childNodes.remove(iKey);
                        }
                    }
                }
            }
            
           
            
            public int getChildCount(){
                return childNodes.size();
            }
            
            public boolean hasChildren(){
                if (childNodes.size() > 0) 
                    return true;
                else
                    return false;
            }
            
            public boolean containsNodeByName(String name) {
                return childNodeNames.containsKey(name);
            }

    public String getDisplayText() {
        return displayText;
    }

    public void setDisplayText(String displayText) {
        this.displayText = displayText;
    }
            
        }
      
