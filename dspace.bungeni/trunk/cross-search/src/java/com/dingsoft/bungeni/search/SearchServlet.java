/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.dingsoft.bungeni.search;

import com.dingsoft.bungeni.search.util.ConfigsLoader;
import com.dingsoft.bungeni.search.util.ResponseTypeDecoder;
import java.io.*;
import java.net.*;

import java.util.ArrayList;
import java.util.Iterator;
import javax.servlet.*;
import javax.servlet.http.*;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.queryParser.ParseException;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.Hits;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.MultiSearcher;
import org.apache.lucene.search.Query;
import org.dspace.content.Bundle;
import org.dspace.content.Collection;
import org.dspace.content.Community;
import org.dspace.content.DCValue;
import org.dspace.content.DSpaceObject;
import org.dspace.content.Item;
import org.dspace.core.Context;
import org.dspace.handle.HandleManager;
import org.dspace.search.DSAnalyzer;


/**
 *This is the Servlet that handles the general search requests for the repository
 * @author Solomon Kariri
 * 
 * <p>This is the Servlet that handles the general search requests for the repository.
 * This class gets the parameters from the request URL and does some processing to produce
 * the results that match a particular query and for a specific page.
 * This classes uses the static methods of Configs loader to get info about the different properties
 * of the system as well as locating of the resources used by the repository
 */
public class SearchServlet extends HttpServlet {
   
    private String dspaceBase="http://192.168.1.10:8090/xmlui";
    private String kohaBase="http://192.168.1.10:80";
    /** 
    * Processes requests for both HTTP <code>GET</code> and <code>POST</code> methods.
    * @param request servlet request
    * @param response servlet response
     * 
     * <p>This is the main method in this class. It does all the necessary invocations on other methods
     * to create the response page for a search request. This class adds the overall layout of the page
     * adding the static features like links and the like that do not vary per page.
     * The rest of the information is added through the invocation of other methods.
    */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        ConfigurationInfo configInfo=ConfigsLoader.getConfigurationInfo();
            try {
                /*If the request is empty or simply blank spaces, the servlet redirects you to the home 
                 page of the repository from where you can do another search
                 */
                if(request.getParameter("query").trim().equals(""))
                {
                    response.sendRedirect("index.jsp");
                }
                
                /* If the request query is not empty then add the static data to the page*/
                out.println("<html>\n" +
                            "<head>\n" +
                            "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n" +
                            "<title>Bungeni Digital Repository</title>\n" +
                            "<link rel=\"shortcut icon\" href=\"/digitalrepository/favicon.ico\" type=\"image/x-icon\"/>\n" +
                            "<link type=\"text/css\" rel=\"stylesheet\" media=\"screen\" href=\"/digitalrepository/style/style.css\" />\n" +
                            /* This method call calls the method that inserts the ajax code used in the response page
                             * for processing features like expanding and collapsing of serach results divs
                             */
                            insertJavaScript(request)+
                            /*Then continue with adding the static stuff
                             */
                            "</head>\n" +
                            "<body>\n" +
                            "<div id=\"ds-main\">\n" +
                            "<div id=\"ds-header\">\n" +
                            "<img alt=\"The Image Logo\" src=\"/digitalrepository/images/logo.gif\" />\n" +
                            " <div id=\"ds-user-box\">\n" +
                            "<p>\n" +
                            "<a href=\"/digitalrepository/#\">Login</a>\n" +
                            "</p>\n" +
                            "</div>\n" +
                            "</div>\n" +
                            "<div id=\"ds-body\">\n" +
                            "<h1 style=\"font-size: 158%;\" class=\"ds-div-head\">Search Bungeni Digital Repository</h1> "+
                            "<form class=\"ds-interactive-div primary\" action=\"/digitalrepository/search\" method=\"get\">" +
                            "<p class=\"ds-paragraph\">Select Repository:...." +
                            "<input type=\"checkbox\" name=\"dspace\" checked /> Digital Repository/DSpace" +
                            "<input type=\"checkbox\" name=\"koha\" checked/> Library/Koha" +
                            "<p class=\"ds-paragraph\">Display Results By....:" +
                            "<input type=\"radio\" name=\"merge\" value=\"yes\" /> Ranking/Relevance" +
                            "<input type=\"radio\" name=\"merge\" value=\"no\" checked /> Repository" +
                            "<p class=\"ds-paragraph\">Search Text..." +
                            "<input class=\"ds-text-field\" name=\"query\" type=\"text\" value=\"\" />" +
                            "<input class=\"ds-button-field\"  name=\"submit\" type=\"submit\" value=\"Go\" />" +
                            "Results Per Page" +
                            "<select style=\"margin:3px 2px 1px 1px ;\" class=\"ds-button-field\" name=\"respp\">" +
                            "<option value=\"5\">5</option>" +
                            "<option value=\"10\">10</option>" +
                            "<option value=\"20\">20</option>" +
                            "<option value=\"30\">30</option>" +
                            "</select>" +
                            "</form>" +
                            " <h1 style=\"font-size: 158%;\" class=\"ds-div-head\">Search Results</h1>\n" +
                            "<p class=\"ds-paragraph\" style=\"font-size: 90%;\">\n" +
                            /*This method call is the actual call that inserts the search results in the result
                             * page in divs. See the method below for details of its functionality
                             */
                            getSearchResults(request)+
                            /*Continue with adding the static stuff
                             */
                            "</div>\n" +
                            " <div id=\"ds-options\">\n" +
                            " <h3 class=\"ds-option-set-head\">Browse</h3>\n" +
                            "<div class=\"ds-option-set\">\n" +
                            "<ul class=\"ds-options-list\">\n" +
                            "<li> \n" +
                            "<h4 class=\"ds-sublist-head\">\n" +
                            "<a title=\"The Bungeni Digital Repository Home\" href=\"http://192.168.1.10:8090/digitalrepository/\">\n" +
                            "Home\n" +
                            "</a>\n" +
                            "</h4>\n" +
                            "</li>\n" +
                            "<li>\n" +
                            "<h4 class=\"ds-sublist-head\">\n" +
                            "<a title=\"The Bungeni Dspace Project for management of Parliaments documents\" href=\""+dspaceBase+"/\">\n" +
                            "Bungeni Dspace\n" +
                            "</a>\n" +
                            "</h4>\n" +
                            "</li>\n" +
                            "<li>\n" +
                            "<h4 class=\"ds-sublist-head\">\n" +
                            " <a title=\"The bungeni Library project\" href=\""+kohaBase+"/\">\n" +
                            "Bungeni Koha\n" +
                            "</a>\n" +
                            "</h4>\n" +
                            "</li>\n" +
                            "</ul>\n" +
                            "</div>\n" +
                            "<h3 class=\"ds-option-set-head\">Search ...</h3>\n" +
                            "<div class=\"ds-option-set\" id=\"ds-search-option\">\n" +
                            "<form method=\"post\" id=\"ds-search-form\" action=\"/digitalrepository/search\">\n" +
                            "<fieldset>\n" +
                            " <input type=\"text\" class=\"ds-text-field \" name=\"query\" />\n" +
                            "<input value=\"Go\" type=\"submit\" name=\"submit\" class=\"ds-button-field \"/>\n" +
                            "</fieldset>\n" +
                            "</form>\n" +
                            "<a href=\"/digitalrepository/advanced-search\">Advanced Search</a>\n" +
                            "</div>\n" +
                            "<h3 class=\"ds-option-set-head\">Bungeni Portal</h3>\n" +
                            "<div class=\"ds-option-set\" id=\"ds-search-option\">\n" +
                            " <ul class=\"ds-options-list\">\n" +
                            "<li>\n" +
                            "<a title=\"\" href=\"http://192.168.1.5:10000/bungeni-public\">Bungeni Home</a>\n" +
                            "</li>\n" +
                            " <li>\n" +
                            "<a title=\"parliamentary activities at the plenary and committees level\" href=\"http://192.168.1.5:10000/bungeni-public/parliamentary-business\">business</a>\n" +
                            "</li>\n" +
                            "<li>\n" +
                            " <a title=\"member of parliaments and political parties represented in parliament\" href=\"http://192.168.1.5:10000/bungeni-public/mps-and-political-grops\">members</a>\n" +
                            "</li>\n" +
                            " <li>\n" +
                            "<a title=\"\" href=\"http://192.168.1.5:10000/bungeni-public/how-parliament-works\">how we work</a>\n" +
                            "</li>\n" +
                            " <li>\n" +
                            "<a title=\"\" href=\"http://192.168.1.5:10000/bungeni-public/organisation\">organisation</a>\n" +
                            "</li>\n" +
                            " <li>\n" +
                            "<a title=\"\" href=\"http://192.168.1.5:10000/bungeni-public/have-your-say\">have-your-say</a>\n" +
                            "</li>\n" +
                            "<li>\n" +
                            "<a title=\"\" href=\"http://192.168.1.5:10000/bungeni-public/visit-parliament\">vist parliament</a>\n" +
                            " </li>\n" +
                            " <li>\n" +
                            "<a title=\"\" href=\"http://192.168.1.5:10000/bungeni-public/resources\">resources</a>\n" +
                            " </li>\n" +
                            "</ul>\n" +
                            "</div>\n" +
                            "</div>\n" +
                            "<div id=\"ds-footer\">\n" +
                            "<p>&copy;2000-2007 Bungeni\n" +
                            "</div>\n" +
                            "</div>\n" +
                            "</body>\n" +
                            "</html>");
        } finally { 
            out.close();
        }
    } 
    /**
     * This is the method that does the actual searching and addition of the search results to the response
     * page
     * 
     * @param request The hHttpServletRequest method associated with this pages request
     * @return A string in html format that is concatenated to the main results to give 
     * the search results for a search request
     * 
     * <p>This is the method that does the actual searching and addition of the search results to the response
     * page. This method uses the dspace API functions to get information about search result items as well as
     * manage to perform  the query on the dspace 
     */
    private String getSearchResults(HttpServletRequest request)
    {
        /*Declare variables that are going to be used for searching both dspace and koha
         * and the multisearcher or compound searcher that combines the two in order to perform a consolidated and compound search on the two indecies
         */
        IndexSearcher kohaSearcher=null;
        IndexSearcher dspaceSeacher=null;
        MultiSearcher compoundSearcher=null;
        //The String that holds all the information to be appendend to the response page
        String results="";
        //boolean variable showing whether the results are to be merged or separated on repository basis
        boolean merge=request.getParameter("merge").equals("yes");
        //boolean value showing wheteher we are going to include dspace in the search
        boolean dspace=false;
        //boolean value showing wheteher we are going to include kohathe search
        boolean koha=false;
        if(request.getParameter("dspace")!=null)
        {
            dspace=request.getParameter("dspace").equals("on");
        }
        if(request.getParameter("koha")!=null)
        {
            koha=request.getParameter("koha").equals("on");
        }
       
        try
        {
            //get the search query from the request
            String query=request.getParameter("query");
            /*reate a compund dspace query to be used for searching all the possible fields in the 
             * dspace repository
             */
            Analyzer dspaceAnalyzer=new DSAnalyzer();
            Query subDspaceQueries[]=new Query[10];
            subDspaceQueries[0]=new QueryParser("keyword",dspaceAnalyzer).parse(query);
            subDspaceQueries[1]=new QueryParser("title",dspaceAnalyzer).parse(query);
            subDspaceQueries[2]=new QueryParser("abstract",dspaceAnalyzer).parse(query);
            subDspaceQueries[3]=new QueryParser("author",dspaceAnalyzer).parse(query);
            subDspaceQueries[4]=new QueryParser("series",dspaceAnalyzer).parse(query);
            subDspaceQueries[5]=new QueryParser("subject",dspaceAnalyzer).parse(query);
            subDspaceQueries[6]=new QueryParser("language",dspaceAnalyzer).parse(query);
            subDspaceQueries[7]=new QueryParser("sponsor",dspaceAnalyzer).parse(query);
            subDspaceQueries[8]=new QueryParser("identifier",dspaceAnalyzer).parse(query);
            subDspaceQueries[9]=new QueryParser("default",dspaceAnalyzer).parse(query);
            Query dspaceQuery=new QueryParser("title", dspaceAnalyzer).parse(query).combine(subDspaceQueries);
            /*nitialize the dspace searcher giving it a parameter of the directory where the 
             dspace index is located 
             */
            dspaceSeacher=new IndexSearcher("/home/undesa/dspace/search");


            /*Perform the same actions for koha as for dspace above
             */
            Query []subKohaQueries=new Query[7];
            subKohaQueries[0]=new QueryParser("dc.creator", dspaceAnalyzer).parse(query);
            subKohaQueries[1]=new QueryParser("dc.publisher", dspaceAnalyzer).parse(query);
            subKohaQueries[2]=new QueryParser("dc.coverage", dspaceAnalyzer).parse(query);
            subKohaQueries[3]=new QueryParser("dc.relation", dspaceAnalyzer).parse(query);
            subKohaQueries[4]=new QueryParser("dc.subject", dspaceAnalyzer).parse(query);
            subKohaQueries[5]=new QueryParser("dc.description", dspaceAnalyzer).parse(query);
            subKohaQueries[6]=new QueryParser("dc.keyword", dspaceAnalyzer).parse(query);
            Query kohaQuery= new QueryParser("dc.subject",dspaceAnalyzer).parse(query).combine(
                    subKohaQueries);
            kohaSearcher=new IndexSearcher("/home/undesa/Desktop/indexer");

            IndexSearcher searchers[]={dspaceSeacher,kohaSearcher};
            Query []queries={kohaQuery,dspaceQuery};
            /*Declare the combined query variable to be used for creating the compound query for searching both 
             * repositories
             */
                    
            Query combinedQuery=null;
            //If we are to search both repositories
            if(koha && dspace)
            {
                combinedQuery=kohaQuery.combine(queries);
            }
            //If we are to search koha alone
            else if(koha && !dspace)
            {
                combinedQuery=kohaQuery;
            }
            //If we are to search dspace alone
            else if(dspace && !koha)
            {
                combinedQuery=dspaceQuery;
            }
            //If non of the repositories is selected for search
            else
            {
                return "No Repository Selected. Please Select at " +
                        "least one repository to search above by checking the corresponding box.";
            }

            compoundSearcher=new MultiSearcher(searchers);
            //Submit the query and store the results in the Hits object
            Hits hits=compoundSearcher.search(combinedQuery);
            
            //Get the number of results in the response
            int numResults=hits.length();
            /*Define the divs that will hold information about the page to enable
             * javascript perfor its manouvers regarding showing different contents.
             * This divs are used as stores for variables whose values have been initialized 
             * at the server e.g. results per page resppdiv. The div names are indicative of 
             the variable stored by the div
             * */
            results+="<div id=\"resppdiv\" style=\"width: 0px; height: 0px; visibility: hidden;\">"+
                    request.getParameter("respp")+
                    "</div>";
            results+="<div id=\"numresdiv\" style=\"width: 0px; height: 0px; visibility: hidden;\">"+
                    numResults+
                    "</div>"; 
            results+="<div id=\"sepres\" style=\"width: 0px; height: 0px; visibility: hidden;\">"+
                    request.getParameter("merge")+
                    "</div>"; 
            results+="<div id=\"curp\" style=\"width: 0px; height: 0px; visibility: hidden;\">"+
                    1+
                    "</div>"; 
            
            //If no results then give the necessary response
            if(numResults==0)
            {
                results+="<p>Your query \""+query+"\" produced no results"+
                        "<div id=\"aspect_artifactbrowser_SimpleSearch_div_search-results\" style=\"width=100%\" class=\"ds-static-div primary\">\n" +
                        "<ul class=\"ds-artifact-list\">"+
                        "<li class=\"ds-artifact-item odd\">\n" +
                        "<div>\n" +
                        "<p>\n" +
                        "<br>No Results To Display"+
                        "</div></li>";
            }
            //If there are results then go a head and design their layout
            else
            {
                results+="<p>Your query \""+query+"\" produced "+numResults+" result(s)\n";
                int respp=Integer.parseInt(request.getParameter("respp"));
                /*Compute the number of dspace and koha requests by iterating over the results and
                 * keeping track of the available dspace responses through a variable dspres
                 */
                
                int dspres=0;
                for(int i=0;i<numResults;i++)
                {
                    if(ResponseTypeDecoder.getResponseTypeForDocument(hits.doc(i))==ResponseConstants.DSPACE_RESPONSE)
                    {
                        ++dspres;
                    }
                }
                //Calculate the number of koha results
                int kohares=numResults-dspres;
                //If the results are to be merged
                if(!merge)
                {
                    //Create the outer covering divs
                    int indecies=(kohares/respp >dspres/respp)?((kohares/respp)+((kohares%respp >0)?1:0)):((dspres/respp)+((dspres%respp>0)?1:0));
                    results+="\n<div class=\"pagination-masked top\">"+
                            "<p class=\"pagination-info\">Click a page below to view its results</p>"+
                            "<ul class=\"pagination-links\">"+
                            "<li class=\"current-page-link\">";
                    /*create the indecies links for different search result page */
                    for(int j=0;j<indecies;j++)
                    {
                        String finalURL=request.getRequestURL().toString()+"?";
                        String queryString=request.getQueryString();
                        if(queryString.indexOf("index")!=-1)
                        {
                            finalURL+=queryString.substring(0, queryString.indexOf("index"));
                        }
                        else
                        {
                            finalURL+=queryString+"&";
                        }
                        
                        finalURL+="index="+(j+1);
                        results+="\n<a href=\""+finalURL+"\">"+(j+1)+"</a>";
                    }
                    /*Create the guiding and actions divs at the top of the page
                     */
                    results+="\n</li>"+
                             "</ul>"+
                             "</div>"; 
                    results+="\n<div id=\"divexpand\"class=\"pagination-masked top\">"+
                            "<p class=\"pagination-info\" style=\"font-size: 11px;\"><a href=\"javascript:expandAll()\">Expand All>></a></p>"+
                            "</div>";
                    results+="\n<div id=\"divcollapse\" class=\"pagination-masked top\" style=\"width: 0px; height: 0px; visibility: hidden;\">"+
                            "<p class=\"pagination-info\" style=\"font-size: 11px;\"><a href=\"javascript:collapseAll()\">&lt;&lt;Collapse All</a></p>"+
                            "</div>";

                    results+="<div id=\"aspect_artifactbrowser_SimpleSearch_div_search-results\" class=\"ds-static-div primary\" style=\"width: 100%;\">\n" +
                            "<ul class=\"ds-artifact-list\">";
                    if(dspres>0)
                    {
                        results+="\n<div id=\"dspacereshead\" class=\"pagination-masked top\" style=\"width: 100%; height: auto; visibility: visible;\">"+
                            "<p class=\"pagination-info\" style=\"font-size: 13px;\">Digital Repository/DSpace Results</p>"+
                            "</div>";
                    }
                    /*variables to keep track of the responses processed and the number of pages available for the results
                     */
                    int dspaceTrack=0;
                    int kohaTrack=0;
                    int largestIndex=0;
                    int currentPage=1;
                    if(request.getParameter("index")!=null)
                    {
                        currentPage=Integer.parseInt(request.getParameter("index"));
                    }
                    int startIndex=(currentPage*respp)-respp;
                    int endIndex=startIndex+respp;
                    int counter=0;
                    /* Fetch Dspace Results and Display Them first depending on the 
                     * number of results per page 
                     */
                    boolean added=false;
                    for(int i=0;i<numResults;i++)
                    {
                        Document doc=hits.doc(i);
                        int docType=ResponseTypeDecoder.getResponseTypeForDocument(doc);
                        DCValue []descriptionMeta=null;
                        DCValue []authorMeta=null;
                        DCValue []dateMeta=null;
                        Bundle []bundles=null;
                        switch(docType)
                        {
                            /*If it is a dspace response then process it ccordingly and 
                             * add the necessary divs for the response to the results
                             */
                            case ResponseConstants.DSPACE_RESPONSE:
                            {
                                if(counter>=startIndex && counter<endIndex)
                                {
                                    String handle=doc.getField("handle").stringValue();
                                    String link=dspaceBase+"/handle/"+handle;
                                    String title="";
                                    String type="Other";
                                    String owningCollection="";

                                    try
                                    {
                                        Context context=new Context();
                                        DSpaceObject dspaceObject=HandleManager.resolveToObject(context, handle);
                                        if(dspaceObject instanceof Item)
                                        {
                                            type="Item";
                                            Item item=(Item)dspaceObject;
                                            title+=item.getName();
                                            descriptionMeta=item.getMetadata("dc.description");
                                            authorMeta=item.getMetadata("dc.contributor.author");
                                            dateMeta=item.getMetadata("dc.date.issued");
                                            owningCollection=item.getOwningCollection().getName();
                                            bundles=item.getBundles();
                                        }
                                        else if(dspaceObject instanceof Collection)
                                        {
                                            type="Collection";
                                            Collection col=(Collection)dspaceObject;
                                            title+=col.getName();
                                        }
                                        else if(dspaceObject instanceof Community)
                                        {
                                            type="Community";
                                            Community com=(Community)dspaceObject;
                                            title+=com.getName();
                                        }
                                        context.complete();

                                    }
                                    catch(Throwable thr)
                                    {
                                    }
                                    try
                                    {
                                        /* Create the actual divs that contain the results and add them to the response
                                         */
                                        String visibility=(dspaceTrack>=Integer.parseInt(request.getParameter("respp")))?"hidden":"visible";
                                        String width=visibility.equals("hidden")?"0px;":"100%;";
                                        String height=visibility.equals("hidden")?"0px;":"auto;";
                                        results+="<li class=\"ds-artifact-item odd\">\n" +
                                            "<div id=\"divmds_"+(dspaceTrack+1)+"\" style=\"visibility: "+visibility+"; width: "+width+" height: "+height+" overflow: hidden;\" >\n" +
                                            "<p>\n" +
                                            title+"<br>Available in <a href=\""+dspaceBase+"\" title=\"Bungeni Dspace\">Bungeni Dspace</a>"+
                                            "<br><a href=\"javascript:showDiv('divds_"+(dspaceTrack+1)+"','divmds_"+(dspaceTrack+1)+"')\" title=\"full details\" >more>></a>\n"+
                                            "</div>" +
                                            "<div id=\"divds_"+(dspaceTrack+1)+"\" style=\"visibility: hidden; width: 0px; height:0px; overflow: hidden;\">\n" +
                                            title+"<br />"+
                                            "<b>Type:</b> "+type+"<br>" +((authorMeta != null)?"<b>Author:</b> "+authorMeta[0].value +"<br>":"") +
                                            ((descriptionMeta != null)?"<b>Description :</b> "+descriptionMeta[0].value +"<br>":"")+
                                            ((dateMeta != null)?"<b>Issue Date :</b> "+dateMeta[0].value +"<br>":"")+
                                            ((type.equals("Item"))?"<b>Owning Collection :</b> "+owningCollection +"<br>":"")+
                                            ((bundles!=null && bundles.length>0)?"<b>Bitstream 1 :</b> "+bundles[0].getBitstreams()[0].getName()+"<br>":"")+
                                            ((bundles!=null && bundles.length>0)?"<b>Bitstream Format :</b> "+bundles[0].getBitstreams()[0].getFormatDescription()+"<br>":"")+
                                            "<a href=\""+link+"\" title=\"Clicking this link will navigate you out of the portal\">Go to Bungeni Dspace and view Item</a><br />"+
                                             "<a href=\"javascript:showDiv('divmds_"+(dspaceTrack+1)+"','divds_"+(dspaceTrack+1)+"')\" title=\"Collapse Details\" >&lt;&lt;collapse</a><br>\n"+
                                            "</div></li>\n";
                                        //Increment the number of dspace responses processed so far
                                        dspaceTrack++;
                                    }
                                    catch(Throwable thr)
                                    {
                                        results+=thr.toString();
                                    }
                                    //Update other counters and status flags accordingly
                                    counter++;
                                    added=true;
                                    break;
                                }
                                else
                                {
                                    counter++;
                                    break;
                                }
                                
                            }
                        }
                    }
                    //If no dspace results were found and dspace had been included in the search then gine the necessary message
                    if(!added && dspace)
                    {
                        results+="<div>No Digital Repository/Dspace results for this page</div>";
                    }
                    
                    /* Initialize the track keeping variables for koha results to be manufactured now in the same
                     * manner the dspace results were. This code is similar to the one shown above for dspace
                     */
                    startIndex=(currentPage*respp)-respp;
                    endIndex=startIndex+respp;
                    counter=0;
                    /*Package the koha results if there are any under the dspace results
                     * /
                     */
                    if(kohares>0)
                    {
                        results+="</ul></div>";
                        results+="<div id=\"aspect_artifactbrowser_SimpleSearch_div_search-results\" class=\"ds-static-div primary\" style=\"width: 100%;\">\n" +
                            "<ul class=\"ds-artifact-list\">";
                        results+="\n<div id=\"kohareshead\" class=\"pagination-masked top\" style=\"width: 100%; height: auto; visibility: visible;\">"+
                            "<p class=\"pagination-info\" style=\"font-size: 13px;\">Library/Koha Results</p>"+
                            "</div>";
                    }
                    /* Fetch Koha Results and Display Them each result in a separate div depending on the 
                     * number of results per page 
                     */
                    added=false;
                    for(int i=0;i<numResults;i++)
                    {
                        Document doc=hits.doc(i);
                        int docType=ResponseTypeDecoder.getResponseTypeForDocument(doc);
                        switch(docType)
                        {
                            case ResponseConstants.KOHARESPONSE:
                            {
                                if(counter>=startIndex && counter<endIndex)
                                {
                                    String biblioNumber="";
                                    String link="";
                                    String title="";
                                    String type="";
                                    String author="";
                                    String publisher="";
                                    String description="";
                                    String date="";
                                    /* Store the documents fields in an arraylist and iterate 
                                     over each adding the necessary info to the display messages*/
                                    ArrayList fields=new ArrayList(doc.getFields());
                                    int fieldsCount=fields.size();
                                    Iterator itor=fields.iterator();
                                    while(itor.hasNext())
                                    {
                                        Field fie=(Field)itor.next();
                                        String fieldName=fie.name();
                                        if(fieldName.equalsIgnoreCase("dc.kohabiblionumber"))
                                        {
                                            biblioNumber=fie.stringValue();
                                            link="";
                                        }
                                        if(fieldName.equalsIgnoreCase("dc.title"))
                                        {
                                            title+=fie.stringValue();
                                        }
                                        if(fieldName.equalsIgnoreCase("dc.itemtypename"))
                                        {
                                            type=fie.stringValue();
                                        }
                                        if(fieldName.equalsIgnoreCase("dc.creator"))
                                        {
                                            author+=fie.stringValue();
                                        }
                                        if(fieldName.equalsIgnoreCase("dc.description"))
                                        {
                                            description+=fie.stringValue();
                                        }
                                        if(fieldName.equalsIgnoreCase("dc.publisher"))
                                        {
                                            publisher+=fie.stringValue();
                                        }
                                        if(fieldName.equalsIgnoreCase("dc.description"))
                                        {
                                            publisher+=fie.stringValue();
                                        }
                                        if(fieldName.equalsIgnoreCase("dc.date"))
                                        {
                                            date=fie.stringValue();
                                        }
                                    }
                                    
                                    /* The actual divs containing the koha results
                                     */
                                    String visibility=(kohaTrack>=Integer.parseInt(request.getParameter("respp")))?"hidden":"visible";
                                    String width=visibility.equals("hidden")?"0px;":"100%;";
                                    String height=visibility.equals("hidden")?"0px;":"auto;";
                                    results+="<li class=\"ds-artifact-item odd\">\n" +
                                            "<div id=\"divmkh_"+(kohaTrack+1)+"\" style=\"visibility: "+visibility+"; width: "+width+" height: "+height+" overflow: hidden;\" >\n" +
                                            "<p>\n" +
                                            title+"<br>Available in <a href=\""+kohaBase+"\" title=\"Bungeni Koha\">Bungeni Koha</a>"+
                                            "<br><a href=\"javascript:showDiv('divkh_"+(kohaTrack+1)+"','divmkh_"+(kohaTrack+1)+"')\" title=\"full details\" >more>></a>\n"+
                                            "</div>" +
                                            "<div id=\"divkh_"+(kohaTrack+1)+"\" style=\"visibility: hidden; width: 0px; height:0px; overflow: hidden;\">\n" +
                                            title+"<br />"+
                                            "<b>Type:</b> "+type+"<br />"+
                                            "<b>Author: </b>"+author+"<br />" +
                                            "<b>Publisher :</b> "+publisher+"<br />"+
                                            "<b>Description :</b> "+description+"<br />"+
                                            "<b>Publishing Date :</b> "+date+"<br />"+
                                            "<a href=\""+link+"\" title=\"Clicking this link will navigate you out of the portal\">Go to Bungeni Koha and view Item</a><br />"+
                                             "<a href=\"javascript:showDiv('divmkh_"+(kohaTrack+1)+"','divkh_"+(kohaTrack+1)+"')\" title=\"Collapse Details\" >&lt;&lt;collapse</a><br>\n"+
                                            "</div></li>\n"; 
                                      kohaTrack++;
                                      counter++;
                                      added=true;
                                    break;
                                }
                                else
                                {
                                    counter++;
                                    break;
                                }
                                
                            }
                        }
                    }
                    if(!added && koha)
                    {
                        results+="<div>No Library/Koha results for this page</div>";
                    }
                    /* Close all the searchers if any had been initialized sucessfully
                     */
                    if(dspaceSeacher!=null)
                    {
                        dspaceSeacher.close();
                    }
                    if(kohaSearcher!=null)
                    {
                        kohaSearcher.close();
                    }
                    if(compoundSearcher!=null)
                    {
                        compoundSearcher.close();
                    }
                    
                }
                
            }
            
        }
        catch(ParseException pe)
        {
        }
        catch(CorruptIndexException cie)
        {
        }
        catch(IOException ioe)
        {
        }
        finally
        {
            if(kohaSearcher!=null)
            {
                try
                {
                    kohaSearcher.close();
                }
                catch(Exception e)
                {
                    
                }
            }
            if(dspaceSeacher!=null)
            {
                try
                {
                    dspaceSeacher.close();
                }
                catch(Exception e)
                {
                    
                }
            }
            if(compoundSearcher !=null)
            {
                try
                {
                    compoundSearcher.close();
                }
                catch(Exception e)
                {
                    
                }
            }
        }
        /*Terminate the outer div for search results after adding the results to the inner divs
         */
        results+="</ul></div>";
        return results;
    }
    
    /**
     * This method adds the ajax code necessary to process the search results in the browser
     * @param request The request object for this request from the browser
     * @return the javascript code for dealing with ajax behavoir in the response page
     * <p>This method adds the ajax code necessary to process the search results in the browser
     */
    private String insertJavaScript(HttpServletRequest request)
    {
        String script="<script type=\"text/javascript\" >\n" +
                //Function for expanding a certain div
                "function showDiv()\n" +
                "{\n" +
                "var argv = showDiv.arguments;" +
                "document.getElementById(argv[0]).style.visibility = \"visible\";\n" +
                "document.getElementById(argv[1]).style.visibility = \"hidden\";\n" +
                "document.getElementById(argv[0]).style.width = \"100%\";\n" +
                "document.getElementById(argv[0]).style.height = \"auto\";\n" +
                "document.getElementById(argv[1]).style.width = \"0px\";\n" +
                "document.getElementById(argv[1]).style.height = \"0px\";\n" +
                "}\n" +
                //Function for collapsing a certain div
                "function collapseDiv()\n" +
                "{\n" +
                "var argv = showDiv.arguments;" +
                "document.getElementById(argv[0]).style.visibility = \"visible\";\n" +
                "document.getElementById(argv[1]).style.visibility = \"hidden\";\n" +
                "document.getElementById(argv[0]).style.width = \"100%\";\n" +
                "document.getElementById(argv[0]).style.height = \"auto\";\n" +
                "document.getElementById(argv[1]).style.width = \"0px\";\n" +
                "document.getElementById(argv[1]).style.height = \"0px\";\n" +
                "}\n" +
                "function hideDiv()\n" +
                "{\n" +
                "var argv = hideDiv.arguments;" +
                "document.getElementById(arg[0]).style.visibility = \"hidden\";\n" +
                "}\n" +
                /* The function that will expand all divs in the current display
                 * */
                "function expandAll()\n" +
                "{\n" +
                "var currentIndex= document.getElementById('curp').innerHTML;\n" +
                "var respp= document.getElementById('resppdiv').innerHTML;\n" +
                "var startIndex= (parseInt(currentIndex)-1)*parseInt(respp)+1;\n" +
                "var numres= document.getElementById('numresdiv').innerHTML;\n" +
                "var div1ds='';\n" +
                "var div2ds='';\n" +
                "var divmDS='div';\n" +
                "var divDS='div';\n" +
                "var div1kh='';\n" +
                "var div2kh='';\n" +
                "var divmKH='div';\n" +
                "var divKH='div';\n" +
                "var i=0;\n" +
                /* Hide the main divs
                 */
                "for(i=0;i<parseInt(respp);i++)\n" +
                "{\n" +
                "divmDS= 'divmds_'+parseInt(i+parseInt(currentIndex)*parseInt(respp)-parseInt(respp)+1);\n" +
                "divDS= 'divds_'+(i+parseInt(currentIndex)*parseInt(respp)-parseInt(respp)+1);\n" +
                "div2mDS= 'divmds_'+parseInt(i+startIndex);\n"+
                "div1ds=document.getElementById(divmDS);\n" +
                "if(null !== div1ds)\n" +
                "{\n" +
                "div1ds.style.width= \"0px\";\n" +
                "div1ds.style.height= \"0px\";\n" +
                "div1ds.style.visibility= \"hidden\";\n" +
                "}\n" +
                /* Now for the full blown divs
                 */               
                "div2ds=document.getElementById(divDS);\n" +
                "if(null !== div2ds)\n" +
                "{\n" +
                "div2ds.style.width= \"100%\";\n" +
                "div2ds.style.height= \"auto\";\n" +
                "div2ds.style.visibility= \"visible\";\n" +
                "}\n" +
                
                /*
                 * Deal with Koha divs now
                 */
                "divmKH= 'divmkh_'+parseInt(i+parseInt(currentIndex)*parseInt(respp)-parseInt(respp)+1);\n" +
                "divKH= 'divkh_'+(i+parseInt(currentIndex)*parseInt(respp)-parseInt(respp)+1);\n" +
                "div2mKH= 'divmkh_'+parseInt(i+startIndex);\n"+
                "div1kh=document.getElementById(divmKH);\n" +
                "if(null !== div1kh)\n" +
                "{\n" +
                "div1kh.style.width= \"0px\";\n" +
                "div1kh.style.height= \"0px\";\n" +
                "div1kh.style.visibility= \"hidden\";\n" +
                "}\n" +
                /* Now for the full blown koha divs
                 */               
                "div2kh=document.getElementById(divKH);\n" +
                "if(null !== div2kh)\n" +
                "{\n" +
                "div2kh.style.width= \"100%\";\n" +
                "div2kh.style.height= \"auto\";\n" +
                "div2kh.style.visibility= \"visible\";\n" +
                "}\n" +
                
                
                "}\n" +
                /* Show the collapse All div and hide the expand all div
                 */
                "document.getElementById('divexpand').style.width=\"0px\";\n"+
                "document.getElementById('divexpand').style.height=\"0px\";\n"+
                "document.getElementById('divexpand').style.visibility=\"hidden\";\n"+
                "document.getElementById('divcollapse').style.width=\"100%\";\n"+
                "document.getElementById('divcollapse').style.height=\"auto\";\n"+
                "document.getElementById('divcollapse').style.visibility=\"visible\";\n"+
                "}\n" +
                "function collapseAll()\n" +
                "{\n" +
                "var currentIndex= document.getElementById('curp').innerHTML;\n" +
                "var respp= document.getElementById('resppdiv').innerHTML;\n" +
                "var startIndex= (parseInt(currentIndex)-1)*parseInt(respp)+1;\n" +
                "var numres= document.getElementById('numresdiv').innerHTML;\n" +
                "var div1ds='';\n" +
                "var div2ds='';\n" +
                "var divmDS='div';\n" +
                "var divDS='div';\n" +
                //The variables for koha divs goes here
                "var div1kh='';\n" +
                "var div2kh='';\n" +
                "var divmKH='div';\n" +
                "var divKH='div';\n" +
                
                "var i=0;\n" +
                
                "for(i=0;i<parseInt(respp);i++)\n" +
                "{\n" +
                
                /* Hide the full blown divs for dspace
                 */
                
                "divmDS= 'divmds_'+parseInt(i+parseInt(currentIndex)*parseInt(respp)-parseInt(respp)+1);\n" +
                "divDS= 'divds_'+(i+parseInt(currentIndex)*parseInt(respp)-parseInt(respp)+1);\n" +
                "div2mDS= 'divmds_'+parseInt(i+startIndex);\n"+
                "div1ds=document.getElementById(divmDS);\n" +
                "if(null !== div1ds)\n" +
                "{\n" +
                "div1ds.style.width= \"100%\";\n" +
                "div1ds.style.height= \"auto\";\n" +
                "div1ds.style.visibility= \"visible\";\n" +
                "}\n" +
                /* Now show the main divs for dspace
                 */               
                "div2ds=document.getElementById(divDS);\n" +
                "if(null !== div2ds)\n" +
                "{\n" +
                "div2ds.style.width= \"0px\";\n" +
                "div2ds.style.height= \"0px\";\n" +
                "div2ds.style.visibility= \"hidden\";\n" +
                "}\n" +
                
                // Now deal with the koha divs
                //Hide the full blown divs for koha
                "divmKH= 'divmkh_'+parseInt(i+parseInt(currentIndex)*parseInt(respp)-parseInt(respp)+1);\n" +
                "divKH= 'divkh_'+(i+parseInt(currentIndex)*parseInt(respp)-parseInt(respp)+1);\n" +
                "div2mKH= 'divmkh_'+parseInt(i+startIndex);\n"+
                "div1kh=document.getElementById(divmKH);\n" +
                "if(null !== div1kh)\n" +
                "{\n" +
                "div1kh.style.width= \"100%\";\n" +
                "div1kh.style.height= \"auto\";\n" +
                "div1kh.style.visibility= \"visible\";\n" +
                "}\n" +
                /* Now show the main divs for koha
                 */               
                "div2kh=document.getElementById(divKH);\n" +
                "if(null !== div2kh)\n" +
                "{\n" +
                "div2kh.style.width= \"0px\";\n" +
                "div2kh.style.height= \"0px\";\n" +
                "div2kh.style.visibility= \"hidden\";\n" +
                "}\n" +
                
                
                "}\n" +
                
                
                /* Show the expand All div and hide the collapse all div
                 */
                "document.getElementById('divexpand').style.width=\"100%\";\n"+
                "document.getElementById('divexpand').style.height=\"auto\";\n"+
                "document.getElementById('divexpand').style.visibility=\"visible\";\n"+
                "document.getElementById('divcollapse').style.width=\"0px\";\n"+
                "document.getElementById('divcollapse').style.height=\"0px\";\n"+
                "document.getElementById('divcollapse').style.visibility=\"hidden\";\n"+
                "}\n" +
                "</script>\n";
        return script;
    }

    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /** 
    * Handles the HTTP <code>GET</code> method.
    * @param request servlet request
    * @param response servlet response
    */
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException {
        processRequest(request, response);
    } 

    /** 
    * Handles the HTTP <code>POST</code> method.
    * @param request servlet request
    * @param response servlet response
    */
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException {
        processRequest(request, response);
    }

    /** 
    * Returns a short description of the servlet.
    */
    public String getServletInfo() {
        return "This is the servlet that deals with general search requests";
    }
    // </editor-fold>
}
