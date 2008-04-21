/*
 * IGeneralNumberingScheme.java
 *
 * Created on March 18, 2008, 2:44 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.numbering.impl;

import java.util.ArrayList;

/**
 * General numbering scheme interface, all numbering scheme classes need to implement this interface (apart form extending BaseNumberingScheme)
 * @author Ashok
 */
public interface IGeneralNumberingScheme {
    /**
     * Sets the starting and ending range for the numbering scheme with a NumberRange object
     * @param range NumberRange object specifying starting and ending range
     */
    public void setRange(NumberRange range);
    /**
     * Optional parameter, allows adding a prefix to the number, useful for generating parent-relative prefixed numbering schemes (i.e. 1.a , 1.b...and so on...)
     * @param parentPrefix prefix to be applied before the generated number
     * @param separator separator between parentPrefix and the generated number
     */
    public void setParentPrefix (String parentPrefix, String separator);
    
    /**
     * sets the parent prefix to attach to the generated number.  uses the default separator "."
     * @param parentPrefix prefix to be added to number
     */
    public void setParentPrefix (String parentPrefix ) ;
    /**
     * generates the number sequence
     */
    public void generateSequence();
    /**
     * returns the generated sequence as an ArrayList
     * @return Returns an ArrayList of generated numbers as a string
     */
    public ArrayList<String> getGeneratedSequence();
}
