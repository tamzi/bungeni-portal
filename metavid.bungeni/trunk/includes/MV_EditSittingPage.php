<?php
class MV_EditSittingPage extends EditPage{
	var $name='';
	var $mv_action;
	var $id='';
	var $sit;
	function __construct($article)
	{
		//$wgRequest;
		$this->name = $article->getTitle()->getText();
		//$this->mode = 
		parent::__construct($article);
	}
	function edit(){
		global $wgOut, $wgUser, $wgHooks, $wgRequest;
 		//check permission if admin show 'edit sitting'
 		if( $wgUser->isAllowed('mv_edit_sitting') ){
 			//if $this->mode ==
 			$this->sit = new MV_Sitting(array('name'=>$this->name));
			$this->sit->db_load_sitting();
			$this->sit->db_load_streams();
			$this->id = $this->sit->id;
			$this->mv_action = $wgRequest->getVal('mv_action'); 	
 			$this->processRequest();
 			$this->displayEditStreams();				
 			if($this->mv_action=='rm_stream'){
 			//make the request look like a GET
 			//that way we don't run importFormData with empty POST
 				$_SERVER['REQUEST_METHOD'] = 'GET';
 			}	
 			//parent::edit();
 		}else
 		{
 			$wgOut->addHTML("error");
 		}
	}
	 		
	function displayEditStreams()
	{
		global $wgRequest,$wgOut,$mvgScriptPath;
		$this->sit = new MV_Sitting(array('name'=>$this->name));
		$this->sit->db_load_sitting();
		$this->sit->db_load_streams();
		$tit = Title::makeTitle(MV_NS_SITTING, $this->name);
		$html='';
		$html.='<form action="'.$tit->getEditURL().'" method="POST">';
		$html.='<input type="hidden" name="mv_action" value="edit_streams">';		
		$html.= '<fieldset><legend>'.wfMsg('mv_remove_streams').'</legend>' . "\n";	
		$html.= '<table width="600" border="0">';	
		$html.='</tr><tr>';
	
		if (count ($this->sit->sitting_streams) != 0)
		{
			foreach ($this->sit->sitting_streams as $obj){				
				$html.='<td width="10">';
				
				
				$h='<a title="'.wfMsg('mv_streams').'"' .
				 ' href="'.$tit->getEditURL().'&mv_action=rm_stream&stream_id='.$obj->id.'"><img src="'.$mvgScriptPath.'/skins/images/delete.png"></td>';
				$html.=$h.'<td><b>'.$obj->name;
				$html.='</b></td></tr>'	;		
			}
		}
		else{
			$html.="<tr><td>Sitting has no streams</td></tr>";
		}
		$html .='</table></fieldset>';
		$html.='</form>';
		
		//add new stream: 
		
		$html.= '<fieldset><legend>'.wfMsg('mv_add_stream').'</legend>' . "\n";	
		$html.= '<table width="600" border="0">';			
			$html.='<tr><td>';
			$spec_list = Title::makeTitle(MV_NS_SPECIAL, "Special:Mv_Add_Stream" );
			$skin = new Linker();
		$html.=$skin->makeKnownLinkObj( $spec_list, 'Add New Stream to this Sitting', 'sitting_id='.$this->id);
			$html.='</td></tr>';
			$html.=	'<tr><td>';
			$spec_list = Title::makeTitle(MV_NS_SPECIAL, "Special:Mv_List_Streams" );
			$html.=$skin->makeKnownLinkObj($spec_list, 'Add Existing Stream to this Sitting', 'sitting_id='.$this->id.'&existing=true');
			$html.='</td></tr>';		
		$html .='</table></fieldset>';					
		$wgOut->addHTML($html);
		return true;
		
	}
	function editSitting()
	{
		global $wgRequest;
		$html = '';
		$html.='<form action="'.$tit->getEditURL().'" method="POST">';
		$html.='<input type="hidden" name="mv_action" value="edit_streams">';		
		$html.= '<fieldset><legend>'.wfMsg('mv_edit_sitting').'</legend>' . "\n";	
	}
	function processRequest()
	{
		global $wgRequest, $wgUser,$mvStreamTable;
 		
 		if($this->mv_action=='rm_stream'){
 			$db = & wfGetDB(DB_WRITE);
 			if ($db->update($mvStreamTable, array('sitting_id'=>-1), array('id'=>$wgRequest->getVal('stream_id')))) {
				return true;
			} else {
			//probably error out before we get here
				return false;
			}
 		}elseif($this->mv_action=='add'){
 			$db = & wfGetDB(DB_WRITE);
 			if ($db->update($mvStreamTable, array('sitting_id'=>$this->id), array('id'=>$wgRequest->getVal('stream_id')))) {
				return true;
			} else {
			//probably error out before we get here
				return false;
			}
 		}
	}
}
?>
