<?php
class MV_Sitting
{
	
	var $id = '';
	var $name = '';
	var $sitting_streams = array();
	//var $formats = '';
	//var $state = '';
	//var $date_start_time = '';
	//var $duration = '';

	function __construct($initVal=array())
	{
		if (is_object($initVal))
			$initVal = get_object_vars($initVal);
		if (is_array($initVal)) {
			foreach ($initVal as $key => $val) {
				//make sure the key exisit and is not private
				if (isset ($this-> $key) && $key[0] != '_') {
					$this-> $key = $val;
				}
			}
		} 	
	}

	function db_load_sitting() {
		global $mvSittingsTable;
		$dbr = & wfGetDB(DB_SLAVE);
		if($this->name!=''){
			$result = $dbr->select($dbr->tableName($mvSittingsTable), '*', array ( 'name' => $this->name));
		}else if($this->id!=''){
			$result = $dbr->select($dbr->tableName($mvSittingsTable), '*', array ('id' => $this->id));
		}
		if ($dbr->numRows($result) == 0)
			return false;
		else
		{
			//load the the database values into the current object:
			$this->__construct($dbr->fetchObject($result));
			return true;
		}
	}
	
	function db_load_streams()
	{
		global $mvStreamTable;
		$dbr = & wfGetDB(DB_SLAVE);
		$result = $dbr->select($dbr->tableName($mvStreamTable), '*', array ('sitting_id' => $this->id) );
		$i = 0;
		while ($row = $dbr->fetchObject($result))
		{
			$this->sitting_streams[$i++] = $row;
		}
		return true;
	}
	/*
	 * Inserts the current sitting
	 */
	function insertSitting() {
		global $mvSittingsTable;
		$insAry = array ();
		foreach ($this as $key => $val) {
			if($key=='name'){
					$insAry[$key] = $val;
			}
		}
		$db = & wfGetDB(DB_WRITE);
		if ($db->insert($mvSittingsTable, $insAry)) {
			return true;
		} else {
			//probably error out before we get here
			return false;
		}
	}
	function save_staff($xmldata, $sitting_id)
	{
		global $sitting_reader, $sitting_editor, $sitting_reporter;
		$response = new AjaxResponse();
		$response->setContentType('text/plain');
		$xmlsd = "".html_entity_decode($xmldata);
		$dbr =& wfGetDB(DB_WRITE);
		$xml = new SimpleXMLElement($xmlsd);
		$result = $dbr->delete($dbr->tableName(sitting_assignment), array('sitting_id'=>$sitting_id));
		foreach($xml->children() as $child)
		{
			$name = $child->getName();
			if ($name=='AssignedEditors')
			{	
				
				foreach($child->children() as $editor)
				{
				 	$editor_id = $editor['id'];
				 	$sql2 = 'INSERT INTO sitting_assignment (user_id, sitting_id) VALUES ('.$editor_id.','.$sitting_id.')';
				 	$result = $dbr->query($sql2);
				}
			}
			else if ($name=='AssignedReaders')
			{
				foreach($child->children() as $reader)
				{
				 	$reader_id = $reader['id'];
				 	$sql2 = 'INSERT INTO sitting_assignment (user_id, sitting_id) VALUES ('.$reader_id.','.$sitting_id.')';
				 	$result = $dbr->query($sql2);
				}
			}
			else if ($name=='AssignedReporters')
			{
				foreach($child->children() as $reporter)
				{
				 	$reporter_id = $reporter['id'];
				 	$sql2 = 'INSERT INTO sitting_assignment (user_id, sitting_id) VALUES ('.$reporter_id.','.$sitting_id.')';
				 	$result = $dbr->query($sql2);
				}
			}
		}
		
		$response->addtext("Changes Saved");
		return $response;
	}
}
?>
