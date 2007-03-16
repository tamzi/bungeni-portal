/*
 * RssDocument.java
 *
 * Created on March 9, 2007, 1:24 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.rssparser;

import java.text.SimpleDateFormat;
import java.util.Iterator;
import java.util.List;
import java.util.Vector;
import org.jdom.Element;
import org.jdom.Namespace;
import org.jdom.output.XMLOutputter;
import org.openoffice.rssreader.BungeniRssDocument;
import org.openoffice.rssreader.BungeniRssHeader;
import org.openoffice.rssreader.BungeniRssRecord;

/**
 *
 * @author ashok
 */
public class RssDocument {
    private Element rootElement;
    private Element channelElement;
    private RssHeader rssHeader;
    private RssRecord[] rssRecords;
    private String[] custom_namespace;
    
    /** Creates a new instance of RssDocument */
    public RssDocument(Element root) {
        rootElement = root;
        channelElement = null ;
    }
    
    public org.openoffice.rssreader.BungeniRssHeader getBungeniRssHeader(){
        org.openoffice.rssreader.BungeniRssHeader bungeniHeaderObj = rssHeader.toBungeniRssHeader();
        return bungeniHeaderObj;
    }
    
    public org.openoffice.rssreader.BungeniRssRecord[] getBungeniRssRecords(){
             org.openoffice.rssreader.BungeniRssRecord[] bungeniRecordObjs  = new org.openoffice.rssreader.BungeniRssRecord[rssRecords.length];
            for (int i=0 ; i < rssRecords.length ; i++){
                bungeniRecordObjs[i] = rssRecords[i].toBungeniRssRecord();
            }
            return bungeniRecordObjs;
    }
    
    public org.openoffice.rssreader.BungeniRssDocument toBungeniRssDocument(){
   
        org.openoffice.rssreader.BungeniRssDocument docObj = new org.openoffice.rssreader.BungeniRssDocument(getBungeniRssHeader(), getBungeniRssRecords());
        
        return docObj;
    }
    //constructor that handles custom namespaces
    public RssDocument(Element root, String[] customNS) {
        rootElement = root;
        channelElement = null ;
        if (customNS.length > 0){
            custom_namespace = new String[customNS.length];
            for (int i= 0; i < customNS.length ; i++)
                custom_namespace[i] = customNS[i];
            }    
    }
    
    
    public boolean buildFeeds(){
        if (buildRssHeader()){
            if (buildRssBody())
                return true;
            else
                return false;        
        }
        else
            return false;
    }
    private Element getChild (Element parent, String childName){
        Element child = parent.getChild(childName);
        if (child == null){
            System.out.println("child element with name " + childName + "does not exist.");
            return null;
        }
        return child;
        
    }
    private String getChildElementText(Element element, String childName){
        Element childElement = getChild(element, childName);
        if (childElement == null){
            return new String("");
        }
        return childElement.getText();
    }
    private boolean buildRssHeader(){
        boolean defaultoutput=false;
        try {
        channelElement = getChild(rootElement, "channel");
        if (channelElement != null ){
            
            //System.out.println("inside building rss header");
            Element title = getChild(channelElement, "title");
            Element link =getChild(channelElement,"link");
            Element desc =getChild(channelElement,"description");
            Element lang =getChild(channelElement,"language");
            Element generator = getChild(channelElement,"generator");
            rssHeader = new RssHeader();
            
            //System.out.println("setting rss header");
            rssHeader.setChanneltitle(title.getText());
            rssHeader.setChanneldescription(desc.getText());
            rssHeader.setChannelgenerator(generator.getText());
            rssHeader.setChannellanguage(lang.getText());
            rssHeader.setChannelurl(link.getText());
            defaultoutput = true;
        }
        else
            defaultoutput = false;
        }
        catch (Exception e){
            System.out.println("error in buildRssHeader : "+ e.getMessage());
        }
        finally{
            return defaultoutput;
        }
    }
    
   private boolean buildRssBody(){
       boolean defaultoutput = false;
       try {
               Vector vRssRecords = new Vector();
               List listItems = channelElement.getChildren("item");
               if (listItems == null){
                    //System.out.println("list items were null");
                   defaultoutput = false;
               }
               else {
                  Iterator items = listItems.iterator();
                  //System.out.println("iterating list items");
                   SimpleDateFormat rfc822_format = new SimpleDateFormat( "EEE, dd MMM yyyy hh:mm:ss z" );                    

                    while (items.hasNext()) {   

                            System.out.println("parsing items");
                            Element item = (Element) items.next();  
                            RssRecord rssRecord = new RssRecord();
                            rssRecord.setFeedtitle(getChildElementText(item, "title"));
                            rssRecord.setFeedlink(getChildElementText(item, "link"));
                            rssRecord.setFeedauthor(getChildElementText(item, "author"));
                            rssRecord.setFeedcategory(getChildElementText(item, "category"));
                            rssRecord.setFeedguid(getChildElementText(item, "guid"));
                            rssRecord.setFeeddate(getChildElementText(item, "pubDate"));
                            String[] strCustom = new String[2];
                            strCustom[0]=""; strCustom[1]="";
                            strCustom = processCustomNamespaces( item);
                            rssRecord.setFeedCustom1(strCustom[0]);
                            rssRecord.setFeedCustom2(strCustom[1]);
                            vRssRecords.addElement(rssRecord);
                  }
                   //convert vector to array
                   
                   rssRecords = new RssRecord[vRssRecords.size()];
                   vRssRecords.toArray(rssRecords);
                   
                   defaultoutput = false;
                } 
           }
       catch(Exception e){
            System.out.println("error in buildRssBody :"+ e.getMessage());
          }
       finally{
           return defaultoutput;
       }
       
       }
   
  private String[] processCustomNamespaces(Element item){
    String[] customReturn = new String[2] ;
    customReturn[0]="";
    customReturn[1]="";
      try {
                 
               /*
               for (int i = 0; i < custom_namespace.length; i++) {

                            String nameSpace = custom_namespace[i];
                            String className = "org.bungeni.rssparser.ns.ns" +
                                                         nameSpace + "Parser";
                            Class cNSclass = java.lang.Class.forName(className);
                            Object nsParserObj = cNSclass.newInstance();
                            nsParserObj.setRootElement(item);
                            nsParserObj.toString();
                        }

                */
                 
                 /* the following is a hack for  the conference */
               
              
               
               Namespace nsBungeni = Namespace.getNamespace("bungeni", "http://bungeni.org/rss/1.0/modules/bungeni/");
               Element fromElement = item.getChild("from",  nsBungeni );               
               Element toElement = item.getChild("to", nsBungeni);
               StringBuffer sbFrom = new StringBuffer("") ;
               StringBuffer sbTo = new StringBuffer("");
               
               if (fromElement != null ){
                   XMLOutputter xmlQ = new XMLOutputter();
                   
                   /*
                    *  === is the the element name element child separator
                    *  ~=~ is the separator between elements
                    *  =~= is the separator between key value pairs
                    */
                   
                   sbFrom.append("from===");
                   if (fromElement.getChild("principal", nsBungeni) != null) {
                       Element principal = fromElement.getChild("principal", nsBungeni);
                       Iterator principalChildren = principal.getChildren().iterator();
                       int i= 0;
                       while (principalChildren.hasNext()) {
                           Element principalChild = (Element)principalChildren.next();
                           System.out.println("child element name = "+ principalChild.getName());
                           if (i > 0)
                            sbFrom.append("~=~"); // record separator
                           i++;
                           sbFrom.append(principalChild.getName());
                           sbFrom.append("=~="); //item value separator                        
                           sbFrom.append(principalChild.getText());
                       }
                      customReturn[0] = sbFrom.toString();
                   }
               }
               
               if (toElement != null) {
                    XMLOutputter xmlQ = new XMLOutputter();
                   sbTo.append("to===");
                   if (toElement.getChild("principal", nsBungeni) != null) {
                       Element principal = toElement.getChild("principal", nsBungeni);
                       Iterator principalChildren = principal.getChildren().iterator();
                       int i= 0;
                       while (principalChildren.hasNext()) {
                           Element principalChild = (Element)principalChildren.next();
                           if (i > 0)
                            sbTo.append("~=~"); // record separator
                           i++;
                           sbTo.append(principalChild.getName());
                           sbTo.append("=~="); //item value separator                        
                           sbTo.append(principalChild.getText());
                       }
                      customReturn[1] = sbTo.toString();
                   }
                
               }
               
               
               
          }         
      
        catch (Exception ex) {
                java.util.logging.Logger.getLogger("global").log(java.util.logging.Level.SEVERE,
                                                                 ex.getMessage(),
                                                                 ex);
            }
         finally{
             return customReturn;
         }
         
 
  } 
   
   
  public String getRssHeader() {
      
      String output = "";
      try {
      output = "Title = "+
      rssHeader.getChanneltitle() + "\n" +
      "URL = "+        
      rssHeader.getChannelurl() + "\n" +
      "Description = " +        
      rssHeader.getChanneldescription() + "\n"+
      "Language = " +
      rssHeader.getChannellanguage();
      }
      catch (Exception e){
          System.out.println("error in getRssHeader : "+ e.getMessage());
      }
      finally {
      return output;
      }
  }

  public String getRssBody() {
      String output = "";
      try {
      System.out.println ("in rss body get");
      for (int i=0 ; i < rssRecords.length ; i++){
          output = output +
          "Record no. "+i+"\n" + 
          "Title = "+
          rssRecords[i].getFeedtitle() + "\n" +
          "Link = "+        
          rssRecords[i].getFeedlink() + "\n" +
          "GUID = "+        
          rssRecords[i].getFeedguid() + "\n" +
          "Feed Date = " +        
          rssRecords[i].getFeeddate() + "\n" +
          "Author = " +
          rssRecords[i].getFeedauthor() + "\n";
        }
      }
      catch (Exception e){
          System.out.println("error in getRssBody : "+ e.getMessage());
      }
      return output;
  }
  
    public String toString(){
        return getRssHeader() + getRssBody();
    }  
}