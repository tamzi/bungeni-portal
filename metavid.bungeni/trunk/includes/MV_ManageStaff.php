<?php
class MV_ManageStaff extends EditPage{
	function __construct($article)
	{
		parent::__construct($article);
	}
	
	function edit(){
		global $wgOut, $wgUser, $wgHooks, $wgRequest;
		$wgOut->clearHTML();
		$this->displayForm();
	}
	
	function displayForm()
	{
		global $wgOut, $wgUser, $wgHooks, $wgRequest,$wgJsMimeType,$mvgScriptPath, $wgTitle, $mvSittingsTable;
		if ($wgUser->isAllowed('managestaff'))
		{
			$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/manageStaff.js\"></script>");
			$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/mv_stream.js\"></script>");
		
			$html = '<h1>Staff Assignments - Sitting : '.$wgTitle->getText().'</h1>';
			$dbr =& wfGetDB(DB_SLAVE);
			$sit = $dbr->select($mvSittingsTable, '*', array('name'=>$wgTitle->getDBKey())); 
			$sitting_id = $dbr->fetchobject($sit)->id;
			$html.='<div id="sitting_id" style="display:none;">'.$sitting_id.'</div>';
			$html.='<div id="response"></div>';
			$html.='<div id="debug"></div>';
			$html .= '<table><form name="staff" action="">';
			$html .= '<tr><td rowspan="2"><fieldset><legend>Available Editors</legend><select name="available_editors" size="10" onclick="editor_onchange(this.value)"></select></fieldset></td>';
			$html .= '<td><a onclick="remove_editor()"><==</a></td>';
			$html .= '<td rowspan="2"><fieldset><legend>Assigned Editors</legend><select name="assigned_editors" size="10" onclick="editor_onchange(this.value)"></select></fieldset></td>';
			$html .= '<td  rowspan="2"  width="400"><fieldset><legend>Current Workload</legend><div height=300 id="editor_workload"></div></fieldset></td>';
			$html .= '<tr><td><a onclick="add_editor()">==></a></td></tr>';
			$html .= '</tr><tr><td rowspan="2"><fieldset><legend>Available Readers</legend><select name="available_readers" size=10 onclick="reader_onchange(this.value)"></select></fieldset></td>';
			$html .= '<td><a onclick="remove_reader()"><==</a></td>';
			$html .= '<td rowspan="2"><fieldset><legend>Assigned Readers</legend><select name="assigned_readers" size=10 onclick="reader_onchange(this.value)"></select></fieldset></td>';
			$html .= '<td rowspan="2"  width="400"><fieldset><legend>Current Workload</legend><div id="reader_workload"></div></fieldset></td></tr>';
			$html .= '<tr><td><a onclick="add_reader()">==></a></td></tr>';
			$html .= '</tr><tr><td rowspan="2"><fieldset><legend>Available Reporters</legend><select name="available_reporters" size=10 onclick="reporter_onchange(this.value)"></select></fieldset></td>';
			$html .= '<td><a onclick="remove_reporter()"><==</a></td>';
			$html .= '<td rowspan="2"><fieldset><legend>Available Reporters</legend><select name="assigned_reporters" size=10 onclick="reporter_onchange(this.value)"></select></fieldset></td>';
			$html .= '<td rowspan="2" width="400"><fieldset><legend>Current Workload</legend><div id="reporter_workload"></div></fieldset></td></tr>';
			$html .= '<tr><td><a onclick="add_reporter()">==></a></td></tr>';
			$html .= '<tr><td></td><td></td><td><a onclick="save()">Save All Changes</a></td>';
			$html .= '</tr>';
			$html .= '</form</table>';
			
		}
		else
		{
			$html = wfMsg('mv_staff_permission');
		}
		$wgOut->addHTML($html);
	}
}
