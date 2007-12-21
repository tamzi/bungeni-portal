/*
 * CommonActions.java
 *
 * Created on December 20, 2007, 5:17 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.commands;

import org.bungeni.editor.macro.ExternalMacro;
import org.bungeni.editor.macro.ExternalMacroFactory;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public class CommonActions {
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(CommonActions.class.getName());

    /** Creates a new instance of CommonActions */
    public CommonActions() {
    }
    
   
    public static boolean action_addImageIntoSection(OOComponentHelper ooDoc, String intoSection, String logoPath) {
        boolean bState = false; 
        try {
            log.debug("executing addImageIntoSection : intoSection = "+ intoSection + " , logoPath = "+logoPath);
             ExternalMacro addImageIntoSection = ExternalMacroFactory.getMacroDefinition("AddImageIntoSection");
             addImageIntoSection.addParameter(ooDoc.getComponent());
             addImageIntoSection.addParameter(intoSection);
             addImageIntoSection.addParameter(logoPath);
             ooDoc.executeMacro(addImageIntoSection.toString(), addImageIntoSection.getParams());
             bState= true;
        } catch (Exception ex) {
            log.error("action_addImageIntoSection: error : " + ex.getMessage());
            bState=false;
         }   finally {
             return bState;
         }
    }
   
     public static boolean action_addSectionIntoSectionwithStyling(OOComponentHelper ooDoc, String parentSection, String newSectionName, long sectionBackColor, float sectionLeftMargin) {
        boolean bState = false; 
        try {
            ExternalMacro AddSectionInsideSection = ExternalMacroFactory.getMacroDefinition("AddSectionInsideSectionWithStyle");
            AddSectionInsideSection.addParameter(ooDoc.getComponent());
            AddSectionInsideSection.addParameter(parentSection);
            AddSectionInsideSection.addParameter(newSectionName);
            AddSectionInsideSection.addParameter(sectionBackColor);
            AddSectionInsideSection.addParameter(sectionLeftMargin);
            ooDoc.executeMacro(AddSectionInsideSection.toString(), AddSectionInsideSection.getParams());
             bState= true;
        } catch (Exception ex) {
            log.error("action_addSectionIntoSectionwithStyling: error : " + ex.getMessage());
            //checkFieldsMessages.add(ex.getLocalizedMessage());
            bState=false;
         }   finally {
             return bState;
         }
    }


  public static boolean action_addDocIntoSection(OOComponentHelper ooDoc, String intoSection, String fragmentName) {
        boolean bState = false; 
       try {
            ExternalMacro insertDocIntoSection = ExternalMacroFactory.getMacroDefinition("InsertDocumentIntoSection");
            insertDocIntoSection.addParameter(ooDoc.getComponent());
            insertDocIntoSection.addParameter(intoSection)  ;
            insertDocIntoSection.addParameter(fragmentName);
            ooDoc.executeMacro(insertDocIntoSection.toString(), insertDocIntoSection.getParams());
            bState= true;
        } catch (Exception ex) {
            log.error("action_addImageIntoSection: error : " + ex.getMessage());
            //checkFieldsMessages.add(ex.getLocalizedMessage());
            bState=false;
         }   finally {
             return bState;
         }
    } 


    public static boolean action_setInputFieldValue(OOComponentHelper ooDoc, String hintName, String strDebateDate, String unprotectSection) {
        boolean bState = false; 
       try {
           ExternalMacro setFieldValue = ExternalMacroFactory.getMacroDefinition("SetReferenceInputFieldValue");
            setFieldValue.addParameter(ooDoc.getComponent());
            setFieldValue.addParameter(hintName);
            setFieldValue.addParameter(strDebateDate);
            setFieldValue.addParameter(unprotectSection);
            ooDoc.executeMacro( setFieldValue.toString(),  setFieldValue.getParams());
            bState= true;
        } catch (Exception ex) {
            log.error("action_addImageIntoSection: error : " + ex.getMessage());
            //checkFieldsMessages.add(ex.getLocalizedMessage());
            bState=false;
         }   finally {
             return bState;
         }
    }  

}
