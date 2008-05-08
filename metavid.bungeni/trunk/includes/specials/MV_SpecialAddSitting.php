<?php
/*
 * MV_SepcialAddStream.php Created on Apr 25, 2007
 *
 * All Metavid Wiki code is Released under the GPL2
 * for more info visit http:/metavid.ucsc.edu/code
 * 
 * @author Michael Dale
 * @email dale@ucsc.edu
 * @url http://metavid.ucsc.edu
 * 
 */
 
if (!defined('MEDIAWIKI')) die();
 
global $IP;
require_once( "$IP/includes/SpecialPage.php" );

function doSpecialAddSitting() {
	$MV_SpecialAddSitting = new MV_SpecialAddSitting();
	$MV_SpecialAddSitting->execute();
}

SpecialPage::addPage( new SpecialPage('Mv_Add_Sitting','',true,'doSpecialAddSitting',false) );

class MV_SpecialAddSitting {
	function execute() {
		global $wgRequest, $wgOut, $wgUser, $mvSitting_name, $mvgIP;   
		#init html output var:
		$html='';                   
        $title_str = $wgRequest->getVal('title');
        $this->sitting_name = ($wgRequest->getVal( 'sitting_name')=='')?'':
        	 	MV_Title::normalizeTitle( $wgRequest->getVal( 'sitting_name') );
        $this->sitting_start_time = 	$wgRequest->getVal('sitting_start_time');                
        $this->sitting_end_time = 	$wgRequest->getVal('sitting_end_time');
        $this->sitting_session_number = 	$wgRequest->getVal('sitting_session_number');
        $this->wpEditToken =	$wgRequest->getVal( 'wpEditToken');
		$this->sitting_desc  = 	$wgRequest->getVal( 'sitting_desc');
		//grab the desc from the wiki page if not in the POST req
		
		if($this->sitting_desc==''){			
			$desTitle = Title::makeTitle(MV_NS_SITTING, $this->sitting_name );		
			//grab the article text:
			$curRevision = Revision::newFromTitle($desTitle);
			if($curRevision)
				$this->stream_desc = $curRevision->getText();
		}		
		
        if($this->sitting_name==''){     
        	//default page request           	                
    		$parts = split('/',$title_str);
    		if(count($parts)>=2){
    			//means we can use part 1 as a sitting name:
    			$this->sitting_name =$parts[1]; 
    		}
		}else{	
			//output add_ status to html
			$html.=$this->add_sitting();						
		}
    	
    	$this->check_permissions();
    	
    	if(count($this->_allowedSittingTypeArray)==0){
    		//break out user lacks permissions to add anything
			$html.=wfMsg('add_sitting_permission');	
			$wgOut->addHTML( $html );	
			return ;				        	
    	}
    		   
    	//output the add sitting form	
		$spectitle = Title::makeTitle( NS_SPECIAL, 'Mv_Add_sitting' );		
		$docutitle = Title::newFromText(wfMsg('mv_add_sitting'), NS_HELP);
		if($this->mode=='edit'){
			$mvSittingTitle = Title::makeTitle(MV_NS_SITTING,  $this->sitting_name);
			if($mvSittingTitle->exists() ){
				$sk = $wgUser->getSkin();			
				$sittingLink = $sk->makeLinkObj( $mvSittingTitle,  $this->sitting_name );
				$html.=wfMsg('mv_edit_sitting_docu', $sittingLink);
			}
		}else{
			$html.= wfMsg('mv_add_sitting_docu', $docutitle->getFullURL()) . "\n";
		}
		
		$html.= '<form name="add_sitting" action="' . $spectitle->escapeLocalURL() . '" method="post" enctype="multipart/form-data">';
		$html.= '<fieldset><legend>'.wfMsg('mv_add_sitting').'</legend>' . "\n" .
		        '<input type="hidden" name="title" value="' . $spectitle->getPrefixedText() . '"/>' ;
		$html.= '<table width="600" border="0">';
					
		$html.= '<td  width="300">';		
		$html.= '<i>'.wfMsg('mv_label_sitting_of')."</i>:";
		$html.= '</td><td>';	
		$html.= '</tr>';
		$html.= '<tr><td><table width="500" align="center">';
		$html.='<tr><td>';	
		$html.= '<input type="radio" name="sitting_of" value="Plenary">Plenary</input>';
		$html.= '</td>';
		$html.= '<td>';
		$html.= '<input type="radio" name="sitting_of" value="Committee on Health">Committee on Health</input>';	
		$html.= '</td></tr>';
		$html.= '<tr><td>';
		$html.= '<input type="radio" name="sitting_of" value="Committee on Education">Committee on Education</input>';
		$html.=	'</td><td>';	
		$html.= '<input type="radio" name="sitting_of" value="Committee on Government Spending">Committee on Government Spending</input>';
		$html.='</td></tr>';
		$html.='<tr><td>';
		$html.= '<input type="radio" name="sitting_of" value="Etc">Etc...</input>';							
		$html.= '</td>';				
		$html.=	'</tr>'."\n";
		$html.=	'</table>';
		$html.= '<br />' . "\n";	
		$html.=	'<tr>';
		$html.= '<td width="140">';		
		$html.= '<i>'.wfMsg('mv_label_sitting_start_date_and_time')."</i>:";
		$html.= '</td><td>';			
		$html.= '<input type="text" name="sitting_start_date_and_time" value="" size="30" maxlength="1024"><br />' . "\n";				
		$html.= '</td>';				
		$html.=	'</tr>'."\n";
		
		$html.= '<td width="140">';		
		$html.= '<i>'.wfMsg('mv_label_sitting_end_date_and_time')."</i>:";
		$html.= '</td><td>';			
		$html.= '<input type="text" name="sitting_end_date_and_time" value="" size="30" maxlength="1024"><br />' . "\n";				
		$html.= '</td>';				
		$html.=	'</tr>'."\n";
			
		$html.= '<td  width="140">';		
		$html.= '<i>'.wfMsg('mv_label_sitting_session_number')."</i>:";
		$html.= '</td><td>';			
		$html.= '<input type="text" name="sitting_session_number" value="" size="30" maxlength="1024"><br />' . "\n";				
		$html.= '</td>';				
		$html.=	'</tr>'."\n";
			
		$html.= '<td  width="140">';		
		$html.= '<i>'.wfMsg('mv_label_sitting_type')."</i>:";
		$html.= '</td><td>';			
		$html.= '<input type="text" name="sitting_type" value="" size="30" maxlength="1024"><br />' . "\n";				
		$html.= '</td>';				
		$html.=	'</tr>'."\n";
		$html.=	'<tr><td valign="top"><i>' .wfMsg('mv_label_sitting_desc') .'</i>:</td><td>';
		
		//add an edit token (for the stream description)
		if ( $wgUser->isLoggedIn() ){
			$token = htmlspecialchars( $wgUser->editToken() );
		}else{
			$token = EDIT_TOKEN_SUFFIX;
		}
		
		$html .= "\n<input type='hidden' value=\"$token\"$docutitle name=\"wpEditToken\" />\n";
			//output the text area: 
		$html .= '<textarea tabindex="1" accesskey="," name="sitting_desc" id="stream_desc" rows=6 cols=5>'.$this->sitting_desc.'</textarea>' . "\n";
		$html .= '<br /><input type="submit" value="' . wfMsg('mv_add_sitting_submit') . "\"/>\n</form>";
		
		$html .= '</td></tr></table>';
    	$html .='</fieldset>';
		  	# Output menu items 
			# @@todo link with language file                
        $wgOut->addHTML( $html );
            
            
        //output the stream files list (if in edit mode)
        //if($this->mode=='edit')
    		//$this->list_streams();  	            
	}
	/* for now its just a list no edit allowed 
	 * (all file management done via maintenance scripts )
	 */
	/*
	function list_streams(){
		global $wgOut;
		$html='';
		$stream =& mvGetMVStream(array('name'=>$this->stream_name));		
		$stream->db_load_stream();
		$stream_files = $stream->getFileList();
		
		if(count($stream_files)==0){
			$html.=wfMsg('mv_no_stream_files');	
			$wgOut->addHTML( $html );
			return ;
		}
		//output filedset container: 
		$html.= '<fieldset><legend>'.wfMsg('mv_file_list').'</legend>' . "\n";	
		$html.= '<table width="600" border="0">';	
		foreach($stream_files as $sf){
				$html.='<tr>';
					$html.='<td width="150">'.$sf->getFullURL().'</td>';
					$html.='<td>'.$sf->get_desc().'</td>';											
				$html.='</tr>';
		}
		$html .='</table></fieldset>';
		$wgOut->addHTML( $html );
		return '';	
	}
	*/
	
	function add_sitting(){	
		$out='';		
	
		//get the stream pointer
		$sitting = new MV_Sitting(array('name'=>$this->sitting_name));
			
		//if the stream is inserted procced with page insertion
		if($sitting->insertSitting()){
			global $wgUser;
			$sk = $wgUser->getSkin();
			
			//insert page
			$sittingTitle =Title::newFromText( $this->sitting_name, MV_NS_SITTING  );
			$wgArticle = new Article( $sittingTitle );
			$success = $wgArticle->doEdit( $this->sitting_desc, wfMsg('mv_summary_add_sitting') );
			if ( $success ) {
				//stream inserted succesfully report to output				
				$sittingLink = $sk->makeLinkObj( $sittingTitle,  $this->sitting_name );		
				$out='sitting '.$sittingLink.' added';													
					 
			} else {
				$out=wfMsg('mv_error_sitting_insert');
			}		
		}	
		return $out;
	}
	
		
	/*
	 * Returns an array of stream types the current user can add
	 * @@todo we should just check the $mvStreamTypePermission directly if we can...
	 * @@todo deprecate this: use mediaWikis user system: 
	 * $wgUser->isAllowed( 'trackback' ) 
	 */
	function check_permissions(){
		global $mvSittingTypePermission, $wgUser;
		$this->_allowedSittingTypeArray = array();
		
		$user_groups = $wgUser->getGroups();
		if($wgUser->isLoggedIn()){
			array_push($user_groups, 'user');
		}
		foreach($mvSittingTypePermission as $type=>$allowed_group_list){
			if(is_array($allowed_group_list)){
				foreach($allowed_group_list as $allowed){
					if(in_array($allowed, $user_groups)){
						$this->_allowedSittingTypeArray[$type]=true;
					}
				}
				
			}			
		}
		return $this->_allowedSittingTypeArray;
	}	
	
}
?>
