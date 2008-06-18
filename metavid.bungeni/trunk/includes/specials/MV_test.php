<?php
if (!defined('MEDIAWIKI')) die();
 
global $IP;
require_once( "$IP/includes/SpecialPage.php" );

function doSpecialTest() {
	$MV_SpecialTest= new MV_test();
	$MV_SpecialTest->execute();
}

SpecialPage::addPage( new SpecialPage('Mv_test','',true,'doSpecialTest',false) );

class MV_test
{
	function execute()
	{
		global $reportersTable,$wgOut, $wgRequest;
		$nameKey = 'mpnamencgsblahbladggfdsafh';
		$tit = Title::newFromText($nameKey, MV_NS_MVD);
		$art = new Article($tit);
		$art->doEdit($_REQUEST['smw_Spoken_By'],'',EDIT_NEW);
	}
}		
?>
