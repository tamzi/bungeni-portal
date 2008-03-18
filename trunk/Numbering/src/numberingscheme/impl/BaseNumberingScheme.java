/*
 * BaseNumberingScheme.java
 *
 * Created on March 18, 2008, 12:53 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package numberingscheme.impl;

import java.util.ArrayList;
import net.sf.saxon.number.AbstractNumberer;
import net.sf.saxon.number.Numberer_en;

/**
 * Base class for numbering schemes, all numbering schemes extend this class
 * @author Ashok
 */
public class BaseNumberingScheme   {
    
    protected NumberRange baseRange = new NumberRange();
    protected ArrayList<Long> baseSequence = new ArrayList<Long>();
    protected ArrayList<String> generatedSequence=new ArrayList<String>();
    
    public BaseNumberingScheme() {
        baseRange = new NumberRange((long)1, (long)10);
        baseSequence = new ArrayList<Long>();
    }
    
    public BaseNumberingScheme(long rStart, long rEnd){
        baseRange = new NumberRange(rStart, rEnd);
        baseSequence = new ArrayList<Long>();
    }
    
    public NumberRange getRange() {
        return baseRange;
    }

    public void setRange(NumberRange range) {
        baseRange = range;
    }

    public ArrayList<Long> getSequence() {
        return baseSequence;
    }

   public void generateSequence() {
      System.out.println("baseRange.start = " + baseRange.start);
      for(long i=baseRange.start;i<=baseRange.end;i++){
            baseSequence.add(i);
        }
    }
    
   public ArrayList<String> getGeneratedSequence(){
       return generatedSequence;
   }
 
}
