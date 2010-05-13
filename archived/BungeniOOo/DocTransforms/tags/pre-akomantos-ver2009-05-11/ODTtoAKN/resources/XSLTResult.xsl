<?xml version="1.0" encoding="UTF-8"?><xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:akn="http://www.akomantoso.org/1.0" exclude-result-prefixes="akn" version="2.0">
    <xsl:output doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" indent="yes" method="xhtml"/>

    <xsl:template match="/">
        
    <xsl:apply-templates/></xsl:template>

    <xsl:template match="akn:*">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="text()">
       <xsl:value-of select="normalize-space(.)"/>
    </xsl:template> 

	<xsl:template match="akn:akomantoso">
		<div>
            <xsl:attribute name="class">main_container akomantoso</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:act">
		<div>
            <xsl:attribute name="class">act_container act</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:bill">
		<div>
            <xsl:attribute name="class">bill_container bill</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:doc">
		<div>
            <xsl:attribute name="class">doc_container doc</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:report">
		<div>
            <xsl:attribute name="class">report_container report</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:debaterecord">
		<div>
            <xsl:attribute name="class">debaterecord_container debaterecord</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:judgment">
		<div>
            <xsl:attribute name="class">judgment_container judgment</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:preface">
		<div>
            <xsl:attribute name="class">preface_container preface</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:preamble">
		<div>
            <xsl:attribute name="class">preamble_container preamble</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:conclusions">
		<div>
            <xsl:attribute name="class">conclusion_container conclusions</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:header">
		<div>
            <xsl:attribute name="class">header_container header</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:attachments">
		<div>
            <xsl:attribute name="class">attachments_container attachments</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:attachment">
		<a>
            <xsl:attribute name="class">attachment attachment</xsl:attribute>
			<xsl:if test="@href">
				<xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </a>
		
	</xsl:template>

	<xsl:template match="akn:body">
		<div>
            <xsl:attribute name="class">body_container body</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:debate">
		<div>
            <xsl:attribute name="class">debate_container debate</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:maincontent">
		<div>
            <xsl:attribute name="class">maincontent_container maincontent</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:judgmentBody">
		<div>
            <xsl:attribute name="class">judgmentBody_container judgmentBody</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:section">
		<div>
            <xsl:attribute name="class">hierarchy section</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:part">
		<div>
            <xsl:attribute name="class">hierarchy part</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:paragraph">
		<div>
            <xsl:attribute name="class">hierarchy paragraph</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:chapter">
		<div>
            <xsl:attribute name="class">hierarchy chapter</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:title">
		<div>
            <xsl:attribute name="class">hierarchy title</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:book">
		<div>
            <xsl:attribute name="class">hierarchy book</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:tome">
		<div>
            <xsl:attribute name="class">hierarchy tome</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:article">
		<div>
            <xsl:attribute name="class">hierarchy article</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:clause">
		<div>
            <xsl:attribute name="class">hierarchy clause</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subsection">
		<div>
            <xsl:attribute name="class">hierarchy subsection</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subpart">
		<div>
            <xsl:attribute name="class">hierarchy subpart</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subparagraph">
		<div>
            <xsl:attribute name="class">hierarchy subparagraph</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subchapter">
		<div>
            <xsl:attribute name="class">hierarchy subchapter</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subtitle">
		<div>
            <xsl:attribute name="class">hierarchy subtitle</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subclause">
		<div>
            <xsl:attribute name="class">hierarchy subclause</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:content">
		<div>
            <xsl:attribute name="class">heirarchy_content</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:num">
		<p>
            <xsl:attribute name="class">hierarchy_num num</xsl:attribute>
 
            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:heading">
		<p>
            <xsl:attribute name="class">hierarchy_heading heading</xsl:attribute>
 
            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:subheading">
		<p>
            <xsl:attribute name="class">hierarchy_subheading subheading</xsl:attribute>
 
            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:sidenote">
		<p>
            <xsl:attribute name="class">hierarchy_sidenote sidenote</xsl:attribute>
 
            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:from">
		<span>
            <xsl:attribute name="class">speec_from from</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:AdministrationOfOath">
		<div>
            <xsl:attribute name="class">speech_hierarchy AdministrationOfOath</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:DeclarationOfVote">
		<div>
            <xsl:attribute name="class">speech_hierarchy DeclarationOfVote</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:Communication">
		<div>
            <xsl:attribute name="class">speech_hierarchy Communication</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:Petitions">
		<div>
            <xsl:attribute name="class">speech_hierarchy Petitions</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:Papers">
		<div>
            <xsl:attribute name="class">speech_hierarchy Papers</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:NoticesOfMotion">
		<div>
            <xsl:attribute name="class">speech_hierarchy NoticesOfMotion</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:Questions">
		<div>
            <xsl:attribute name="class">speech_hierarchy Questions</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:Address">
		<div>
            <xsl:attribute name="class">speech_hierarchy Address</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:ProceduralMotions">
		<div>
            <xsl:attribute name="class">speech_hierarchy ProceduralMotions</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:PointOfOrder">
		<div>
            <xsl:attribute name="class">speech_hierarchy PointOfOrder</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subdivision">
		<div>
            <xsl:attribute name="class">speech_hierarchy subdivision</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:speech">
		<div>
            <xsl:attribute name="class">speech speech</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:question">
		<div>
            <xsl:attribute name="class">speech question</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:answer">
		<div>
            <xsl:attribute name="class">speech answer</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:other">
		<div>
            <xsl:attribute name="class">speech other</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:comment">
		<div>
            <xsl:attribute name="class">speech comment</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:list">
		<ol>
            <xsl:attribute name="class">hierarchy list</xsl:attribute>
 
            <xsl:apply-templates/>
        </ol>
		
	</xsl:template>

	<xsl:template match="akn:introduction">
		<div>
            <xsl:attribute name="class">judgment_part introduction</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:background">
		<div>
            <xsl:attribute name="class">judgment_part background</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:motivation">
		<div>
            <xsl:attribute name="class">judgment_part motivation</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:decision">
		<div>
            <xsl:attribute name="class">judgment_part decision</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:tblock">
		<div>
            <xsl:attribute name="class">generic_block tblock</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:item">
		<li>
            <xsl:attribute name="class">hierarchy item</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </li>
		
	</xsl:template>

	<xsl:template match="akn:toc">
		<div>
            <xsl:attribute name="class">toc</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:tocitem">
		<p>
            <xsl:attribute name="class">tocitem</xsl:attribute>
			<xsl:if test="@href">
				<xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:ActType">
		<span>
            <xsl:attribute name="class">inline_meta ActType</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:ActTitle">
		<span>
            <xsl:attribute name="class">inline_meta ActTitle</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:ActNumber">
		<span>
            <xsl:attribute name="class">inline_meta ActNumber</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:ActProponent">
		<span>
            <xsl:attribute name="class">inline_meta ActProponent</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:ActDate">
		<span>
            <xsl:attribute name="class">inline_meta ActDate</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:ActPurpose">
		<span>
            <xsl:attribute name="class">inline_meta ActPurpose</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:judgmentType">
		<span>
            <xsl:attribute name="class">inline_meta judgmentType</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:judgmentTitle">
		<span>
            <xsl:attribute name="class">inline_meta judgmentTitle</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:judgmentNumber">
		<span>
            <xsl:attribute name="class">inline_meta judgmentNumber</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:courtType">
		<span>
            <xsl:attribute name="class">inline_meta courtType</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:neutralCitation">
		<span>
            <xsl:attribute name="class">inline_meta neutralCitation</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:party">
		<span>
            <xsl:attribute name="class">inline_meta party</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:judge">
		<span>
            <xsl:attribute name="class">inline_meta judge</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:judgmentDate">
		<span>
            <xsl:attribute name="class">inline_meta judgmentDate</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:mref">
		<div>
            <xsl:attribute name="class">reference_container mref</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:ref">
		<a>
            <xsl:attribute name="class">ref</xsl:attribute>
			<xsl:if test="@href">
				<xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </a>
		
	</xsl:template>

	<xsl:template match="akn:rref">
		<div>
            <xsl:attribute name="class">reference_container rref</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:mod">
		<div>
            <xsl:attribute name="class">modification</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:mmod">
		<div>
            <xsl:attribute name="class">modification_container mmod</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:rmod">
		<div>
            <xsl:attribute name="class">modification_container rmod</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:quotedText">
		<span>
            <xsl:attribute name="class">quoted quotedText</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:quotedStructure">
		<div>
            <xsl:attribute name="class">quoted quotedStructure</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:def">
		<span>
            <xsl:attribute name="class">def</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:ins">
		<span>
            <xsl:attribute name="class">ins</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:del">
		<span>
            <xsl:attribute name="class">del</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:omissis">
		<span>
            <xsl:attribute name="class">omissis</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:noteref">
		<a>
            <xsl:attribute name="class">ref noteref</xsl:attribute>
			<xsl:if test="@href">
				<xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </a>
		
	</xsl:template>

	<xsl:template match="akn:recordedTime">
		<span>
            <xsl:attribute name="class">recorderedTime</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:eol">
		<br>
            <xsl:attribute name="class">eol</xsl:attribute>
 
            <xsl:apply-templates/>
        </br>
		
	</xsl:template>

	<xsl:template match="akn:eop">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:hcontainer">
		<div>
            <xsl:attribute name="class">generic_hierarchy hcontainer</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:container">
		<div>
            <xsl:attribute name="class">generic_container container</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:block">
		<div>
            <xsl:attribute name="class">generic_block block</xsl:attribute>
			<xsl:if test="@name">
				<xsl:attribute name="name"><xsl:value-of select="@name"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:inline">
		<span>
            <xsl:attribute name="class">generic_inline inline </xsl:attribute>
			<xsl:if test="@name">
				<xsl:attribute name="name"><xsl:value-of select="@name"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:marker">
		<span>
            <xsl:attribute name="class">generic_marker marker</xsl:attribute>
			<xsl:if test="@name">
				<xsl:attribute name="name"><xsl:value-of select="@name"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:foreign">
		<div>
            <xsl:attribute name="class">foreign_elements foreign</xsl:attribute>
			<xsl:if test="@name">
				<xsl:attribute name="name"><xsl:value-of select="@name"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:div">
		<div>
            <xsl:attribute name="class">html_container div</xsl:attribute>
			<xsl:if test="@id">
				<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:p">
		<p>
            <xsl:attribute name="class">html_paragraph p</xsl:attribute>
 
            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:li">
		<li>
            <xsl:attribute name="class">html_list_item li</xsl:attribute>
 
            <xsl:apply-templates/>
        </li>
		
	</xsl:template>

	<xsl:template match="akn:span">
		<span>
            <xsl:attribute name="class">html_inline span</xsl:attribute>
			<xsl:if test="@name">
				<xsl:attribute name="name"><xsl:value-of select="@name"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:b">
		<b>
            <xsl:attribute name="class">html_bold b</xsl:attribute>
 
            <xsl:apply-templates/>
        </b>
		
	</xsl:template>

	<xsl:template match="akn:i">
		<i>
            <xsl:attribute name="class">html_italic i</xsl:attribute>
 
            <xsl:apply-templates/>
        </i>
		
	</xsl:template>

	<xsl:template match="akn:a">
		<a>
            <xsl:attribute name="class">html_anchor a</xsl:attribute>
			<xsl:if test="@href">
				<xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </a>
		
	</xsl:template>

	<xsl:template match="akn:img">
		<img>
            <xsl:attribute name="class">html_img img</xsl:attribute>
			<xsl:if test="@href">
				<xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </img>
		
	</xsl:template>

	<xsl:template match="akn:ul">
		<ul>
            <xsl:attribute name="class">html_unordered_list ul</xsl:attribute>
 
            <xsl:apply-templates/>
        </ul>
		
	</xsl:template>

	<xsl:template match="akn:ol">
		<ol>
            <xsl:attribute name="class">html_ordered_list ol</xsl:attribute>
 
            <xsl:apply-templates/>
        </ol>
		
	</xsl:template>

	<xsl:template match="akn:table">
		<table>
            <xsl:attribute name="class">html_table table</xsl:attribute>
			<xsl:if test="@border">
				<xsl:attribute name="border"><xsl:value-of select="@border"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="@cellspacing">
				<xsl:attribute name="cellspacing"><xsl:value-of select="@cellspacing"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="@cellpadding">
				<xsl:attribute name="cellpadding"><xsl:value-of select="@cellpadding"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </table>
		
	</xsl:template>

	<xsl:template match="akn:tr">
		<tr>
            <xsl:attribute name="class">html_table_row tr</xsl:attribute>
 
            <xsl:apply-templates/>
        </tr>
		
	</xsl:template>

	<xsl:template match="akn:th">
		<th>
            <xsl:attribute name="class">html_table_heading_column th</xsl:attribute>
			<xsl:if test="@colspan">
				<xsl:attribute name="colspan"><xsl:value-of select="@colspan"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="@rowspan">
				<xsl:attribute name="rowspan"><xsl:value-of select="@rowspan"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </th>
		
	</xsl:template>

	<xsl:template match="akn:td">
		<td>
            <xsl:attribute name="class">html_table_column td</xsl:attribute>
			<xsl:if test="@colspan">
				<xsl:attribute name="colspan"><xsl:value-of select="@colspan"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="@rowspan">
				<xsl:attribute name="rowspan"><xsl:value-of select="@rowspan"/></xsl:attribute>
			</xsl:if>

            <xsl:apply-templates/>
        </td>
		
	</xsl:template>

	<xsl:template match="akn:meta">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:identification">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:FRBRWork">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:FRBRExpression">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:FRBRManifestation">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:FRBRItem">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:this">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:uri">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:alias">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:date">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:author">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:components">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:component">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:preservation">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:publication">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:classification">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:keyword">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:lifecycle">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:event">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:workflow">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:action">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:analysis">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:ActiveModifications">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:PassiveModifications">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:TextualMod">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:MeaningMod">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:ScopeMod">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:ForceMod">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:EfficacyMod">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:Legal">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:source">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:destination">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:force">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:efficacy">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:application">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:duration">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:condition">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:old">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:new">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:domain">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:references">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:Original">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:PassiveRef">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:ActiveRef">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:Jurisprudence">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:HasAttachment">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:AttachmentOf">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:TLCPerson">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:TLCOrganization">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:TLCConcept">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:TLCObject">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:TLCEvent">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:TLCPlace">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:TLCProcess">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:TLCRole">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:TLCTerm">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:TLCReference">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:notes">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:note">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:proprietary">
		<xsl:apply-templates/>
		
	</xsl:template>


</xsl:stylesheet>