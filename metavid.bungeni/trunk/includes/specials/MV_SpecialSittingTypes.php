<?php 
if (!defined('MEDIAWIKI')) die();
 
global $IP;
//require_once( "$IP/includes/SpecialPage.php" );

function doSpecialSittingTypes() {
	$MV_SpecialSittingTypes = new MV_SpecialSittingTypes();
	$MV_SpecialSittingTypes->execute();
}
SpecialPage::addPage( new SpecialPage('Mv_Sitting_Types','',true,'doSpecialSittingTypes',true) );

class MV_SpecialSittingTypes
{
	function displayTypes()
	{
		global $sittingTypesTable, $mvgScriptPath, $wgOut, $wgTitle, $wgRequest;
		$html='';
		$html.='<fieldset><legend>Available Sitting Types</legend>';
		$dbr = wfGetDB(DB_SLAVE); 
		$result = $dbr->select($sittingTypesTable, '*');
		if ($result->numRows() == 0)
		{
			$html .= 'There are currently no sitting types';
		}
		else
		{
			while ($row = $dbr->fetchobject($result))
			{
				$html.='<a title="Remove sitting type"' .
				 ' href="'.$wgTitle->getLocalURL("action=remove&id=$row->id").'"><img src="'.$mvgScriptPath.'/skins/images/delete.png"></a>';
				 $html .= $row->type."<br>"; 
			}
		}
		
		$html.='</fieldset>';
		$wgOut->addHTML($html);
	}
	
	function execute()
	{
		$this->processReq();
		$this->displayTypes();
		$this->form();
	}
	
	function form()
	{
		global $wgRequest, $wgOut, $wgTitle;
		$html = '';
		$html .= '<fieldset><legend>Add a Sitting Type</legend><form action="'.$wgRequest->getRequestURL().'" method="post">';
		$html .= 'Sitting type <input type="text" name="sitting_type"><br>';
		$html .= '<input type="submit" name="submit" value="Add sitting type">';
		$html .= '<input type="hidden" name="action" value="add">';
		$html .= '</form></fieldset>';
		$wgOut->addHTML($html);
	}
	
	function processReq()
	{
		global $wgRequest, $sittingTypesTable;
		if ($wgRequest->getVal("action") == 'remove')
		{
			if  ($wgRequest->getVal('id') != '')
			{
				$id = $wgRequest->getVal('id');
				$dbr = wfGetDB(DB_WRITE);	
				$result = $dbr->delete($sittingTypesTable, array('id'=>$id));
			}
		}
		elseif ($wgRequest->getVal("action") == 'add')
		{
			if  ($wgRequest->getVal('sitting_type') != '')
			{
				$type = $wgRequest->getVal('sitting_type');
				$dbr = wfGetDB(DB_WRITE);	
				$result = $dbr->insert($sittingTypesTable, array('type'=>$type));
			}
		} 
	}
}
?>
