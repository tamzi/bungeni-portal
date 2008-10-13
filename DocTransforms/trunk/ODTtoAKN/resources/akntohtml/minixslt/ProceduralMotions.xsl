<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.akomantoso.org/1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
    <xsl:output indent="yes" method="xml"/>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="*">
        <xsl:element name="{node-name(.)}">
            <xsl:for-each select="@*">
                <xsl:attribute name="{name(.)}">
                    <xsl:value-of select="."/>
                </xsl:attribute>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>

    <xsl:template match="ProceduralMotions">
        <div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
 
            <xsl:apply-templates />
        </div>
    </xsl:template>
    
    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>

</xsl:stylesheet>
