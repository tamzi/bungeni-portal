<?php 
if (!defined('MEDIAWIKI')) die();
 
global $IP;
//require_once( "$IP/includes/SpecialPage.php" );

function doSpecialCategories() {
	$MV_SpecialSittingTypes = new MV_SpecialCategories();
	$MV_SpecialSittingTypes->execute();
}
SpecialPage::addPage( new SpecialPage('Mv_Categories','',true,'doSpecialCategories',true) );

class MV_SpecialCategories
{
	function displayTypes()
	{
		global $categoriesTable, $mvgScriptPath, $wgOut, $wgTitle, $wgRequest;
		$html='';
		$html.='<fieldset><legend>Available Categories</legend>';
		$dbr = wfGetDB(DB_SLAVE); 
		$result = $dbr->select($categoriesTable, '*');
		if ($result->numRows() == 0)
		{
			$html .= 'There are currently no Categories';
		}
		else
		{
			while ($row = $dbr->fetchobject($result))
			{
				$html.='<a title="Remove Category"' .
				 ' href="'.$wgTitle->getLocalURL("action=remove&id=$row->id").'"><img src="'.$mvgScriptPath.'/skins/images/delete.png"></a>';
				 $html .= $row->title."<br>"; 
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
		$html .= '<fieldset><legend>Add a Category</legend><form action="'.$wgRequest->getRequestURL().'" method="post">';
		$html .= 'Category <input type="text" name="category_title"><br>';
		$html .= '<input type="submit" name="submit" value="Add Category">';
		$html .= '<input type="hidden" name="action" value="add">';
		$html .= '</form></fieldset>';
		$wgOut->addHTML($html);
	}
	
	function processReq()
	{
		global $wgRequest, $categoriesTable;
		if ($wgRequest->getVal("action") == 'remove')
		{
			if  ($wgRequest->getVal('id') != '')
			{
				$id = $wgRequest->getVal('id');
				$dbr = wfGetDB(DB_WRITE);	
				$result = $dbr->delete($categoriesTable, array('id'=>$id));
			}
		}
		elseif ($wgRequest->getVal("action") == 'add')
		{
			if  ($wgRequest->getVal('title') != '')
			{
				$category_title = $wgRequest->getVal('category_title');
				$dbr = wfGetDB(DB_WRITE);	
				$result = $dbr->insert($categoriesTable, array('title'=>$category_title));
			}
		} 
	}
}
?>
