<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.akomantoso.org/" xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
    xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
    xmlns:math="http://www.w3.org/1998/Math/MathML"
    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
    xmlns:ooo="http://openoffice.org/2004/office" xmlns:ooow="http://openoffice.org/2004/writer"
    xmlns:oooc="http://openoffice.org/2004/calc" xmlns:dom="http://www.w3.org/2001/xml-events"
    xmlns:xforms="http://www.w3.org/2002/xforms"
    exclude-result-prefixes="xsl xsd xsi text office style table draw fo xlink dc meta number svg chart dr3d math form script ooo ooow oooc dom xforms"
    version="1.0">
    <xsl:output indent="yes" method="xml"/>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

	<xsl:template match="p">
		<pippo>
			<xsl:apply-templates />
		</pippo>
	</xsl:template>

   <xsl:template match="text:reference-mark-start">
   		<text:reference-mark-start>
   			<xsl:attribute name="class" select="@text:name" />
        	<xsl:apply-templates/>
		</text:reference-mark-start>
    </xsl:template>

   <xsl:template match="text:reference-mark-end">
   		<text:reference-mark-end>
   			<xsl:attribute name="class" select="@text:name" />
        	<xsl:apply-templates/>
		</text:reference-mark-end>
    </xsl:template>

    <xsl:template match="text:sequence-decls">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="text:sequence-decl">
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="*">
        <xsl:element name="{name()}">
            <xsl:for-each select="@*">
            	<xsl:if test="not(.='')">
	                <xsl:attribute name="{name(.)}">
	                    <xsl:value-of select="."/>
	                </xsl:attribute>
				</xsl:if>
            </xsl:for-each>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
     
	<xsl:template match="*[@text:style-name or @text:outline-level]">
        <xsl:element name="{name()}">
            <xsl:for-each select="@*[not(name(.)='text:style-name') and not(name(.)='text:outline-level')]">
            	<xsl:if test="not(.='')">
	                <xsl:attribute name="{name(.)}">
	                    <xsl:value-of select="."/>
	                </xsl:attribute>
				</xsl:if>
            </xsl:for-each>
			<xsl:attribute name="class" select="@text:style-name" />
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
 	  
    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>

</xsl:stylesheet>
