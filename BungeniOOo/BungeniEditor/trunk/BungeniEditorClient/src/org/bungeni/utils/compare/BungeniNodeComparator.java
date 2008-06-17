package org.bungeni.utils.compare;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.TreeMap;
import org.bungeni.utils.BungeniBNode;

public class BungeniNodeComparator {
    private  TreeMap<Integer, BungeniNodeDifference> diffMapInsert = new TreeMap<Integer, BungeniNodeDifference>();
    private  TreeMap<Integer, BungeniNodeDifference> diffMapUpdate = new TreeMap<Integer, BungeniNodeDifference>();
    private  TreeMap<Integer, BungeniNodeDifference> diffMapDelete = new TreeMap<Integer, BungeniNodeDifference>();

    class DifferenceChain {
        BungeniNodeDifference diff;
        DifferenceChain nextDifference = null;
        DifferenceChain prevDifference = null;
        
        @Override
        public String toString(){
            String output = "--- BEGIN DIFF CHAIN --- \n";
            output += "DIFF : " + diff.toString() + "\n";
            DifferenceChain nextDiff = nextDifference;
            while (nextDiff != null) {
                output += "DIFF : " + nextDiff.diff.toString()  + "\n";
                nextDiff = nextDiff.nextDifference;
            }
            output += " --- END DIFFERENCE CHAIN --- \n";
            return output;
        }
        
        
    }
        
    private void clearMaps(){
        diffMapInsert.clear();
        diffMapDelete.clear();
        diffMapUpdate.clear();
    }
   
    private void diffAdd(Integer nKey, BungeniNodeDifference diff) {
        switch (diff.getDiffState()) {
        case INSERT:
            update (getDiffMapInsert(),nKey, diff);
            break;
        case UPDATE:
            update (getDiffMapUpdate(),nKey, diff);
            break;
        case DELETE:
            update (getDiffMapDelete(),nKey, diff);
            break;
        default:
            break;
        }
        
    }
    private void update (TreeMap<Integer, BungeniNodeDifference> map, Integer nKey, BungeniNodeDifference diff) {
        map.put(nKey, diff);        
    }
        
    
    private void processUpdateChains() {
        ArrayList<DifferenceChain> dcList = new ArrayList<DifferenceChain>();
        Iterator<Integer> iterKey = getDiffMapUpdate().keySet().iterator();
        while (iterKey.hasNext()) {
           Integer nKey = iterKey.next();
           BungeniNodeDifference n = getDiffMapUpdate().get(nKey);
           DifferenceChain dc = new DifferenceChain();
           Integer changeTo = n.getUpdateFromIndex();
           String changeToName = n.getUpdateFromName();
           dc.diff = n;
           if (!existsInChainList(dcList, n)) {
               dcList.add(dc);
               DifferenceChain dcPrev = dc;
               for  (;; ) {
                   if (getDiffMapUpdate().containsKey(changeTo)){
                        BungeniNodeDifference nchain = getDiffMapUpdate().get(changeTo);
                        if (existsInChainList(dcList, nchain)) {
                            break;
                        }
                        DifferenceChain dcChain = new DifferenceChain();
                        dcChain.diff = nchain;
                        dcPrev.nextDifference = dcChain;
                        dcChain.prevDifference = dcPrev;
                        changeTo = nchain.getUpdateFromIndex();
                   } else
                       break;
               } 
           }    
        }
        
        for (DifferenceChain d: dcList) {
            System.out.println(d);
        }
    }
    
    private boolean existsInChainList(ArrayList<DifferenceChain> dclist, BungeniNodeDifference nchain) {
        for (DifferenceChain d : dclist) {
            DifferenceChain drunning = d;
                while (drunning != null) { 
                     BungeniNodeDifference ncomp = drunning.diff;
                     if (ncomp.getDiffKey().equals(nchain.getDiffKey())) {
                        return true;
                     }
                     drunning = drunning.nextDifference; 
                }
        }
        return false;
    }
    public void compareAndDiff(BungeniBNode root1, BungeniBNode root2){
        compare(root1, root2);
        processUpdateChains();
    }
           public void compare (BungeniBNode root1, BungeniBNode root2){
                       
                       TreeMap<Integer, BungeniBNode> root2children = root2.getChildrenByOrder();
                        for (Integer root2child : root2children.keySet()) {
                            BungeniBNode aNode = root2children.get(root2child);
                            if (root1.containsNodeByName(aNode.getName())) { //root1 contains the child
                                   System.out.println("root1 contains  " + aNode.getName());
                                   //check if index of node in root1 == index of node in root2
                                   BungeniBNode nNode = root1.getChildNodeByName(aNode.getName());
                                   Integer indexinroot1 = root1.indexOfChild(nNode);
                                   //BungeniBNode nNodeInRoot2 = root2children.get(root2child);
                                   //Integer indexinroot2 = root2.indexOfChild(nNodeInRoot2);
                                   if (indexinroot1 != root2child) {
                                     //  System.out.println("root1 contains " + aNode.getName() + " at unequal index (move " + aNode.getName() + " from " + indexinroot1 + " to "+ root2child+") or (insert "+aNode.getName() + " at " + root2child + ")");
                                       BungeniNodeDifference nodeDiff = new BungeniNodeDifference ();
                                       nodeDiff.diffUpdate(aNode.getName(), indexinroot1, aNode.getName(), root2child);
                                       this.diffAdd(indexinroot1, nodeDiff);
                                   }
                               }  else {
                                
                               // System.out.println("root1 does not contain  " + aNode.getName() + " (add child to root1 at index : "+ root2child + " )");
                                       BungeniNodeDifference nodeDiff = new BungeniNodeDifference ();
                                       nodeDiff.diffInsert(aNode.getName(), root2child);
                                       this.diffAdd(root2child, nodeDiff);
                               }
                           }
                        
                        //now look for deletions in the original map...
                        final HashMap<String, BungeniBNode>root1children = root1.getChildrenByName();
                        //final HashMap<String, BungeniBNode>root2childrenbyname = root2.getChildrenByName();
                        for (String root1child: root1children.keySet()){
                            if (!root2.containsNodeByName(root1child)) {
                                BungeniBNode rChild = root1children.get(root1child);
                                Integer indexofrChild = root1.indexOfChild(rChild);
                                BungeniNodeDifference diff = new BungeniNodeDifference();
                                diff.diffDelete(rChild.getName(), indexofrChild);
                                this.diffAdd(indexofrChild, diff);
                            }
                        }
           //     }
           //} 
           
       }

    public TreeMap<Integer, BungeniNodeDifference> getDiffMapInsert() {
        return diffMapInsert;
    }

    public TreeMap<Integer, BungeniNodeDifference> getDiffMapUpdate() {
        return diffMapUpdate;
    }

    public TreeMap<Integer, BungeniNodeDifference> getDiffMapDelete() {
        return diffMapDelete;
    }
    
    
}