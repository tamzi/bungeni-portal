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
		<xslt step="0" name="root" href="resources/odttoakn/minixslt/debaterecord/back/root.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='body']">
		<xslt step="1" name="body" href="resources/odttoakn/minixslt/debaterecord/back/body.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='MastHead']">
		<xslt step="2" name="MastHead" href="resources/odttoakn/minixslt/debaterecord/back/MastHead.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Observation']">
		<xslt step="3" name="Observation" href="resources/odttoakn/minixslt/debaterecord/back/Observation.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='TabledDocuments']">
		<xslt step="4" name="TabledDocuments" href="resources/odttoakn/minixslt/debaterecord/back/TabledDocuments.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='TabledDocumentsList']">
		<xslt step="5" name="TabledDocumentsList" href="resources/odttoakn/minixslt/debaterecord/back/TabledDocumentsList.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='GroupActivity']">
		<xslt step="6" name="GroupActivity" href="resources/odttoakn/minixslt/debaterecord/back/GroupActivity.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Speech']">
		<xslt step="7" name="Speech" href="resources/odttoakn/minixslt/debaterecord/back/Speech.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='QuestionsContainer']">
		<xslt step="8" name="QuestionsContainer" href="resources/odttoakn/minixslt/debaterecord/back/QuestionsContainer.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='QuestionAnswer']">
		<xslt step="9" name="QuestionAnswer" href="resources/odttoakn/minixslt/debaterecord/back/QuestionAnswer.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Question']">
		<xslt step="10" name="Question" href="resources/odttoakn/minixslt/debaterecord/back/Question.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='PointOfOrder']">
		<xslt step="11" name="PointOfOrder" href="resources/odttoakn/minixslt/debaterecord/back/PointOfOrder.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='ProceduralMotion']">
		<xslt step="12" name="ProceduralMotion" href="resources/odttoakn/minixslt/debaterecord/back/ProceduralMotion.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='MotionsContainer']">
		<xslt step="13" name="MotionsContainer" href="resources/odttoakn/minixslt/debaterecord/back/MotionsContainer.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Motion']">
		<xslt step="14" name="Motion" href="resources/odttoakn/minixslt/debaterecord/back/Motion.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Person']">
		<xslt step="15" name="Person" href="resources/odttoakn/minixslt/debaterecord/back/Person.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='ActionEvent']">
		<xslt step="16" name="ActionEvent" href="resources/odttoakn/minixslt/debaterecord/back/ActionEvent.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Communication']">
		<xslt step="17" name="Communication" href="resources/odttoakn/minixslt/debaterecord/back/Communication.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Conclusion']">
		<xslt step="18" name="Conclusion" href="resources/odttoakn/minixslt/debaterecord/back/Conclusion.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='span']">
		<xslt step="19" name="span" href="resources/odttoakn/minixslt/debaterecord/back/span.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='p']">
		<xslt step="20" name="p" href="resources/odttoakn/minixslt/debaterecord/back/p.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='ref']">
		<xslt step="21" name="ref" href="resources/odttoakn/minixslt/debaterecord/back/ref.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='heading']">
		<xslt step="22" name="heading" href="resources/odttoakn/minixslt/debaterecord/back/heading.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='subheading']">
		<xslt step="23" name="subheading" href="resources/odttoakn/minixslt/debaterecord/back/subheading.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='list']">
		<xslt step="24" name="list" href="resources/odttoakn/minixslt/debaterecord/back/list.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='item']">
		<xslt step="25" name="item" href="resources/odttoakn/minixslt/debaterecord/back/item.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='a']">
		<xslt step="26" name="a" href="resources/odttoakn/minixslt/debaterecord/back/a.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='meta']">
		<xslt step="27" name="meta" href="resources/odttoakn/minixslt/debaterecord/back/meta.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='identification']">
		<xslt step="28" name="identification" href="resources/odttoakn/minixslt/debaterecord/back/identification.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='FRBRWork']">
		<xslt step="29" name="FRBRWork" href="resources/odttoakn/minixslt/debaterecord/back/FRBRWork.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='FRBRExpression']">
		<xslt step="30" name="FRBRExpression" href="resources/odttoakn/minixslt/debaterecord/back/FRBRExpression.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='FRBRManifestation']">
		<xslt step="31" name="FRBRManifestation" href="resources/odttoakn/minixslt/debaterecord/back/FRBRManifestation.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='this']">
		<xslt step="32" name="this" href="resources/odttoakn/minixslt/debaterecord/back/this.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='uri']">
		<xslt step="33" name="uri" href="resources/odttoakn/minixslt/debaterecord/back/uri.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='date']">
		<xslt step="34" name="date" href="resources/odttoakn/minixslt/debaterecord/back/date.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='author']">
		<xslt step="35" name="author" href="resources/odttoakn/minixslt/debaterecord/back/author.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='publication_mcontainer']">
		<xslt step="36" name="publication_mcontainer" href="resources/odttoakn/minixslt/debaterecord/back/publication_mcontainer.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='publication']">
		<xslt step="37" name="publication" href="resources/odttoakn/minixslt/debaterecord/back/publication.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='references']">
		<xslt step="38" name="references" href="resources/odttoakn/minixslt/debaterecord/back/references.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='TLCOrganization']">
		<xslt step="39" name="TLCOrganization" href="resources/odttoakn/minixslt/debaterecord/back/TLCOrganization.xsl" />
		<xsl:apply-templates />
	</xsl:template>


</xsl:stylesheet>