<?php
/*
 * MV_SpecialListSittings.php Created on Apr 24, 2007
 *
 * All Metavid Wiki code is Released Under the GPL2
 * for more info visit http:/metavid.ucsc.edu/code
 * 
 * @author Miano Njoka
 * @email mianonjoka@gmail.com
 * @url http://wwww.bungeni.org
 */
  
if (!defined('MEDIAWIKI')) die();


function doSpecialListSittings($par = null) {
	list( $limit, $offset ) = wfCheckLimits();
	$rep = new MV_SpecialListSittings();
	return $rep->doQuery( $offset, $limit );
}

SpecialPage::addPage( new SpecialPage('Mv_List_Sittings','',true,'doSpecialListSittings',false) );

class MV_SpecialListSittings extends QueryPage {

	function getName() {
		return "MV_List_Sittings";
	}

	function isExpensive() {
		return false;
	}

	function isSyndicated() { return true; }

	function getPageHeader() {		
		return '<p>' . wfMsg('mv_list_sittings_docu') . "</p><br />\n";
	}
	
	function getSQL() {
		global $mvSittingsTable;
		$dbr =& wfGetDB( DB_SLAVE );
		//$relations = $dbr->tableName( 'smw_relations' );
		//$NSrel = SMW_NS_RELATION;
		# QueryPage uses the value from this SQL in an ORDER clause.
		/*return "SELECT 'Relations' as type,
					{$NSrel} as namespace,
					relation_title as title,
					relation_title as value,
					COUNT(*) as count
					FROM $relations
					GROUP BY relation_title";*/
		$mv_sittings_table = $dbr->tableName( $mvSittingsTable );
		/* @@todo replace with query that displays more info
		 * such as 
		 * date modified 
		 * stream length
		 * formats available
		 * number of associative metadata chunks */
		return "SELECT
				`id` as `sitting_id`,
				`name` as title,
				`name` as value " . 
				"FROM $mv_sittings_table ";
				
	}
	
	//function getOrder() {
	//	return ' ORDER BY `mv_streams`.`date_start_time` DESC ';
			//($this->sortDescending() ? 'DESC' : '');
	//}
	
	function sortDescending() {
		return false;
	}

	function formatResult( $skin, $result ) {
		global $wgUser, $wgLang, $mvImageArchive;
		
		#make sure the first letter is upper case (makeTitle() should do that)		
		$result->title = strtoupper($result->title[0]) . substr($result->title, 1);		
		//$img_url = $mvImageArchive . $result->title . '?size=icon&time=0:00:00';
		//$img_url = MV_StreamImage::getStreamImageURL($result->stream_id, '0:00:00', 'icon', true);
		//$img_html = '<img src="'.$img_url . '" width="80" height="60">';
		
				
		$title = Title::makeTitle( MV_NS_SITTING, $result->title  );
		//$spec_list = Title::makeTitle(MV_NS_SPECIAL, "Special:Mv_List_Streams");
		$text =  $title->getText();
		$id = $result->sitting_id;
		$rlink = $skin->makeKnownLinkObj( $title, $text );		
		//if admin expose an edit link
		if( $wgUser->isAllowed('delete') ){
			$rlink.=' '.$skin->makeKnownLinkObj( Title::makeTitle(MV_NS_SITTING, $title->getText()),
						'edit', 'action=edit' );
		}
		return $rlink;
	}
}

?>
