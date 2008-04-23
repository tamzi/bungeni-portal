/*
 * replaceTextWithField.java
 *
 * Created on February 4, 2008, 12:06 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.commands;

import org.apache.commons.chain.Command;
import org.apache.commons.chain.Context;
import org.bungeni.editor.selectors.BungeniFormContext;
import org.bungeni.ooo.ooDocFieldSet;

/**
 *
 * @author Administrator
 */
public class replaceTextWithField implements Command {
    
    /** Creates a new instance of replaceTextWithField */
    public replaceTextWithField() {
    }

    public boolean execute(Context context) throws Exception {
        BungeniFormContext formContext = (BungeniFormContext) context;
        //IBungeniForm iForm = formContext.getBungeniForm();
        ooDocFieldSet fieldSet = (ooDocFieldSet) formContext.getFieldSets("document_field_set").get(0);
        boolean bRet = CommonActions.action_replaceTextWithField(formContext.getOoDocument(), fieldSet.getFieldName(), fieldSet.getFieldValue());
        formContext.getFieldSets("document_field_set").remove(fieldSet);
        return false;
    }
    
}
