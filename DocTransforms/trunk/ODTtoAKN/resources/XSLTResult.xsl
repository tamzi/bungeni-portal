<?xml version="1.0" encoding="UTF-8"?><xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:akn="http://www.akomantoso.org/1.0" version="2.0">
    <xsl:output indent="yes" method="xml"/>

    <xsl:template match="/">
        <html><head/><body><xsl:apply-templates/></body></html>
    </xsl:template>

    <xsl:template match="akn:*">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="text()">
       <xsl:value-of select="normalize-space(.)"/>
    </xsl:template> 

	<xsl:template match="akn:akomantoso">
		<div>
            <xsl:attribute name="class">main_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:act">
		<div>
            <xsl:attribute name="class">act_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:bill">
		<div>
            <xsl:attribute name="class">bill_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:doc">
		<div>
            <xsl:attribute name="class">doc_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:report">
		<div>
            <xsl:attribute name="class">report_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:debaterecord">
		<div>
            <xsl:attribute name="class">debaterecord_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:judgment">
		<div>
            <xsl:attribute name="class">judgment_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:preface">
		<div>
            <xsl:attribute name="class">preface_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:preamble">
		<div>
            <xsl:attribute name="class">preamble_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:conclusions">
		<div>
            <xsl:attribute name="class">conclusion_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:header">
		<div>
            <xsl:attribute name="class">header_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:attachments">
		<div>
            <xsl:attribute name="class">attachments_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:attachment">
		<a>
            <xsl:attribute name="class">attachment</xsl:attribute>
			<xsl:attribute name="href" select="@href"/>

            <xsl:apply-templates/>
        </a>
		
	</xsl:template>

	<xsl:template match="akn:body">
		<div>
            <xsl:attribute name="class">body_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:debate">
		<div>
            <xsl:attribute name="class">debate_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:maincontent">
		<div>
            <xsl:attribute name="class">maincontent_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:judgmentBody">
		<div>
            <xsl:attribute name="class">judgmentBody_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:section">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:part">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:paragraph">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:chapter">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:title">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:book">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:tome">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:article">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:clause">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subsection">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subpart">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subparagraph">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subchapter">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subtitle">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subclause">
		<div>
            <xsl:attribute name="class">hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

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
            <xsl:attribute name="class">hierarchy_num</xsl:attribute>
 
            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:heading">
		<p>
            <xsl:attribute name="class">hierarchy_heading</xsl:attribute>
 
            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:subheading">
		<p>
            <xsl:attribute name="class">hierarchy_subheading</xsl:attribute>
 
            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:sidenote">
		<p>
            <xsl:attribute name="class">hierarchy_sidenote</xsl:attribute>
 
            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:from">
		<span>
            <xsl:attribute name="class">speec_from</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:AdministrationOfOath">
		<div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:DeclarationOfVote">
		<div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:Communication">
		<div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:Petitions">
		<div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:Papers">
		<div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:NoticesOfMotion">
		<div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:Questions">
		<div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:Address">
		<div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:ProceduralMotions">
		<div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:PointOfOrder">
		<div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:subdivision">
		<div>
            <xsl:attribute name="class">speech_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:speech">
		<div>
            <xsl:attribute name="class">speech_speech</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:question">
		<div>
            <xsl:attribute name="class">speech_question</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:answer">
		<div>
            <xsl:attribute name="class">speech_answer</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:other">
		<div>
            <xsl:attribute name="class">speech_other</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:comment">
		<div>
            <xsl:attribute name="class">speech_comment</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:list">
		<ol>
            <xsl:attribute name="class">akomantoso_list</xsl:attribute>
 
            <xsl:apply-templates/>
        </ol>
		
	</xsl:template>

	<xsl:template match="akn:introduction">
		<div>
            <xsl:attribute name="class">introduction</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:background">
		<div>
            <xsl:attribute name="class">background</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:motivation">
		<div>
            <xsl:attribute name="class">motivation</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:decision">
		<div>
            <xsl:attribute name="class">decision</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:tblock">
		<div>
            <xsl:attribute name="class">title_block</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:item">
		<li>
            <xsl:attribute name="class">akomantoso_list_item</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

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
            <xsl:attribute name="class">toc_item</xsl:attribute>
			<xsl:attribute name="href" select="@href"/>

            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:ActType">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:ActTitle">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:ActNumber">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:ActProponent">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:ActDate">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:ActPurpose">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:judgmentType">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:judgmentTitle">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:judgmentNumber">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:courtType">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:neutralCitation">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:party">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:judge">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:judgmentDate">
		<span>
            <xsl:attribute name="class">inline_meta</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:mref">
		<div>
            <xsl:attribute name="class">multipe_references_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:ref">
		<a>
            <xsl:attribute name="class">reference</xsl:attribute>
			<xsl:attribute name="href" select="@href"/>

            <xsl:apply-templates/>
        </a>
		
	</xsl:template>

	<xsl:template match="akn:rref">
		<div>
            <xsl:attribute name="class">range_references_container</xsl:attribute>
 
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
            <xsl:attribute name="class">multiple_modifications_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:rmod">
		<div>
            <xsl:attribute name="class">range_modifications_container</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:quotedText">
		<span>
            <xsl:attribute name="class">quoted_text</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:quotedStructure">
		<div>
            <xsl:attribute name="class">quoted_structure</xsl:attribute>
 
            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:def">
		<span>
            <xsl:attribute name="class">definition</xsl:attribute>
 
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
		<span>
            <xsl:attribute name="class">noteref</xsl:attribute>
			<xsl:attribute name="href" select="@href"/>

            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:recordedTime">
		<span>
            <xsl:attribute name="class">time</xsl:attribute>
 
            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:eol">
		<br>
            <xsl:attribute name="class">end_of_line</xsl:attribute>
 
            <xsl:apply-templates/>
        </br>
		
	</xsl:template>

	<xsl:template match="akn:eop">
		<xsl:apply-templates/>
		
	</xsl:template>

	<xsl:template match="akn:hcontainer">
		<div>
            <xsl:attribute name="class">generic_hierarchy</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:container">
		<div>
            <xsl:attribute name="class">generic_container</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:block">
		<div>
            <xsl:attribute name="class">generic_block</xsl:attribute>
			<xsl:attribute name="name" select="@name"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:inline">
		<span>
            <xsl:attribute name="class">generic_inline</xsl:attribute>
			<xsl:attribute name="name" select="@name"/>

            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:marker">
		<span>
            <xsl:attribute name="class">generic_marker</xsl:attribute>
			<xsl:attribute name="name" select="@name"/>

            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:foreign">
		<div>
            <xsl:attribute name="class">foreign_elements</xsl:attribute>
			<xsl:attribute name="name" select="@name"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:div">
		<div>
            <xsl:attribute name="class">html_container</xsl:attribute>
			<xsl:attribute name="id" select="@id"/>

            <xsl:apply-templates/>
        </div>
		
	</xsl:template>

	<xsl:template match="akn:p">
		<p>
            <xsl:attribute name="class">html_paragraph</xsl:attribute>
 
            <xsl:apply-templates/>
        </p>
		
	</xsl:template>

	<xsl:template match="akn:li">
		<li>
            <xsl:attribute name="class">html_list_item</xsl:attribute>
 
            <xsl:apply-templates/>
        </li>
		
	</xsl:template>

	<xsl:template match="akn:span">
		<span>
            <xsl:attribute name="class">html_inline</xsl:attribute>
			<xsl:attribute name="name" select="@name"/>

            <xsl:apply-templates/>
        </span>
		
	</xsl:template>

	<xsl:template match="akn:b">
		<b>
            <xsl:attribute name="class">html_bold</xsl:attribute>
 
            <xsl:apply-templates/>
        </b>
		
	</xsl:template>

	<xsl:template match="akn:i">
		<i>
            <xsl:attribute name="class">html_italic</xsl:attribute>
 
            <xsl:apply-templates/>
        </i>
		
	</xsl:template>

	<xsl:template match="akn:a">
		<a>
            <xsl:attribute name="class">html_anchor</xsl:attribute>
			<xsl:attribute name="href" select="@href"/>

            <xsl:apply-templates/>
        </a>
		
	</xsl:template>

	<xsl:template match="akn:img">
		<img>
            <xsl:attribute name="class">html_img</xsl:attribute>
			<xsl:attribute name="href" select="@href"/>

            <xsl:apply-templates/>
        </img>
		
	</xsl:template>

	<xsl:template match="akn:ul">
		<ul>
            <xsl:attribute name="class">html_unordered_list</xsl:attribute>
 
            <xsl:apply-templates/>
        </ul>
		
	</xsl:template>

	<xsl:template match="akn:ol">
		<ol>
            <xsl:attribute name="class">html_ordered_list</xsl:attribute>
 
            <xsl:apply-templates/>
        </ol>
		
	</xsl:template>

	<xsl:template match="akn:table">
		<table>
            <xsl:attribute name="class">html_table</xsl:attribute>
			<xsl:attribute name="border" select="@border"/>
			<xsl:attribute name="cellspacing" select="@cellspacing"/>
			<xsl:attribute name="cellpadding" select="@cellpadding"/>

            <xsl:apply-templates/>
        </table>
		
	</xsl:template>

	<xsl:template match="akn:tr">
		<tr>
            <xsl:attribute name="class">html_table_row</xsl:attribute>
 
            <xsl:apply-templates/>
        </tr>
		
	</xsl:template>

	<xsl:template match="akn:th">
		<th>
            <xsl:attribute name="class">html_table_heading_column</xsl:attribute>
			<xsl:attribute name="colspan" select="@colspan"/>
			<xsl:attribute name="rowspan" select="@rowspan"/>

            <xsl:apply-templates/>
        </th>
		
	</xsl:template>

	<xsl:template match="akn:td">
		<td>
            <xsl:attribute name="class">html_table_column</xsl:attribute>
			<xsl:attribute name="colspan" select="@colspan"/>
			<xsl:attribute name="rowspan" select="@rowspan"/>

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