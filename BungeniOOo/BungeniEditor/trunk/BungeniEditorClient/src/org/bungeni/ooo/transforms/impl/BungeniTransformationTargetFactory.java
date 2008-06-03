/*
 * BungeniTransformationTargetFactory.java
 *
 * Created on June 3, 2008, 4:31 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.ooo.transforms.impl;

/**
 *
 * @author Administrator
 */
public class BungeniTransformationTargetFactory {
        private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(BungeniTransformationTargetFactory.class.getName());

    /** Creates a new instance of BungeniTransformationTargetFactory */
    public BungeniTransformationTargetFactory() {
    }
    
    public static IBungeniDocTransform getTransformClass(BungeniTransformationTarget aTarget) {
         IBungeniDocTransform aTransform = null;
       try {
           Class transformClass;
             transformClass = Class.forName(aTarget.targetClass);
             aTransform = (IBungeniDocTransform) transformClass.newInstance();

       } catch (ClassNotFoundException ex) {
           log.error("getTransformClass:"+ ex.getMessage());
        } finally {
             return aTransform;
        }
    }


    
}
