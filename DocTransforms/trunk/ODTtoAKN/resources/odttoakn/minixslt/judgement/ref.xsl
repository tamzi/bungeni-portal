<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
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
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="*[@name='ref']">
		<xsl:if test="@href">
			<xsl:if test="@class">
				<xsl:choose>
					<!--check if caseNumber attribute exists then generate a 'from' -->
					<xsl:when test="@class='mBungeniCaseNo'">
						<caseNumber>
							<xsl:value-of select="."/>
						</caseNumber>
					</xsl:when>
					<!-- the party element -->
					<xsl:when test="@class='BungeniPartyName'">
						<party>
						<!-- we use the tokenize() function to extract the refersTo attrib 
						from the reference href the id is a generated one -->
						<xsl:variable name="strHref"><xsl:value-of select="@href" /></xsl:variable>
						<xsl:variable name="tokenizedHref" select="tokenize($strHref,';')"/>
						<xsl:attribute name="refersTo">
						   <xsl:value-of select="$tokenizedHref[1]" />
						</xsl:attribute>
						<xsl:attribute name="id">
						   <xsl:value-of select="generate-id()" />
						</xsl:attribute>
						 <xsl:value-of select="."/>
						</party>
					</xsl:when>						
					<!-- otherwise generate normal reference -->
					<xsl:otherwise>
					     <ref>
					       <xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
					     </ref>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
		</xsl:if>
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="text()">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
</xsl:stylesheet>
