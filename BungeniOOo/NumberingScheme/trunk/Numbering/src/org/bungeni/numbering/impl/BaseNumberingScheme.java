/*
 * BaseNumberingScheme.java
 *
 * Created on March 18, 2008, 12:53 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.numbering.impl;

import java.util.ArrayList;

/**
 * Base class for numbering schemes, all numbering schemes extend this class
 * @author Ashok
 */
public class BaseNumberingScheme   {
    
    /**
     * NumberRange object used by base class
     */
    protected NumberRange baseRange = new NumberRange();
    /**
     * baseSequence ArrayList object, (long) never used directly by the derived class, but used to generate the derived class sequence
     */
    protected ArrayList<Long> baseSequence = new ArrayList<Long>();
    /**
     * ArrayList that stores the derived class generated sequence, (Array of strings)
     */
    protected ArrayList<String> generatedSequence=new ArrayList<String>();
    static String DEFAULT_SEPARATOR = ".";
    protected boolean hasPrefix = false;
    protected String parentPrefix ;
    protected String parentPrefixSeparator = DEFAULT_SEPARATOR;
    
    /**
     * base class constructor, needs to be explicitly invoked with super() from the derived class
     */
    public BaseNumberingScheme() {
        baseRange = new NumberRange((long)1, (long)10);
        baseSequence = new ArrayList<Long>();
    }
    
    /**
     * constructor that takes in start, end ranges, called with super(long, long) from the deriveed class overriden constructor
     */
    public BaseNumberingScheme(long rStart, long rEnd){
        baseRange = new NumberRange(rStart, rEnd);
        baseSequence = new ArrayList<Long>();
    }
    
    /**
     * returns the NumberRange object
     */
    public NumberRange getRange() {
        return baseRange;
    }

    /**
     * sets the NumberRange object
     */
    public void setRange(NumberRange range) {
        baseRange = range;
    }

    /**
     * Returns the baseSequence object
     */
    public ArrayList<Long> getSequence() {
        return baseSequence;
    }

    /**
     * generates the baseSequence (list of Long objects)
     */
   public void generateSequence() {
      System.out.println("baseRange.start = " + baseRange.start);
      for(long i=baseRange.start;i<=baseRange.end;i++){
            baseSequence.add(i);
        }
    }
    
    /**
     * returns the generatedSequence object (the derived sequence)
     */
   public ArrayList<String> getGeneratedSequence(){
       return generatedSequence;
   }
   
   public boolean hasParentPrefix() {
       return hasPrefix;
   }
   
   public void setParentPrefix (String pPrefix, String pSeparator) {
       setParentPrefix (pPrefix);
       this.parentPrefixSeparator = pSeparator;
   }
 
   public void setParentPrefix (String pPrefix) {
       this.hasPrefix = true;
       this.parentPrefix = pPrefix;
   }
   
   public void addNumberToSequence (String number) {
       if (hasParentPrefix()) {
           generatedSequence.add(parentPrefix + parentPrefixSeparator + number);
       } else {
            generatedSequence.add(number);
       }
   }
   
}
