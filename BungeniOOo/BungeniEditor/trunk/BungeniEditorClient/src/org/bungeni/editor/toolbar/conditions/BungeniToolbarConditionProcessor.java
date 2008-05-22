/*
 * BungeniToolbarConditionProcessor.java
 *
 * Created on January 26, 2008, 3:27 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.toolbar.conditions;

import java.util.ArrayList;
import java.util.HashMap;
import org.bungeni.editor.toolbar.conditions.operators.baseOperator;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.utils.CommonExceptionUtils;

/**
 *
 * @author Administrator
 */
public class BungeniToolbarConditionProcessor {
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(BungeniToolbarConditionProcessor.class.getName());
 
    protected OOComponentHelper ooDocument;
    protected BungeniToolbarConditionOperator matchedCondition = null;
    protected String conditionValue;
    protected String[] individualConditions;
    protected HashMap<String, BungeniToolbarConditionOperator> operators = new HashMap<String, BungeniToolbarConditionOperator>();

    
    /** Creates a new instance of BungeniToolbarConditionProcessor */
    public BungeniToolbarConditionProcessor(OOComponentHelper ooDoc, String conditionVal) {
        this.ooDocument = ooDoc;
        this.conditionValue = conditionVal;
        operators = BungeniToolbarConditionOperatorFactory.getObjects();
        processOperators(conditionVal);
    }
    
    public void setOOComponentHandle(OOComponentHelper ooIncoming) {
        if (ooDocument == ooIncoming) { //incoming ooDoc handle = cached ooDoc handle
            return;
        } else {
            this.ooDocument = ooIncoming;
        }
    }
    protected void processOperators(String fullConditionValue) {
        //we split string by operators 
        //currently only a single type of operator identification is supported
        log.debug("1. processOperators: "+ fullConditionValue );
        java.util.Iterator<String> keys = operators.keySet().iterator();
        while (keys.hasNext()) {
            String key = keys.next();
            BungeniToolbarConditionOperator condition = operators.get(key);
            if (fullConditionValue.indexOf(condition.getCondition()) != -1) {
                matchedCondition = condition;
                individualConditions = fullConditionValue.split(condition.getCondition());
                return;
            }
        } 
        //if it has reached here, no conditions were matched, i.e. it is a singular evaluation condition
        
    }
    
    private boolean evaluateWithOperator(){
        boolean bResult = false;
        try {
        //use the matched condition to evaluate the condition
          String conditionProcessorClass = matchedCondition.getConditionProcessorClass();
          IBungeniToolbarConditionOperator selectedOperator;
          Class processorClassRef;
          processorClassRef = Class.forName(conditionProcessorClass);
          selectedOperator = (IBungeniToolbarConditionOperator)processorClassRef.newInstance();
          selectedOperator.setOOoComponentHelper(ooDocument);
          selectedOperator.setOperatingCondition(matchedCondition, individualConditions);
          bResult = selectedOperator.result();
         } catch (InstantiationException ex) {
               log.error("evaluateWithOperator: " + ex.getMessage());
               log.error("evaluateWithOperator : " + this.conditionValue);
               log.error("evaluateWithOperator: " + CommonExceptionUtils.getStackTrace(ex));
           } catch (IllegalAccessException ex) {
               log.error("evaluateWithOperator: " + ex.getMessage());
               log.error("evaluateWithOperator : " + this.conditionValue);
               log.error("evaluateWithOperator: " + CommonExceptionUtils.getStackTrace(ex));
           }  catch (ClassNotFoundException ex) {
               log.error("evaluateWithOperator: " + ex.getMessage());
               log.error("evaluateWithOperator : " + this.conditionValue);
               log.error("evaluateWithOperator: " + CommonExceptionUtils.getStackTrace(ex));
          }  finally {
            return bResult;
        }
    }
    
    private boolean evaluateWithoutOperator(){
        boolean bResult = false;
        try {   
            
            BungeniToolbarCondition toolbarCond =    new BungeniToolbarCondition(conditionValue);
            IBungeniToolbarCondition iCondition = baseOperator.getConditionObject(toolbarCond.getConditionClass());
            iCondition.setOOoComponentHelper(ooDocument);
            bResult = iCondition.processCondition(toolbarCond) ;
          } catch (Exception ex) {
               log.error("evaluateWithoutOperator: " + ex.getMessage());
               log.error("evaluateWithoutOperator : " + this.conditionValue);
               log.error("evaluateWithoutOperator: " + CommonExceptionUtils.getStackTrace(ex));
          } finally {
              return bResult;
        }
    }
    
    
    synchronized public boolean evaluate() {
        boolean bResult = false;
        if (matchedCondition == null) {
            //singular condition
           bResult = evaluateWithoutOperator();
        } else {
           bResult =  evaluateWithOperator();
        }
        return bResult;
    }

 
}
