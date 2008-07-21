<?php
/*
 * MV_SpecialListStreams.php Created on Apr 24, 2007
 *
 * All Metavid Wiki code is Released Under the GPL2
 * for more info visit http:/metavid.ucsc.edu/code
 * 
 * @author Michael Dale
 * @email dale@ucsc.edu
 * @url http://metavid.ucsc.edu
 */
  
if (!defined('MEDIAWIKI')) die();


function doSpecialListStreams($par = null) {
	global $wgRequest,$wgOut;
	$sitting_id = ($wgRequest->getVal('sitting_id'));
	$existing= $wgRequest->getVal('existing');
	if (($sitting_id != ""))
	{
		list( $limit, $offset ) = wfCheckLimits();
		$rep = new MV_SpecialListStreams($sitting_id,$existing);
		$rep->doQuery( $offset, $limit );
	}
	else
	{
		$wgOut->addHTML( wfMsg('edit_sitting_missing') );
	}
}

SpecialPage::addPage( new SpecialPage('Mv_List_Streams','',false,'doSpecialListStreams',false) );

class MV_SpecialListStreams extends QueryPage {
	function __construct($sitting_id,$existing)
	{
		$this->sitting_id = $sitting_id;
		$this->existing = $existing;
	}
	function getName() {
		return "MV_List_Streams";
	}

	function isExpensive() {
		return false;
	}

	function isSyndicated() { return true; }

	function getPageHeader() {
			global $SittingAssignmentsTable;
			$dbr =& wfGetDB( DB_SLAVE );
			$sql = 'SELECT ug_user FROM user_groups WHERE ug_user IN (SELECT user_id FROM sitting_assignment WHERE sitting_id='.$this->sitting_id.') and ug_group="editor"';
		$editors  = $dbr->query($sql);
			$sql = 'SELECT ug_user FROM user_groups WHERE ug_user IN (SELECT user_id FROM sitting_assignment WHERE sitting_id='.$this->sitting_id.') and ug_group="reader"';
		$readers  = $dbr->query($sql);
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user IN (SELECT user_id FROM sitting_assignment WHERE sitting_id='.$this->sitting_id.') and ug_group="reporter"';
		$reporters  = $dbr->query($sql);
			$html = '';
			$html .= '<table border=1><thead>Staff assigned to this sitting</thead><tr><td>Editors</td><td>Readers</td><td>Reporters</td></tr>';
			$html .= '<tr><td><table>';
			while ($rowEditors = $dbr->fetchobject($editors))
			{
				$user = User::newFromId($rowEditors->ug_user);
				$name = $user->getRealName();
				$html .= "<tr><td>$name</td></tr>";	
			}
			$html .= '</table></td>';
			$html .='<td><table>';
			while ($rowReaders = $dbr->fetchobject($readers))
			{
				$user = User::newFromId($rowReaders->ug_user);
				$name = $user->getRealName();
				$html .= "<tr><td>$name</td></tr>";	
			}
			$html .= '</table></td>';
			$html .= '<td><table>';
			while ($rowReporters = $dbr->fetchobject($reporters))
			{
				$user = User::newFromId($rowReporters->ug_user);
				$name = $user->getRealName();
				$html .= "<tr><td>$name</td></tr>";	
			}
			$html .= '</table></td>';
			$html .= '</tr></table>';
			return $html;
		//return '<div name="user-tab"></div><p>' . wfMsg('mv_list_streams_docu') . "</p><br />\n";
	}
	function getSQL() {
		global $mvStreamTable;
		
			$dbr =& wfGetDB( DB_SLAVE );
			$mv_streams_table = $dbr->tableName( $mvStreamTable );
			if ((($this->existing)=='') || (($this->existing)=='false'))
			{
				return "SELECT
					`id` as `stream_id`,
					`name` as title,
					`name` as value, 
					`sitting_id` as sit_id " . 
					"FROM $mv_streams_table ".
					"WHERE sitting_id=".$this->sitting_id;
			}
			elseif ($this->existing=='true')
			{
					return "SELECT
					`id` as `stream_id`,
					`name` as title,
					`name` as value, 
					`sitting_id` as sit_id " . 
					"FROM $mv_streams_table ".
					"WHERE sitting_id=-1";
			}	
	}
	function getOrder() {
		return ' ORDER BY `mv_streams`.`date_start_time` DESC ';
			//($this->sortDescending() ? 'DESC' : '');
	}
	
	function sortDescending() {
		return false;
	}

	function formatResult( $skin, $result ) {
		global $wgUser, $wgLang, $mvImageArchive;
		$sit = new MV_Sitting(array('id'=>$this->sitting_id));
		$sit->db_load_sitting();
		#make sure the first letter is upper case (makeTitle() should do that)		
		$result->title = strtoupper($result->title[0]) . substr($result->title, 1);		
		$img_url = $mvImageArchive . $result->title . '?size=icon&time=0:00:00';
		$img_url = MV_StreamImage::getStreamImageURL($result->stream_id, '0:00:00', 'icon', true);
		$img_html = '<img src="'.$img_url . '" width="80" height="60">';
		
				
		$title = Title::makeTitle( MV_NS_STREAM, $result->title  );
		$rlink = $skin->makeLinkObj( $title,  $img_html . ' '. $title->getText()  );		
		//if admin expose an edit link
		if( $this->existing=='false' ){
			$rlink.=' '.$skin->makeKnownLinkObj( Title::makeTitle(MV_NS_STREAM, $title->getText()),
						'edit', 'action=edit' );
		}
		else
		{
			$rlink.=' '.$skin->makeKnownLinkObj( Title::makeTitle(MV_NS_SITTING, $sit->name ),
						'add', 'action=edit&mv_action=add&stream_id='.$result->stream_id);
		}
		return $rlink;
	}
}

?>
