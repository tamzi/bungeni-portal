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
		$spectitle = Title::makeTitle( NS_SPECIAL, 'Mv_add_edit_sitting' );		
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
		$html.='<tr>';			
		$html.= '<td  width="300">';		
		$html.= '<i>'.wfMsg('mv_label_sitting_of')."</i>:";
		$html.= '</td>';
		$html.= '<td>';
		$html.='<select name="sitting_of">';
		$html.= '<option value="Plenary">Plenary</option>';	
		$html.= '<option value="Committee_on_Health">Committee on Health</option>';	
		$html.= '<option value="Committee_on_Education">Committee on Education</option>';
		$html.= '<option value="Committee_on_Government Spending">Committee on Government Spending</option>';
		$html.= '<option name="sitting_of" value="Etc">Etc...</option>';							
		$html.= '</select></td>';				
		$html.=	'</tr>'."\n";
		$html.=	'<tr>';
		$html.= '<td width="140">';		
		$html.= '<i>'.wfMsg('mv_label_sitting_start_date_and_time')."</i>:";
		$html.= '</td><td>';			
		//$html.= '<input type="text" name="sitting_start_date_and_time" value="" size="30" maxlength="1024"><br />' . "\n";	
		$html.= '<input type="text" value="24.12.2007 12:55" readonly name="sitting_start_date_and_time"><input type="button" value="Cal" onclick="displayCalendar(document.add_sitting.sitting_start_date_and_time,\'yyyy/mm/dd hh:ii\',this,true)">';			
		$html.= '</td>';				
		$html.=	'</tr>'."\n";
		
		$html.= '<td width="140">';		
		$html.= '<i>'.wfMsg('mv_label_sitting_end_date_and_time')."</i>:";
		$html.= '</td><td>';			
		//$html.= '<input type="text" name="sitting_end_date_and_time" value="" size="30" maxlength="1024"><br />' . "\n";				
		$html.= '<input type="text" value="24.12.2007 12:55" readonly name="sitting_end_date_and_time"><input type="button" value="Cal" onclick="displayCalendar(document.add_sitting.sitting_start_date_and_time,\'yyyy/mm/dd hh:ii\',this,true)">';	
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
		$html.= '<select name="sitting_type">';	
		$html.= '<option value="Morning" size="30">Morning</option>';	
		$html.= '<option value="Afternoon" size="30">Afternoon</option>';
		$html.= '<option value="Emergency" size="30">Emergency</option>';			
		$html.= '</select>';
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
