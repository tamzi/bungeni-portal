/*
 * addDocumentMetadata.java
 *
 * Created on December 20, 2007, 9:55 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.commands;

import org.apache.commons.chain.Command;
import org.apache.commons.chain.Context;
import org.bungeni.editor.selectors.BungeniFormContext;
import org.bungeni.editor.selectors.IBungeniForm;
import org.bungeni.commands.CommonActions;
import org.bungeni.ooo.ooDocMetadata;
import org.bungeni.ooo.ooDocMetadataFieldSet;

/**
 *
 * @author Administrator
 */
public class addDocumentMetadata {
    
    /**
     * Creates a new instance of addDocumentMetadata
     * Requires: ooDocMetadataFieldSet object to be set prior to invoking the command from the caller class
     */
     public boolean execute(Context context) throws Exception {
        BungeniFormContext formContext = (BungeniFormContext) context;
       // IBungeniForm iForm = formContext.getBungeniForm();
        
        ooDocMetadataFieldSet metaFieldSet = formContext.getMetadataFieldSets().get(0);
        ooDocMetadata meta = new ooDocMetadata(formContext.getOoDocument());
        meta.AddProperty(metaFieldSet.getMetadataName(), metaFieldSet.getMetadataValue());
        formContext.getMetadataFieldSets().remove(metaFieldSet);
        
        return false;
     }
}