<?php
/*
 * MV_StreamFiles.php Created on Sep 25, 2007
 * 
 * All Metavid Wiki code is Released Under the GPL2
 * for more info visit http:/metavid.ucsc.edu/code
 * 
 * @author Michael Dale
 * @email dale@ucsc.edu
 * @url http://metavid.ucsc.edu
 */
 if ( !defined( 'MEDIAWIKI' ) )  die( 1 );
 
 /*
  * MvStreamFile hanndles the mapping of path types to urls & 
  * active record style mannagment of the mv_stream_files table
  */
 
 class MvStreamFile{
 	var $stream_id='';
 	var $base_offset='';//base offset from the stream  date_start_time
 	var $duration='';	//duration of clip.
 	var $path_type='';
 	var $file_desc_msg='';
 	var $path='';
 	
 	function MvStreamFile($initVal, &$parent_stream){
 		$this->parent_stream = $parent_stream;
 		//convert the object to an array
		if (is_object($initVal))
			$initVal = get_object_vars($initVal);
		if (is_array($initVal)) {
			foreach ($initVal as $key => $val) {
				//make sure the key exisit and is not private
				if (isset ($this-> $key) && $key[0] != '_') {
					$this->$key = $val;
				}
			}
		}
 	}
 	/*
 	 * returns the path with {sn} replaced with stream name if present
 	 */
 	function getPath(){
 		return str_replace('{sn}',$this->parent_stream->name, $this->path);
 	}
 	function get_link(){ 		
 		global $mvVideoArchivePaths;
 		if(isset($mvVideoArchivePaths[ $this->path_type ] )){
 			//we can return the link
 			return $mvVideoArchivePaths[ $this->path_type ] . $this->getPath();
 		}else{
 			if($this->path_type=='ext_url'){
 				return $this->getPath();
 			}
 		}
 		return null;	
 	}
 	function get_desc(){
 		return $this->file_desc_msg;
 	}
 }
?>
