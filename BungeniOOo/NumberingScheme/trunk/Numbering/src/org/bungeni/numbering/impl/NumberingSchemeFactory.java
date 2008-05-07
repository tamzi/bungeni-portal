/*
 * NumberingSchemeFactory.java
 *
 * Created on March 18, 2008, 2:20 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.numbering.impl;

import java.util.ArrayList;
import java.util.Iterator;

/**
 * Factory class to generate Numbering scheme objects
 * @author Ashok
 */
public class NumberingSchemeFactory {
    
    /** Creates a new instance of NumberingSchemeFactory */
    public NumberingSchemeFactory() {
    }
    
    /**
     * takes a parameter based on which the appropriate numbering scheme class is generated
     */
     public static IGeneralNumberingScheme getNumberingScheme(String schemeName) {
      IGeneralNumberingScheme scheme = null;
      String schemeClassPrefix = "org.bungeni.numbering.schemes.";
      String schemeClass = null;
       try {
           if (schemeName.equals("ROMAN")) {
               schemeClass = schemeClassPrefix + "schemeRoman";
           } else if (schemeName.equals("ALPHA")) {
               schemeClass = schemeClassPrefix + "schemeAlphabetical";
           } else
               schemeClass = schemeClassPrefix + "schemeNumeric";
           
             Class clsScheme;
             clsScheme = Class.forName(schemeClass);
             scheme = (IGeneralNumberingScheme) clsScheme.newInstance();
       } catch (ClassNotFoundException ex) {
        System.out.println("class not found = " + ex.getMessage());
       } finally {
             return scheme;
        }
    }
     
    public static void main(String[] args) {
        /*create a numbering scheme object based on a parametr...
         *"ALPHA" will generate a alpha numeric numbering scheme object
         *"ROMAN" will generate a roman numeral numbering scheme object
         *"GENERAL" will generate a numeric serial numbering scheme object
         */
        IGeneralNumberingScheme inumScheme = null;
        inumScheme = NumberingSchemeFactory.getNumberingScheme("ROMAN");
        inumScheme.setRange(new NumberRange((long)12, (long)26));
        inumScheme.generateSequence();
        /*the numbering sequence has been generated, now display the sequence*/
        ArrayList<String> seq = inumScheme.getGeneratedSequence();
        Iterator<String> iter = seq.iterator();
        while (iter.hasNext()) {
            System.out.println(iter.next().toString());
        }
    } 
}
