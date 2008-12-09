/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.editor.metadata;

/**
 *
 * @author undesa
 */
public class DocumentPart {
    String PartName;
    String PartDescription;
    
    public DocumentPart(){
        PartName = PartDescription = "";
    }
    public DocumentPart(String pName, String pDesc) {
        PartName = pName;
        PartDescription = pDesc;
    }
}
