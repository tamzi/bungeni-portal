<?xml version="1.0" encoding="UTF-8"?>

<!--
  template.xsl

  Version: $Revision: 1.7 $
 
  Date: $Date: 2006/07/27 22:54:52 $
 
  Copyright (c) 2002-2005, Hewlett-Packard Company and Massachusetts
  Institute of Technology.  All rights reserved.
 
  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are
  met:
 
  - Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
 
  - Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
 
  - Neither the name of the Hewlett-Packard Company nor the name of the
  Massachusetts Institute of Technology nor the names of their
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
 
  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
  ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
  HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
  USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
  DAMAGE.
-->

<!--
    TODO: Describe this XSL file    
    Author: Alexey Maslov
    
-->    

<xsl:stylesheet xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
	xmlns:dri="http://di.tamu.edu/DRI/1.0/"
	xmlns:mets="http://www.loc.gov/METS/"
	xmlns:xlink="http://www.w3.org/TR/xlink/"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
	xmlns:dim="http://www.dspace.org/xmlns/dspace/dim"
	xmlns:xhtml="http://www.w3.org/1999/xhtml"
	xmlns:mods="http://www.loc.gov/mods/v3"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns="http://www.w3.org/1999/xhtml"
	exclude-result-prefixes="i18n dri mets xlink xsl dim xhtml mods dc">
    
    <xsl:import href="../dri2xhtml.xsl"/>
    <xsl:output indent="yes"/>
    
    
    <!-- An example of an existing template copied from structural.xsl and overridden -->  
    <xsl:template name="buildFooter">
        <div id="ds-footer">
            &cpy;2000-2007 Bungeni
            <div id="ds-footer-links">
                <a>
                    <xsl:attribute name="href">
                        <xsl:value-of select="/dri:document/dri:meta/dri:pageMeta/dri:metadata[@element='contextPath'][not(@qualifier)]"/>
                        <xsl:text>/contact</xsl:text>
                    </xsl:attribute>
                    <i18n:text>xmlui.dri2xhtml.structural.contact-link</i18n:text>
                </a>
                <xsl:text> | </xsl:text>
                <a>
                    <xsl:attribute name="href">
                        <xsl:value-of select="/dri:document/dri:meta/dri:pageMeta/dri:metadata[@element='contextPath'][not(@qualifier)]"/>
                        <xsl:text>/feedback</xsl:text>
                    </xsl:attribute>
                    <i18n:text>xmlui.dri2xhtml.structural.feedback-link</i18n:text>
                </a>
            </div>
        </div>
</xsl:template>

<xsl:template name="buildHeader">
	<div id="ds-header">
		<img src="images/publiclogo.gif" alt="The Image Logo" />
	    <a>
		<xsl:attribute name="href">
		    <xsl:value-of select="/dri:document/dri:meta/dri:pageMeta/dri:metadata[@element='contextPath'][not(@qualifier)]"/>
		</xsl:attribute>
		<span id="ds-header-logo">&#160;</span>
	    </a>
	    <h1 class="pagetitle">
	    	<xsl:choose>
	    		<!-- protectiotion against an empty page title -->
	    		<xsl:when test="not(/dri:document/dri:meta/dri:pageMeta/dri:metadata[@element='title'])">
	    			<xsl:text> </xsl:text>
	    		</xsl:when>
	    		<xsl:otherwise>
	    			<xsl:copy-of select="/dri:document/dri:meta/dri:pageMeta/dri:metadata[@element='title']/node()"/>
	    		</xsl:otherwise>
	    	</xsl:choose>
	    		
	    </h1>
	    <h2 class="static-pagetitle"><i18n:text>xmlui.dri2xhtml.structural.head-subtitle</i18n:text></h2>
	    
	    
	    <ul id="ds-trail">
	    	<xsl:choose>
		    	<xsl:when test="count(/dri:document/dri:meta/dri:pageMeta/dri:trail) = 0">
		        	<li class="ds-trail-link first-link"> - </li>
		        </xsl:when>
		        <xsl:otherwise>
		        	<xsl:apply-templates select="/dri:document/dri:meta/dri:pageMeta/dri:trail"/>
		        </xsl:otherwise>
		</xsl:choose>
	    </ul>
	   
	    
	    <xsl:choose>
		<xsl:when test="/dri:document/dri:meta/dri:userMeta/@authenticated = 'yes'">
		    <div id="ds-user-box">
		        <p>
		            <a>
		                <xsl:attribute name="href">
		                    <xsl:value-of select="/dri:document/dri:meta/dri:userMeta/
		                        dri:metadata[@element='identifier' and @qualifier='url']"/>
		                </xsl:attribute>
		                <i18n:text>xmlui.dri2xhtml.structural.profile</i18n:text>
		                <xsl:value-of select="/dri:document/dri:meta/dri:userMeta/
		                    dri:metadata[@element='identifier' and @qualifier='firstName']"/>
		                <xsl:text> </xsl:text>
		                <xsl:value-of select="/dri:document/dri:meta/dri:userMeta/
		                    dri:metadata[@element='identifier' and @qualifier='lastName']"/>
		            </a>
		            <xsl:text> | </xsl:text>
		            <a>
		                <xsl:attribute name="href">
		                    <xsl:value-of select="/dri:document/dri:meta/dri:userMeta/
		                        dri:metadata[@element='identifier' and @qualifier='logoutURL']"/>
		                </xsl:attribute>
		                <i18n:text>xmlui.dri2xhtml.structural.logout</i18n:text>
		            </a>
		        </p>
		    </div>
		</xsl:when>
		<xsl:otherwise>
		    <div id="ds-user-box">
		        <p>
		            <a>
		                <xsl:attribute name="href">
		                    <xsl:value-of select="/dri:document/dri:meta/dri:userMeta/
		                        dri:metadata[@element='identifier' and @qualifier='loginURL']"/>
		                </xsl:attribute>
		                <i18n:text>xmlui.dri2xhtml.structural.login</i18n:text>
		            </a>
		        </p>
		    </div>
		</xsl:otherwise>
	    </xsl:choose>
	    
	</div>
	</xsl:template>

    
</xsl:stylesheet>
