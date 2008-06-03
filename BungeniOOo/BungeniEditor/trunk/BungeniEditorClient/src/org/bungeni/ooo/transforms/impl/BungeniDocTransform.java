/*
 * BungeniDocTransform.java
 *
 * Created on June 3, 2008, 1:44 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.ooo.transforms.impl;

import com.sun.star.frame.XStorable;
import com.sun.star.lang.XComponent;
import java.util.HashMap;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public abstract class BungeniDocTransform implements IBungeniDocTransform {
    /** Creates a new instance of BungeniDocTransform */
    protected HashMap<String,Object> transformParams = new HashMap<String,Object>();

    public BungeniDocTransform(HashMap<String, Object> params) {
        setParams(params);
    }
    
    public BungeniDocTransform(){
        
    }
    
    public void setParams(HashMap<String, Object> params) {
        this.transformParams = params;
    }
    
    protected HashMap<String,Object> getParams(){
        return this.transformParams;
    }
    
    abstract public boolean transform(OOComponentHelper ooDocument) ;
    
  
}
