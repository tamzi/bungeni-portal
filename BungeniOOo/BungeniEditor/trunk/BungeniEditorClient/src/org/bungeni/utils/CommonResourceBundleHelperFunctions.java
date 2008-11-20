/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.utils;

/**
 *
 * @author undesa
 */
public  class CommonResourceBundleHelperFunctions {
    
    public static String getSectionMetaString(String name) {
        return BungeniResourceBundleFactory.getString("SectionMetaNames", name);
    }

    public static String getDocMetaString(String name) {
        return BungeniResourceBundleFactory.getString("DocMetaNames", name);
    }
    
    
}
