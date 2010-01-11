/*
 * RssHeader.java
 *
 * Created on March 9, 2007, 12:24 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.rssparser;
import org.openoffice.rssreader.BungeniRssHeader;
/**
 *
 * @author ashok
 */
public class RssHeader {
    private String channelTitle;
    private String channelURL;
    private String channelDescription;
    private String channelLanguage;
    private String channelGenerator;
    
    
    /** Creates a new instance of RssHeader */
    public RssHeader() {
        channelTitle = "";
        channelURL = "";
        channelDescription = "";
        channelLanguage = "";
        channelGenerator = "";    
    }
    
   public org.openoffice.rssreader.BungeniRssHeader toBungeniRssHeader(){
    return new org.openoffice.rssreader.BungeniRssHeader (channelTitle,channelURL,channelDescription,channelLanguage,channelGenerator);  
   }
           
           
   public void setChanneltitle(String varchannelTitle) {
                channelTitle= varchannelTitle;
                }


    public String getChanneltitle() {
                    return channelTitle;
                    }



    public void setChannelurl(String varchannelURL) {
                    channelURL= varchannelURL;
                    }


    public String getChannelurl() {
                    return channelURL;
                    }



    public void setChanneldescription(String varchannelDescription) {
                    channelDescription= varchannelDescription;
                    }


    public String getChanneldescription() {
                    return channelDescription;
                    }



    public void setChannellanguage(String varchannelLanguage) {
                    channelLanguage= varchannelLanguage;
                    }


    public String getChannellanguage() {
                    return channelLanguage;
                    }



    public void setChannelgenerator(String varchannelGenerator) {
                    channelGenerator= varchannelGenerator;
                    }


    public String getChannelgenerator() {
                    return channelGenerator;
                    }
    }
