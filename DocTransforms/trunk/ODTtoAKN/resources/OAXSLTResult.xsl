<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
    <xsl:output indent="yes" method="xml"/>

    <xsl:template match="/">
        
    <xsl:apply-templates/></xsl:template>

    <xsl:template match="*">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="text()">
       <xsl:value-of select="normalize-space(.)"/>
    </xsl:template> 

	<xsl:template match="*[@name='debaterecord']">
		<debateRecord>
 
            <xsl:apply-templates/>
        </debateRecord>
		
	</xsl:template>

	<xsl:template match="*[@name='MastHead']">
		<preface>
 
            <xsl:apply-templates/>
        </preface>
		
	</xsl:template>

	<xsl:template match="*[@name='Observation']">
		<scene>
 
            <xsl:apply-templates/>
        </scene>
		
	</xsl:template>

	<xsl:template match="*[@name='GroupActivity']">
		<subdivision>
 
            <xsl:apply-templates/>
        </subdivision>
		
	</xsl:template>

	<xsl:template match="*[@name='Speech']">
		<speech>
 
            <xsl:apply-templates/>
        </speech>
		
	</xsl:template>

	<xsl:template match="*[@name='QuestionsContainer']">
		<subdivision>
 
            <xsl:apply-templates/>
        </subdivision>
		
	</xsl:template>

	<xsl:template match="*[@name='QuestionAnswer']">
		<questions>
 
            <xsl:apply-templates/>
        </questions>
		
	</xsl:template>

	<xsl:template match="*[@name='Question']">
		<question>
 
            <xsl:apply-templates/>
        </question>
		
	</xsl:template>

	<xsl:template match="*[@name='PointOfOrder']">
		<pointOfOrder>
 
            <xsl:apply-templates/>
        </pointOfOrder>
		
	</xsl:template>

	<xsl:template match="*[@name='ProceduralMotion']">
		<proceduralMotions>
 
            <xsl:apply-templates/>
        </proceduralMotions>
		
	</xsl:template>

	<xsl:template match="*[@name='Person']">
		<from>
 
            <xsl:apply-templates/>
        </from>
		
	</xsl:template>

	<xsl:template match="*[@name='ActionEvent']">
		<actionEvent>
 
            <xsl:apply-templates/>
        </actionEvent>
		
	</xsl:template>

	<xsl:template match="*[@name='Communication']">
		<communication>
 
            <xsl:apply-templates/>
        </communication>
		
	</xsl:template>

	<xsl:template match="*[@name='Conclusion']">
		<conclusions>
 
            <xsl:apply-templates/>
        </conclusions>
		
	</xsl:template>

	<xsl:template match="*[@name='span']">
		<span>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="*[@name='p']">
		<p>
 
            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="*[@name='ref']">
		<ref>
			<xsl:if test="@href">
				<xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </ref>
		
	</xsl:template>

	<xsl:template match="*[@name='heading']">
		<heading>
 
            <xsl:apply-templates/>
        </heading>
		
	</xsl:template>

	<xsl:template match="*[@name='subheading']">
		<subheading>
 
            <xsl:apply-templates/>
        </subheading>
		
	</xsl:template>


</xsl:stylesheet>