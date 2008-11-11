/*
 * HTMLTransform.java
 *
 * Created on June 3, 2008, 4:15 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.ooo.transforms.loadable;

import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.transforms.impl.BungeniDocTransform;

/**
 *
 * @author Administrator
 */
public class AnXmlTransform extends BungeniDocTransform {
        private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(AnXmlTransform.class.getName());
 
    /** Creates a new instance of HTMLTransform */
    public AnXmlTransform() {
        super();
    }

    public boolean transform(OOComponentHelper ooDocument) {
        boolean bState = false;
        try {
       //      XStorable docStore =ooDocument.getStorable();
       //     String urlString = (String) getParams().get("StoreToUrl");
       //     docStore.storeToURL(urlString, getTransformProps().toArray(new PropertyValue[getTransformProps().size()]));
            bState= true;
        } catch (Exception ex) {
            log.error("transform : " + ex.getMessage());
        }
        return bState;
    }
    

}
