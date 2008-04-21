/*
 * RomanNumerals.java
 *
 * Created on March 13, 2008, 4:16 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.numbering;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.ListIterator;
import net.sf.saxon.number.Numberer_en;
/**
 *
 * @author undesa
 */
public class RomanNumerals {
    
    public long start;
    public long end;
    public static Numberer_en numbererObj=new Numberer_en();
    /** Creates a new instance of RomanNumerals */
    public RomanNumerals() {
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
    
    public static void main(String[]args){
        RomanNumerals test=new RomanNumerals();
        test.setRange(25,76);
        long startRange=test.getStart();
        long endRange=test.getEnd();
        System.out.println("Start range: " + numbererObj.toRoman(startRange) + " End Range: " + numbererObj.toRoman(endRange));
        //populate a list with the range of numbers
        ArrayList<Long> list=new ArrayList<Long>();
        for(long i=startRange;i<=endRange;i++){
            list.add(i);
        }
               
        
        //start a sequence of numbers based upon the range
       System.out.println("Starting Numbering Scheme");
       ListIterator<Long> listIterator= list.listIterator();
        while(listIterator.hasNext()){
          
            
            Object nextItem=listIterator.next();
            Long romanNumeral=(Long)nextItem;
         
           System.out.println("Roman Numeral- " + numbererObj.toRoman(romanNumeral));
            
            
            
        }
    }
    
}
