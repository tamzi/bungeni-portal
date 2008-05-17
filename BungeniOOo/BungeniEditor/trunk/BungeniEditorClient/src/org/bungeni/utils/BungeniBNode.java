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
            private Object nodeObject = null;
            
            /*Stores child nodes by order*/
            private TreeMap<Integer, BungeniBNode> childNodes = new TreeMap<Integer,BungeniBNode>();
            /*Stores child nodes by name*/
            private HashMap<String, BungeniBNode> childNodeNames = new HashMap<String,BungeniBNode>();
            private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(BungeniBNode.class.getName());
                
            public BungeniBNode(String n) {
                Name = n;
            }
            
            public BungeniBNode(String n, Object obj) {
                nodeObject = obj;
            }
            
            public String getName() {
                return Name;
            }
            
            public Object getNodeObject(){
                return nodeObject;
            }
            
            public boolean hasNodeObject(){
                return ((nodeObject == null) ? false: true);
            }
            public String toString(){
                return getName();
            }
            public HashMap<String,BungeniBNode> getChildrenByName() {
                return childNodeNames;
            }
            
            public TreeMap<Integer,BungeniBNode> getChildrenByOrder(){
                return childNodes;
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
            
        }
      
