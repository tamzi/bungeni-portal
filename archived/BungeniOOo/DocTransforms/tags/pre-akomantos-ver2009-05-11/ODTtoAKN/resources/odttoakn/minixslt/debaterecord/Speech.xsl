<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version="2.0">
    <xsl:output indent="yes" method="xml" encoding="UTF-8"/>

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
            <xsl:apply-templates />
        </xsl:element>
    </xsl:template>

    <xsl:template match="*[@name='Speech']">
        <speech>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id" /></xsl:attribute>
			</xsl:if>
            <xsl:if test="@BungeniSpeechBy">
				<xsl:attribute name="by"><xsl:value-of select="@BungeniPersonID" /></xsl:attribute>
			</xsl:if>
            <xsl:if test="@BungeniSpeechTo">
				<xsl:attribute name="to"><xsl:value-of select="@BungeniSpeechTo" /></xsl:attribute>
			</xsl:if>
        <!--    <xsl:if test="@BungeniPersonRole">
				<xsl:attribute name="as"><xsl:value-of select="@BungeniPersonRole" /></xsl:attribute>
			</xsl:if> -->
            <from>
                <xsl:apply-templates select="*[position()=1]/*" />
            </from>
            <xsl:apply-templates select="*[not(position()=1)]" /> 
        </speech>
    </xsl:template>
    
    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template> 

</xsl:stylesheet>
