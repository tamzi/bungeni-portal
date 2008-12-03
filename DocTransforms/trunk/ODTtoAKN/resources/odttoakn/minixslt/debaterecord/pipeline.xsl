<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
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

	<xsl:template match="*[@name='debaterecord']">
		<xslt step="0" name="debaterecord" href="resources/odttoakn/minixslt/debaterecord/debaterecord.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='MastHead']">
		<xslt step="1" name="MastHead" href="resources/odttoakn/minixslt/debaterecord/MastHead.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Observation']">
		<xslt step="2" name="Observation" href="resources/odttoakn/minixslt/debaterecord/Observation.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='GroupActivity']">
		<xslt step="3" name="GroupActivity" href="resources/odttoakn/minixslt/debaterecord/GroupActivity.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Speech']">
		<xslt step="4" name="Speech" href="resources/odttoakn/minixslt/debaterecord/Speech.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='QuestionsContainer']">
		<xslt step="5" name="QuestionsContainer" href="resources/odttoakn/minixslt/debaterecord/QuestionsContainer.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='QuestionAnswer']">
		<xslt step="6" name="QuestionAnswer" href="resources/odttoakn/minixslt/debaterecord/QuestionAnswer.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Question']">
		<xslt step="7" name="Question" href="resources/odttoakn/minixslt/debaterecord/Question.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='PointOfOrder']">
		<xslt step="8" name="PointOfOrder" href="resources/odttoakn/minixslt/debaterecord/PointOfOrder.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='ProceduralMotion']">
		<xslt step="9" name="ProceduralMotion" href="resources/odttoakn/minixslt/debaterecord/ProceduralMotion.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Person']">
		<xslt step="10" name="Person" href="resources/odttoakn/minixslt/debaterecord/Person.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='ActionEvent']">
		<xslt step="11" name="ActionEvent" href="resources/odttoakn/minixslt/debaterecord/ActionEvent.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Communication']">
		<xslt step="12" name="Communication" href="resources/odttoakn/minixslt/debaterecord/Communication.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='Conclusion']">
		<xslt step="13" name="Conclusion" href="resources/odttoakn/minixslt/debaterecord/Conclusion.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='span']">
		<xslt step="14" name="span" href="resources/odttoakn/minixslt/debaterecord/span.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='p']">
		<xslt step="15" name="p" href="resources/odttoakn/minixslt/debaterecord/p.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='ref']">
		<xslt step="16" name="ref" href="resources/odttoakn/minixslt/debaterecord/ref.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='heading']">
		<xslt step="17" name="heading" href="resources/odttoakn/minixslt/debaterecord/heading.xsl" />
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="*[@name='subheading']">
		<xslt step="18" name="subheading" href="resources/odttoakn/minixslt/debaterecord/subheading.xsl" />
		<xsl:apply-templates />
	</xsl:template>


</xsl:stylesheet>