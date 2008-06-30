<?php

class MV_Editors
{
	function getEditors()
	{
		global $editorsTable;
		$dbr =& wfGetDB(DB_SLAVE);
		$result = $dbr->select($editorsTable, '*');
		$html='';
		while ($row = $dbr->fetchobject($result))
			$html.= '<option value="'.$row->id.'">'.$row->name.'</option>'; 
		return $html;
	}
	
	function get_assigned($sitting_id)
	{
		global $editorsTable, $sitting_editor;
		$dbr =& wfGetDB(DB_SLAVE);
		//$sql = 'SELECT * FROM '.$editorsTable.' WHERE id IN ( SELECT editor_id FROM '.$sitting_editor.' WHERE sitting_id='.$sitting_id.')';
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user IN (SELECT user_id FROM sitting_assignment WHERE sitting_id='.$sitting_id.') and ug_group="editor"';
		$editors  = $dbr->query($sql);
		$xml = new AjaxResponse();
		$xml->setContentType('text/xml');
		$xml->addtext('<'.'?xml version="1.0" encoding="utf-8" ?'.">"); 
		$xml->addtext('<Response>'."");
		while ($rowEditors = $dbr->fetchobject($editors))
		{
			$user = User::newFromId($rowEditors->ug_user);
			$name = $user->getRealName();
			$xml->addtext('<Editor id="'.$rowEditors->ug_user.'" name="'.$name.'">');
			$xml->addtext('</Editor>');
		} 
		$xml->addtext('</Response>');
		return $xml;
	}
	
	function get_available_editors($sitting_id)
	{
		global $editorsTable, $sitting_editor;
		$dbr =& wfGetDB(DB_SLAVE);
		//$sql = 'SELECT user_id FROM '.$sitting_assignments.',user_groups WHERE sitting_assignments.sitting_id='.$sitting_id.' and user_groups.user_group="editor")';
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user NOT IN (SELECT user_id FROM sitting_assignment WHERE sitting_id='.$sitting_id.') and ug_group="editor"';
		$editors  = $dbr->query($sql);
		$xml = new AjaxResponse();
		$xml->setContentType('text/xml');
		$xml->addtext('<'.'?xml version="1.0" encoding="utf-8" ?'.">"); 
		$xml->addtext('<Response>'."");
		while ($rowEditors = $dbr->fetchobject($editors))
		{
			$user = User::newFromId($rowEditors->ug_user);
			$name = $user->getRealName();
			$xml->addtext('<Editor id="'.$rowEditors->ug_user.'" name="'.$name.'">');
			$xml->addtext('</Editor>');
		} 
		$xml->addtext('</Response>');
		return $xml;
	}
	/*
	function getUnAssigned()
	{
		global $readersTable, $readersAssignmentTable;
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT * FROM '.$readersTable.' WHERE id NOT IN ( SELECT reader_id FROM '.$readersAssignmentTable.')';
		$unassigned = $dbr->query($sql);
		$xml = new AjaxResponse();
		$xml->setContentType('text/xml');
		$xml->addtext('<'.'?xml version="1.0" encoding="utf-8" ?'.">"); 
		$xml->addtext('<Response>'."");
		while ($row = $dbr->fetchobject($unassigned))
		{
			$xml->addtext('<Reader name="'.$row->name.'" id="'.$row->id.'"></Reader>');
		}
		$xml->addtext('</Response>');
		return $xml;
	}
	
	function save($xmlstr)
	{
		global $readersAssignmentTable;
		$response = new AjaxResponse();
		$response->setContentType('text/plain');
		$xmlsd = "".html_entity_decode($xmlstr);
		$dbr =& wfGetDB(DB_WRITE);
		$xml = new SimpleXMLElement($xmlsd);
		$result = $dbr->delete($readersAssignmentTable, "*");
		foreach($xml->children() as $ed)
		{
			$editor_id = $ed['id'];
			foreach($ed->children() as $reader)
			{
				 $reader_id = $reader['id'];
				 $sql2 = 'INSERT INTO '.$readersAssignmentTable.' (editor_id, reader_id) VALUES ('.$editor_id.','.$reader_id.')';
				 $result = $dbr->query($sql2);
			}
		}
		$response->addtext("Changes Saved");
		return $response;
	}
	*/
	function get_workload($id)
	{
		global $sitting_editor, $mvSittingsTable;
		$dbr =& wfGetDB(DB_SLAVE);
		$sittings = $dbr->select($dbr->tablename(sitting_assignment), '*', array('user_id'=>$id));
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
}

?>
