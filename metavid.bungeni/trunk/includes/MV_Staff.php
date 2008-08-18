<?php

class MV_Staff
{
	function saveOrder($xmlsd)
	{
		global $reporterOrderTable, $readerOrderTable, $editorOrderTable;
		$response = new AjaxResponse();
		$response->setContentType('text/plain');
		$xmlstr = ''.html_entity_decode($xmlsd);
		$dbr =& wfGetDB(DB_WRITE);
		
		$xml = new SimpleXMLElement($xmlstr);
		
		//delete all in table
		$result = $dbr->delete($editorOrderTable,"*"); 
		$result = $dbr->delete($readerOrderTable,"*");
		$result = $dbr->delete($reporterOrderTable,"*");
		
		foreach($xml->children() as $child)
		{
			if ($child->getName()=='Editor')
			{ 
				$sql = 'INSERT INTO '.$editorOrderTable.' (id, rank) VALUES ('.$child['id'].','.$child['rank'].')';
				$result = $dbr->query($sql);
			}
			elseif ($child->getName()=='Reader')
			{
				$sql = 'INSERT INTO '.$readerOrderTable.' (id, rank) VALUES ('.$child['id'].','.$child['rank'].')';
				$result = $dbr->query($sql);
			}
			elseif ($child->getName()=='Reporter')
			{
				$sql = 'INSERT INTO '.$reporterOrderTable.' (id, rank) VALUES ('.$child['id'].','.$child['rank'].')';
				$result = $dbr->query($sql);
			}
		}
		
		$response->addtext("Changes Saved");
		return $response;
	}
}

?>
