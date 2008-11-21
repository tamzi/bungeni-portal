<?php

if ( !defined( 'MEDIAWIKI' ) ) die();

class MV_SpecialAddSitting extends SpecialPage {
	public function __construct() {
		parent::__construct('Add_Sitting');
	}

	function execute() {
		global $wgOut, $wgRequest, $wgUser, $mvgScriptPath, $wgJsMimeType;
		
		if( $wgUser->isAllowed('add_sitting') ){
			$this->type = htmlspecialchars($wgRequest->getVal('type'));
			$this->date_held = htmlspecialchars($wgRequest->getText('date_held'));
			$this->duration = htmlspecialchars($wgRequest->getText('duration'));
			$this->info = htmlspecialchars($wgRequest->getText('info'));
		
			$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/tabview/assets/border_tabs.css',
                     					'type' => 'text/css' ) );
			$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/tabview/assets/skin-sam.css',
                     					'type' => 'text/css' ) );
                     	$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/tabview/assets/tabview.css',
                     					'type' => 'text/css' ) );
                     	$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/tabview/assets/tabview-core.css',
                     					'type' => 'text/css' ) );
                     	$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/build/fonts/fonts-min.css',
                     					'type' => 'text/css' ) );
                     	$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/build/calendar/assets/skins/sam/calendar.css',
                     					'type' => 'text/css' ) );
                     	$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/build/button/assets/skins/sam/button.css',
                     					'type' => 'text/css' ) );
                     	$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/sitting.css',
                     					'type' => 'text/css' ) );				
			$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/build/yahoo-dom-event/yahoo-dom-event.js\"></script>");
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/build/calendar/calendar-min.js\"></script>");
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/build/container/container_core-min.js\"></script>");
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/build/element/element-beta-min.js\"></script>");
			$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/build/button/button-min.js\"></script>");
			$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/sitting.js\"></script>");
			$wgOut->addHTML($this->processForm());
			$wgOut->addHTML($this->getForm());
		}
		else
		{
			$wgOut->addHTML('<div class="errorbox">You DO NOT have permission to add a Sitting</div>');
		}
		
		$wgOut->setPageTitle('Add Sitting');
	}
	
	function processForm()
	{
		global $wgRequest;
		$posted = $wgRequest->wasPosted();
		if ($posted)
		{
			$error = false;
			$s = '<ul>';
			if ('' == trim($this->type)){
				$error = true;
				$s .= '<li>Sitting Type</li>';
			}
			if ('' == trim($this->date_held)){
				$error = true;
				$s .= '<li>Date Held</li>';
			}
			$s .= '</ul>';
			if ($error)
			{
				return '<div class="errorbox">Fill in the following Fields'.$s.'</div> <br/>';
			}
			else
			{
				if ( ( '' != trim($this->type) ) && ( '' != trim($this->date_held) ) )
					$sitting_name = $this->type.'_'.date( 'j_F_Y', strtotime($this->date_held));
				else
					return '<div class="errorbox">An error occured generating Sitting Name. Notify Administrator</div>';
					
				$title = Title::newFromText( $sitting_name, MV_NS_STREAM );
				$article = new Article( $title );
				if ('' != trim($this->info))
				{
					$text = $this->info . " [[Date Held::".$this->date_held."| ]] [[Type::".$this->type."| ]] ";
				}
				else
				{
					$text = " [[Date Held::".$this->date_held."| ]] [[Type::".$this->type."| ]] ";
				}
				
				if ($article->exists())
				{
					return '<div class="errorbox">A sitting with the same name already exists</div>';
				}
				else
				{
					$mvTitle = new MV_Title( $sitting_name );
					$stream =& mvGetMVStream( array( 'name' => $sitting_name, 'duration'=>$this->duration ) );
					if ( $stream->insertStream( 'metavid_file' ) ) {
						$article->doEdit($text, 'Sitting');
						$article->doRedirect(false,'','action=edit&new=true');
					}
					else
					{
						return '<div class="errorbox">An Error occured when adding Sitting to database</div>';
					}
					
				}
			}
		}
	} 
	
	
	function typeSelector()
	{
		$dbr = wfGetDB(DB_SLAVE); 
		
		$result = $dbr->select($dbr->tablename('sitting_types'), '*');
		$s = '';
		$s .= Xml::openElement('select', array('name'=>'type'));
		while ($row = $dbr->fetchObject($result))
		{
			if (!is_null($this->type) && ($this->type == $row->name))
			{
				$s .= Xml::option($row->name,str_replace(' ', '_',$row->name), true);
			}
			else
			{
				$s .= Xml::option($row->name,str_replace(' ', '_',$row->name));
			}	
		}
		$s .= Xml::closeElement('select');
		return $s;
	}
	
	function getForm(){
		global $wgRequest, $wgUser;
		$skin = $wgUser->getSkin();
		
		$s .= '<div class="yui-navset">'; 
		$s .= '<ul class="yui-nav">'; 
	        $s .= '<li class="selected"><a href="'.$this->getTitle()->getLocalURL().'"><em>Sitting Details</em></a></li>'; 
	        $s .= '<li><a><em>Media</em></a></li>'; 
	        $s .= '<li><a><em>Staff</em></a></li>'; 
	        $s .= '<li><a><em>Takes</em></a></li>'; 
	    	$s .= '</ul>';             
	    //	$s .= '<div class="yui-content">'; 
	        
	    	
		//$s .= Xml::openElement('div', array('class'=>'addMP yui-content'));
		$s .= '<table name="add_Sitting_table" width=90%>';
		$s .=  Xml::openElement('form', array( 'method' => 'post', 'action' => $this->getTitle()->getLocalURL(),  'id' => 'Add-Sitting-form' ));
		$s .= '<tr><td>';
		$s .= Xml::openElement('label', array('name'=>'lbl_type'));
		$s .= 'Type';
		$s .= Xml::closeElement('label');
		$s .= '</td><td>';
		$s .= $this->typeSelector();
		$s .= '</td></tr>';
		
		$s .= '<tr><td>';
		$s .= Xml::openElement('label', array('name'=>'lbl_date'));
		$s .= 'Date Held';
		$s .= Xml::closeElement('label');
		$s .= '</td><td>';
		//$s.= '<input type="text" value="2008/08/24" name="date_held"><input type="button" value="Cal" onclick="displayCalendar(document.Add-Sitting-form.date-held,\'yyyy/mm/dd\',this, true)"><div id="cal1"></div>';
$s .= <<< MOREHTML
<div class="field" id="datefields">
		<select id="month" name="month">
	        	<option value="01">01</option>
	        	<option value="02">02</option>
	        	<option value="03">03</option>
	        	<option value="04">04</option>
	        	<option value="05">05</option>
	        	<option value="06">06</option>
	        	<option value="07">07</option>
	        	<option value="08">08</option>
	        	<option value="09">09</option>
	        	<option value="10">10</option>
	        	<option value="11">11</option>
	        	<option value="12">12</option>
	        </select>

	        <select id="day" name="day">
	        	<option value="01">01</option>
	        	<option value="02">02</option>
	        	<option value="03">03</option>
	        	<option value="04">04</option>
	        	<option value="05">05</option>
	        	<option value="06">06</option>
	        	<option value="07">07</option>
	        	<option value="08">08</option>
	        	<option value="09">09</option>
	        	<option value="10">10</option>
	        	<option value="11">11</option>
	        	<option value="12">12</option>
	        	<option value="13">13</option>
	        	<option value="14">14</option>
	        	<option value="15">15</option>
	        	<option value="16">16</option>
	        	<option value="17">17</option>
	        	<option value="18">18</option>
	        	<option value="19">19</option>
	        	<option value="20">20</option>
	        	<option value="21">21</option>
	        	<option value="22">22</option>
	        	<option value="23">23</option>
	        	<option value="24">24</option>
	        	<option value="25">25</option>
	        	<option value="26">26</option>
	        	<option value="27">27</option>
	        	<option value="28">28</option>
	        	<option value="29">29</option>
	        	<option value="30">30</option>
	        	<option value="31">31</option>
	        </select>
			
		</div>
MOREHTML;
		$s .= '<input type="text" id="date_held" name="date_held" value="">';
		
		$s .= '</td></tr>';
		
		$s .= '<tr><td>'; 
		$s .= Xml::openElement('label', array('name'=>'lbl_duration'));
		$s .= 'Duration ';
		$s .= Xml::closeElement('label');
		$s .= '</td><td>';
		$s .= Xml::openElement('input', array('type'=>'text','name'=>'Info'));
		$s .= Xml::closeElement('input');
		$s .= '</td><tr>';
		
		$s .= '<tr><td>'; 
		$s .= Xml::openElement('label', array('name'=>'duration'));
		$s .= 'Info ';
		$s .= Xml::closeElement('label');
		$s .= '</td><td>';
		$s .= Xml::textarea('info', $this->info, 40, 5);
		$s .= '</td><tr>';
		
		
		
		$s .= '<tr><td>';
		$s .= '<button type="button" onclick="window.location="'.$skin->makeSpecialUrl("Sittings").'"" name="cancel">Cancel</button>';
		$s .= '</td><td>';
		$s .= Xml::submitButton('Next');
		$s .= '</td></tr>';
		$s .= Xml::closeElement('form');
		$s .= '</table>';
		//$s .= Xml::closeElement('div');
		//$s .= '</div>'; 
		$s .= '</div>'; 
		return $s;
	}
}
