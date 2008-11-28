<?php

if ( !defined( 'MEDIAWIKI' ) ) die();

class MV_SpecialAddSitting extends SpecialPage {

	var $start_time;
	var $start_date;
	var $type;
	var $duration;
	var $info;
	public function __construct() {
		parent::__construct('Add_Sitting');
	}

	function execute() {
		global $wgOut, $wgRequest, $wgUser, $mvgScriptPath, $wgJsMimeType;
		
		if( $wgUser->isAllowed('add_sitting') ){
			$this->type = htmlspecialchars($wgRequest->getVal('type'));
			
			$this->start_date = htmlspecialchars($wgRequest->getText('month')) . '/'. htmlspecialchars($wgRequest->getText('day')).'/'. htmlspecialchars($wgRequest->getText('year'));
			$this->start_date_mysql = htmlspecialchars($wgRequest->getText('year')) . '-'. htmlspecialchars($wgRequest->getText('month')).'/'. htmlspecialchars($wgRequest->getText('day'));
			$this->start_time = htmlspecialchars($wgRequest->getText('hour')) . ':'. htmlspecialchars($wgRequest->getText('min')).':00';
			
			$this->end_date = htmlspecialchars($wgRequest->getText('month2')) . '/'. htmlspecialchars($wgRequest->getText('day2')).'/'. htmlspecialchars($wgRequest->getText('year2'));
			$this->end_date_mysql = htmlspecialchars($wgRequest->getText('year2')) . '-'. htmlspecialchars($wgRequest->getText('month2')).'/'. htmlspecialchars($wgRequest->getText('day2'));
			$this->end_time = htmlspecialchars($wgRequest->getText('hour2')) . ':'. htmlspecialchars($wgRequest->getText('min2')).':00';
			
			$this->duration = strtotime($this->end_date.' '.$this->end_time) - strtotime($this->start_date.' '.$this->start_time);
			
			$this->info = htmlspecialchars($wgRequest->getText('info'));
		
			$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/build/tabview/assets/border_tabs.css',
                     					'type' => 'text/css' ) );
			$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/build/tabview/assets/skin-sam.css',
                     					'type' => 'text/css' ) );
                     	$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/build/tabview/assets/tabview.css',
                     					'type' => 'text/css' ) );
                     	$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/build/tabview/assets/tabview-core.css',
                     					'type' => 'text/css' ) );
                     	$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/build/fonts/fonts-min.css',
                     					'type' => 'text/css' ) );
                     	$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/build/calendar/assets/calendar.css',
                     					'type' => 'text/css' ) );
                     	$wgOut->addLink(array( 'rel' => 'stylesheet',
                     					'href' => $mvgScriptPath . '/skins/build/button/assets/skins/button.css',
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
			$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/sitting2.js\"></script>");
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
			if ('' == trim($this->start_date)){
				$error = true;
				$s .= '<li>Date Held</li>';
			}
			if ('' == trim($this->end_date)){
				$error = true;
				$s .= '<li>End Date</li>';
			}
			if ($this->duration < 1){
				$error = true;
				$s .= '<li>Time settings are incorrect</li>';
			}
			$s .= '</ul>';
			if ($error)
			{
				return '<div class="errorbox">Fill in the following Fields'.$s.'</div> <br/>';
			}
			else
			{
				if ( ( '' != trim($this->type) ) && ( '' != trim($this->start_date) ) )
					$sitting_name = $this->type.'_'.date( 'j_F_Y', strtotime($this->start_date));
				else
					return '<div class="errorbox">An error occured generating Sitting Name. Notify Administrator</div>';
					
				$title = Title::newFromText( $sitting_name, MV_NS_STREAM );
				$article = new Article( $title );
				if ('' != trim($this->info))
				{
					$text = $this->info . " [[Date Held::".$this->start_date."| ]] [[Type::".$this->type."| ]] ";
				}
				else
				{
					$text = " [[Date Held::".$this->start_date."| ]] [[Type::".$this->type."| ]] ";
				}
				
				if ($article->exists())
				{
					return '<div class="errorbox">A sitting with the same name already exists</div>';
				}
				else
				{
					$mvTitle = new MV_Title( $sitting_name );
					$stream =& mvGetMVStream( array( 'name' => $sitting_name) );
					$stream->duration = $this->duration;
					$stream->date_start_time = $this->start_date_mysql .' '.$this->start_time;
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
		$s .= 'Start Date';
		$s .= Xml::closeElement('label');
		$s .= '</td><td>';
		//$s.= '<input type="text" value="2008/08/24" name="start_date"><input type="button" value="Cal" onclick="displayCalendar(document.Add-Sitting-form.date-held,\'yyyy/mm/dd\',this, true)"><div id="cal1"></div>';
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

		$s .= '<input type="text" id="year" name="year" value=""></input>';
		$s .= '</td></tr>';
		$s .= '<tr><td>';
		$s .= 'Start Time';
 		$s .='</td><td>';
		$s .= <<< YETANOTHER
<select id="hour" name="hour">
			<option value="00">00</option>
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
	        </select>
YETANOTHER;

$s .= <<< YETANOTHERB
<select id="min" name="min">
	        	<option value="00">00</option>
	        	<option value="05">05</option>
	        	<option value="10">10</option>
	        	<option value="15">15</option>
	        	<option value="20">20</option>
	        	<option value="25">25</option>
	        	<option value="30">30</option>
	        	<option value="35">35</option>
	        	<option value="40">40</option>
	        	<option value="45">45</option>
	        	<option value="50">50</option>
	        	<option value="55">55</option>
	        </select>
YETANOTHERB;
		$s .= '</td></tr>';
$s .= '<tr><td>';
		$s .= Xml::openElement('label', array('name'=>'lbl_date2'));
		$s .= 'End Date';
		$s .= Xml::closeElement('label');
		$s .= '</td><td>';

$s .= <<< MOREHTMLD
<div class="field" id="datefields2">
		<select id="month2" name="month2">
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

	        <select id="day2" name="day2">
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
MOREHTMLD;

		$s .= '<input type="text" id="year2" name="year2" value=""></input>';
		$s .= '</td></tr>';
		$s .= '<tr><td>';
		$s .= 'End Time';
 		$s .='</td><td>';
		$s .= <<< YETANOTHERD
<select id="hour2" name="hour2">
			<option value="00">00</option>
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
	        </select>
YETANOTHERD;
$s .= <<< YETANOTHERD
<select id="min2" name="min2">
	        	<option value="00">00</option>
	        	<option value="05">05</option>
	        	<option value="10">10</option>
	        	<option value="15">15</option>
	        	<option value="20">20</option>
	        	<option value="25">25</option>
	        	<option value="30">30</option>
	        	<option value="35">35</option>
	        	<option value="40">40</option>
	        	<option value="45">45</option>
	        	<option value="50">50</option>
	        	<option value="55">55</option>
	        </select>
YETANOTHERD;
		$s .= '</td></tr>';
		
		
		
		$s .= '<tr><td>'; 
		$s .= Xml::openElement('label', array('name'=>'lbl_info'));
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
