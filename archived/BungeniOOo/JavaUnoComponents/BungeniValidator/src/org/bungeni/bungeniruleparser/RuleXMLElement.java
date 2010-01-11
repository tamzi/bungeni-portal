/*
 * RuleXMLElement.java
 *
 * Created on February 16, 2007, 11:20 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.bungeniruleparser;

import java.util.List;
import org.jdom.Element;
import org.openoffice.bungenivalidator.BungeniRuleElement;

/**
 *
 * @author Ashok Hariharan
 */
public class RuleXMLElement {
    public String elementName; //name of element
   
    public String ruleElementType; //block or tag
    public String elementType; //repeat or none
    public String maxOccurs;
    public String parentElement; //parent element of current element
    public String nextElement; //hash index to next element
    public String previousElement; //hash index to previous element
    
    /** Creates a new instance of RuleXMLElement */
    
    public RuleXMLElement() {
        //System.out.println("default constructor RuleXMLElement");
        elementName = "";
        ruleElementType = "";
        maxOccurs = "";
        parentElement = "";
        nextElement = "";
        previousElement = "";
        
    }
    

    public String getRuleElementType(){
        return ruleElementType;
    }   
    public String getMaxOccurs(){
        return maxOccurs;
    }        

    public org.openoffice.bungenivalidator.BungeniRuleElement toBungeniRuleElement(){
        
        return new org.openoffice.bungenivalidator.BungeniRuleElement 
                (elementName, ruleElementType, elementType, 
                maxOccurs, parentElement, nextElement, previousElement);
                 
    }
 
 public String toString(){

        return "\n\tElement Name: " + elementName + "\n" +
                "\tRule Element Type: " + ruleElementType + "\n" +
                "\tPrevious Element: " + previousElement + "\n" +
                "\tNext Element: "+ nextElement + "\n"+
                "\tParent Element: "+ parentElement + "\n" +
                "\t --------------------------------------------------- \n\n";
                    
    }
            
    
    public String getElementName(){
        return elementName;
    }
    
     public RuleXMLElement(Element ruleElement){
        //System.out.println("Inside main constructor ruleXMLElement"); 
        elementName = ruleElement.getName();
        
        if (elementName.startsWith("block-"))
            ruleElementType="block";
        else if (elementName.equals("error"))
            ruleElementType="error";
        else
            ruleElementType="tag";
  
       if (!ruleElementType.equals("error")) {
           
           if (ruleElement.getAttribute("maxOccurs") == null)
                maxOccurs = "";
            else
                maxOccurs = ruleElement.getAttributeValue("maxOccurs");

           if (ruleElement.getAttribute("type") == null)
                elementType = "none";
            else
                elementType = ruleElement.getAttributeValue("type");

           if (ruleElement.getParentElement() != null)
               parentElement = ruleElement.getParentElement().getName();
           else
               parentElement = "";

            nextElement = getNextSibling(ruleElement);
            previousElement = getPrevSibling(ruleElement);
        
        }
        //System.out.println("End of main constructor ruleXMLElement"); 
        
    }
     
     
     
    private String getPrevSibling(Element myElement){
        
     String sibling ="";
     
    Element parent = myElement.getParentElement();
    if (parent == null )return null;
    List children = parent.getChildren();
    int myIndex = children.indexOf(myElement);
    //get prevSibling
    if(myIndex > 0 && myIndex < children.size()) {
        Element prevElement = (Element)children.get(myIndex - 1);
        sibling = prevElement.getName();
    }
    
    return sibling;
    
    }
    
    private String getNextSibling(Element myElement){
        
     String sibling ="";
     
    Element parent = myElement.getParentElement();
    if (parent == null )return null;
    List children = parent.getChildren();
    int myIndex = children.indexOf(myElement);
  
    //get nextSibling
    if(myIndex >= 0 && myIndex < children.size() - 1) {
        Element nextElement = (Element)children.get(myIndex + 1);
        sibling = nextElement.getName();
    }
    return sibling;
}
    
         
    
    
   
}
