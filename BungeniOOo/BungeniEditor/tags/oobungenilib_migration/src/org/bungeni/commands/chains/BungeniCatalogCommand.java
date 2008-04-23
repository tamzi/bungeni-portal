/*
 * BungeniCatalogCommand.java
 *
 * Created on December 26, 2007, 6:33 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.commands.chains;

import java.util.HashMap;

/**
 *
 * @author Administrator
 */
public class BungeniCatalogCommand {


     private String formName;
     private String catalogSource;
    
     private String formMode ;
     private String commandCatalog;
     private String commandChain;
             
    /** Creates a new instance of BungeniCatalogCommand */
    public BungeniCatalogCommand() {
    }
    
    public BungeniCatalogCommand(HashMap<String,String> cmdCatalog) {

        setFormName(cmdCatalog.get("FORM_NAME"));
        setCatalogSource(cmdCatalog.get("CATALOG_SOURCE"));
        setFormMode(cmdCatalog.get("FORM_MODE"));
        setCommandCatalog(cmdCatalog.get("COMMAND_CATALOG"));
        setCommandChain(cmdCatalog.get("COMMAND_CHAIN"));

    }

    public String getFormName() {
        return formName;
    }

    public void setFormName(String formName) {
        this.formName = formName;
    }

    public String getCatalogSource() {
        return catalogSource;
    }

    public void setCatalogSource(String catalogSource) {
        this.catalogSource = catalogSource;
    }

    public org.bungeni.editor.selectors.SelectorDialogModes getFormMode() {
        return Enum.valueOf(org.bungeni.editor.selectors.SelectorDialogModes.class, formMode);
    }

    public void setFormMode(String formMode) {
        this.formMode = formMode;
    }

    public String getCommandCatalog() {
        return commandCatalog;
    }

    public void setCommandCatalog(String commandCatalog) {
        this.commandCatalog = commandCatalog;
    }

    public String getCommandChain() {
        return commandChain;
    }

    public void setCommandChain(String commandChain) {
        this.commandChain = commandChain;
    }
    
}
