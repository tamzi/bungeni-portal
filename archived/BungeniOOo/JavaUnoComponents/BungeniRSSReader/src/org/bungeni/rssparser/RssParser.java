/*
 * RssParser.java
 *
 * Created on March 9, 2007, 12:21 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.rssparser;

/*
 * RssParser.java
 *
 * Created on March 9, 2007, 11:04 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

/**
 *
 * @author Administrator
 */
import java.net.URL;
import java.text.ParseException;
import org.jdom.Document;
import org.jdom.Element;
import org.jdom.input.SAXBuilder;
import org.openoffice.rssreader.BungeniRssHeader;
import org.openoffice.rssreader.BungeniRssRecord;
import org.openoffice.rssreader.BungeniRssDocument;


/** Parse-and-print example that parses RSS 2.0 */
public class RssParser {
    Document feedDoc;
    RssDocument rssDocument;
    
    public RssParser(URL url) throws Exception {
        SAXBuilder builder = new SAXBuilder();       
        feedDoc = builder.build(url); 
        
    }
    
    public void parseFeed() throws ParseException{
        Element root = feedDoc.getRootElement();        //|#3
        String[] ns = new String[1];
        ns[0]="bungeni";
        rssDocument = new RssDocument(root, ns);
        rssDocument.buildFeeds();   
    }
    
    public void printFeed(){
        System.out.println(rssDocument.toString());
    }
    
    public String feedContents() {
        
        return rssDocument.toString();
    }
    
    public org.openoffice.rssreader.BungeniRssHeader rssHeader(){
        return rssDocument.getBungeniRssHeader();
    }
    
    public org.openoffice.rssreader.BungeniRssRecord[] rssRecords(){
        return rssDocument.getBungeniRssRecords();
    }
}

