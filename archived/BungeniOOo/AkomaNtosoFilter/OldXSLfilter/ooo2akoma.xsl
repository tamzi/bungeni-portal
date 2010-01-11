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

   <xsl:key name="Answer" match="text:h[@text:style-name='answer']"
   	use="generate-id((preceding-sibling::text:h[@text:style-name='session']|
        preceding-sibling::text:h[@text:style-name='agenda']|
        preceding-sibling::text:h[@text:style-name='question'])[last()])" />

    <xsl:key name="question" match="text:h[@text:style-name='question']"
	 use="generate-id(preceding-sibling::text:h[@text:style-name='agenda'][1])"/>

    <xsl:key name="agenda" match="text:h[@text:style-name='agenda']"
	 use="generate-id(preceding-sibling::text:h[@text:style-name='session'][1])"/>

    <xsl:key name="paper-details" match="text:p[@text:style-name='paper-details']"
	 use="generate-id(preceding-sibling::text:p[@text:style-name='papers'][1])"/>

    <xsl:key name="notice" match="text:p[@text:style-name='notice']"
	 use="generate-id(preceding-sibling::text:p[@text:style-name='notice-of-motion'][1])"/>

   <xsl:key name="notice-text" match="text:p[@text:style-name='noticetext']"
   	use="generate-id((preceding-sibling::text:p[@text:style-name='notice-of-motion']|
        preceding-sibling::text:p[@text:style-name='notice'])[last()])" />
	 

    <xsl:template match="/">
        <xsl:apply-templates select="office:document"/>
    </xsl:template>
    <xsl:template match="office:document">
        <xsl:apply-templates select="office:body"/>
    </xsl:template>
	<xsl:template match="office:body">
       <xsl:apply-templates select="office:text"/>
    </xsl:template>
    
    <xsl:template match="office:text">
    <akomantoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
						xmlns="http://www.akomantoso.org/1.0">
		<minutes>
			<debate>
			<xsl:apply-templates select="text:p[@text:style-name='prayers']" mode="prayers"/>
			<xsl:apply-templates select="text:p[@text:style-name='papers']" mode="papers"/>
			<xsl:apply-templates select="text:p[@text:style-name='notice-of-motion']" mode="notice-of-motion"/>
			<xsl:apply-templates select="key('Answer',generate-id())" mode="answer"/>
			<xsl:apply-templates select="text:h[@text:style-name='session']" mode="session"/>
			</debate>
        </minutes>
        </akomantoso>
    </xsl:template>

<xsl:template match="office:script">
</xsl:template>


<xsl:template match="office:settings">
</xsl:template>

<xsl:template match="office:font-decls">
</xsl:template>


 <xsl:template match="text:p" mode="notice-of-motion">
 <subdivision id="notices">
	<title><xsl:apply-templates/></title>
			 <xsl:apply-templates select="key('notice',generate-id())" mode="notice"/>
 </subdivision>
 </xsl:template>

 <xsl:template match="text:p" mode="notice">
 <subdivision id="notices_{generate-id()}">
	<title><xsl:apply-templates/></title>
			 <xsl:apply-templates select="key('notice-text',generate-id())" mode="noticetext"/>
 </subdivision>
 </xsl:template>

 <xsl:template match="text:p" mode="noticetext">
 <speech>
	<xsl:apply-templates/>
 </speech>
 </xsl:template>


 <xsl:template match="text:p" mode="prayers">
 <subdivision id="prayers">
	<title><xsl:apply-templates/></title>
 </subdivision>
 </xsl:template>

 <xsl:template match="text:p" mode="papers">
 <subdivision id="papers">
	<title><xsl:apply-templates/></title>
		<xsl:apply-templates select="key('paper-details',generate-id())" mode="paper-details"/>
 </subdivision>
 </xsl:template>

 <xsl:template match="text:p" mode="paper-details">
 <other id="{generate-id()}">
	 <xsl:apply-templates />
 </other>
 </xsl:template>

 <xsl:template match="text:h" mode="session">
 <subdivision id="qa">
	<title><xsl:apply-templates/></title>
	 <xsl:apply-templates select="key('Answer',generate-id())" mode="answer"/>
	 <xsl:apply-templates select="key('agenda',generate-id())" mode="agenda"/>
 </subdivision>
 </xsl:template>

 <xsl:template match="text:h" mode="agenda">
 <subdivision id="que{generate-id()}"><title><xsl:apply-templates/></title>
	 <xsl:apply-templates select="key('Answer',generate-id())" mode="answer"/>
	 <xsl:apply-templates select="key('question',generate-id())" mode="question"/>
 </subdivision>
 </xsl:template>

 <xsl:template match="text:h" mode="question">
 <question><title><xsl:apply-templates/></title>
	 <xsl:apply-templates select="key('Answer',generate-id())" mode="answer"/>
 </question>
 </xsl:template>

 <xsl:template match="text:h" mode="answer">
	<answer>
	<xsl:value-of select="."/>
 	</answer>
 </xsl:template>



</xsl:stylesheet>
