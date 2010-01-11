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
	function __construct()
	{
	}
	
	function displayTypes()
	{
		global $sittingTypesTable, $mvgScriptPath;
		$html='';
		$html='<fieldset><legend>Add a Sitting Type</legend>';
		$dbr = wfGetDB(DB_SLAVE); 
		$result = $dbr->select($sittingTypesTable, '*');
		if ($result == 0)
		{
			$html = 'There are currently no sitting types';
		}
		else
		{
			while ($row = $dbr->fetchobject($result))
			{
				$html.='<a title="Remove sitting type"' .
				 ' href="'.$wgRequest->getRequestURL().'&mv_action=rm_sitting_type&rid='.$row->id.'"><img src="'.$mvgScriptPath.'/skins/images/delete.png"></a>';
				 $html .= $row->type."<br>"; 
			}
		}
		
		$html='</fieldset>';
		$wgOut->addHTML($html);
	}
	
	function execute()
	{
		processReq();
		displayTypes();
		form();
	}
	
	function form()
	{
		global $wgTitle;
		$html = '';
		$html .= '<fieldset><legend>Add a Sitting Type</legend><form action="'.$wgTitle->getLocalURL().'" method="post">';
		$html .= 'Sitting type <input type="text" name="sitting_type"><br>';
		$html .= '<input type="submit" name="submit">';
		$html .= '</form></fieldset>';
		$wgOut->addHTML($html);
	}
	
	function processReq()
	{
	}
}
?>
