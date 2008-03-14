/*
 * Main.java
 *
 * Created on March 12, 2008, 3:13 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */


package numbering;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.ListIterator;
import net.sf.saxon.number.Numberer_en;
import net.sf.saxon.number.AbstractNumberer;
/**
 *
 * @author undesa
 */
public class NumberingScheme {
   
    public long start;
    public long end;
    public static Numberer_en numbererObj=new Numberer_en();
   
    /** Creates a new instance of __NAME__ */
    public NumberingScheme() {
        super();
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
    
   
    
    public static void main(String[] args){
        NumberingScheme test=new NumberingScheme();
        test.setRange(25,76);
        long startRange=test.getStart();
        long endRange=test.getEnd();
        System.out.println("Start range: " + startRange + " End Range: " + endRange);
        //populate a list with the range of numbers
        ArrayList<Long> list=new ArrayList<Long>();
        for(long i=startRange;i<=endRange;i++){
            list.add(i);
        }
               
        
        //start a sequence of numbers based upon the range
        System.out.println("Starting Numbering Scheme");
        
        
      // ListIterator<Long> listIterator= list.listIterator();
       
       int loop=25;
       
       for (ListIterator i =list.listIterator(); i.hasNext(); loop++) {
              System.out.println(loop + ": " + i.next()); //get next(first) item in loop and go in front of next(second) item in loop
              System.out.println(loop + ": " + i.previous()); //get previous(first) item in loop and go in front of previous(before first) item in loop
              if (i.hasPrevious()) {
                 System.out.println(loop + ": " + i.previous()); //get previous(before first) item in loop and go in front of previous(before before first) item in loop
                 System.out.println(loop + ": " + i.next()); //get next(before first) item in loop and go in front of next(first) item in loop
              }
              System.out.println(loop + ": " + i.next()); //get next(first) item in loop and go in front of next(second) item in loop
       }
       
       
      /* while(listIterator.hasNext()){
          
            
            Object nextItem=listIterator.next();
            Long romanNumeral=(Long)nextItem;
            
    
         
          // System.out.println("Base Decimal- " + nextItem);
            
            
            
        }*/
        
    }
    
   

}