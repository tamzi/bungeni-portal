/*
 * ooDocMetadata.java
 *
 * Created on September 27, 2007, 10:20 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.ooo;

import com.sun.star.beans.UnknownPropertyException;

/**
 *
 * @author Administrator
 */
public class ooDocMetadata {
    private OOComponentHelper ooDocument;
   private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(ooDocMetadata.class.getName());
  
    /** Creates a new instance of ooDocMetadata */
    public ooDocMetadata(OOComponentHelper docHandle) {
        ooDocument  = docHandle;
    }
    
    public void AddProperty (String propertyName, String propertyValue ){
        if (!PropertyExists(propertyName)) {
        ooDocument.addProperty(propertyName, propertyValue);
        } else {
            SetProperty(propertyName, propertyValue);
        }
    }
    
    public void SetProperty (String propertyName, String propertyValue ) {
        ooDocument.setPropertyValue(propertyName, propertyValue);
    }
    
    public boolean PropertyExists (String propertyName) {
        return ooDocument.propertyExists(propertyName);
    }
    
    public String GetProperty (String propertyName)  {
        String propertyValue = null;
       try {
        if (PropertyExists (propertyName))
                propertyValue = ooDocument.getPropertyValue(propertyName);
       } catch (UnknownPropertyException ex) {
                log.debug("GetProperty:"+propertyName+" "+ ex.getMessage());
               
       } finally {
       return propertyValue;
       }
    }
}
