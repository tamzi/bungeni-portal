/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.utils;

/**
 *
 * @author undesa
 */
public class CommonStringFunctions {
      
    public static String stripNonAlphanumeric(String s) { 
         return s.replaceAll("[^a-zA-Z0-9]", ""); 
      }
      
    public static String makeReferenceFriendlyString(String s) {
        return stripNonAlphanumeric(s);
    }
}
