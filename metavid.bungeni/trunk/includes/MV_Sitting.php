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
		//load the the database values into the current object:
		$this->__construct($dbr->fetchObject($result));
		return true;
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
}
?>
