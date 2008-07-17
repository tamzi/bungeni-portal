<%-- 
    Document   : index
    Created on : Jun 17, 2008, 2:00:30 PM
    Author     : undesa
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Bungeni Digital Repository</title>
        <link rel="shortcut icon" href="/digitalrepository/favicon.ico" type="image/x-icon"/>
        <link type="text/css" rel="stylesheet" media="screen" href="/digitalrepository/style/style.css" />
        
        
        
    </head>
    <body>
        <div id="ds-main">
            <div id="ds-header">
                <img alt="The Image Logo" src="/digitalrepository/images/logo.gif" />
                <div id="ds-user-box">
                    <p>
                        <a href="/digitalrepository/#">Login</a>
                    </p>
                </div>
            </div>
            <div id="ds-body">
                <h1 style="font-size: 158%;" class="ds-div-head">Welcome to Bungeni Digital Repository</h1>
                <p class="ds-paragraph" style="font-size: 90%;">Some text here. Some text here. 
                Some text here. Some text here. Some text here. 
                Some text here. Some text here. Some text here. 
                Some text here. Some text here. Some text here. 
                Some text here. Some text here. Some text here. 
                Some text here. Some text here. Some text here. 
                Some text here. Some text here. Some text here. 
                Some text here. Some text here. Some text here. 
                Some text here. Some text here. Some text here.
                Some text here. Some text here. Some text here. 
                Some text here. Some text here. Some text here. 
                Some text here. Some text here. Some text here. 
                Some text here. </p>
                <h1 style="font-size: 158%;" class="ds-div-head">Search Bungeni Digital Repository</h1>
                <form class="ds-interactive-div primary" action="/digitalrepository/search" method="get">
                <p class="ds-paragraph">Select Repository....:
                    <input type="checkbox" name="dspace" checked /> Digital Repository/DSpace
                    <input type="checkbox" name="koha" checked/> Library/Koha
                <p class="ds-paragraph">Display Results By.....:
                    <input type="radio" name="merge" value="yes" /> Ranking/Relevance
                    <input type="radio" name="merge" value="no" checked /> Repository
                <p class="ds-paragraph">Search Text...
                    <input class="ds-text-field" name="query" type="text" value="" />
                    <input class="ds-button-field"  name="submit" type="submit" value="Go" />
                    Results Per Page
                    <select style="margin:3px 2px 1px 1px ;" class="ds-button-field" name="respp">
                        <option value="5">5</option>
                        <option value="10">10</option>
                        <option value="20">20</option>
                        <option value="30">30</option>
                    </select>
                    <p class="ds-paragraph">
                        Sort Items By
                        <select style="margin: 3px 2px 1px 1px ;" class="ds-button-field" name="orderby">
                            <option value="relevance">Relevance</option>
                            <option value="title">Title</option>
                            <option value="pubdate">Issue Date</option>
                        </select>
                        In Order
                        <select style="margin: 3px 2px 1px 1px ;" class="ds-button-field" name="orderby">
                            <option value="desc">Descending</option>
                            <option value="asc">Asceding</option>
                        </select>
                    </p>
                </form>
            </div>
            <div id="ds-options">
                <h3 class="ds-option-set-head">Browse</h3>
                <div class="ds-option-set">
                    <ul class="ds-options-list">
                        <li>
                            <h4 class="ds-sublist-head">
                                <a title="The Bungeni Digital Repository Home" href="http://192.168.1.10:8090/digitalrepository/">
                                    Home
                                </a>
                            </h4>
                        </li>
                        <li>
                            <h4 class="ds-sublist-head">
                                <a title="The Bungeni Dspace Project for management of Parliaments documents" href="http://192.168.1.10:8090/xmlui/">
                                    Bungeni Dspace
                                </a>
                            </h4>
                        </li>
                        <li>
                            <h4 class="ds-sublist-head">
                                <a title="The bungeni Library project" href="http://192.168.1.10">
                                    Bungeni Koha
                                </a>
                            </h4>
                        </li>
                    </ul>
                </div>
                <h3 class="ds-option-set-head">Search...</h3>
                    <div class="ds-option-set" id="ds-search-option">
                        <form method="post" id="ds-search-form" action="/digitalrepository/search">
                            <fieldset>
                            <input type="text" class="ds-text-field " name="query" />
                            <input value="Go" type="submit" name="submit" class="ds-button-field "/>
                            </fieldset>
                        </form>
                        <a href="/digitalrepository/advanced-search">Advanced Search</a>
                    </div>
                <h3 class="ds-option-set-head">Bungeni Portal</h3>
                <div class="ds-option-set" id="ds-search-option">
                    <ul class="ds-options-list">
                        <li>
                            <a title="" href="http://192.168.1.5:10000/bungeni-public">Bungeni Home</a>
                        </li>
                        <li>
                            <a title="parliamentary activities at the plenary and committees level" href="http://192.168.1.5:10000/bungeni-public/parliamentary-business">business</a>
                        </li>
                        <li>
                            <a title="member of parliaments and political parties represented in parliament" href="http://192.168.1.5:10000/bungeni-public/mps-and-political-grops">members</a>
                        </li>
                        <li>
                            <a title="" href="http://192.168.1.5:10000/bungeni-public/how-parliament-works">how we work</a>
                        </li>
                        <li>
                            <a title="" href="http://192.168.1.5:10000/bungeni-public/organisation">organisation</a>
                        </li>
                        <li>
                            <a title="" href="http://192.168.1.5:10000/bungeni-public/have-your-say">have-your-say</a>
                        </li>
                        <li>
                            <a title="" href="http://192.168.1.5:10000/bungeni-public/visit-parliament">vist parliament</a>
                        </li>
                        <li>
                            <a title="" href="http://192.168.1.5:10000/bungeni-public/resources">resources</a>
                        </li>
                    </ul>
                </div>
            </div>
            <div id="ds-footer">
                <p>&copy;2000-2007 Bungeni
            </div>
        </div>
    </body>
</html>
