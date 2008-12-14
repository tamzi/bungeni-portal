<?php
class MV_ManageStaff extends EditPage{

	var $stream_id;	
	
	function __construct($article)
	{
		
		$title = $article->getTitle();
		$mvTitle = new MV_Title( $title->mDbkeyform );
		$this->stream_id = $mvTitle->getStreamId();
		parent::__construct($article);
	}
	
	function edit(){
		global $wgOut, $wgUser, $wgHooks, $wgRequest;
		$wgOut->clearHTML();
		$this->displayForm();
	}
	
	function displayForm()
	{
		global $wgOut, $wgUser, $wgHooks, $wgRequest,$wgJsMimeType,$mvgScriptPath, $wgTitle;
		if ($wgUser->isAllowed('managestaff'))
		{
			//$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/manageStaff.js\"></script>");
			$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/mv_stream.js\"></script>");
			$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/build/yahoo-dom-event/yahoo-dom-event.js\"></script>");
			$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/build/animation/animation-min.js\"></script>");
			$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/build/dragdrop/dragdrop-min.js\"></script>");
			$mvCssUrl = $mvgScriptPath . '/skins/drag.css';
			$wgOut->addLink(array(
				'rel'   => 'stylesheet',
				'type'  => 'text/css',
				'media' => 'all',
				'href'  => $mvCssUrl
			));				
			$mvCssUrl = $mvgScriptPath . '/skins/build/fonts/fonts-min.css';
			$wgOut->addLink(array(
				'rel'   => 'stylesheet',
				'type'  => 'text/css',
				'media' => 'all',
				'href'  => $mvCssUrl
			));	
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
			$html .= '<div class="admin_links"><a href='.htmlspecialchars($this->mTitle->getFullUrl() ).'>Back to Sitting</a></div>';
			$html .= '<div class="yui-navset">'; 
		$html .= '<ul class="yui-nav">'; 
		if ($wgRequest->getText('new')=='true')
		{
	        	$html .= '<li><a href="'.'"><em>Sitting Details</em></a></li>'; 
	        }
	        if ($wgRequest->getText('new')=='true')
		{
	        	$html .= '<li><a href="' . $this->mTitle->getFullUrl('action=edit&new=true') . '"><em>Media</em></a></li>'; 
	        }
	        else
	        {
	        	$html .= '<li><a href="' . $this->mTitle->getFullUrl('action=edit') . '"><em>Media</em></a></li>'; 
	        }
	        if ($wgRequest->getText('new')=='true')
		{
	        	$html .= '<li class="selected"><a href="'.$this->mTitle->getFullUrl('action=staff&new=true').'"><em>Staff</em></a></li>'; 
	        }
	        else
	        {
	        	$html .= '<li class="selected"><a href="'.$this->mTitle->getFullUrl('action=staff').'"><em>Staff</em></a></li>'; 
	        }
	        if ($wgRequest->getText('new')=='true')
		{
	        	$html .= '<li><a href="'.$this->mTitle->getFullUrl('action=takes&new=true').'"><em>Takes</em></a></li>'; 
	    	}
	    	else
	    	{
	    		$html .= '<li><a href="'.$this->mTitle->getFullUrl('action=takes').'"><em>Takes</em></a></li>';
	    	}
	    	$html .= '</ul></div>';   
			$html .= $this->getAvailableEditors($this->stream_id);
			$html .= $this->getAssignedEditors($this->stream_id);
			
			$html .= $this->getAvailableReaders($this->stream_id);
			$html .= $this->getAssignedReaders($this->stream_id);
			
			$html .= $this->getAvailableReporters($this->stream_id);
			$html .= $this->getAssignedReporters($this->stream_id);
			
			if ($wgRequest->getText('new')=='true')
			{
				$html .= '<div id="user_actions"><table><tr><td>';
				$html .= '<input id="showButton" type="button" value="Save Changes"/>';
				$html .= '</td>';
				$html .= '<td>';
				$html .= '<button onclick=location.href="'.$this->mTitle->getFullUrl('action=edit&new=true').'">Back</button>';
				$html .= '</td>';
				$html .= '<td>';
				//$html .= '<button onclick=location.href="'.$this->mTitle->getFullUrl('action=takes&new=true').'">Next</button>';
				$html .= '<button onclick=location.href="'.$this->mTitle->getFullUrl('action=takes&new=true').'">Next</button>';
				$html .= '</td></tr></table></div>';
				$wgOut->setPageTitle('Create New Sitting Takes');
			}
			else
			{
				$html .= '<div id="user_actions"><input id="showButton" type="button" value="Save Changes"/></div>';
			}	
			
			
			$html.='<div id="debug"></div>';
			$html.='<div id="response"></div></div>';
			//$html.='<div id="stream_id">'.$this->stream_id.'</div>';
			
			/*
			$html.='<div id="stream_id" style="display:none;">'.$stream_id.'</div>';
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
			*/
			
			$inlinescript = '';
			$inlinescript .= <<< SCRIPT
<script type="text/javascript">

(function() {

var Dom = YAHOO.util.Dom;
var Event = YAHOO.util.Event;
var DDM = YAHOO.util.DragDropMgr;

//////////////////////////////////////////////////////////////////////////////
// example app
//////////////////////////////////////////////////////////////////////////////
YAHOO.example.DDApp = {
    init: function() {
        var i=0, j=1, str;
        new YAHOO.util.DDTarget("ul1", "editor");
        new YAHOO.util.DDTarget("ul2", "editor");
		new YAHOO.util.DDTarget("ul3", "reader");
        new YAHOO.util.DDTarget("ul4", "reader");
        new YAHOO.util.DDTarget("ul5", "reporter");
        new YAHOO.util.DDTarget("ul6", "reporter");
			i = 0;
			var elements = YAHOO.util.Dom.getElementsByClassName("list1", 'li');
			while (i<elements.length)
			{
					new YAHOO.example.DDList(elements[i].id, "editor");
				i++;
			}
			i = 0;
			var elements = YAHOO.util.Dom.getElementsByClassName("list2", 'li');
			while (i<elements.length)
			{
					new YAHOO.example.DDList(elements[i].id, "editor");
				i++;
			}
			i = 0;
			var elements = YAHOO.util.Dom.getElementsByClassName("list3", 'li');
			while (i<elements.length)
			{
					new YAHOO.example.DDList(elements[i].id, "reader");
				i++;
			}
			i = 0;
			var elements = YAHOO.util.Dom.getElementsByClassName("list4", 'li');
			while (i<elements.length)
			{
					new YAHOO.example.DDList(elements[i].id, "reader");
				i++;
			}
			i = 0;
			var elements = YAHOO.util.Dom.getElementsByClassName("list5", 'li');
			while (i<elements.length)
			{
					new YAHOO.example.DDList(elements[i].id, "reporter");
				i++;
			}
			i = 0;
			var elements = YAHOO.util.Dom.getElementsByClassName("list6", 'li');
			while (i<elements.length)
			{
					new YAHOO.example.DDList(elements[i].id, "reporter");
				i++;
			}
        Event.on("showButton", "click", this.showOrder);
        Event.on("switchButton", "click", this.switchStyles);
    },

    showOrder: function() {
        var parseList = function(ul, title) {
            var items = ul.getElementsByTagName("li");
            var tag="";
            var out = "<"+title+">";
            if (title == "AssignedReporters")
            	tag = "reporter";
            else if (title == "AssignedReaders")
            	tag = "reader";
            else if (title == "AssignedEditors")
            	tag = "editor";
            	
            for (i=0;i<items.length;i=i+1) {
                out += "<" + tag + " id=\"" + items[i].id + "\"></" +tag + ">";
            }
            out += "</"+title+">";
            return out;
        };

        var ul2=Dom.get("ul1"), ul4=Dom.get("ul3"), ul6=Dom.get("ul5");
        response = "<Data>" + parseList(ul2, "AssignedEditors") + parseList(ul4, "AssignedReaders") + parseList(ul6, "AssignedReporters") + "</Data>";
        var post_vars = new Object();
		var args = new Object();
		document.getElementById('debug').innerHTML = response;
		post_vars['xmldata'] = response;
		post_vars['stream_id'] = stream_id;
		sajax_request_type='POST';
		mv_sajax_do_call('mv_save_staff',args, onResponse, post_vars);

    },

    switchStyles: function() {
        Dom.get("ul1").className = "draglist_alt";
        Dom.get("ul2").className = "draglist_alt";
        Dom.get("ul3").className = "draglist_alt";
        Dom.get("ul4").className = "draglist_alt";
        Dom.get("ul5").className = "draglist_alt";
        Dom.get("ul6").className = "draglist_alt";
    }
};

//////////////////////////////////////////////////////////////////////////////
// custom drag and drop implementation
//////////////////////////////////////////////////////////////////////////////

YAHOO.example.DDList = function(id, sGroup, config) {

    YAHOO.example.DDList.superclass.constructor.call(this, id, sGroup, config);

    this.logger = this.logger || YAHOO;
    var el = this.getDragEl();
    Dom.setStyle(el, "opacity", 0.67); // The proxy is slightly transparent

    this.goingUp = false;
    this.lastY = 0;
};

YAHOO.extend(YAHOO.example.DDList, YAHOO.util.DDProxy, {

    startDrag: function(x, y) {
        this.logger.log(this.id + " startDrag");

        // make the proxy look like the source element
        var dragEl = this.getDragEl();
        var clickEl = this.getEl();
        Dom.setStyle(clickEl, "visibility", "hidden");

        dragEl.innerHTML = clickEl.innerHTML;

        Dom.setStyle(dragEl, "color", Dom.getStyle(clickEl, "color"));
        Dom.setStyle(dragEl, "backgroundColor", Dom.getStyle(clickEl, "backgroundColor"));
        Dom.setStyle(dragEl, "border", "2px solid gray");
    },

    endDrag: function(e) {

        var srcEl = this.getEl();
        var proxy = this.getDragEl();

        // Show the proxy element and animate it to the src element's location
        Dom.setStyle(proxy, "visibility", "");
        var a = new YAHOO.util.Motion( 
            proxy, { 
                points: { 
                    to: Dom.getXY(srcEl)
                }
            }, 
            0.2, 
            YAHOO.util.Easing.easeOut 
        )
        var proxyid = proxy.id;
        var thisid = this.id;

        // Hide the proxy and show the source element when finished with the animation
        a.onComplete.subscribe(function() {
                Dom.setStyle(proxyid, "visibility", "hidden");
                Dom.setStyle(thisid, "visibility", "");
            });
        a.animate();
    },

    onDragDrop: function(e, id) {

        // If there is one drop interaction, the li was dropped either on the list,
        // or it was dropped on the current location of the source element.
        if (DDM.interactionInfo.drop.length === 1) {

            // The position of the cursor at the time of the drop (YAHOO.util.Point)
            var pt = DDM.interactionInfo.point; 

            // The region occupied by the source element at the time of the drop
            var region = DDM.interactionInfo.sourceRegion; 

            // Check to see if we are over the source element's location.  We will
            // append to the bottom of the list once we are sure it was a drop in
            // the negative space (the area of the list without any list items)
            if (!region.intersect(pt)) {
                var destEl = Dom.get(id);
                var destDD = DDM.getDDById(id);
                destEl.appendChild(this.getEl());
                destDD.isEmpty = false;
                DDM.refreshCache();
            }

        }
    },

    onDrag: function(e) {

        // Keep track of the direction of the drag for use during onDragOver
        var y = Event.getPageY(e);

        if (y < this.lastY) {
            this.goingUp = true;
        } else if (y > this.lastY) {
            this.goingUp = false;
        }

        this.lastY = y;
    },

    onDragOver: function(e, id) {
    
        var srcEl = this.getEl();
        var destEl = Dom.get(id);

        // We are only concerned with list items, we ignore the dragover
        // notifications for the list.
        if (destEl.nodeName.toLowerCase() == "li") {
            var orig_p = srcEl.parentNode;
            var p = destEl.parentNode;

            if (this.goingUp) {
                p.insertBefore(srcEl, destEl); // insert above
            } else {
                p.insertBefore(srcEl, destEl.nextSibling); // insert below
            }

            DDM.refreshCache();
        }
    }
});

Event.onDOMReady(YAHOO.example.DDApp.init, YAHOO.example.DDApp, true);

})();
</script>		
		
SCRIPT;

$otherscript = <<< OTHERSCRIPT
<script type="text/javascript">
function onResponse( req )
{
	var ready=req.readyState;
  	var data=req.responseText;
  	if (req.status!=200) {
    	document.getElementById('response').innerHTML="loading...";
    }else
    {	
    	document.getElementById('response').innerHTML=data;
	}
}
</script>
OTHERSCRIPT;

$yetanotherscript = '<script type="text/javascript"> var stream_id='.$this->stream_id.'</script>';


$wgOut->addHTML($yetanotherscript);
$wgOut->addHTML($otherscript);
$wgOut->addHTML($inlinescript);

		}
		else
		{
			$html = wfMsg('mv_staff_permission');
		}
		$wgOut->addHTML($html);
	}
function getAssignedEditors($stream_id)
	{
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user IN (SELECT user_id FROM stream_assignment WHERE stream_id='.$stream_id.') and ug_group="editor"';
		$editors  = $dbr->query($sql);
		$html.='<div id="assignedEditors"><h3>Assigned Editors</h3><ul id="ul1" class="draglist">';
		while ($rowEditors = $dbr->fetchobject($editors))
		{
			$user = User::newFromId($rowEditors->ug_user);
			$name = $user->getRealName();
			$html.= '<li class="list1" id="'.$rowEditors->ug_user.'">'.$name.'</li>';
		} 
		$html.='</ul></div>';
		return $html;
	}
	
function getAvailableEditors($stream_id)
	{
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user NOT IN (SELECT user_id FROM stream_assignment WHERE stream_id='.$stream_id.') and ug_group="editor"';
		$editors  = $dbr->query($sql);
		$html.='<div id="unassignedEditors"><h3>Available Editors</h3><ul id="ul2" class="draglist">';
		while ($rowEditors = $dbr->fetchobject($editors))
		{
			$user = User::newFromId($rowEditors->ug_user);
			$name = $user->getRealName();
			$html.= '<li class="list2" id="'.$rowEditors->ug_user.'">'.$name.'</li>';
		} 
		$html.='</ul></div>';
		return $html;
	}


function getAssignedReaders($stream_id)
	{
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user IN (SELECT user_id FROM stream_assignment WHERE stream_id='.$stream_id.') and ug_group="reader"';
		$editors  = $dbr->query($sql);
		$html.='<div id="assignedReaders"><h3>Assigned Readers</h3><ul id="ul3" class="draglist">';
		while ($rowReaders = $dbr->fetchobject($editors))
		{
			$user = User::newFromId($rowReaders->ug_user);
			$name = $user->getRealName();
			$html.= '<li class="list3" id="'.$rowReaders->ug_user.'">'.$name.'</li>';
		} 
		$html.='</ul></div>';
		return $html;
	}
	
function getAvailableReaders($stream_id)
	{
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user NOT IN (SELECT user_id FROM stream_assignment WHERE stream_id='.$stream_id.') and ug_group="reader"';
		$editors  = $dbr->query($sql);
		$html.='<div id="unassignedReaders"><h3>Available Readers</h3><ul id="ul4" class="draglist">';
		while ($rowReaders = $dbr->fetchobject($editors))
		{
			$user = User::newFromId($rowReaders->ug_user);
			$name = $user->getRealName();
			$html.= '<li class="list4" id="'.$rowReaders->ug_user.'">'.$name.'</li>';
		} 
		$html.='</ul></div>';
		return $html;
	}

function getAssignedReporters($stream_id)
	{
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user IN (SELECT user_id FROM stream_assignment WHERE stream_id='.$stream_id.') and ug_group="reporter"';
		$reporters  = $dbr->query($sql);
		$html.='<div id="assignedReporters"><h3>Assigned Reporters</h3><ul id="ul5" class="draglist">';
		while ($rowReporters = $dbr->fetchobject($reporters))
		{
			$user = User::newFromId($rowReporters->ug_user);
			$name = $user->getRealName();
			$html.= '<li class="list5" id="'.$rowReporters->ug_user.'">'.$name.'</li>';
		} 
		$html.='</ul></div>';
		return $html;
	}
	
function getAvailableReporters($stream_id)
	{
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user NOT IN (SELECT user_id FROM stream_assignment WHERE stream_id='.$stream_id.') and ug_group="reporter"';
		$reporters  = $dbr->query($sql);
		$html.='<div id="unassignedReporters"><h3>Available Reporters</h3><ul id="ul6" class="draglist">';
		while ($rowReporters = $dbr->fetchobject($reporters))
		{
			$user = User::newFromId($rowReporters->ug_user);
			$name = $user->getRealName();
			$html.= '<li class="list6" id="'.$rowReporters->ug_user.'">'.$name.'</li>';
		} 
		$html.='</ul></div>';
		return $html;
	}
}
