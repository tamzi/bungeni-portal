/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.dingsoft.bungeni.search;

import com.dingsoft.bungeni.search.util.ResponseTypeDecoder;
import java.io.*;
import java.net.*;

import javax.servlet.*;
import javax.servlet.http.*;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.Document;
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
 *
 * @author undesa
 */
public class SearchServlet extends HttpServlet {
   
    private String dspaceBase="http://192.168.1.10:8090/xmlui/";
    private String kohaBase="http://192.168.1.10:80/";
    /** 
    * Processes requests for both HTTP <code>GET</code> and <code>POST</code> methods.
    * @param request servlet request
    * @param response servlet response
    */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
            try {
                if(request.getParameter("query").trim().equals(""))
                {
                    response.sendRedirect("index.jsp");
                }
                out.println("<html>\n" +
                            "<head>\n" +
                            "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n" +
                            "<title>Bungeni Digital Repository</title>\n" +
                            "<link rel=\"shortcut icon\" href=\"/digitalrepository/favicon.ico\" type=\"image/x-icon\"/>\n" +
                            "<link type=\"text/css\" rel=\"stylesheet\" media=\"screen\" href=\"/digitalrepository/style/style.css\" />\n" +
                            insertJavaScript(request)+
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
                            getSearchResults(request)+
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
                            "<a title=\"The Bungeni Dspace Project for management of Parliaments documents\" href=\"http://192.168.1.10:8090/xmlui/\">\n" +
                            "Bungeni Dspace\n" +
                            "</a>\n" +
                            "</h4>\n" +
                            "</li>\n" +
                            "<li>\n" +
                            "<h4 class=\"ds-sublist-head\">\n" +
                            " <a title=\"The bungeni Library project\" href=\"http://192.168.1.10\">\n" +
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
    
    private String getSearchResults(HttpServletRequest request)
    {
        IndexSearcher kohaSearcher=null;
        IndexSearcher dspaceSeacher=null;
        MultiSearcher compoundSearcher=null;
        String results="";
        boolean test=true;
        try
        {
            String query=request.getParameter("query");
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
            dspaceSeacher=new IndexSearcher("/home/undesa/dspace/search");


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
            Query combinedQuery=kohaQuery.combine(queries);

            compoundSearcher=new MultiSearcher(searchers);
            Hits hits=compoundSearcher.search(combinedQuery);
            
            int numResults=hits.length();
            /*Define the divs that will hold information about the page to enable
             * javascript perfor its manouvers regarding showing different contents
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
            else
            {
                results+="<p>Your query \""+query+"\" produced "+numResults+" result(s)\n";
                int respp=Integer.parseInt(request.getParameter("respp"));
                int dspres=0;
                for(int i=0;i<numResults;i++)
                {
                    if(ResponseTypeDecoder.getResponseTypeForDocument(hits.doc(i))==ResponseConstants.DSPACE_RESPONSE)
                    {
                        ++dspres;
                    }
                }
                int kohares=numResults-dspres;
                int indecies=(kohares/respp >dspres/respp)?((kohares/respp)+((kohares%respp >0)?1:0)):((dspres/respp)+((dspres%respp>0)?1:0));
                results+="\n<div class=\"pagination-masked top\">"+
                        "<p class=\"pagination-info\">Click a page below to view its results</p>"+
                        "<ul class=\"pagination-links\">"+
                        "<li class=\"current-page-link\">";
                for(int j=0;j<indecies;j++)
                {
                    results+="\n<a href=\"javascript:showResForPage(\'"+(j+1)+"\')\">"+(j+1)+"</a>";
                }
                        
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
            }
            int dspaceTrack=0;
            int kohaTrack=0;
            int largestIndex=0;
            
            /* Fetch Dspace Results and Display Them first depending on the 
             * number of results per page 
             */
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
                    case ResponseConstants.DSPACE_RESPONSE:
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
                                 "<br><a href=\"javascript:showDiv('divmds_"+(dspaceTrack+1)+"','divds_"+(dspaceTrack+1)+"')\" title=\"Collapse Details\" >&lt;&lt;collapse</a>\n"+
                                "</div></li>\n"; 
                            dspaceTrack++;
                        }
                        catch(Throwable thr)
                        {
                            results+=thr.toString();
                        }
                        
                        break;
                    }
                }
            }
            
            /* Fetch Koha Results and Display Them first depending on the 
             * number of results per page 
             */
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
                    case ResponseConstants.KOHARESPONSE:
                    {
                        if(true)
                        {
                            break;
                        }
                        String biblioNumber=doc.getField("dc.kohabiblionumber").stringValue();
                        String link=kohaBase+"cgi-bin/koha/opac-detail.pl?biblionumber="+biblioNumber;
                        String title=doc.getField("dc.title").stringValue();
                        results+="<li class=\"ds-artifact-item odd\">\n" +
                                "<div>\n" +
                                "<p>\n" +
                                 "<a href=\""+link+"\" title=\""+title+"\">"+title+"</a>"+
                                "<br>Available in <a href=\""+kohaBase+"\" title=\"Bungeni Koha\">Bungeni Koha</a>"+
                                "</div></li>";
                        break;
                    }
                }
            }
            if(numResults>0)
            {
                int respp=Integer.parseInt(request.getParameter("respp"));
                int dspres=0;
                for(int i=0;i<numResults;i++)
                {
                    if(ResponseTypeDecoder.getResponseTypeForDocument(hits.doc(i))==ResponseConstants.DSPACE_RESPONSE)
                    {
                        ++dspres;
                    }
                }
                int kohares=numResults-dspres;
                int indecies=(kohares/respp >dspres/respp)?((kohares/respp)+((kohares%respp >0)?1:0)):((dspres/respp)+((dspres%respp>0)?1:0));
               /* results+="\n<div class=\"pagination-masked bottom\">"+
                        "<p class=\"pagination-info\">Click a page below to view its results</p>"+
                        "<ul class=\"pagination-links\">"+
                        "<li class=\"current-page-link\">";
                for(int j=0;j<indecies;j++)
                {
                    results+="\n<a href=\"javascript:showResForPage(\'"+(j+1)+"\')\">"+(j+1)+"</a>";
                }
                results+="\n</li>"+
                         "</ul>"+
                         "</div>"; 
                results+="\n<div id=\"divexpandbot\"class=\"pagination-masked top\">"+
                        "<p class=\"pagination-info\" style=\"font-size: 11px;\"><a href=\"javascript:expandAll()\">Expand All>></a></p>"+
                        "</div>";
                results+="\n<div id=\"divcollapsebot\" class=\"pagination-masked top\" style=\"width: 0px; height: 0px; visibility: hidden;\">"+
                        "<p class=\"pagination-info\" style=\"font-size: 11px;\"><a href=\"javascript:collapseAll()\">&lt;&lt;Collapse All</a></p>"+
                        "</div>"; */
            }
            dspaceSeacher.close();
            kohaSearcher.close();
            compoundSearcher.close();
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
        results+="</ul></div>";
        return results;
    }
    
    private String insertJavaScript(HttpServletRequest request)
    {
        String script="<script type=\"text/javascript\" >\n" +
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
                "function showResForPage()\n" +
                "{\n" +
                "var argv = showResForPage.arguments;\n" +
                "var currentIndex= document.getElementById('curp').innerHTML;\n" +
                "var page= argv[0];\n" +
                "var respp= document.getElementById('resppdiv').innerHTML;\n" +
                "var startIndex= (parseInt(page)-1)*parseInt(respp)+1;\n" +
                "var numres= document.getElementById('numresdiv').innerHTML;\n" +
                "var div1ds='';\n" +
                "var div2ds='';\n" +
                "var div3ds='';\n" +
                "var divmDS='div';\n" +
                "var div2mDS='div';\n" +
                "var divDS='div';\n" +
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
                "div2ds.style.width= \"0px\";\n" +
                "div2ds.style.height= \"0px\";\n" +
                "div2ds.style.visibility= \"hidden\";\n" +
                "}\n" +
               /* Finally show the main divs for the new page
                */
                "div3ds=document.getElementById(div2mDS);\n" +
                "if(null !== div3ds)\n" +
                "{\n" +
                "div3ds.style.width= \"100%\";\n" +
                "div3ds.style.height= \"auto\";\n" +
                "div3ds.style.visibility= \"visible\";\n" +
                "}\n" +
                "}\n" +
                /* Set the value of the current index div to the new div
                 */
                "document.getElementById('curp').innerHTML=page;\n"+
                /* Show the expand All div and hide the collapse all div
                 */
                "document.getElementById('divexpand').style.width=\"100%\";\n"+
                "document.getElementById('divexpand').style.height=\"auto\";\n"+
                "document.getElementById('divexpand').style.visibility=\"visible\";\n"+
                "document.getElementById('divcollapse').style.width=\"0px\";\n"+
                "document.getElementById('divcollapse').style.height=\"0px\";\n"+
                "document.getElementById('divcollapse').style.visibility=\"hidden\";\n"+
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
                "div1ds.style.width= \"100%\";\n" +
                "div1ds.style.height= \"auto\";\n" +
                "div1ds.style.visibility= \"visible\";\n" +
                "}\n" +
                /* Now for the full blown divs
                 */               
                "div2ds=document.getElementById(divDS);\n" +
                "if(null !== div2ds)\n" +
                "{\n" +
                "div2ds.style.width= \"0px\";\n" +
                "div2ds.style.height= \"0px\";\n" +
                "div2ds.style.visibility= \"hidden\";\n" +
                "}\n" +
                "}\n" +
                /* Show the collapse All div and hide the expand all div
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
        return "Short description";
    }
    // </editor-fold>
}
