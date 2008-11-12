/*
 * PDFTransform.java
 *
 * Created on June 3, 2008, 1:48 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.ooo.transforms.loadable;

import com.sun.star.beans.PropertyValue;
import com.sun.star.frame.XStorable;
import java.util.ArrayList;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.transforms.impl.BungeniDocTransform;
import org.bungeni.ooo.utils.CommonExceptionUtils;

/**
 *
 * @author Administrator
 */
public class ODTSaveTransform extends BungeniDocTransform {

      private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(ODTSaveTransform.class.getName());
 
    /** Creates a new instance of PDFTransform */
    public ODTSaveTransform() {
        super();
    }

    public boolean transform(OOComponentHelper ooDocument) {
        boolean bState = false;
       try {
             XStorable docStore =ooDocument.getStorable();
            String urlString = (String) getParams().get("StoreToUrl");
            PropertyValue[] props = getTransformProps().toArray(new PropertyValue[getTransformProps().size()]);
            docStore.storeAsURL(urlString, props);
            bState= true;
       } catch (com.sun.star.io.IOException ex) {
            log.error("transform : "+ ex.getMessage());
            log.error("transform : " + CommonExceptionUtils.getStackTrace(ex));
       }
        return bState;
    }
    
    private ArrayList<PropertyValue> getTransformProps(){
        ArrayList<PropertyValue> props = new ArrayList<PropertyValue>(0);
        //return an empty array to use native format
        return props;
    }
    
}
