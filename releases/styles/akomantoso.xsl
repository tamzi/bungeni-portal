<?xml version="1.0" encoding="UTF-8"?>
<!-- ===================================================================== 
	PAPI sample XSLT stylesheet                                                  
	
	
	Release  15/01/2006                                                 
	Fabio Vitali - University of Bologna                                
	
	The present XSLT stylesheet uses DTD entities to manage variability
	and reach flexibility. This allows a single stylesheet to handle multiple
	document types and different uses for the same element types. Additional 
	XSLT stylesheets for specific document types do not need such complexity. 
	===================================================================== -->
	
<!DOCTYPE xsl:stylesheet [

<!ENTITY resolver "http://www.parliaments.info/PAPI/resolver.php?urn=">  <!--
      The resolver entity contains the URL of the URN->URL resolver for PAPI --> 

<!ENTITY title "t">  <!--
      The title entity control the content of the title of the document. Possible values: 
      - t:  just the ActTitle, 
      - tn: the ActTitle and then the ActNumber, 
      - nt: the ActNumber and then the ActTitle     -->
      
<!ENTITY OneCol   "papi:report[.//papi:item]"> 
<!ENTITY LeftPane "papi:act | papi:bill | papi:doc | papi:report | papi:minutes">  <!-- 
     The layout entities control the overall layout organization of the page. 
     They contain the doc type of the document that will be shown in that layout: 
      - OneCol: A single column with all data vertically spaced
      - LeftPane: the topmost area contains the preface, a left pane contains
                  a list of links to the sections of the clauses part, and a
                  large column on the right contains the rest of the document.  -->

<!ENTITY hierarchyN-T-C    "papi:section     | papi:part | papi:paragraph   | papi:chapter | dummy"> 
<!ENTITY hierarchyNT-C     "papi:article     | papi:item[papi:title]        | papi:artigo  | dummy">
<!ENTITY hierarchyNC       "papi:clause      | papi:item[not(papi:title)]   | dummy">
<!ENTITY hierarchyT-C      "papi:subdivision | dummy">   <!--
       The hierarchy* entities control the type of layout to be given to hierarchical elements in PAPI documents. 
       These are three of the many possible layouts: 
       - N-T-C: puts on separate lines (-) the (N)um first, then the (T)itle, then the (C)ontent of the element. 
       - NT-C:  puts on the same line the  (N)um and the (T)itle, and on a separate line the (C)ontent of the element
       - NC:    puts on the same line the  (N)um and the (C)ontent of the element. Shows no (T)itle. 
       - T-C:   puts on separate lines the  (T)itle and the (C)ontent of the element. Shows no (N)um. 
       In all cases, the full list of papi:-prefixed elements must be given, separated by "|" and ended with "dummy" -->
  
  <!--  DO NOT MODIFY THE FOLLOWING ENTITIES UNLESS YOU KNOW WHAT YOU ARE DOING!!!  -->
  <!ENTITY docs              "papi:act | papi:bill | papi:doc | papi:report | papi:minutes" >
  <!ENTITY hierElements      "papi:hcontainer | papi:section    | papi:part    | papi:paragraph   | papi:chapter  | 
                              papi:article    | papi:clause     |  papi:partie | papi:paragraphe  | papi:chapitre |  
                              papi:artigo     | papi:subdivision | papi:item">
  <!ENTITY EndOfHierarchy    "*[local-name()!='num' and local-name()!='title'and local-name()!='subtitle']" >
  
  <!ENTITY containerElements "papi:*">
  <!ENTITY blockElements     "papi:block      | papi:toc      | papi:speech | papi:question | papi:item">
  <!ENTITY inlineElements    "papi:inline     | papi:ref      | papi:def       ">
  <!ENTITY PAPItitleInline   "papi:ActType    | papi:ActTitle | papi:ActNumber | 
                              papi:ActProponent | papi:ActDate | papi:ActPurpose ">
  <!ENTITY markerElements    "papi:marker     | papi:noteref  | papi:recordedTime">
  <!ENTITY htmlElements      "papi:p          | papi:ul       | papi:ol        | papi:li      | papi:table   | 
                              papi:tr         | papi:td       | papi:th        | papi:span    | papi:b       | 
                              papi:i          | papi:a        | papi:img">

  
  <!ENTITY hierarchyTOC      "papi:preamble   | papi:section  | papi:part      | 
                              papi:paragraph  | papi:chapter  |  papi:article  | papi:artigo  | 
                              papi:subdivision | papi:item[papi:title] | dummy">
  
  <!-- The following entities allow the programmer to show debug messages when needed. 
       Because of a bug in Internet Explorer, they CAN NEVER be empty. 
       A stupid comment has been inserted instead. -->
  <!ENTITY debug  '<xsl:comment xmlns:xsl="http://www.w3.org/1999/XSL/Transform">debug message</xsl:comment>'>
  <!ENTITY sdebug  '<xsl:comment xmlns:xsl="http://www.w3.org/1999/XSL/Transform">special debug message</xsl:comment>'>
  
  ]>
  <xsl:stylesheet version="1.0" xmlns:papi="http://www.parliaments.info/PAPI/1.0" xmlns="http://www.w3.org/1999/xhtml"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="html" encoding="UTF-8" indent="yes"/>
	<!-- ======================================================== -->
	<!--                                                          -->
	<!--  Main Template                                           -->
	<!--                                                          -->
	<!-- ======================================================== -->
	<xsl:template match="/">
		<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
				<xsl:call-template name="title-&title;"/>
				<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
				<link href="../styles/style.css" rel="stylesheet"/>
			</head>
			<body>
				<xsl:apply-templates/>
			</body>
		</html>
	</xsl:template>
  	<xsl:template match="@*">
  		<xsl:copy-of select="."/>
  	</xsl:template>
  	<!-- ======================================================== -->
	<!--                                                          -->
	<!--  Title Templates                                         -->
	<!--                                                          -->
	<!-- ======================================================== -->
	<xsl:template name="title-t">
		<title>
			<xsl:value-of select="//papi:ActTitle"/>
		</title>
	</xsl:template>
	<xsl:template name="title-tn">
		<title>
			<xsl:value-of select="//papi:ActTitle"/>
			<xsl:if test="//papi:ActNumber">
				<xsl:text> - </xsl:text>
				<xsl:value-of select="//papi:ActNumber"/>
			</xsl:if>
		</title>
	</xsl:template>
	<xsl:template name="title-nt">
		<title>
			<xsl:value-of select="//papi:ActNumber"/>
			<xsl:if test="//papi:ActTitle">
				<xsl:text> - </xsl:text>
				<xsl:value-of select="//papi:ActTitle"/>
			</xsl:if>
		</title>
	</xsl:template>
	<!-- ======================================================== -->
	<!--                                                          -->
	<!--  Layout Templates                                        -->
	<!--                                                          -->
	<!-- ======================================================== -->
  	<xsl:template match="&OneCol;">
  		&debug;
  		<xsl:apply-templates select="papi:preface"/>
  		<xsl:apply-templates select="papi:preamble"/>
  		<xsl:apply-templates select="papi:clauses | papi:maincontent | papi:debate"/>
  		<xsl:apply-templates select="papi:conclusions"/>
  		<xsl:apply-templates select="papi:attachments"/>
  		<xsl:apply-templates select="papi:meta"/>
  	</xsl:template>
  	<xsl:template match="&LeftPane;">
  		&debug;
  		<table cellpadding="0" cellspacing="5" border="0" width="100%">
			<tr style="margin:top:30px; margin-bottom:30px;">
				<td colspan="2">
					<xsl:apply-templates select="papi:preface"/>
				</td>
			</tr>
			<tr valign="top">
				<xsl:if test="papi:clauses | papi:maincontent | papi:debate | papi:attachments">
					<td width="20%" style="border: thin solid #bbbbbb; background-color: #ffffcc;">
						<div class="toc-head">Table of Content</div>
						<xsl:apply-templates select="papi:preface | papi:preamble | papi:clauses | papi:maincontent | papi:debate | papi:attachments" mode="Link"/>
						<xsl:apply-templates select="papi:meta" mode="Link"/>
					</td>
				</xsl:if>
				<td width="80%" style="padding-top:15px;">
					<xsl:apply-templates select="papi:preamble"/>
					<xsl:apply-templates select="papi:clauses | papi:maincontent | papi:debate"/>
					<xsl:apply-templates select="papi:conclusions"/>
					<xsl:apply-templates select="papi:attachments"/>
					<xsl:apply-templates select="papi:meta"/>
				</td>
			</tr>
		</table>
	</xsl:template>
  	<!-- ======================================================== -->
  	<!--                                                          -->
  	<!--  individual templates                                    -->
  	<!--                                                          -->
  	<!-- ======================================================== -->
  	
  	<xsl:template match="papi:tocitem">
  		<div class="tocitem-{@level}">
  			<a href="#{@idref}"><xsl:apply-templates/></a>
  		</div>
  	</xsl:template>
  	<xsl:template match="papi:p" priority="0.3">
  		<xsl:element name="div">
  			<xsl:apply-templates select="@*"/>
  			<xsl:apply-templates/>
  		</xsl:element>
  	</xsl:template>
  	<xsl:template match="papi:ref" priority="0.3">
  		<a>
  			<xsl:apply-templates select="@*"/>
  			<xsl:apply-templates/>
  		</a>
  	</xsl:template>
  	<xsl:template match="papi:recordedTime" priority="0.3">
  		<span class="time"> [<xsl:value-of select="substring(@time, 1, 5)"/>] </span>
  	</xsl:template>
  	<xsl:template match="@href">
  		<xsl:attribute name="href">
	  		<xsl:if test="starts-with(.,'urn:papi:')">
	  			<xsl:text>&resolver;</xsl:text>
	  		</xsl:if>
  			<xsl:value-of select="."/>
  		</xsl:attribute>
  	</xsl:template>
  	<xsl:template match="papi:speech | papi:question" priority="0.3">
  		<div class="{name()}">
  			<xsl:apply-templates select="@*"/>
  			<span class="speech-by">
   				<xsl:value-of select="//papi:person[@id=current()/@by]/@long"/>
  				<xsl:text>: </xsl:text>
  			</span>
  			<xsl:apply-templates/>
  		</div>
  	</xsl:template>
  	<xsl:template match="@by"/>
   	
  	<!-- ======================================================== -->
	<!--                                                          -->
	<!--  Template for main content type patterns of PAPI         -->
	<!--                                                          -->
	<!-- ======================================================== -->
  	<xsl:template match="&containerElements;">
  		&sdebug;
  		<div class="{name()}"><a name="{name()}-{count(preceding::*[name()=name(current())])+1}">
	  		<xsl:apply-templates/>
  		</a></div>
  	</xsl:template>
  	<xsl:template match="&blockElements;" priority="0.25">
		&debug;
		<div class="{name()}">
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates/>
		</div>
	</xsl:template>
  	<xsl:template match="&inlineElements;" priority="0.25">
  		&debug;
  		<span class="{name()}">
  			<xsl:apply-templates select="@*"/>
  			<xsl:apply-templates/>
  		</span>
  	</xsl:template>
  	<xsl:template match="&PAPItitleInline;" priority="0.25">
  		&debug;
  		<span class="{name()}" title="{name()}">
  			<xsl:apply-templates select="@*"/>
  			<xsl:apply-templates/>
  		</span>
  	</xsl:template>
  	<xsl:template match="&markerElements;" priority="0.25">
		&debug;
		<span class="{name()}"><xsl:apply-templates select="@*"/>[]</span>
	</xsl:template>
  	<xsl:template match="&htmlElements;" priority="0.25">
  		<xsl:element name="{name()}">
  			<xsl:apply-templates select="@*"/>
  			<xsl:apply-templates/>
  		</xsl:element>
  	</xsl:template>
  	<!-- ======================================================== -->
	<!--                                                          -->
	<!--  Template for hierarchical elements                      -->
	<!--                                                          -->
	<!-- ======================================================== -->
  	
  	<xsl:template match="&hierarchyN-T-C;" priority="0.30">
  		&debug;
  		<div class="cont-{name()}">
  			<div class="num-{name()}"><a name="{@id}">
  				<xsl:call-template name="num"/>
  			</a></div>
  			<div class="title-{name()}">
  				<xsl:apply-templates select="papi:title"/>
  			</div>
  			<xsl:apply-templates select="&hierElements; | &EndOfHierarchy;"/>
  		</div>
  	</xsl:template>
  	<xsl:template match="&hierarchyNT-C;" priority="0.30">
  		&debug;
  		<xsl:variable name="num"><xsl:call-template name="num"/></xsl:variable>
  		<div class="cont-{name()}">
  			<div class="head-{name()}"><a name="{@id}">
  				<xsl:value-of select="$num"/>
  				<xsl:if test="$num!=''">
  					<xsl:text> - </xsl:text>
  				</xsl:if>
  				<xsl:apply-templates select="papi:title"/>
  			</a></div>
  			<xsl:apply-templates select="papi:subtitle"/>
   			<xsl:apply-templates select="&hierElements; | &EndOfHierarchy;"/>
  		</div>
  	</xsl:template>
  	<xsl:template match="&hierarchyNC;" priority="0.30">
  		&debug;
  		<xsl:variable name="num"><xsl:call-template name="num"/></xsl:variable>
  		<xsl:choose>
  			<xsl:when test="$num!=''">
		  		<table class="cont-{name()}" >
  					<tr>
  						<td class="num-{name()}">
  							<div><xsl:value-of select="$num"/></div>
  						</td>
  						<td>
  							<xsl:apply-templates select="&hierElements; | &EndOfHierarchy;"/>
  						</td>
  					</tr>
  				</table>
  			</xsl:when>
  			<xsl:otherwise>
  				<div class="cont-{name()}">
  					<xsl:apply-templates select="&hierElements; | &EndOfHierarchy;"/>
  				</div>
  			</xsl:otherwise>
  		</xsl:choose>
  	</xsl:template>
  	<xsl:template match="&hierarchyT-C;" priority="0.30">
  		&debug;
  		<div class="cont-{name()}">
  			<div class="title-{name()}"><a name="{@id}">
  				<xsl:apply-templates select="papi:title"/>
  			</a></div>
  			<xsl:apply-templates select="&hierElements; | &EndOfHierarchy;"/>
  		</div>
  	</xsl:template>
  	<xsl:template match="&hierElements;" priority="0.25">
  		&debug;
  		<div class="cont-{name()}">
  			<xsl:call-template name="num"/>
  			<xsl:apply-templates select="papi:title"/>
  			<xsl:apply-templates select="&hierElements; | &EndOfHierarchy;"/>
  		</div>
  	</xsl:template>
  	<xsl:template match="papi:title">
  		<span class="{local-name()}">
  			<xsl:apply-templates/>
  		</span>
  	</xsl:template>
  	<xsl:template name="num">
  		<xsl:choose>
  			<xsl:when test="papi:num">
  				<span class="num"><xsl:value-of select="papi:num"/></span>
  			</xsl:when>
  			<xsl:when test="ancestor-or-self::*[@numbering='on']">
  				<span class="num"><xsl:number/></span>
  			</xsl:when>
  		</xsl:choose>
  	</xsl:template>
  	<!-- ======================================================== -->
	<!--                                                          -->
	<!--  Modo Link (left pane)                                   -->
	<!--                                                          -->
	<!-- ======================================================== -->
  	<xsl:template match="papi:clauses | papi:maincontent | papi:debate" mode="Link">
  		&debug;
  		<xsl:apply-templates mode="Link"/>
	</xsl:template>
	<xsl:template match="&hierarchyTOC;" mode="Link" priority="0.25">
		&debug;
		<div>
			<xsl:attribute name="class">
				<xsl:text>toc-</xsl:text>
				<xsl:value-of select="name()"/>
				<xsl:if test="count(ancestor::*[name()=name(current())])">
					<xsl:text>-</xsl:text>
					<xsl:value-of select="count(ancestor::*[name()=name(current())])"/>
				</xsl:if>
			</xsl:attribute>
			<a href="#{@id}">
				<xsl:apply-templates select="papi:num | papi:title" mode="Link"/>
			</a>
		</div>
		<xsl:apply-templates select="&hierarchyTOC;" mode="Link"/>
	</xsl:template>
  	<xsl:template match="papi:num" mode="Link">
  		&debug;
  		<xsl:value-of select="."/>
  		<xsl:if test="following-sibling::papi:title">
			<xsl:text> - </xsl:text>
		</xsl:if>
	</xsl:template>
  	<xsl:template match="papi:title" mode="Link">
  		&debug;
  		<xsl:apply-templates/>
	</xsl:template>
  	<xsl:template match="papi:preamble" mode="Link" priority="0.3">
   		<div class="toc-{name()}">
  			<a href="#preamble">Preamble</a>
  		</div>
  	</xsl:template>
  	<xsl:template match="papi:attachments" mode="Link">
  		&debug;
  		<div class="toc-attachments">
  			<a href="#{attachment[1]/@id}">Attachments</a>
  		</div>
  	</xsl:template>
  	<xsl:template match="papi:meta" mode="Link">
  		&debug;
  		<hr style="margin-top:15pt;"/>
  		<div class="toc-meta">
  			<a href="#meta">Information about this document</a>
  		</div>
  	</xsl:template>
  	<xsl:template match="*" mode="Link"/>
  	
  	
  	<!-- ======================================================== -->
	<!--                                                          -->
	<!--  metadata templates                                      -->
	<!--                                                          -->
	<!-- ======================================================== -->
  	<xsl:template match="papi:descriptor">
   			<xsl:apply-templates/>
  	</xsl:template>
  	<xsl:template match="papi:meta">
  		&debug;
  		<hr/>
  		<div class="meta">
  			<table border="0" cellpadding="2" cellspacing="0" width="75%" align="center" style="margin-left: 15px;">
  				<tr><td colspan="2" class="important" style="text-align:left"><a name="meta">Information about this document</a></td></tr>
  				<xsl:apply-templates/>
  			</table>
  		</div>
  	</xsl:template>
  	<xsl:template match="papi:publication">
  		<tr>
  			<th>Publication</th>
  			<td>Published on <xsl:value-of select="@date"/> by <xsl:value-of select="@type"/> num. <xsl:value-of select="@num"/></td>
  		</tr>
  	</xsl:template>
  	<xsl:template match="papi:enactmentDate">
  		<tr>
  			<th>Date of enactment</th>
  			<td><xsl:value-of select="@date"/></td>
  		</tr>
  	</xsl:template>
  	<xsl:template match="papi:uri">
  		<tr>
  			<th>Official URI</th>
  			<td><a><xsl:apply-templates select="@href"/><xsl:value-of select="@href"/></a></td>
  		</tr>
  	</xsl:template>
  	<xsl:template match="papi:editors">
  		<tr>
  			<th>Editor<xsl:if test="count(*)>1">s</xsl:if></th>
  			<td><xsl:apply-templates/></td>
  		</tr>
  	</xsl:template>
  	<xsl:template match="papi:editor">
  		<xsl:if test="position()>2">, </xsl:if>
  		<xsl:value-of select="@name"/>
  		<xsl:text> (doing </xsl:text>
  		<xsl:value-of select="@contribution"/>
  		<xsl:text> on </xsl:text>
  		<xsl:value-of select="@date"/>
  		<xsl:text>)</xsl:text>
  	</xsl:template>  	
</xsl:stylesheet>
