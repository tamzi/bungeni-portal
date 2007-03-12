/*
 * RuleXMLValidator.java
 *
 * Created on February 16, 2007, 11:20 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.bungeniruleparser;

import java.util.HashMap;

/**
 *
 * @author ashok hariharan
 * @description container class for rulexmliterator
 */
public class RuleXMLValidator {
    private RuleXMLIterator m_rxi;
    /** Creates a new instance of RuleXMLValidator */
    public RuleXMLValidator() {
        m_rxi = new RuleXMLIterator();
    }
    
    public RuleXMLValidator(String xmlFile){
        m_rxi = new RuleXMLIterator(xmlFile);
        m_rxi.buildRules();
    }
    
    public String checkElement(String strElementName){
       if( m_rxi.hasTag(strElementName)){
           return (new String("0~Valid"));
       }
       else{
           //fails test for existence of style
           //return failure message
           return (new String("-1~Invalid Style"));
       }
           
    }
    
    public String[] keys(){
        String[] obj = m_rxi.Keys();
        if (obj == null)
            return null;
        else
            return obj;
     }
    
    public RuleXMLElement getElement(String styleName){
        if (m_rxi.hasTag(styleName))
            return  m_rxi.getElement(styleName);
        else
            return null;
    }
  /*  
    public int ExecuteRuleEngine(){
        m_rxi.Parse();
        buildRuleStructures();
        return 0;
    }
   * 
   */ 
    /*iterate through the rule xml and build rule validation structures*/
    private void buildRuleStructures(){
        
        
    }
}
