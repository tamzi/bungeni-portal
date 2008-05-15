/*
 * sectionExists.java
 *
 * Created on January 26, 2008, 10:25 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.toolbar.conditions.runnable;

import com.sun.star.beans.UnknownPropertyException;
import com.sun.star.beans.XPropertySet;
import com.sun.star.container.XNamed;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.text.XTextRange;
import com.sun.star.text.XTextSection;
import com.sun.star.text.XTextViewCursor;
import com.sun.star.uno.Any;
import org.bungeni.editor.BungeniEditorProperties;
import org.bungeni.editor.toolbar.conditions.BungeniToolbarCondition;
import org.bungeni.editor.toolbar.conditions.IBungeniToolbarCondition;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.ooo.utils.CommonExceptionUtils;

/**
 * 
 * Contextual evauluator that checks if the cursor is in a particular section in the document.
 * e.g. cursorInSection:section_name
 * will evaluate to true if the cursor is placed in section called section_name
 * will evaluate to false if the cursor is placed in section not called section_name
 * will evaluate to false if the cursor is not placed in a section.
 * @author Administrator
 */
public class cursorInSection implements IBungeniToolbarCondition {
    private OOComponentHelper ooDocument;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(cursorInSection.class.getName());
 
    /** Creates a new instance of sectionExists */
    public cursorInSection() {
    }

    public void setOOoComponentHelper(OOComponentHelper ooDocument) {
        this.ooDocument = ooDocument;
    }

    private String getSectionFromRange(XTextRange theRange ) {
        String theSectionName = ""; 
        try {
            XPropertySet rangeProps= ooQueryInterface.XPropertySet(theRange);
            XTextSection sectionInRange;
            sectionInRange = (XTextSection) ((Any) rangeProps.getPropertyValue("TextSection")).getObject();
             if ( sectionInRange != null) {
                 XNamed nameOfSection = ooQueryInterface.XNamed(sectionInRange);
                 theSectionName = nameOfSection.getName();       
             }
        } catch (UnknownPropertyException ex) {
            log.error("getSectionFromRange: " + ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error("getSectionFromRange: " + ex.getMessage());
        } finally {
            return theSectionName;
        }
    }
    
    private boolean check_condition(String sectionCurrent, String sectionCheck) {
             if (sectionCurrent.matches(sectionCheck)) 
                     return true;
             else
                     return false;
    }
    
    
    boolean check_cursorInSection (BungeniToolbarCondition condition) {
        boolean bReturn = true;
        try {
        String sectionToActUpon =  condition.getConditionValue();
        if (sectionToActUpon.equals("root")) {
           String activeDoc =  BungeniEditorProperties.getEditorProperty("activeDocumentMode");
           sectionToActUpon = BungeniEditorProperties.getEditorProperty("root:"+activeDoc);
        }
        XTextViewCursor viewCursor = ooDocument.getViewCursor();
        XPropertySet loXPropertySet = ooQueryInterface.XPropertySet(viewCursor);
        XTextSection matchedSection = (XTextSection)((Any)loXPropertySet.getPropertyValue("TextSection")).getObject();
        if (matchedSection != null){
                log.debug("check_cursorInSection: matchedSection was not null");
                //cursor is indeed inside a section
                //check if cursor is collapsed
                if (viewCursor.isCollapsed()) {
                        log.debug("check_cursorInSection: viewCursor is collapsed");
                        String matchedSectionName = ooQueryInterface.XNamed(matchedSection).getName();
                        bReturn = check_condition(matchedSectionName, sectionToActUpon);
                    //evaluate condition immeediately
                } else {
                    //get start range
                    XTextRange rangeStart = viewCursor.getStart();
                    //get end range
                    XTextRange rangeEnd = viewCursor.getEnd();
                    String strSectRangeStart = "", strSectRangeEnd = "";
                    strSectRangeStart =  this.getSectionFromRange(rangeStart);
                    strSectRangeEnd = this.getSectionFromRange(rangeEnd);
                    if (strSectRangeStart.equals(strSectRangeEnd))  {
                        log.debug("check_cursorInSection: start and end range sections are equal");
                        //evaluate condition here
                        bReturn = check_condition(strSectRangeStart, sectionToActUpon);
                    } else {
                        log.debug("check_cursorInSection: start and end range sections are NOT equal");
                        //fail condition if the starting span section is not equal to the ending span section
                        bReturn = false;
                    }
                }
         } else  {
             log.debug("check_cursorInSection: matchedSection was null");
             bReturn = false;
         }
            
        } catch (UnknownPropertyException ex) {
            log.error("check_cursorInSection: " + ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error("check_cursorInSection: " + ex.getMessage());
        } finally {
            return bReturn;
        }
    }
    
    public boolean processCondition(BungeniToolbarCondition condition) {
       // System.out.println("processing condition: "+ ooDocument.getDocumentTitle());
        return check_cursorInSection(condition);
    }
        
 


 }
