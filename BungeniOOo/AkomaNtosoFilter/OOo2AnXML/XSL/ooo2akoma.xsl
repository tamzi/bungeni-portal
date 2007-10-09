<?xml version="1.0" encoding="UTF-8"?>
<!--

   $RCSfile: ooo2akoma.xsl,v $

   $Revision: 0.1 $


	The Contents of this file are made available subject to
	the terms of GNU Lesser General Public License Version 2.1.


	  GNU Lesser General Public License Version 2.1
	  =============================================
	  Copyright 2005 by Sun Microsystems, Inc.
	  901 San Antonio Road, Palo Alto, CA 94303, USA

	  This library is free software; you can redistribute it and/or
	  modify it under the terms of the GNU Lesser General Public
	  License version 2.1, as published by the Free Software Foundation.

	  This library is distributed in the hope that it will be useful,
	  but WITHOUT ANY WARRANTY; without even the implied warranty of
	  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
	  Lesser General Public License for more details.

	  You should have received a copy of the GNU Lesser General Public
	  License along with this library; if not, write to the Free Software
	  Foundation, Inc., 59 Temple Place, Suite 330, Boston,
	  MA  02111-1307  USA

-->
<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" 
xmlns:xlink="http://www.w3.org/1999/xlink" 
xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" 
xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" 
xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" 
xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" 
xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" 
xmlns:dc="http://purl.org/dc/elements/1.1/" 
xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" 
xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" 
xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" 
xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" 
xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" 
xmlns:math="http://www.w3.org/1998/Math/MathML" 
xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" 
xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" 
xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" 
xmlns:ooo="http://openoffice.org/2004/office" 
xmlns:ooow="http://openoffice.org/2004/writer" 
xmlns:oooc="http://openoffice.org/2004/calc" 
xmlns:dom="http://www.w3.org/2001/xml-events" 
xmlns="http://www.akomantoso.org/1.0"
exclude-result-prefixes="office table style text draw svg   dc config xlink meta oooc dom ooo chart math dr3d form script ooow draw">
<xsl:output method="xml" indent="yes" omit-xml-declaration="no"   />

<!-- keys -->
<xsl:key name="listTypes" match="text:list-style" use="@style:name"/>

    <xsl:template match="/">
        <xsl:apply-templates select="office:document-content" />
    </xsl:template>
    
    <xsl:template match="office:document-content">
     <akomantoso>
       <debaterecord>
         <identification>
           <!--put identification information here-->
         </identification>
         <xsl:apply-templates select="/office:document-content/office:body/office:text/text:section[@text:name='root']//text:section[@text:name='prayers']//text:section[@text:name='masthead_datetime']"  mode="metaPublication" />
        <references>  
    		<xsl:apply-templates select="office:automatic-styles" mode="metadata" />
    	</references>
     	 <xsl:apply-templates select="office:body/office:text/text:section[@text:name='root']" mode="body" />
       </debaterecord>
      </akomantoso>
    </xsl:template>

	<!-- styles processing, the metadata is stored with the styles -->
	<xsl:template match="office:automatic-styles" mode="metadata">
		<xsl:apply-templates />
	 </xsl:template>
	 
	<!-- for the metadata we are interested only in section styles --> 
	<xsl:template match="style:style">
		<xsl:choose>
			<xsl:when test="@style:family='section'">
				<xsl:call-template name="process-section-style"/>
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	 
	<!-- process-section-style -->
	<xsl:template name="process-section-style">
		<xsl:apply-templates />
	</xsl:template>
	
	<xsl:template match="style:section-properties[@Bungeni_QuestionID]">
	  <xsl:element name="Person" >
		<xsl:if test="string(@Bungeni_QuestionMemberFromURI)">
		<xsl:attribute name="href"><xsl:value-of select="@Bungeni_QuestionMemberFromURI" /></xsl:attribute>
		</xsl:if>
		<xsl:if test="string(@Bungeni_QuestionMemberFrom)">
		<xsl:attribute name="showAs"><xsl:value-of select="@Bungeni_QuestionMemberFrom" /></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">
		<xsl:call-template name="getIdentifier" />
		</xsl:attribute>
	  </xsl:element>	
	</xsl:template>
	
	<xsl:template match="style:section-properties[@Bungeni_SpeechBy]">
  <xsl:element name="Person" >
		<xsl:if test="string(@Bungeni_SpeechByURI)">
		<xsl:attribute name="href"><xsl:value-of select="@Bungeni_SpeechByURI" /></xsl:attribute>
		</xsl:if>
		<xsl:if test="string(@Bungeni_SpeechBy)">
		<xsl:attribute name="showAs"><xsl:value-of select="@Bungeni_SpeechBy" /></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">
		<xsl:call-template name="getIdentifier" />
		</xsl:attribute>
	  </xsl:element>	
 </xsl:template>
 
 <xsl:template name="getIdentifier" >
 	<xsl:variable name="referencedStyle" select="parent::style:style/@style:name" />
 	<xsl:value-of select="//text:section[@text:style-name=$referencedStyle]/text:section[starts-with(@text:name, 'meta')]/@text:name" />
 </xsl:template>
 

 	
	 <xsl:template match="office:body/office:text/text:section[@text:name='root']" mode="body">
		<preface>
		<xsl:apply-templates select="//text:section[@text:name='prayers']" />
		</preface>
		<debatebody>
		<xsl:apply-templates select="//text:section[@text:name='papers']" />
		<xsl:apply-templates select="//text:section[@text:name='qa']" />
	 	</debatebody>
	</xsl:template>

	 <xsl:template match="//text:section[@text:name='papers']" >
     <subdivision id="papers">
      	<xsl:apply-templates />
     </subdivision> 	
     </xsl:template>
     
     <xsl:template match="//text:section[@text:name='prayers']" >
        	<xsl:apply-templates />
     </xsl:template>

     <xsl:template match="//text:section[@text:name='qa']" >
       <subdivision id="qa">
        	<xsl:apply-templates />
       </subdivision>	
     </xsl:template>
          
     
     <xsl:template match="//text:section[starts-with(@text:name,'question')]" >
     	<xsl:element name="subdivision">
     		<xsl:attribute name="id"><xsl:value-of select="@text:name" /></xsl:attribute>
     		<xsl:apply-templates />
     	</xsl:element>
     </xsl:template>
     
     <xsl:template match="//text:section[contains(@text:name,'-speech')]" >
     	<xsl:element name="speech">
     		<xsl:attribute name="by"><xsl:value-of select="text:section[starts-with(@text:name, 'meta')]/@text:name" /></xsl:attribute>
     		<xsl:apply-templates />
     	</xsl:element>
     </xsl:template>

     <xsl:template match="//text:section[starts-with(@text:name,'question') and contains(@text:name, '-que')]" >
     	<xsl:element name="question">
     		<xsl:attribute name="by"><xsl:value-of select="text:section[starts-with(@text:name, 'meta')]/@text:name" /></xsl:attribute>
     		<xsl:apply-templates />
     	</xsl:element>
     </xsl:template>
          
     <xsl:template match="//text:section[starts-with(@text:name,'meta-mp-')]" >
     	<xsl:element name="from">
     		<xsl:value-of select="translate(., '{}','')" />
     	</xsl:element>
     </xsl:template>
     
     
     
	<!-- merging question - text -->     
	<!--
	<xsl:template match="text:p[@text:style-name='question-text']">
	   <xsl:call-template name="newLineMode" />
	   <question-text>		<xsl:apply-templates select="child::node()" mode="Others"/>		<xsl:apply-templates select="following-sibling::*[1][self::text:p[@text:style-name='question-text']]" mode="MoreSiblings" />	  
	   </question-text>
	  <xsl:apply-templates select="following-sibling::*[not(self::text:p[@text:style-name='question-text'])][1]" />	
	</xsl:template>	
	<xsl:template match="text:p[@text:style-name='question-text']" mode="MoreSiblings">		<xsl:call-template name="newLineMode" />		<xsl:apply-templates select="child::node()" mode="Others"/>		<xsl:apply-templates select="following-sibling::*[1][self::text:p[@text:style-name='question-text']]" mode="MoreSiblings" />	</xsl:template>	<xsl:template match="*" mode="Others">		<xsl:apply-templates />	</xsl:template>	<xsl:template name="newLineMode"><xsl:text>&#xa;</xsl:text></xsl:template>
	-->
     
     
     <!-- publication date and time -->
      <xsl:template match="/office:document-content/office:body/office:text/text:section[@text:name='root']//text:section[@text:name='prayers']//text:section[@text:name='masthead_datetime']" mode="metaPublication"  >
      
      <!-- parse date and strip preceeding and following characters -->
      <xsl:variable name="origDateString" select="text:p/text:placeholder[@text:description='debaterecord_official_date']"/>
      	  <xsl:variable name="firstReplaceDateString">	    <xsl:call-template name="replaceCharsInString">	      <xsl:with-param name="stringIn" select="string($origDateString)"/>	      <xsl:with-param name="charsIn" select="'&lt;'"/>	      <xsl:with-param name="charsOut" select="''"/>	    </xsl:call-template>
	   </xsl:variable>
	   
	  <xsl:variable name="secondReplaceDateString">	    <xsl:call-template name="replaceCharsInString">	      <xsl:with-param name="stringIn" select="string($firstReplaceDateString)"/>	      <xsl:with-param name="charsIn" select="'&gt;'"/>	      <xsl:with-param name="charsOut" select="''"/>	    </xsl:call-template>
	   </xsl:variable>

      <!-- parse date and strip preceeding and following characters -->
      <xsl:variable name="origTimeString" select="text:p/text:placeholder[@text:description='debaterecord_official_time']"/>
      <xsl:variable name="firstReplaceTimeString">	    <xsl:call-template name="replaceCharsInString">	      <xsl:with-param name="stringIn" select="string($origTimeString)"/>	      <xsl:with-param name="charsIn" select="'&lt;'"/>	      <xsl:with-param name="charsOut" select="''"/>	    </xsl:call-template>
	   </xsl:variable>
	   
	  <xsl:variable name="secondReplaceTimeString">	    <xsl:call-template name="replaceCharsInString">	      <xsl:with-param name="stringIn" select="string($firstReplaceTimeString)"/>	      <xsl:with-param name="charsIn" select="'&gt;'"/>	      <xsl:with-param name="charsOut" select="''"/>	    </xsl:call-template>
	   </xsl:variable>
	  
        <xsl:element name="publication">
  		   	<xsl:attribute name="date">
			   	<xsl:value-of select="$secondReplaceDateString" />
	   		</xsl:attribute>
	   		<xsl:attribute name="time">
	   			<xsl:value-of select="$secondReplaceTimeString" />
	   		</xsl:attribute>
	 	  	<xsl:attribute name="name">internal</xsl:attribute>
	 	  	<xsl:attribute name="showAs">Internal Circulation Only</xsl:attribute>
	   </xsl:element> 
	  </xsl:template>
 
 	<!-- here is the template that does the replacement -->	<xsl:template name="replaceCharsInString">	  <xsl:param name="stringIn"/>	  <xsl:param name="charsIn"/>	  <xsl:param name="charsOut"/>	  <xsl:choose>	    <xsl:when test="contains($stringIn,$charsIn)">	      <xsl:value-of select="concat(substring-before($stringIn,$charsIn),$charsOut)"/>	      <xsl:call-template name="replaceCharsInString">	        <xsl:with-param name="stringIn" select="substring-after($stringIn,$charsIn)"/>	        <xsl:with-param name="charsIn" select="$charsIn"/>	        <xsl:with-param name="charsOut" select="$charsOut"/>	      </xsl:call-template>	    </xsl:when>	    <xsl:otherwise>	      <xsl:value-of select="$stringIn"/>	    </xsl:otherwise>	  </xsl:choose>	</xsl:template>
	
	<xsl:template match="text:section" mode="prayersSection">
		<xsl:value-of select="." />
	</xsl:template>
	
	<!-- generic templates -->
	

<!-- convert list to xhtml list -->
<xsl:template match="text:list">
	<xsl:variable name="level" select="count(ancestor::text:list)+1"/>
	
	<!-- the list class is the @text:style-name of the outermost
		<text:list> element -->
	<xsl:variable name="listClass">
		<xsl:choose>
			<xsl:when test="$level=1">
				<xsl:value-of select="@text:style-name"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="ancestor::text:list[last()]/@text:style-name"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	
	<!-- Now select the <text:list-level-style-foo> element at this
		level of nesting for this list -->
	<xsl:variable name="node" select="key('listTypes',$listClass)/*[@text:level='$level']"/>

	<!-- emit appropriate list type -->
	<xsl:choose>
		<xsl:when test="local-name($node)='list-level-style-number'">
			<ol class="{concat($listClass,'_',$level)}">
				<xsl:apply-templates/>
			</ol>
		</xsl:when>
		<xsl:otherwise>
			<ul class="{concat($listClass,'_',$level)}">
				<xsl:apply-templates/>
			</ul>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="text:list-item">
	<li><xsl:apply-templates/></li>
</xsl:template>

<!-- convert to xhtml links -->
	
<xsl:template match="text:a">
<a href="{@xlink:href}"><xsl:apply-templates/></a>
</xsl:template>	


<!-- strip empty text:p tags -->

<xsl:template match="text:p[@text:style-name='Standard']" >
	<xsl:choose>
		<xsl:when test="not(string(.))">
			<!-- remove the empty paragraph -->
		</xsl:when>
		<xsl:otherwise>
			<xsl:apply-templates />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<!-- convert paragraphs to xhtml paragraphs -->

<xsl:template match="text:p">
	<div class="{translate(@text:style-name,'.','_')}">
		<xsl:apply-templates/>
		<xsl:if test="count(node())=0"><br /></xsl:if>
	</div>
</xsl:template>



<!-- process headings -->

<xsl:template match="text:h[@text:style-name='question-title']">
<title><xsl:value-of select="." /></title>
</xsl:template>

<xsl:template match="text:h[@text:style-name='papers']">
<title><xsl:value-of select="." /></title>
</xsl:template>


<xsl:template match="text:h[@text:style-name='qa-title']">
<title><xsl:value-of select="." /></title>
</xsl:template>

<xsl:template match="text:h">
	<xsl:variable name="level">
		<xsl:choose>
			<xsl:when test="@text:outline-level &gt; 6">6</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="@text:outline-level"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<xsl:element name="{concat('h', $level)}">
		<xsl:attribute name="class">
			<xsl:value-of select="translate(@text:style-name,'.','_')"/>
		</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>



	
</xsl:stylesheet>
