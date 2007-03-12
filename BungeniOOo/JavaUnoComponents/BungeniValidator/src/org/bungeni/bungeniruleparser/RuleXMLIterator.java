/*
 * RuleXMLIterator.java
 *
 * Created on February 16, 2007, 11:20 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.bungeniruleparser;



import org.jdom.JDOMException;
import org.jdom.input.SAXBuilder;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.TreeMap;
import org.jdom.Document;
import org.jdom.Element;
import org.jdom.xpath.*;
/**
 *
 * @author ashok
 */
public class RuleXMLIterator {
    private String xmlFileName; //file name of inputsource xml file
    private SAXBuilder xmlParser; //jdom parser object
    private Document xmlDoc; //xml document object
    private HashMap m_ruleMap; //rule map object
    private HashMap _tagSequenceMap; //element name sequence map
    private TreeMap m_tagSequenceMap; //tree map sequencer
    private Integer _tagSequencer; //sequencer object
    
    /** Creates a new instance of RuleXMLIterator */
    public RuleXMLIterator() {
       // System.out.println("initiailizing objects in RuleXMLIterator");
        m_ruleMap = new HashMap();
        m_tagSequenceMap = new TreeMap();
       _tagSequenceMap = new HashMap();        
        xmlFileName = "";
        
    }
    
    public RuleXMLIterator(String xmlFile){
        //System.out.println("initiailizing parser in RuleXMLIterator");
        m_ruleMap = new HashMap();
        m_tagSequenceMap = new TreeMap();
        _tagSequenceMap = new HashMap();
        _tagSequencer = new Integer(0);
        /*after initializing variables init xml parser*/
        xmlParser = new org.jdom.input.SAXBuilder();
        xmlFileName = xmlFile;
    }
  /*  
    public void Parse() {
        try     {
            xmlDoc = xmlParser.build(xmlFileName);
            org.jdom.Element root = xmlDoc.getRootElement();
            listChildren(root, 0);
        }
        catch (JDOMException e){
             System.out.println(" is not well-formed.");
             System.out.println(e.getMessage());
        }
        catch (IOException ex) {
            System.out.println(ex.getMessage());
                                                    
        }
       
    }
  */
    public void buildRules(){
        try{
            xmlDoc = xmlParser.build(xmlFileName);
            org.jdom.Element root = xmlDoc.getRootElement();
            //rule map is built inside the recursive funciton
            iterateRules(root, 0);
            //rule map is built now
            //now generate the ordered treemap
            m_tagSequenceMap = new TreeMap(_tagSequenceMap);
        }
        catch (JDOMException e){
             System.out.println(" is not well-formed.");
             System.out.println(e.getMessage());
        }
        catch (IOException ex) {
            System.out.println(ex.getMessage());
                                                    
        }
    }
    
    public void printRuleMap(){
        System.out.println("Rule Map :: " + m_ruleMap);
        
    }
    
    
   public String[] Keys(){
        
       if (m_ruleMap.keySet().size() == 0 ) return null;
       Object[] objectArray = m_ruleMap.keySet().toArray();
       String[] strKeySet = (String[])m_ruleMap.keySet().toArray(new String[m_ruleMap.keySet().size()]);

       return strKeySet;
               
    }
   
    public boolean hasTag(String elementName){
        if (m_ruleMap.containsKey(elementName))
            return true;
        else
            return false;
                 
    }
    
    public RuleXMLElement getElement(String styleName){
        RuleXMLElement rxe= new RuleXMLElement();
        rxe =(RuleXMLElement) m_ruleMap.get(styleName);
        return rxe;
    }

    public void printSequenceMap() {
        System.out.println("Sequence Map :: " + m_tagSequenceMap);
    }
    private void iterateRules(Element current, int depth){
        //printSpaces(depth);
        //System.out.println(current.getName()+ " depth = "+ (new Integer(depth)).toString());
        
        //dont put error elements in hashmap
        if (!current.getName().equals("error")) {
            _tagSequencer++;
            RuleXMLElement rxeObj;
            rxeObj = new RuleXMLElement(current);
            //System.out.println("rxObj element name = "+ rxeObj.getElementName());
            m_ruleMap.put(rxeObj.getElementName(), rxeObj);
            _tagSequenceMap.put(_tagSequencer, rxeObj.getElementName());
            
        }
        
        List children = current.getChildren();
        Iterator iterator = children.iterator();
        
        while (iterator.hasNext()) {
        
            Element child = (Element) iterator.next();
            iterateRules(child, depth+1);
        
        }
        
    }
    
    /*
    
  public  void listChildren(Element current, int depth) {
   try{
    printSpaces(depth);
    System.out.println("name ="  +current.getName());
    System.out.println("id = "+current.getAttribute("id"));
    System.out.println("type = "+current.getAttribute("type"));
    System.out.println("maxOccurs = "+current.getAttribute("maxOccurs"));
    if (current.getParentElement() != null){
    System.out.println("parent name = " + current.getParentElement().getName());
    }
    String[] siblingobj = new String[2];
    siblingobj = getPrevNextSiblings(current);
    if (siblingobj != null) {
    System.out.println("prev sibling = "+ siblingobj[0]);
    System.out.println("next sibling = "+ siblingobj[1]);
    }
    List children = current.getChildren();
    Iterator iterator = children.iterator();
    while (iterator.hasNext()) {
      Element child = (Element) iterator.next();
      listChildren(child, depth+1);
    }
    }
   catch (Exception e){
       System.out.println(e.getMessage());
   }
    
  }
  */

 private String[] getPrevNextSiblings(Element myElement){ 
     String[] siblings = new String[2];
    Element parent = myElement.getParentElement();
    if (parent == null )return null;
    List children = parent.getChildren();
    int myIndex = children.indexOf(myElement);
    //get prevSibling
    if(myIndex > 0 && myIndex < children.size()) {
        Element prevElement = (Element)children.get(myIndex - 1);
        siblings[0] = prevElement.getName();
    }
    //get nextSibling
    if(myIndex >= 0 && myIndex < children.size() - 1) {
        Element nextElement = (Element)children.get(myIndex + 1);
        siblings[1] = nextElement.getName();
    }
    return siblings;
}

  private int elementExists(String strElement){
      int nReturn = 0;
              try     {
            java.util.List foundElements = org.jdom.xpath.XPath.selectNodes(xmlDoc,
                                                                       "//" +
                                                                       strElement);
            if (foundElements.size() > 0){
                nReturn = foundElements.size();
            }
        }
        catch (JDOMException ex) {
            System.out.println( ex.getMessage());
        }
        finally {
            return nReturn;
        }
    
      
  }
  
  private  void printSpaces(int n) {
    
    for (int i = 0; i < n; i++) {
      System.out.print(' '); 
    }
    
  }


}

