<?php

if (!defined('MEDIAWIKI')) die();
 
global $IP;
require_once( "$IP/includes/SpecialPage.php" );

function doSpecialManageReporters() {
	$MV_SpecialManageReporters = new MV_SpecialManageReporters();
	$MV_SpecialManageReporters->execute();
}

SpecialPage::addPage( new SpecialPage('Mv_manage_reporters','',true,'doSpecialManageReporters',false) );

class MV_SpecialManageReporters
{
	function execute()
	{
		global $wgOut,$wgJsMimeType,$mvgScriptPath;
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/manageReporters.js\"></script>");
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/mv_stream.js\"></script>");
		$html='<div id="response"></div>';
		$html.='<form name=test >';
		$html.='<table>';
		$html.='<tr><td>Readers</td><td></td><td>Reporters assigned to a Reader</td><td></td><td>Unassigned Reporters</td></tr>';
		$html.='<tr><td>';
		$html.='<select name="editor" size=20 onchange=load()>';
		$html.='</select>';
		$html.='</td>';
		$html.='<td>-></td>';
		$html.='<td>';
		$html.='<select name="assigned" size=20 width=20>';
		$html.='</select>';
		$html.='</td>';
		$html.='<td><table><tr><td> <a onclick="add()"> <== </a></td></tr><tr><td><a onclick="remove()"> ==> </a></td></tr></table></td>';
		$html.='<td>';
		$html.='<select name="unassigned" size=20 width=20>';
		$html.='</select>';
		$html.='</td>';
		$html.='</tr>';
		$html.='<tr>';
		$html.='<td><a onclick="save()">Save Changes</a><td>';
		$html.='</tr>';
		$html.='</table>';
		$html.='<input type="hidden" name="xmldata"></input>';
		$html.='</form>';
		$html .='<div id="test"></div>';
		$wgOut->addHTML($html);
	}
}
?>
