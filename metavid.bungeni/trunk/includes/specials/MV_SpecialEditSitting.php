<?php
if (!defined('MEDIAWIKI')) die();
 
global $IP;
require_once( "$IP/includes/SpecialPage.php" );

function doSpecialAddEditSitting() {
	$MV_SpecialAddSitting = new MV_SpecialEditSitting();
	$MV_SpecialAddSitting->execute();
}

SpecialPage::addPage( new SpecialPage('Mv_add_edit_Sitting','',true,'doSpecialAddEditSitting',false) );
//SpecialPage::addPage( new SpecialPage('Mv_add_edit_Sitting','',true,'doSpecialAddSitting',false) );

class MV_SpecialEditSitting extends SpecialPage{	 
	function execute(){	
		global $wgRequest, $wgOut, $wgUser, $wgArticle;
		$sitting_of = $wgRequest->getVal('sitting_of');	
		$session_number = $wgRequest->getVal('session_number');
		$sitting_start_date_time = 	$wgRequest->getVal('sitting_start_date_and_time');                
        $sitting_end_date_time = 	$wgRequest->getVal('sitting_end_time');
        $sitting_session_number = 	$wgRequest->getVal('sitting_session_number');
        $wpEditToken =	$wgRequest->getVal( 'wpEditToken');
		$sitting_desc  = 	$wgRequest->getVal( 'sitting_desc');
		$sitting_name = $sitting_of.'-'.$sitting_start_date_time;
		//$sitting_of.'-'.$sitting_start_date_time.'-'
		$title = Title::newFromText( $sitting_name, MV_NS_SITTING  );
		$wgArticle = new Article($title);
		$wgArticle->doEdit( $sitting_desc, wfMsg('mv_summary_add_sitting') );
		$dbkey = $title->getDBKey();
		$sitting = new MV_Sitting(array('name'=>$dbkey));
		//$sitting->db_load_sitting();
		//$sitting->db_load_streams();
		$sitting->insertSitting();
			//$title = new Title(MV_NS_SITTING,$sitting_name);
			
			
			if ($wgArticle->exists())
			{
				$wgOut->redirect($title->getEditURL());		
			}
			else
			{
				$html.= 'Article '.$sitting_name.' does not exist';
				$wgOut->addHtml($html);
			}
			
	}
	
}
?>
