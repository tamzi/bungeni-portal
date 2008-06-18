package org.bungeni.utils.compare;

 public class DifferenceChain {
        public BungeniNodeDifference diff;
        public DifferenceChain nextDifference = null;
        public DifferenceChain prevDifference = null;
        
        @Override
        public String toString(){
            String output = "";
            output += "--- BEGIN DIFF CHAIN size ("+chainSize()+")--- \n";
            output += "DIFF : " + diff.toString() + "\n";
            DifferenceChain nextDiff = nextDifference;
            while (nextDiff != null) {
                output += "DIFF : " + nextDiff.diff.toString()  + "\n";
                nextDiff = nextDiff.nextDifference;
            }
            output += " --- END DIFFERENCE CHAIN --- \n";
            return output;
        }
        
        public int chainSize(){
            int n=1;
            DifferenceChain nextDiff = nextDifference;
            while (nextDiff != null) {
                n++;
                nextDiff = nextDiff.nextDifference;
            }
            return n;
        }
        
    }