<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version="2.0">
    <xsl:output indent="yes" method="xml"/>

    <xsl:template match="/">
        <stylesheets>
            <xsl:apply-templates/>
        </stylesheets>
    </xsl:template>

    <xsl:template match="*">
        <xsl:apply-templates />
    </xsl:template>

    <xsl:template match="text()">
       <xsl:value-of select="normalize-space(.)" />
    </xsl:template> 

	<xsl:template match="*[@name='root']">
		<xslt step="0" name="root" href="resources/odttoakn/minixslt/bill/root.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='body']">
		<xslt step="1" name="body" href="resources/odttoakn/minixslt/bill/body.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='MastHead']">
		<xslt step="2" name="MastHead" href="resources/odttoakn/minixslt/bill/MastHead.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Preamble']">
		<xslt step="3" name="Preamble" href="resources/odttoakn/minixslt/bill/Preamble.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Part']">
		<xslt step="4" name="Part" href="resources/odttoakn/minixslt/bill/Part.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Chapter']">
		<xslt step="5" name="Chapter" href="resources/odttoakn/minixslt/bill/Chapter.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='SubChapter']">
		<xslt step="6" name="SubChapter" href="resources/odttoakn/minixslt/bill/SubChapter.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Section']">
		<xslt step="7" name="Section" href="resources/odttoakn/minixslt/bill/Section.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Paragraph']">
		<xslt step="8" name="Paragraph" href="resources/odttoakn/minixslt/bill/Paragraph.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Title']">
		<xslt step="9" name="Title" href="resources/odttoakn/minixslt/bill/Title.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Book']">
		<xslt step="10" name="Book" href="resources/odttoakn/minixslt/bill/Book.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Tome']">
		<xslt step="11" name="Tome" href="resources/odttoakn/minixslt/bill/Tome.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Article']">
		<xslt step="12" name="Article" href="resources/odttoakn/minixslt/bill/Article.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Clause']">
		<xslt step="13" name="Clause" href="resources/odttoakn/minixslt/bill/Clause.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='SubSection']">
		<xslt step="14" name="SubSection" href="resources/odttoakn/minixslt/bill/SubSection.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='SubPart']">
		<xslt step="15" name="SubPart" href="resources/odttoakn/minixslt/bill/SubPart.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='SubParagraph']">
		<xslt step="16" name="SubParagraph" href="resources/odttoakn/minixslt/bill/SubParagraph.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='SubTitle']">
		<xslt step="17" name="SubTitle" href="resources/odttoakn/minixslt/bill/SubTitle.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='SubClause']">
		<xslt step="18" name="SubClause" href="resources/odttoakn/minixslt/bill/SubClause.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Conclusion']">
		<xslt step="19" name="Conclusion" href="resources/odttoakn/minixslt/bill/Conclusion.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='span']">
		<xslt step="20" name="span" href="resources/odttoakn/minixslt/bill/span.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='p']">
		<xslt step="21" name="p" href="resources/odttoakn/minixslt/bill/p.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='ref']">
		<xslt step="22" name="ref" href="resources/odttoakn/minixslt/bill/ref.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='heading']">
		<xslt step="23" name="heading" href="resources/odttoakn/minixslt/bill/heading.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='subheading']">
		<xslt step="24" name="subheading" href="resources/odttoakn/minixslt/bill/subheading.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='list']">
		<xslt step="25" name="list" href="resources/odttoakn/minixslt/bill/list.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='item']">
		<xslt step="26" name="item" href="resources/odttoakn/minixslt/bill/item.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='a']">
		<xslt step="27" name="a" href="resources/odttoakn/minixslt/bill/a.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='content']">
		<xslt step="28" name="content" href="resources/odttoakn/minixslt/bill/content.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='meta']">
		<xslt step="29" name="meta" href="resources/odttoakn/minixslt/bill/meta.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='identification']">
		<xslt step="30" name="identification" href="resources/odttoakn/minixslt/bill/identification.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='FRBRWork']">
		<xslt step="31" name="FRBRWork" href="resources/odttoakn/minixslt/bill/FRBRWork.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='FRBRExpression']">
		<xslt step="32" name="FRBRExpression" href="resources/odttoakn/minixslt/bill/FRBRExpression.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='FRBRManifestation']">
		<xslt step="33" name="FRBRManifestation" href="resources/odttoakn/minixslt/bill/FRBRManifestation.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='this']">
		<xslt step="34" name="this" href="resources/odttoakn/minixslt/bill/this.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='uri']">
		<xslt step="35" name="uri" href="resources/odttoakn/minixslt/bill/uri.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='date']">
		<xslt step="36" name="date" href="resources/odttoakn/minixslt/bill/date.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='author']">
		<xslt step="37" name="author" href="resources/odttoakn/minixslt/bill/author.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='publication_mcontainer']">
		<xslt step="38" name="publication_mcontainer" href="resources/odttoakn/minixslt/bill/publication_mcontainer.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='publication']">
		<xslt step="39" name="publication" href="resources/odttoakn/minixslt/bill/publication.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='references']">
		<xslt step="40" name="references" href="resources/odttoakn/minixslt/bill/references.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='TLCOrganization']">
		<xslt step="41" name="TLCOrganization" href="resources/odttoakn/minixslt/bill/TLCOrganization.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='TLCPerson']">
		<xslt step="42" name="TLCPerson" href="resources/odttoakn/minixslt/bill/TLCPerson.xsl" />
		<xsl:apply-templates />
	</xsl:template>


</xsl:stylesheet>