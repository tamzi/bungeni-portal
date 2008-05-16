/*
 * BungeniEditorPropertiesHelper.java
 *
 * Created on May 16, 2008, 4:38 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor;

/**
 *
 * @author Administrator
 */
public class BungeniEditorPropertiesHelper {
    
    /** Creates a new instance of BungeniEditorPropertiesHelper */
    public BungeniEditorPropertiesHelper() {
    }
    
    public static String getDocumentRoot(){
        String activeDoc = BungeniEditorProperties.getEditorProperty("activeDocumentMode");
        String docRoot = BungeniEditorProperties.getEditorProperty("root:" + activeDoc.trim());
        return docRoot;
    }
}
