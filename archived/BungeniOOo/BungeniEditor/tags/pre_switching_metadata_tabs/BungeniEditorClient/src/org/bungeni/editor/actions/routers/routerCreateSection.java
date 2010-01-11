/*
 * routerCreateSection.java
 *
 * Created on March 11, 2008, 12:54 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.actions.routers;

import com.sun.star.text.XText;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextViewCursor;
import java.util.HashMap;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.actions.toolbarSubAction;
import org.bungeni.error.BungeniMsg;
import org.bungeni.error.BungeniValidatorState;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public class routerCreateSection extends defaultRouter {
   private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(routerCreateSection.class.getName());
 

    /** Creates a new instance of routerCreateSection */
    public routerCreateSection() {
        super();
        
    }
    
    public BungeniValidatorState route_TextSelectedInsert(toolbarAction action, toolbarSubAction subAction, OOComponentHelper ooDocument) {
     String newSectionName = "";
      newSectionName = get_newSectionNameForAction(action, ooDocument);
         if (newSectionName.length() == 0 ) {
             
         } else {
            boolean bAction = action_createSystemContainerFromSelection(ooDocument, newSectionName);
            if (bAction ) {
                //set section type metadata
                ooDocument.setSectionMetadataAttributes(newSectionName, get_newSectionMetadata(action));
            } else {
                log.error("routeAction_TextSelectedInsertAction_CreateSection: error while creating section ");
                return new BungeniValidatorState(true, new BungeniMsg("FAILURE_CREATE_SECTION"));
            }
         }      
      return new BungeniValidatorState(true, new BungeniMsg("SUCCESS")); 
    }

    
    
    /**** 
     *
     * private APIs for this action 
     *
     ****/
 private String get_newSectionNameForAction(toolbarAction pAction, OOComponentHelper ooDocument) {
         String newSectionName = "";
         if (pAction.action_numbering_convention().equals("single")) {
             newSectionName = pAction.action_naming_convention();
         } else if (pAction.action_numbering_convention().equals("serial")) {
             String sectionPrefix = pAction.action_naming_convention();
             for (int i=1 ; ; i++) {
                if (ooDocument.hasSection(sectionPrefix+i)) {
                    continue;
                } else {
                    newSectionName = sectionPrefix+i;
                    break;
                }
             }
           
         } else {
             log.error("get_newSectionNameForAction: invalid action naming convention: "+ pAction.action_naming_convention());
         }
         return newSectionName;
    }

 private boolean action_createSystemContainerFromSelection(OOComponentHelper ooDoc, String systemContainerName){
        boolean bResult = false; 
        try {
        XTextViewCursor xCursor = ooDoc.getViewCursor();
        XText xText = xCursor.getText();
        XTextContent xSectionContent = ooDoc.createTextSection(systemContainerName, (short)1);
        xText.insertTextContent(xCursor, xSectionContent , true); 
        bResult = true;
        } catch (com.sun.star.lang.IllegalArgumentException ex) {
            bResult = false;
            log.error("in addTextSection : "+ex.getLocalizedMessage(), ex);
        }  finally {
            return bResult;
        }
    }

     private HashMap<String,String> get_newSectionMetadata(toolbarAction pAction) {
         HashMap<String,String> metaMap = new HashMap<String,String>();
         metaMap.put("BungeniSectionType", pAction.action_section_type());
         return metaMap;
     }
}
