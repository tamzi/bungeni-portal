<?php

if (!defined('MEDIAWIKI')) die();
 
global $IP;
require_once( "$IP/includes/SpecialPage.php" );

function doSpecialOrderReporters() {
	$MV_SpecialOrderReporters = new MV_SpecialOrderReporters();
	$MV_SpecialOrderReporters->execute();
}

SpecialPage::addPage( new SpecialPage('Mv_order_reporters','',true,'doSpecialOrderReporters',false) );

class MV_SpecialOrderReporters
{
	function execute()
	{
		global $wgOut,$wgJsMimeType,$mvgScriptPath, $queue;
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/orderReporters.js\"></script>");
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/mv_stream.js\"></script>");
		$html .= "<div id=\"success\"></div>";
		$html.='<form name=test >';
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
		$html.="<img src=\"{$mvgScriptPath}/skins/images/up.png\" onclick=up()>";
		$html.="</td></tr><tr><td> <img src=\"{$mvgScriptPath}/skins/images/down.png\" onclick=down()></td></tr>";
		$html.='</table>';
		$html.='<input type="hidden" name="xmldata"></input>';
		$html.='</form>';
		$html.='<a onclick=save()>save</a>';
		$wgOut->addHTML($html);
	}
}
?>
