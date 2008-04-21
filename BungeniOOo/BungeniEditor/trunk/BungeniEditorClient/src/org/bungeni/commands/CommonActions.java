/*
 * CommonActions.java
 *
 * Created on December 20, 2007, 5:17 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.commands;

import com.sun.star.text.XText;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextCursor;
import org.bungeni.editor.macro.ExternalMacro;
import org.bungeni.editor.macro.ExternalMacroFactory;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.utils.CommonExceptionUtils;

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
            log.error("in action_addImageIntoSection:" + CommonExceptionUtils.getStackTrace(ex));
            bState=false;
         }   finally {
             return bState;
         }
    }
   
    public static boolean action_addSectionInsideSection(OOComponentHelper ooDoc, String targetSection, String newSection ) {
    boolean bState = false; 
        try {
            
            ExternalMacro AddSectionInsideSection =ExternalMacroFactory.getMacroDefinition("AddSectionInsideSection");
            AddSectionInsideSection.addParameter(ooDoc.getComponent());
            AddSectionInsideSection.addParameter(targetSection);
            AddSectionInsideSection.addParameter(newSection);
            ooDoc.executeMacro(AddSectionInsideSection.toString(), AddSectionInsideSection.getParams());
             bState= true;
        } catch (Exception ex) {
            log.error("action_addSectionIntoSection: error : " + ex.getMessage());
            log.error("in action_addSectionIntoSection:" + CommonExceptionUtils.getStackTrace(ex));
            //checkFieldsMessages.add(ex.getLocalizedMessage());
            bState=false;
         }   finally {
             return bState;
         }    
        
    }
    
    public static boolean action_insertSectionAfterSection(OOComponentHelper ooDoc, String targetSection, String newSection ) {
    boolean bState = false; 
        try {
            
        ExternalMacro createSectionMacro = ExternalMacroFactory.getMacroDefinition("InsertSectionAfterSection");
        createSectionMacro.addParameter(ooDoc.getComponent());
        createSectionMacro.addParameter(newSection);
        createSectionMacro.addParameter(targetSection);
        ooDoc.executeMacro(createSectionMacro.toString(), createSectionMacro.getParams());
             bState= true;
        } catch (Exception ex) {
            log.error("action_insertSectionAfterSection: error : " + ex.getMessage());
            log.error("in action_insertSectionAfterSection:" + CommonExceptionUtils.getStackTrace(ex));
            //checkFieldsMessages.add(ex.getLocalizedMessage());
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
            log.error("in action_addSectionIntoSectionwithStyling:" + CommonExceptionUtils.getStackTrace(ex));
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
            log.error("action_addDocIntoSection: error : " + ex.getMessage());
            log.error("in action_addDocIntoSection:" + CommonExceptionUtils.getStackTrace(ex));
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
            log.error("actionn_setInputFieldValue: error : " + ex.getMessage());
            log.error("in actionn_setInputFieldValue:" + CommonExceptionUtils.getStackTrace(ex));
            //checkFieldsMessages.add(ex.getLocalizedMessage());
            bState=false;
         }   finally {
             return bState;
         }
    }  

    
    public static boolean action_searchAndReplace(OOComponentHelper ooDoc, String searchFor, String replaceWith) {
        boolean bState = false; 
       try {
           ExternalMacro searchAndReplace= ExternalMacroFactory.getMacroDefinition("SearchAndReplace");
            searchAndReplace.addParameter(ooDoc.getComponent());
            searchAndReplace.addParameter(searchFor);
            searchAndReplace.addParameter(replaceWith);
            ooDoc.executeMacro( searchAndReplace.toString(),  searchAndReplace.getParams());
            bState= true;
        } catch (Exception ex) {
            log.error("action_searchAndReplace: error : " + ex.getMessage());
            log.error("in action_searchAndReplace:" + CommonExceptionUtils.getStackTrace(ex));
            //checkFieldsMessages.add(ex.getLocalizedMessage());
            bState=false;
         }   finally {
             return bState;
         }
    }  

    public static boolean action_createRootSection(OOComponentHelper ooDoc, String sectionName) {
        boolean bResult = false;
        try {
            XText docText = ooDoc.getTextDocument().getText();
            XTextCursor docCursor = docText.createTextCursor();
            docCursor.gotoStart(false);
            docCursor.gotoEnd(true);
            XTextContent theContent = ooDoc.createTextSection(sectionName, (short)1);
            docText.insertTextContent(docCursor, theContent, true);
            bResult = true;
        } catch (IllegalArgumentException ex) {
            log.error("in action_createRootSection :" + ex.getMessage());
            log.error("in action_createRootSection :" + CommonExceptionUtils.getStackTrace(ex));
        } finally {
            return bResult;
        }
    }
    
     public static boolean action_replaceTextWithField(OOComponentHelper ooDoc, String hintName, String hintPlaceholderValue) {
        boolean bState = false; 
        try {
            ExternalMacro ReplaceTextWithField = ExternalMacroFactory.getMacroDefinition("ReplaceTextWithField");
            ReplaceTextWithField.addParameter(ooDoc.getComponent());
            ReplaceTextWithField.addParameter(hintName);
            ReplaceTextWithField.addParameter(hintPlaceholderValue);
            ooDoc.executeMacro(ReplaceTextWithField.toString(), ReplaceTextWithField.getParams());
             bState= true;
        } catch (Exception ex) {
            log.error("action_replaceTextWithField: error : " + ex.getMessage());
            log.error("in action_replaceTextWithField:" + CommonExceptionUtils.getStackTrace(ex));
            //checkFieldsMessages.add(ex.getLocalizedMessage());
            bState=false;
         }   finally {
             return bState;
         }
     }
    
     
     public static boolean action_InsertArrayAsBulletListAtCurrentCursor(OOComponentHelper ooDoc, String[] titles, String[] uris) {
         boolean bState = false;
         try{
                ExternalMacro InsertArrayAsBulletListAtCurrentCursor = ExternalMacroFactory.getMacroDefinition("InsertArrayAsBulletListAtCurrentCursor");
                InsertArrayAsBulletListAtCurrentCursor.addParameter(ooDoc.getComponent());
                InsertArrayAsBulletListAtCurrentCursor.addParameter(titles);
                InsertArrayAsBulletListAtCurrentCursor.addParameter(uris);
                ooDoc.executeMacro(InsertArrayAsBulletListAtCurrentCursor.toString(), InsertArrayAsBulletListAtCurrentCursor.getParams());
                  } catch(Exception ex) {
             
         } finally {
             return bState;
         }
     }
     public static boolean action_insertArrayAsBulletList(OOComponentHelper ooDoc, String bookmarkName, String[] titles, String[] uris) {
        boolean bState = false; 
        try {
             ExternalMacro insertArrayAsBulletList = ExternalMacroFactory.getMacroDefinition("InsertArrayAsBulletList");
                insertArrayAsBulletList.addParameter(ooDoc.getComponent());
                insertArrayAsBulletList.addParameter(bookmarkName);
                insertArrayAsBulletList.addParameter(titles);
                insertArrayAsBulletList.addParameter(uris);
                ooDoc.executeMacro(insertArrayAsBulletList.toString(), insertArrayAsBulletList.getParams());
             bState= true;
        } catch (Exception ex) {
            log.error("action_insertArrayAsBulletList: error : " + ex.getMessage());
            log.error("in action_insertArrayAsBulletList:" + CommonExceptionUtils.getStackTrace(ex));
            //checkFieldsMessages.add(ex.getLocalizedMessage());
            bState=false;
         }   finally {
             return bState;
         }
     }
     
     
     
 }
