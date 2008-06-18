<?php

class MV_Reporters
{
	function save($str)
	{
		global $reportersTable;
		$matches=array();
		$dbr =& wfGetDB(DB_WRITE);
		$success = false;
		$i = 1;
		if ($x=(preg_match_all("/([0-9]+)/",$str,$matches)))
		{
			$success  = 'Changes Saved';
			foreach($matches[1] as $n)
			{
				$sql = 'UPDATE '. $reportersTable. ' SET order_number='.$i.' WHERE id='.$n;
				if ($result = $dbr->query($sql))
					$success = true;
				else
					$success = false;
				$i++;
			}
			if ($success)
				return 'Changes Saved';
		}
		else
		{
			return 'An error occured. REPORT THIS TO THE ADMINISTRATOR IMMEDIATELY';
		}
	}
	
	function get_workload($id)
	{
		global $sitting_reporter, $mvSittingsTable;
		$dbr =& wfGetDB(DB_SLAVE);
		$sittings = $dbr->select($sitting_reporter, '*', array('reporter_id'=>$id));
		$xml = new AjaxResponse();
		$xml->setContentType('text/xml');
		$xml->addtext('<'.'?xml version="1.0" encoding="utf-8" ?'.">"); 
		$xml->addtext('<Response>'."");
		while ($row = $dbr->fetchobject($sittings))
		{
			$sit = $dbr->select($mvSittingsTable, '*', array('id'=>$row->sitting_id));
			$row2 = $dbr->fetchobject($sit);
			$xml->addtext('<Sitting id="'.$row2->id.'" name="'.$row2->name.'">');
			$xml->addtext('</Sitting>');
		} 
		$xml->addtext('</Response>');
		return $xml;
	}
	
	function get_available_reporters($sitting_id)
	{
		global $reportersTable, $sitting_reporter;
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT * FROM '.$reportersTable.' WHERE id NOT IN ( SELECT reporter_id FROM '.$sitting_reporter.' WHERE sitting_id='.$sitting_id.')';
		$reporters  = $dbr->query($sql);
		$xml = new AjaxResponse();
		$xml->setContentType('text/xml');
		$xml->addtext('<'.'?xml version="1.0" encoding="utf-8" ?'.">"); 
		$xml->addtext('<Response>'."");
		while ($rowReporters = $dbr->fetchobject($reporters))
		{
			$xml->addtext('<Reporter id="'.$rowReporters->id.'" name="'.$rowReporters->name.'">');
			$xml->addtext('</Reporter>');
		} 
		$xml->addtext('</Response>');
		return $xml;
	}
	
	function get_assigned($sitting_id)
	{
		global $reportersTable, $sitting_reporter;
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT * FROM '.$reportersTable.' WHERE id IN ( SELECT reporter_id FROM '.$sitting_reporter.' WHERE sitting_id='.$sitting_id.')';
		$reporters  = $dbr->query($sql);
		$xml = new AjaxResponse();
		$xml->setContentType('text/xml');
		$xml->addtext('<'.'?xml version="1.0" encoding="utf-8" ?'.">"); 
		$xml->addtext('<Response>'."");
		while ($rowReporters = $dbr->fetchobject($reporters))
		{
			$xml->addtext('<Reporter id="'.$rowReporters->id.'" name="'.$rowReporters->name.'">');
			$xml->addtext('</Reporter>');
		} 
		$xml->addtext('</Response>');
		return $xml;
	}
}
?>
