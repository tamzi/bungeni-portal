<?php
/*
 * MV_SpecialListUnusedStreamFiles.php Created on Apr 24, 2007
 *
 * All Metavid Wiki code is Released Under the GPL2
 * for more info visit http:/metavid.ucsc.edu/code
 * 
 * @author Miano Njoka
 * @email mianonjoka@gmail.com
 * @url http://wwww.bungeni.org
 */
  
if (!defined('MEDIAWIKI')) die();


function doSpecialListUnusedStreamFiles($par = null) {
	list( $limit, $offset ) = wfCheckLimits();
	$rep = new MV_SpecialListUnusedStreamFiles();
	return $rep->doQuery( $offset, $limit );
}

SpecialPage::addPage( new SpecialPage('Mv_list_unused_streams','',false,'doSpecialListUnusedStreamFiles',false) );

class MV_SpecialListUnusedStreamFiles extends QueryPage {

	function getName() {
		return "MV_SpecialListUnusedStreamFiles";
	}

	function isExpensive() {
		return false;
	}

	function isSyndicated() { return true; }

	function getPageHeader() {		
		return '<p>' . wfMsg('mv_list_sittings_docu') . "</p><br />\n";
	}
	
	function getSQL() {
		global $mvStreamFilesTable, $mvMediaFilesTable;
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
		$mvtable = $dbr->tableName( $mvMediaFilesTable );
		/* @@todo replace with query that displays more info
		 * such as 
		 * date modified 
		 * stream length
		 * formats available
		 * number of associative metadata chunks */
		return "SELECT
				`id` as `id`,
				`path` as title,
				`id` as value,
				duration,
				base_offset,
				file_desc_msg " . 
				"FROM $mvtable ".
				"WHERE id not in (SELECT file_id FROM $mvStreamFilesTable)";
				
	}
	
	//function getOrder() {
	//	return ' ORDER BY `mv_streams`.`date_start_time` DESC ';
			//($this->sortDescending() ? 'DESC' : '');
	//}
	
	function sortDescending() {
		return false;
	}

	function formatResult( $skin, $result ) {
		global $wgUser, $wgLang, $mvImageArchive,$mvgScriptPath, $wgRequest;
		
		#make sure the first letter is upper case (makeTitle() should do that)		
		//$result->title = strtoupper($result->title[0]) . substr($result->title, 1);		
		//$img_url = $mvImageArchive . $result->title . '?size=icon&time=0:00:00';
		//$img_url = MV_StreamImage::getStreamImageURL($result->stream_id, '0:00:00', 'icon', true);
		//$img_html = '<img src="'.$img_url . '" width="80" height="60">';
		
				
		//$title = Title::makeTitle( MV_NS_SITTING, $result->title  );
		//$spec_list = Title::makeTitle(MV_NS_SPECIAL, "Special:Mv_List_Streams");
		$stream_id = $wgRequest->getVal('stream_id');
		$stream_name = MV_Stream :: getStreamNameFromId($stream_id);
		//$stream_name = 'New';
		$title = Title :: newFromText( $stream_name, MV_NS_STREAM  );
		
		$text =  $result->title;
		
		
		$form = '<form method="post" action="'.$title->getEditURL().'">';
		$form.='<input type="hidden" name="mv_action" value="add_existing_stream_file"></input>';
		$form.='<input type="hidden" name="sf_new'.'[stream_id]" value="'.$stream_id.'"></input>';
		$form.='<input type="hidden" name="sf_new'.'[id]" value="'.$result->id.'"></input>';
		//$form.='<input type="hidden" name="sf_new'.'[duration]" value="'.$result->duration.'"></input>';
		//$form.='<input type="hidden" name="sf_new'.'[base_offset]" value="'.$result->base_offset.'"></input>';
		//$form.='<input type="hidden" name="sf_new'.'[path]" value="'.$text.'"></input>';
		//$form.='<input type="hidden" name="sf_new'.'[file_desc_mesg]" value="'.$result->file_desc_mesg.'"></input>';
		$form.= '<input type="submit" name="submit" value="Add"></input>';
		$form.= '</form>';
		$rlink = $text.$form;
		return $rlink;
	}
}

?>
