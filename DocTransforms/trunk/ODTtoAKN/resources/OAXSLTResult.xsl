<?xml version="1.0" encoding="UTF-8"?><xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
    <xsl:output indent="yes" method="xml"/>

    <xsl:template match="/">
        
    <xsl:apply-templates/></xsl:template>

    <xsl:template match="*">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="text()">
       <xsl:value-of select="normalize-space(.)"/>
    </xsl:template> 

	<xsl:template match="*[@name='root']">
		<debateRecord>
 
            <xsl:apply-templates/>
        </debateRecord>
		
	</xsl:template>

	<xsl:template match="*[@name='body']">
		<debate>
 
            <xsl:apply-templates/>
        </debate>
		
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

	<xsl:template match="*[@name='TabledDocuments']">
		<papers>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </papers>
		
	</xsl:template>

	<xsl:template match="*[@name='TabledDocumentsList']">
		<other>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </other>
		
	</xsl:template>

	<xsl:template match="*[@name='GroupActivity']">
		<subdivision>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </subdivision>
		
	</xsl:template>

	<xsl:template match="*[@name='Speech']">
		<speech>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </speech>
		
	</xsl:template>

	<xsl:template match="*[@name='QuestionsContainer']">
		<subdivision>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </subdivision>
		
	</xsl:template>

	<xsl:template match="*[@name='QuestionAnswer']">
		<questions>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </questions>
		
	</xsl:template>

	<xsl:template match="*[@name='Question']">
		<question>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </question>
		
	</xsl:template>

	<xsl:template match="*[@name='PointOfOrder']">
		<pointOfOrder>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </pointOfOrder>
		
	</xsl:template>

	<xsl:template match="*[@name='ProceduralMotion']">
		<proceduralMotions>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </proceduralMotions>
		
	</xsl:template>

	<xsl:template match="*[@name='MotionsContainer']">
		<noticesOfMotion>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </noticesOfMotion>
		
	</xsl:template>

	<xsl:template match="*[@name='Motion']">
		<subdivision>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </subdivision>
		
	</xsl:template>

	<xsl:template match="*[@name='Person']">
		<from>
 
            <xsl:apply-templates/>
        </from>
		
	</xsl:template>

	<xsl:template match="*[@name='ActionEvent']">
		<actionEvent>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </actionEvent>
		
	</xsl:template>

	<xsl:template match="*[@name='Communication']">
		<communication>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </communication>
		
	</xsl:template>

	<xsl:template match="*[@name='Conclusion']">
		<conclusions>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

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

	<xsl:template match="*[@name='list']">
		<list>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </list>
		
	</xsl:template>

	<xsl:template match="*[@name='item']">
		<item>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </item>
		
	</xsl:template>


</xsl:stylesheet>