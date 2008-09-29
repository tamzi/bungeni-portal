<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.akomantoso.org/"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
    xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
    xmlns:math="http://www.w3.org/1998/Math/MathML"
    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
    xmlns:ooo="http://openoffice.org/2004/office" 
    xmlns:ooow="http://openoffice.org/2004/writer"
    xmlns:oooc="http://openoffice.org/2004/calc" 
    xmlns:dom="http://www.w3.org/2001/xml-events"
    xmlns:xforms="http://www.w3.org/2002/xforms"
    exclude-result-prefixes="xsl xsd xsi text office style table draw fo xlink dc meta number svg chart dr3d math form script ooo ooow oooc dom xforms"
    version="1.0">
    <xsl:output indent="yes" method="xml" />
    <xsl:param name="type" />
    <xsl:param name="name" />
	<xsl:param name="owner" />
	<xsl:param name="bungeniSectionType" />
    <xsl:param name="result" />
    <xsl:param name="attributes" />
    <xsl:template match="/">
		<xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="*">
        <xsl:choose>
            <xsl:when test="name(.) = $type and (@text:name=$name or @BungeniSectionType=$bungeniSectionType)">
               <xsl:variable name="currentElement" select="." />
               <xsl:element name="{$result}">
                   <xsl:for-each select="tokenize($attributes,',')">
               	   		<xsl:variable name="oldname" select="substring-before(.,'=')" />
						<xsl:variable name="newname" select="substring-before(substring-after(.,'='),';')" />
						<xsl:variable name="value" select="substring-after(substring-after(.,'='),';')" />
						<xsl:choose>
							<xsl:when test="$newname!='null'">
								<xsl:if test="not($currentElement/@*[name(.)=$value]='')">
									<xsl:attribute name="{$newname}">
										<xsl:value-of select="$currentElement/@*[name(.)=$value]" />
									</xsl:attribute>
								</xsl:if>
							</xsl:when>
						</xsl:choose>
				   </xsl:for-each>
                   <xsl:apply-templates/>
               </xsl:element> 
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="{name(.)}">
                    <xsl:for-each select="@*">
                        <xsl:attribute name="{name(.)}">
                            <xsl:value-of select="."/>
                        </xsl:attribute>
                    </xsl:for-each>
                    <xsl:apply-templates/>
                </xsl:element> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
	    
    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>
</xsl:stylesheet>