<?php
class MV_Takes extends EditPage{
	var $name='';
	var $mvd_tracks = array('Take_en');
	var $stream_id='';
	function __construct($article)
	{
		$this->name = $article->getTitle()->getPartialURL();
		$title = $article->getTitle();
		$mvTitle = new MV_Title( $title->mDbkeyform );
		$this->stream_id = $mvTitle->getStreamId();
		parent::__construct($article);
	}
	
	function edit(){
		global $wgOut, $wgUser, $wgHooks, $wgRequest, $mvgScriptPath, $wgJsMimeType;
		$wgOut->clearHTML();
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/mv_stream.js\"></script>");
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/build/yahoo-dom-event/yahoo-dom-event.js\"></script>");
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/build/animation/animation-min.js\"></script>");
		$wgOut->addScript("<script type=\"{$wgJsMimeType}\" src=\"{$mvgScriptPath}/skins/build/dragdrop/dragdrop-min.js\"></script>");
		$mvCssUrl = $mvgScriptPath . '/skins/drag_takes.css';
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
		new YAHOO.util.DDTarget("ul2", "reader");   
        new YAHOO.util.DDTarget("ul3", "reporter");
     
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
		post_vars['sitting_id'] = document.getElementById("sitting_id").innerHTML;
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
$wgOut->clearHTML();
$wgOut->addHTML($otherscript);
$wgOut->addHTML($inlinescript);
global $mv_default_take_duration;
		if ($wgRequest->getVal('mv_action')=='generate')
		{
			 
			if (is_numeric($wgRequest->getVal('take_duration')))
			{
				$time = $wgRequest->getVal('take_duration');
			}
			else
			{
				$time = $mv_default_take_duration;
			}
			$duration = (int)$time;
			$html .= '<div id="response">'.$this->generate($duration).'</div>';
		}
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
	        	$html .= '<li><a href="'.$this->mTitle->getFullUrl('action=staff&new=true').'"><em>Staff</em></a></li>'; 
	        }
	        else
	        {
	        	$html .= '<li><a href="'.$this->mTitle->getFullUrl('action=staff').'"><em>Staff</em></a></li>'; 
	        }
	        if ($wgRequest->getText('new')=='true')
		{
	        	$html .= '<li class="selected"><a href="'.$this->mTitle->getFullUrl('action=takes&new=true').'"><em>Takes</em></a></li>'; 
	    	}
	    	else
	    	{
	    		$html .= '<li class="selected"><a href="'.$this->mTitle->getFullUrl('action=takes').'"><em>Takes</em></a></li>';
	    	}
	    	$html .= '</ul></div>';   
		$html .= $this->displayForm();
		$wgOut->addHTML($html);
	}
	
	function displayForm()
	{
		global $wgOut;
		$title = Title::makeTitle(MV_NS_STREAM, $this->name);
		$html.= '<fieldset><legend>Generate Takes</legend>' . "\n";	
		$html.='<form action="'.$title->getFullURL('action=takes').'" method="POST">';
		$html.='<P>Take Duration<input type="text" name="take_duration"></input><input type="submit" value="Generate Takes"></input>';
		$html.='<input name="mv_action" value="generate" type="hidden"></input>';
		$html.='</form';
		$html.='</fieldset>';
		$html.='<fieldset><legend>Takes</legend>';
		$html.= $this->takes();
		$html.='</fieldset>';
		return $html;
		
	}
	
	function takes()
	{
		global $mvgIP, $wgRequest, $wgOut;
		require_once($mvgIP . '/includes/MV_Index.php');
		require_once($mvgIP . '/includes/MV_MetavidInterface/MV_Overlay.php');
		$s = MV_Stream::newStreamByName($this->name);
		if (!$s->db_load_stream())
			return "An error occured please notify Administrator";
		
		$dbr =& wfGetDB(DB_SLAVE);	
		$result = & MV_Index::getMVDInRange($s->getStreamId(), 
							0, 
							$s->getDuration(), 
							$this->mvd_tracks);					
							
		if ($wgRequest->getText('new')=='true')
			{
				$h .= '<div class="navigation"><table><tr><td>';
				$h .= '<button onclick=location.href="'.$this->mTitle->getFullUrl('action=staff&new=true').'">Back</button>';
				$h .= '</td>';
				$h .= '<td>';
				$h .= '<button onclick=location.href="'.$this->mTitle->getFullUrl().'">Finish</button>';
				$h .= '</td></tr></table></div>';
				$wgOut->setPageTitle('Create New Sitting Takes');
		}							
		if($dbr->numRows($result) == 0){
			return "No takes have been generated ".$this->name.' - '. $s->getStreamId().' - '.$s->getDuration() .$h;	
		}else{
			$i = 0;
			$temp = array();
			while($row = $dbr->fetchObject($result)){
				$mvdTitle = new MV_Title( $row->wiki_title );
				$curRevision = Revision::newFromTitle($mvdTitle);			
				$wikitext = $curRevision->getText();
				$smw_attr = MV_Overlay::get_and_strip_semantic_tags($wikitext);
				$temp[$i]['start_time'] = $row->start_time;
				$temp[$i]['end_time'] = $row->end_time;
				$temp[$i]['Reported by'] =''.$smw_attr['Reported By'];
				$temp[$i]['Read by'] =''.$smw_attr['Read By'];
				$temp[$i]['Edited by'] =''. $smw_attr['Edited By'];
				$i++;
			}
			
			
			$html = '<table><tr><th>Time</th><th>Editors</th><th>Readers</th><th>Reporters</th></tr><tr><td><ul id="ul-takes" class="draglist">';
			for ($j=0; $j < $i; $j++)
			{
				$html.='<li class="li-takes">'.$temp[$j]['start_time'].' -> '.$temp[$j]['end_time'].'</li>';
			}
			$html.='</ul></td>';
			
			$html .= '<td><ul id="ul1" class="draglist">';
			for ($j=0; $j < $i; $j++)
			{
				$html.='<li class="list1">'.$temp[$j]['Edited by'].'</li>';
			}
			$html.='</ul></td>';
			
			$html .= '<td><ul id="ul2"  class="draglist">';
			for ($j=0; $j < $i; $j++)
			{
				$html.='<li class="list2">'.$temp[$j]['Read by'].'</li>';
			}
			$html.='</ul></td>';
			
			$html .= '<td> <ul id="ul3"  class="draglist">';
			for ($j=0; $j < $i; $j++)
			{
				$html.='<li class="list3">'.$temp[$j]['Reported by'].'</li>';
			}
			$html.='</ul></td></tr></table>';
			
			
			
			return $html.$h;
		}
	}
	
	
	function generate($take_duration)
	{
		global $mvgIP;
		require_once($mvgIP . '/includes/MV_Index.php');
		$s = MV_Stream::newStreamByName($this->name);
		if (!$s->db_load_stream())
			return "An error occured while loading stream info please notify Administrator";
		$stream_duration = $s->getDuration();
		if ($stream_duration === NULL)
			return "Error: Stream Duration not set";
		//$sitting_id = $s->getSittingId();
		
		$editors = $this->getAssignedEditors($this->stream_id);
		$readers = $this->getAssignedReaders($this->stream_id);
		$reporters = $this->getAssignedReporters($this->stream_id);
		
		$editors_count = count($editors);
		$readers_count = count($readers);
		$reporters_count = count($reporters);
		$html = '';
		if ($editors_count == 0)
		{
			$html .= "No Editors Assigned";
			return $html;
		}
		if ($readers_count == 0)
		{
			$html .= "No Readers Assigned";
			return $html;
		}
		if ($reporters_count == 0)
		{
			$html .= "No Reporters Assigned";
			return $html;
		}
		//delete all existing take transcripts
		
		$dbr =& wfGetDB(DB_SLAVE);	
		$result = & MV_Index::getMVDInRange($s->getStreamId(), 
							0, 
							$s->getDuration(), 
							$this->mvd_tracks);	
						
		while($row = $dbr->fetchObject($result)){
			$title = Title::newFromText ( $row->wiki_title, MV_NS_MVD );
			$art = new Article( $title );
			if ($art->exists())
			{
				$art->doDelete( "new takes generated", true);
			}
		}
		
		$num_editor = 0;
		$num_reader = 0;
		$num_reporter = 0;
		
		for ($i = 0; $i < $stream_duration; $i = $i + $take_duration)
		{
			$start_time = $i;
			$end_time = $i + $take_duration;

			$title_text = 'Take_en:'.$this->name.'/'.seconds2ntp($start_time).'/'.seconds2ntp($end_time);
			$title = Title::newFromText($title_text, MV_NS_MVD);
			$editor = User::newFromId($editors[$num_editor]);
			$editor_name = $editor->getRealName();

			$reader = User::newFromId($readers[$num_editor]);
			$reader_name = $reader->getRealName();
			
			$reporter = User::newFromId($reporters[$num_editor]);
			$reporter_name = $reporter->getRealName();
			
						
			
			
			$article = new Article($title);
			$text = '[[Edited By::'.$editor_name.']], '.'[[Read By::'.$reader_name.']], '.'[[Reported By::'.$reporter_name.']], '.'[[Status::Incomplete]] [[Stream::'.$this->name.']]';
			$article->doEdit($text,'Automatically Generated',EDIT_NEW);
			if ($num_editor < ($editors_count-1))
			{
				$num_editor++;
			}
			else
			{
				$num_editor = 0;
			}	
			if ($num_reader < ($readers_count-1))
			{
				$num_reader++;
			}
			else
			{
				$num_reader = 0;
			}	
			if ($num_reporter < ($reporters_count-1))
			{
				$num_reporter++;
			}
			else
			{
				$num_reporter = 0;
			}
		}
		
		$html .= 'Takes Successfully Generated';
		return $html;
	}
	
	function getAssignedEditors($stream_id)
	{
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user IN (SELECT user_id FROM stream_assignment WHERE stream_id='.$stream_id.') and ug_group="editor"';
		$editors  = $dbr->query($sql);
		$i=0;
		while ($rowEditors = $dbr->fetchobject($editors))
		{
			$id[$i++] = $rowEditors->ug_user;
		} 
		return $id;
	}
	
	function getAssignedReaders($stream_id)
	{
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user IN (SELECT user_id FROM stream_assignment WHERE stream_id='.$stream_id.') and ug_group="reader"';
		$readers  = $dbr->query($sql);
		$i = 0;
		while ($rowReaders = $dbr->fetchobject($readers))
		{
			$id[$i++] = $rowReaders->ug_user;
		} 
		return $id;
	}
	
	function getAssignedReporters($stream_id)
	{
		$dbr =& wfGetDB(DB_SLAVE);
		$sql = 'SELECT ug_user FROM user_groups WHERE ug_user IN (SELECT user_id FROM stream_assignment WHERE stream_id='.$stream_id.') and ug_group="reporter"';
		$reporters  = $dbr->query($sql);
		$i = 0;
		while ($rowReporters = $dbr->fetchobject($reporters))
		{
			$id[$i++] = $rowReporters->ug_user;
		} 
		return $id;
	}
}

?>
