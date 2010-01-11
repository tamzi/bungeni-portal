/*
 * RssRecord.java
 *
 * Created on March 9, 2007, 12:23 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.rssparser;

import java.text.SimpleDateFormat;
import java.util.Date;
import org.openoffice.rssreader.BungeniRssRecord;
/**
 *
 * @author ashok
 */
public class RssRecord {
    
    /** Creates a new instance of RssRecord */
    
    private String feedTitle;
    private String feedLink;
    private String feedGUID;
    private String feedAuthor;
    private String feedCategory;
    private String feedDate;
    private String feedCustom1;
    private String feedCustom2;
    private String feedCustom3;
    private String feedCustom4;
    private String feedContent;
    
    public RssRecord() {
        feedTitle="";
        feedLink="";
        feedGUID="";
        feedAuthor="";
        feedCategory="";
        feedDate="";
        feedCustom1="";
        feedCustom2="";
        feedCustom3="";
        feedCustom4="";
        feedContent="";
        
    }
    
    
    
    public org.openoffice.rssreader.BungeniRssRecord toBungeniRssRecord(){
        return new org.openoffice.rssreader.BungeniRssRecord(feedTitle, feedLink, feedGUID, 
                feedAuthor, feedCategory, feedDate, feedCustom1, feedCustom2, feedCustom3,feedCustom4, feedContent );
    }
            
    public void setFeedtitle(String varfeedTitle) {
                feedTitle= varfeedTitle;
                }


    public String getFeedtitle() {
                return feedTitle;
                }

    public void setFeedlink(String varfeedLink) {
                feedLink= varfeedLink;
                }


    public String getFeedlink() {
                return feedLink;
                }

    public void setFeedguid(String varfeedGUID) {
                feedGUID= varfeedGUID;
                }


    public String getFeedguid() {
                return feedGUID;
                }
    
    public void setFeedauthor(String varfeedAuthor) {
                feedAuthor= varfeedAuthor;
                }


    public String getFeedauthor() {
                return feedAuthor;
                }

    public void setFeedcategory(String varfeedCategory) {
                feedCategory= varfeedCategory;
                }
    
    
    public void setFeedCustom1 (String varCustom1){
        feedCustom1=varCustom1;
    }

    
    public void setFeedCustom2 (String varCustom2){
        feedCustom2=varCustom2;
    }

      
    public String getFeedCustom1 (){
        return feedCustom1;
    }
     
      
    public String getFeedCustom2 (){
        return feedCustom2;
    }
    
    public String getFeedCustom3 (){
        return feedCustom3;
    }
    
    
    public String getFeedCustom4 (){
        return feedCustom4;
    }
    
        
    

    public String getFeedcategory() {
                return feedCategory;
                }

    public void setFeeddate(String varfeedDate) {
            try {
            SimpleDateFormat rfc822_format = new SimpleDateFormat( "EEE, dd MMM yyyy hh:mm:ss z" );                    
            if (varfeedDate != null || varfeedDate.length() > 0 ){
                        Date pubDate = rfc822_format.parse(varfeedDate);
                        feedDate = pubDate.toString();
              }
            }
            catch (Exception e){
                System.out.println("error in setFeedDate : "+ e.getMessage());
            }
        }


    public String getFeeddate() {
                return feedDate;
                }    
    
}
