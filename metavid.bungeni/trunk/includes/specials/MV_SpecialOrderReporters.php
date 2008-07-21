<?php

if (!defined('MEDIAWIKI')) die();
 
global $IP;
require_once( "$IP/includes/SpecialPage.php" );

function doSpecialOrderStaff() {
	$MV_SpecialOrderStaff = new MV_SpecialOrderStaff();
	$MV_SpecialOrderStaff->execute();
}

SpecialPage::addPage( new SpecialPage('Mv_order_staff','',true,'doSpecialOrderStaff',false) );

class MV_SpecialOrderStaff
{
	function execute()
	{
		global $wgOut,$wgJsMimeType,$mvgScriptPath, $queue;
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/orderReporters.js\"></script>");
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/mv_stream.js\"></script>");
		$html .= "<div id=\"success\"></div>";
		$html.='<form name=staff >';
		$html.='<table>';
		$html.='<tr><td colspan=2>Available Reporters</td></tr>';
		$html.='<tr><td rowspan=2><select name=reporters size=20>';
		
		foreach($queue as $q)
		{
			global $reportersTable, $queue;
			$dbr =& wfGetDB(DB_SLAVE);
			$sql = 'SELECT name FROM '.$reportersTable.' WHERE id = '.$q;
			$result = $dbr->query($sql);
			$row=$dbr->fetchObject($result);
			$html.='<option value='.$q.'>'.$row->name.'</option>';
		}
		
		$html.='</select></td><td>';  
		$html.="<img src=\"{$mvgScriptPath}/skins/images/arrows/sortup.png\" onclick=up()>";
		$html.="</td></tr><tr><td> <img src=\"{$mvgScriptPath}/skins/images/arrows/sortdown.png\" onclick=down()></td></tr>";
		$html.='</table>';
		$html.='<input type="hidden" name="xmldata"></input>';
		$html.='</form>';
		$html.='<a onclick=save()>save</a>';
		$wgOut->addHTML($html);
	}
}
?>
