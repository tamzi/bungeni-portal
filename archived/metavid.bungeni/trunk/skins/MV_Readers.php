<?php

class MV_Readers
{
	function getReaders()
	{
		global $readersTable;
		$dbr =& wfGetDB(DB_SLAVE);
		$result = $dbr->select($editorsTable, '*');
		$html='';
		while ($row = $dbr->fetchobject($result))
			$html.= '<option value="'.$row->id.'">'.$row->name.'</option>'; 
		return $html;
	}
	
	function getAssigned()
	{
		global $readersTable, $reportersTable, $reportersAssignmentTable;
		$dbr =& wfGetDB(DB_SLAVE);
		$readers = $dbr->select($reportersTable, '*');
		$xml = new AjaxResponse();
		$xml->setContentType('text/xml');
		$xml->addtext('<'.'?xml version="1.0" encoding="utf-8" ?'.">"); 
		$xml->addtext('<Response>'."");
		
		while ($rowReaders = $dbr->fetchobject($readers))
		{
			$result = $dbr->select($reportersAssignmentTable, '*',array(reader_id=>($rowReaders->id)));
			$xml->addtext('<Reader id="'.$rowReaders->id.'" name="'.$rowReaders->name.'">');
			while ($rowReporter = $dbr->fetchobject($result))
			{
				$reporterresult = $dbr->select($reportersTable, '*',array(id=>($rowReporter->reporter_id)));
				if ($row = $dbr->fetchobject($reporterresult))
					$xml->addtext('<Reporter name="'.$row->name.'" id="'.$row->id.'"></Reporter>');
			}
			$xml->addtext('</Reader>');
		} 
		$xml->addtext('</Response>');
		return $xml;
	}
	
	function getUnAssigned()
	{
		global $reportersTable, $reportersAssignmentTable;
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT * FROM '.$reportersTable.' WHERE id NOT IN ( SELECT reader_id FROM '.$reportersAssignmentTable.')';
		$unassigned = $dbr->query($sql);
		$xml = new AjaxResponse();
		$xml->setContentType('text/xml');
		$xml->addtext('<'.'?xml version="1.0" encoding="utf-8" ?'.">"); 
		$xml->addtext('<Response>'."");
		while ($row = $dbr->fetchobject($unassigned))
		{
			$xml->addtext('<Reporter name="'.$row->name.'" id="'.$row->id.'"></Reporter>');
		}
		$xml->addtext('</Response>');
		return $xml;
	}
	
	function save($xmlstr)
	{
		global $reportersAssignmentTable;
		$response = new AjaxResponse();
		$response->setContentType('text/plain');
		$xmlsd = "".html_entity_decode($xmlstr);
		$dbr =& wfGetDB(DB_WRITE);
		$xml = new SimpleXMLElement($xmlsd);
		$result = $dbr->delete($reportersAssignmentTable, "*");
		foreach($xml->children() as $reader)
		{
			$reader_id = $reader['id'];
			foreach($ed->children() as $reporter)
			{
				 $reporter_id = $reporter['id'];
				 $sql2 = 'INSERT INTO '.$reportersAssignmentTable.' (reader_id, reporter_id) VALUES ('.$reader_id.','.$reporter_id.')';
				 $result = $dbr->query($sql2);
			}
		}
		$response->addtext("Changes Saved");
		return $response;
	}
}

?>
