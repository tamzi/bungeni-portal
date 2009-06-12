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
		<xslt step="0" name="root" href="resources/odttoakn/minixslt/debaterecord/root.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='body']">
		<xslt step="1" name="body" href="resources/odttoakn/minixslt/debaterecord/body.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='MastHead']">
		<xslt step="2" name="MastHead" href="resources/odttoakn/minixslt/debaterecord/MastHead.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Observation']">
		<xslt step="3" name="Observation" href="resources/odttoakn/minixslt/debaterecord/Observation.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='TabledDocuments']">
		<xslt step="4" name="TabledDocuments" href="resources/odttoakn/minixslt/debaterecord/TabledDocuments.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='TabledDocumentsList']">
		<xslt step="5" name="TabledDocumentsList" href="resources/odttoakn/minixslt/debaterecord/TabledDocumentsList.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='GroupActivity']">
		<xslt step="6" name="GroupActivity" href="resources/odttoakn/minixslt/debaterecord/GroupActivity.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Speech']">
		<xslt step="7" name="Speech" href="resources/odttoakn/minixslt/debaterecord/Speech.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='QuestionsContainer']">
		<xslt step="8" name="QuestionsContainer" href="resources/odttoakn/minixslt/debaterecord/QuestionsContainer.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='QuestionAnswer']">
		<xslt step="9" name="QuestionAnswer" href="resources/odttoakn/minixslt/debaterecord/QuestionAnswer.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Question']">
		<xslt step="10" name="Question" href="resources/odttoakn/minixslt/debaterecord/Question.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='PointOfOrder']">
		<xslt step="11" name="PointOfOrder" href="resources/odttoakn/minixslt/debaterecord/PointOfOrder.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='ProceduralMotion']">
		<xslt step="12" name="ProceduralMotion" href="resources/odttoakn/minixslt/debaterecord/ProceduralMotion.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='MotionsContainer']">
		<xslt step="13" name="MotionsContainer" href="resources/odttoakn/minixslt/debaterecord/MotionsContainer.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Motion']">
		<xslt step="14" name="Motion" href="resources/odttoakn/minixslt/debaterecord/Motion.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Person']">
		<xslt step="15" name="Person" href="resources/odttoakn/minixslt/debaterecord/Person.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='ActionEvent']">
		<xslt step="16" name="ActionEvent" href="resources/odttoakn/minixslt/debaterecord/ActionEvent.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Communication']">
		<xslt step="17" name="Communication" href="resources/odttoakn/minixslt/debaterecord/Communication.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Conclusion']">
		<xslt step="18" name="Conclusion" href="resources/odttoakn/minixslt/debaterecord/Conclusion.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='span']">
		<xslt step="19" name="span" href="resources/odttoakn/minixslt/debaterecord/span.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='p']">
		<xslt step="20" name="p" href="resources/odttoakn/minixslt/debaterecord/p.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='ref']">
		<xslt step="21" name="ref" href="resources/odttoakn/minixslt/debaterecord/ref.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='heading']">
		<xslt step="22" name="heading" href="resources/odttoakn/minixslt/debaterecord/heading.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='subheading']">
		<xslt step="23" name="subheading" href="resources/odttoakn/minixslt/debaterecord/subheading.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='list']">
		<xslt step="24" name="list" href="resources/odttoakn/minixslt/debaterecord/list.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='item']">
		<xslt step="25" name="item" href="resources/odttoakn/minixslt/debaterecord/item.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='a']">
		<xslt step="26" name="a" href="resources/odttoakn/minixslt/debaterecord/a.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='meta']">
		<xslt step="27" name="meta" href="resources/odttoakn/minixslt/debaterecord/meta.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='identification']">
		<xslt step="28" name="identification" href="resources/odttoakn/minixslt/debaterecord/identification.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='FRBRWork']">
		<xslt step="29" name="FRBRWork" href="resources/odttoakn/minixslt/debaterecord/FRBRWork.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='FRBRExpression']">
		<xslt step="30" name="FRBRExpression" href="resources/odttoakn/minixslt/debaterecord/FRBRExpression.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='FRBRManifestation']">
		<xslt step="31" name="FRBRManifestation" href="resources/odttoakn/minixslt/debaterecord/FRBRManifestation.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='this']">
		<xslt step="32" name="this" href="resources/odttoakn/minixslt/debaterecord/this.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='uri']">
		<xslt step="33" name="uri" href="resources/odttoakn/minixslt/debaterecord/uri.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='date']">
		<xslt step="34" name="date" href="resources/odttoakn/minixslt/debaterecord/date.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='author']">
		<xslt step="35" name="author" href="resources/odttoakn/minixslt/debaterecord/author.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='publication_mcontainer']">
		<xslt step="36" name="publication_mcontainer" href="resources/odttoakn/minixslt/debaterecord/publication_mcontainer.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='publication']">
		<xslt step="37" name="publication" href="resources/odttoakn/minixslt/debaterecord/publication.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='references']">
		<xslt step="38" name="references" href="resources/odttoakn/minixslt/debaterecord/references.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='TLCOrganization']">
		<xslt step="39" name="TLCOrganization" href="resources/odttoakn/minixslt/debaterecord/TLCOrganization.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='TLCPerson']">
		<xslt step="40" name="TLCPerson" href="resources/odttoakn/minixslt/debaterecord/TLCPerson.xsl" />
		<xsl:apply-templates />
	</xsl:template>

</xsl:stylesheet>