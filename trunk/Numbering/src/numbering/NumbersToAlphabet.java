/*
 * NumbersToAlphabet.java
 *
 * Created on March 14, 2008, 10:17 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package numbering;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.ListIterator;
import net.sf.saxon.number.AbstractNumberer;
import net.sf.saxon.number.Numberer_en;
/**
 *
 * @author undesa
 */
public class NumbersToAlphabet extends AbstractNumberer{
    
    public long start;
    public long end;
    public static NumbersToAlphabet numbererObj;
    
    /** Creates a new instance of NumbersToAlphabet */
    public NumbersToAlphabet() {
        
    }
    
     public void setRange(long s, long e){
        this.start=s;
        this.end=e;
        
    }
    public long getEnd(){
        return this.end;
    }
     
    public long getStart(){
        return this.start;
    }
    
    public static void main(String [] args){
        numbererObj=new NumbersToAlphabet();
        numbererObj.setRange(1,25);
        long startRange=numbererObj.getStart();
        long endRange=numbererObj.getEnd();
        System.out.println("Start range: " + startRange + " End Range: " + endRange);
        
        ArrayList<Long> list=new ArrayList<Long>();
        for(long i=startRange;i<=endRange;i++){
            list.add(i);
        }
               
        
        //start a sequence of numbers based upon the range
       System.out.println("Starting Numbering Scheme");
       ListIterator<Long> listIterator= list.listIterator();
        while(listIterator.hasNext()){
          
            
            Object nextItem=listIterator.next();
            Long numberSequence=(Long)nextItem;
         
           System.out.println("Alphabet - " + numbererObj.toAlphaSequence(numberSequence,"ABCDEFGHIJKLMOPQRSTUVWXYZ"));
            
            
            
        }
    }

    public String toWords(long l) {
        return null;
    }

    public String toOrdinalWords(String string, long l, int i) {
         return null;
    }

    public String monthName(int i, int i0, int i1) {
         return null;
    }

    public String dayName(int i, int i0, int i1) {
         return null;
    }

    
}
