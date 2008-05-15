<?php

if (!defined('MEDIAWIKI')) die();
 
global $IP;
require_once( "$IP/includes/SpecialPage.php" );

function doSpecialManageReaders() {
	$MV_SpecialManageReaders = new MV_SpecialManageReaders();
	$MV_SpecialManageReaders->execute();
}

SpecialPage::addPage( new SpecialPage('Mv_manage_readers','',true,'doSpecialManageReaders',false) );

class MV_SpecialManageReaders
{

	function execute()
	{
		global $wgOut;
		$html='';
		$html.='<form name=test>';
		$html.='<table>';
		$html.='<tr><td>';
		$html.='<select name="editor" size=20 onchange=load(this.value)>';
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
		$html.='<td><input type=submit value="Save Changes"></input><td>';
		$html.='</tr>';
		$html.='</table>';
		$html.='</form>';
		$wgOut->addHTML($html);
	}
}
?>
