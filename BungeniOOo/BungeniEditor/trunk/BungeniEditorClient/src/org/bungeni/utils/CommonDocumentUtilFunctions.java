/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.utils;

import java.util.Random;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author undesa
 */
public class CommonDocumentUtilFunctions {
    
    public static String getUniqueSectionName(String prefixName, OOComponentHelper ooDocument) {
        String sName = "";
        for (;;) {
            Random sRandom = new Random();
            int nRandom = sRandom.nextInt(10000);
            if (!ooDocument.hasSection(prefixName+nRandom)) {
                sName = prefixName + nRandom ;
                break;
            }
        }
      return sName; 
    } 
    
    public static String getUniqueReferenceName(String prefixName, OOComponentHelper ooDocument) {
        String sName = "";
        for (;;) {
            Random sRand = new Random();
            int nRandom = sRand.nextInt(10000);
            if (ooDocument.getReferenceMarks().hasByName(prefixName+nRandom)) {
                continue;
            } else 
                return prefixName + nRandom;
        }
    }
}
