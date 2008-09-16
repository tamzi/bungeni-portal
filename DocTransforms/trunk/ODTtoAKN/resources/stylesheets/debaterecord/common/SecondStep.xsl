<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                xmlns="http://www.akomantoso.org/"
                xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
                version="1.0">
    <xsl:output indent="yes" method="xml"/>
    
    <xsl:template match="/">
       <xsl:apply-templates />
    </xsl:template>
    
    <xsl:template match="text:p" >
         <p>
             <xsl:apply-templates />
         </p>
    </xsl:template>
    
    <xsl:template match="*">
        <xsl:element name="{name()}">
            <xsl:for-each select="@*">
                <xsl:attribute name="{name(.)}">
                    <xsl:value-of select="."/>
                </xsl:attribute>
            </xsl:for-each>
            <xsl:apply-templates />
        </xsl:element>        
    </xsl:template>
    
    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>
</xsl:stylesheet>
